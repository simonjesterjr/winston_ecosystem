# frozen_string_literal: true
# Shares-only TS75 vs TS77 overnight bakeoff stamp (heat OFF, caps 3/10).
# FOR PBR Ops / Sawtooth Ops — CoS does NOT stamp/enqueue from chat.
#
# Host (sawtooth-ai):
#   cd /home/johnkoisch/Documents/com/sawtooth
#   DRY_RUN=1 ./bin/compose exec -T -e DRY_RUN=1 winston_unit_test bin/rails runner \
#     /ecosystem/docs/analysis/2026-09-23-stamp-shares-only-ts75-vs-ts77-bakeoff.rb
#   ./bin/compose exec -T winston_unit_test bin/rails runner \
#     /ecosystem/docs/analysis/2026-09-23-stamp-shares-only-ts75-vs-ts77-bakeoff.rb
#
# Cloned from 2026-09-21-stamp-teal-ts75-heat-on-r01.rb (#763–#770 trail).
# Diffs: leap_fulfillment OMITTED; heat hash OMITTED; caps 3/10; 4 books × TS75/77 × r01/r02.
# Idempotent on cell_key. New rows only. Enqueues PortfolioBacktestJob. Does not wait.

require "json"

DRY_RUN = ENV["DRY_RUN"].to_s.match?(/\A(1|true|yes)\z/i)
EXPERIMENT = "shares_only_ts75_vs_ts77_bakeoff_20260923"
STAMP_DATE = "20260923"
AUTHZ = {
  "authorized_by" => "john",
  "reason" => "shares_only_ts75_vs_ts77_bakeoff_ibkr_l2_path_2026-09-23",
}.freeze
INITIAL = 30_000.0
MAX_PER_SYMBOL = 3
MAX_PER_PORTFOLIO = 10
REPORT_PATH = "/ecosystem/docs/analysis/2026-09-23-stamp-shares-only-ts75-vs-ts77-bakeoff-report.json"
NOTE_PATH = "/ecosystem/docs/analysis/2026-09-23-stamp-shares-only-ts75-vs-ts77-bakeoff.md"

BOOKS = [
  { seed: "blue",   portfolio_id: 7 },
  { seed: "indigo", portfolio_id: 411 },
  { seed: "teal",   portfolio_id: 412 },
  { seed: "copper", portfolio_id: 413 },
].freeze
TS_IDS = [75, 77].freeze
RISKS = [0.01, 0.02].freeze

TS_SIGNAL_EXPECT = {
  75 => { entry: "Breakout20DayStrategy", exit: "Breakout10DayStrategy" },
  77 => { entry: "Breakout55DayStrategy", exit: "Breakout20DayStrategy" },
}.freeze

def results_hash(run)
  raw = if run.respond_to?(:results_parsed)
          run.results_parsed
        else
          run.try(:results_json)
        end
  h = raw.is_a?(Hash) ? raw : (JSON.parse(raw.to_s) rescue {})
  h = {} unless h.is_a?(Hash)
  h.respond_to?(:deep_stringify_keys) ? h.deep_stringify_keys : h.transform_keys(&:to_s)
end

def risk_tag(risk)
  (risk - 0.01).abs < 1e-9 ? "r01" : "r02"
end

def cell_key_for(seed:, risk:, ts_id:)
  "#{seed}_rst_legacy_#{risk_tag(risk)}_shares_ts#{ts_id}_caps3x10_#{STAMP_DATE}"
end

def resolve_tss!(strategy_class)
  tss = TradingSignalStrategy.find_by(strategy_class: strategy_class)
  raise "Missing TradingSignalStrategy strategy_class=#{strategy_class}" unless tss
  tss
end

def resolve_entry_exit_for_ts(ts)
  expect = TS_SIGNAL_EXPECT[ts.id]
  entry = ts.try(:primary_entry_signal)
  entry = resolve_tss!(expect[:entry]) if entry.nil? && expect
  raise "TS##{ts.id} no primary entry" unless entry

  exit_ids = Array(ts.try(:resolved_exit_strategy_ids)).map(&:to_i).reject(&:zero?)
  exits = TradingSignalStrategy.where(id: exit_ids).to_a
  exits = [resolve_tss!(expect[:exit])] if exits.empty? && expect
  raise "TS##{ts.id} no exit strategies" if exits.empty?

  conf_ids = Array(
    ts.try(:resolved_confirmational_entry_strategy_ids) || ts.try(:confirmational_entry_strategy_ids)
  ).map(&:to_i).reject(&:zero?)
  conf = conf_ids.first ? TradingSignalStrategy.find_by(id: conf_ids.first) : nil
  { entry: entry, exits: exits, conf: conf }
end

def find_existing(portfolio_id, cell_key)
  PortfolioBacktestRun.where(portfolio_id: portfolio_id).order(id: :desc).find do |r|
    results_hash(r)["cell_key"].to_s == cell_key
  end
end

def create_pbr!(portfolio:, ts:, risk:)
  overrides = {
    "risk_percentage" => risk,
    "initial_capital" => INITIAL,
    "risk_evaluation_strategy" => "static",
    "stop_strategy" => "move_to_last_entry",
    "atr_multiplier" => 2.0,
    "max_positions_per_symbol" => MAX_PER_SYMBOL,
    "max_positions_per_portfolio" => MAX_PER_PORTFOLIO,
    "max_leverage" => 3.0,
    "ignore_first_signal" => true,
    "always_in_market" => false,
    "pyramid_atr_multiplier" => 0.5,
    "max_pyramid" => 4,
    "enable_position_swap" => false,
    "risk_scale_policy" => "none",
    "skip_next_after_winner" => false,
  }

  base_config = {
    "initial_capital" => INITIAL,
    "ignore_first_signal" => true,
    "always_in_market" => false,
    "max_positions_per_symbol" => MAX_PER_SYMBOL,
    "max_positions_per_portfolio" => MAX_PER_PORTFOLIO,
    "risk_evaluation_strategy" => "static",
    "risk_scale_policy" => "none",
    "stop_strategy" => "move_to_last_entry",
    "risk_percentage" => risk,
    "atr_multiplier" => 2.0,
    "max_leverage" => 3.0,
    "enable_position_swap" => false,
    "skip_next_after_winner" => false,
    "per_market" => {
      "pyramid_atr_multiplier" => 0.5,
      "max_pyramid" => 4,
      "atr_multiplier" => 2.0,
    },
  }

  sig = resolve_entry_exit_for_ts(ts)
  if PortfolioBacktestRunFactory.respond_to?(:create_from_optimization!)
    run = PortfolioBacktestRunFactory.create_from_optimization!(
      portfolio: portfolio,
      entry_strategy: sig[:entry],
      exit_strategies: sig[:exits],
      base_config: base_config,
      confirmational_entry_strategy: sig[:conf]
    )
    if PortfolioBacktestRunFactory.respond_to?(:attach_trading_strategy_provenance!)
      PortfolioBacktestRunFactory.attach_trading_strategy_provenance!(run, ts)
    end
    run
  else
    PortfolioBacktestRunFactory.create_from_trading_strategy!(
      portfolio: portfolio,
      trading_strategy: ts,
      initial_capital: INITIAL,
      overrides: overrides
    )
  end
end

def apply_shares_dna!(run, cell_key:, risk:, ts:, seed:)
  if run.respond_to?(:portfolio_backtest_market_configs)
    run.portfolio_backtest_market_configs.find_each do |mc|
      u = {}
      u[:leap_expiration_days] = nil if mc.respond_to?(:leap_expiration_days=)
      u[:leap_atr_offset] = nil if mc.respond_to?(:leap_atr_offset=)
      u[:leap_pyramid_level] = nil if mc.respond_to?(:leap_pyramid_level=)
      u[:max_pyramid] = mc.max_pyramid.presence || 4 if mc.respond_to?(:max_pyramid=)
      u[:pyramid_atr_multiplier] = mc.pyramid_atr_multiplier.presence || 0.5 if mc.respond_to?(:pyramid_atr_multiplier=)
      u[:atr_multiplier] = mc.atr_multiplier.presence || 2.0 if mc.respond_to?(:atr_multiplier=)
      mc.update!(u) if u.any?
    end
  end

  rj = results_hash(run)
  %w[leap_fulfillment leap_atr_offset leap_expiration_days heat].each { |k| rj.delete(k) }

  rj.merge!(
    "authorization" => AUTHZ,
    "experiment" => EXPERIMENT,
    "cell_key" => cell_key,
    "stamp_reason" => "shares_only_ts75_vs_ts77_bakeoff_caps3x10_heat_off",
    "book_seed" => seed,
    "fill_cadence" => "resting_stop_touch",
    "entry_fill_cadence" => "price_level_touch",
    "pyramid_fill_cadence" => "price_level_touch",
    "fill_arm" => "resting",
    "heat_mode" => "legacy",
    "risk_percentage" => risk,
    "no_volatility_exit" => true,
    "atr_multiplier" => 2.0,
    "pyramid_atr_multiplier" => 0.5,
    "max_pyramid" => 4,
    "stop_strategy" => "move_to_last_entry",
    "risk_evaluation_strategy" => "static",
    "max_leverage" => 3.0,
    "ignore_first_signal" => true,
    "always_in_market" => false,
    "skip_next_after_winner" => false,
    "trading_strategy_id" => ts.id,
    "trading_strategy_name" => ts.name,
    "trading_strategy_fingerprint" => ts.try(:fingerprint),
    "instrument_mode" => "shares",
    "max_positions_per_symbol" => MAX_PER_SYMBOL,
    "max_positions_per_portfolio" => MAX_PER_PORTFOLIO
  )

  upd = {
    initial_capital: INITIAL,
    risk_percentage: risk,
    stop_strategy: "move_to_last_entry",
    max_positions_per_symbol: MAX_PER_SYMBOL,
    max_positions_per_portfolio: MAX_PER_PORTFOLIO,
    atr_multiplier: 2.0,
    results_json: rj.to_json,
    status: :pending,
  }
  upd[:max_leverage] = 3.0 if run.respond_to?(:max_leverage=)
  upd[:risk_evaluation_strategy] = "static" if run.respond_to?(:risk_evaluation_strategy=)
  run.update!(upd)
  run
end

def enqueue!(run)
  job = %w[PortfolioBacktestJob RunPortfolioBacktestJob PortfolioBacktestRunJob].filter_map { |n|
    Object.const_get(n) if Object.const_defined?(n)
  }.first
  raise "No PortfolioBacktestJob class found" unless job
  job.perform_later(run.id)
  "enqueued:#{job.name}"
end

def verify_shares_heat_off!(run)
  rj = results_hash(run)
  raise "VERIFY FAIL ##{run.id}: leap_fulfillment=#{rj['leap_fulfillment'].inspect}" if rj["leap_fulfillment"].present?
  raise "VERIFY FAIL ##{run.id}: heat hash present" if rj["heat"].is_a?(Hash) && rj["heat"].present?
  unless run.max_positions_per_symbol.to_i == MAX_PER_SYMBOL
    raise "VERIFY FAIL ##{run.id}: max_positions_per_symbol=#{run.max_positions_per_symbol}"
  end
  unless run.max_positions_per_portfolio.to_i == MAX_PER_PORTFOLIO
    raise "VERIFY FAIL ##{run.id}: max_positions_per_portfolio=#{run.max_positions_per_portfolio}"
  end
  true
end

puts "=== Shares-only TS75 vs TS77 bakeoff stamp ==="
puts "DRY_RUN=#{DRY_RUN} experiment=#{EXPERIMENT}"
puts "caps=#{MAX_PER_SYMBOL}/#{MAX_PER_PORTFOLIO} heat=OFF leap=OMITTED"
puts "factory methods=#{PortfolioBacktestRunFactory.singleton_methods(false).sort.inspect}"

cells = BOOKS.product(TS_IDS, RISKS).map do |book, ts_id, risk|
  {
    seed: book[:seed],
    portfolio_id: book[:portfolio_id],
    ts_id: ts_id,
    risk: risk,
    cell_key: cell_key_for(seed: book[:seed], risk: risk, ts_id: ts_id),
  }
end

puts "planned_cells=#{cells.size}"
cells.each { |c| puts "  #{c[:cell_key]} p#{c[:portfolio_id]}" }

if DRY_RUN
  File.write(REPORT_PATH, JSON.pretty_generate(dry_run: true, planned: cells, at: Time.now.to_s))
  puts "DRY_RUN complete — no rows written."
  exit 0
end

rows = []
cells.each do |c|
  portfolio = Portfolio.find(c[:portfolio_id])
  ts = TradingStrategy.find(c[:ts_id])
  ck = c[:cell_key]
  print "stamp #{ck} ... "

  existing = find_existing(c[:portfolio_id], ck)
  if existing
    verify_shares_heat_off!(existing)
    enq = if %w[pending failed queued].include?(existing.status.to_s)
            enqueue!(existing)
          else
            "skip_enqueue:status=#{existing.status}"
          end
    puts "REUSE ##{existing.id} status=#{existing.status} #{enq}"
    rows << c.merge(pbr_id: existing.id, reused: true, enqueue: enq, status: existing.status.to_s)
    next
  end

  run = create_pbr!(portfolio: portfolio, ts: ts, risk: c[:risk])
  apply_shares_dna!(run, cell_key: ck, risk: c[:risk], ts: ts, seed: c[:seed])
  verify_shares_heat_off!(run)
  enq = enqueue!(run)
  puts "NEW ##{run.id} #{enq}"
  rows << c.merge(pbr_id: run.id, reused: false, enqueue: enq, status: run.status.to_s)
end

report = {
  stamped_at: Time.now.to_s,
  experiment: EXPERIMENT,
  caps: { max_positions_per_symbol: MAX_PER_SYMBOL, max_positions_per_portfolio: MAX_PER_PORTFOLIO },
  heat: "OFF",
  leap_fulfillment: nil,
  fill: "resting_stop_touch",
  stop: "move_to_last_entry",
  atr_multiplier: 2.0,
  initial_capital: INITIAL,
  rows: rows,
}
File.write(REPORT_PATH, JSON.pretty_generate(report))

md = +""
md << "# Shares-only TS75 vs TS77 bakeoff — stamp report\n\n"
md << "- **When:** #{Time.now}\n"
md << "- **Experiment:** `#{EXPERIMENT}`\n"
md << "- **Caps:** max_positions_per_symbol=#{MAX_PER_SYMBOL}, max_positions_per_portfolio=#{MAX_PER_PORTFOLIO}\n"
md << "- **Heat:** OFF · **LEAP:** omitted · **Fill:** resting_stop_touch · **Stop:** move_to_last_entry 2N\n\n"
md << "| cell_key | PBR | portfolio | TS | risk | reused | enqueue |\n"
md << "|----------|-----|-----------|----|------|--------|---------|\n"
rows.each do |r|
  md << "| `#{r[:cell_key]}` | **##{r[:pbr_id]}** | p#{r[:portfolio_id]} | #{r[:ts_id]} | #{r[:risk]} | #{r[:reused]} | #{r[:enqueue]} |\n"
end
md << "\nReport JSON: `#{REPORT_PATH}`\n"
File.write(NOTE_PATH, md)

puts "=== done rows=#{rows.size} report=#{REPORT_PATH} ==="
