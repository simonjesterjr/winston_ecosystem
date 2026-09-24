# frozen_string_literal: true
# Shares-only TS75 modified-heat bakeoff stamp (heat knobs 3/6/10/10, caps 3/10).
# FOR PBR Ops / Sawtooth Ops — CoS does NOT stamp/enqueue from chat.
#
# Host (sawtooth-ai):
#   cd /home/johnkoisch/Documents/com/sawtooth
#   DRY_RUN=1 ./bin/compose exec -T -e DRY_RUN=1 winston_unit_test bin/rails runner \
#     /ecosystem/docs/analysis/2026-09-24-stamp-shares-ts75-modified-heat-bakeoff.rb
#   ./bin/compose exec -T winston_unit_test bin/rails runner \
#     /ecosystem/docs/analysis/2026-09-24-stamp-shares-ts75-modified-heat-bakeoff.rb
#
# Clone pattern: 2026-09-23-stamp-shares-only-ts75-vs-ts77-bakeoff.rb (shares / caps / omit leap)
# Heat writer: 2026-09-21-stamp-teal-ts75-heat-on-r01.rb + evolve heat_for (full heat hash).
# Diffs vs prior shares bakeoff: TS75 only; ALWAYS write heat hash; heat_mode=turtle;
# modified knobs 3/6/10/10 (not classic 4/6/10/12). Idempotent on cell_key. New rows only.
# Enqueues PortfolioBacktestJob. Does not wait. Do NOT restamp Teal LEAP #767–#770.

require "json"

DRY_RUN = ENV["DRY_RUN"].to_s.match?(/\A(1|true|yes)\z/i)
EXPERIMENT = "shares_ts75_mod_heat_bakeoff_20260924"
STAMP_DATE = "20260924"
AUTHZ = {
  "authorized_by" => "john",
  "reason" => "shares_ts75_modified_heat_bakeoff_caps3x10_2026-09-24",
}.freeze
INITIAL = 30_000.0
MAX_PER_SYMBOL = 3
MAX_PER_PORTFOLIO = 10
TS_ID = 75
REPORT_PATH = "/ecosystem/docs/analysis/2026-09-24-stamp-shares-ts75-modified-heat-bakeoff-report.json"
NOTE_PATH = "/ecosystem/docs/analysis/2026-09-24-stamp-shares-ts75-modified-heat-bakeoff.md"

BOOKS = [
  { seed: "blue",   portfolio_id: 7 },
  { seed: "indigo", portfolio_id: 411 },
  { seed: "teal",   portfolio_id: 412 },
  { seed: "copper", portfolio_id: 413 },
].freeze
RISKS = [0.01, 0.02].freeze

# Modified turtle heat (Operator: 3, 6, _, 10 max per portfolio).
# loose==direction (10) accepted by PortfolioHeatConfig / HeatCapacityGate on host.
MODIFIED_TURTLE_HEAT = {
  "unit_risk_fraction" => 0.01,
  "max_units_per_market" => 3,
  "max_units_closely_correlated_same_direction" => 6,
  "max_units_loosely_correlated_same_direction" => 10,
  "max_units_single_direction" => 10,
  "correlation" => {
    "source" => "pcs_pairwise",
    "close_threshold" => 0.7,
    "loose_threshold" => 0.4,
    "window" => "methodology",
  },
}.freeze

TS_SIGNAL_EXPECT = {
  75 => { entry: "Breakout20DayStrategy", exit: "Breakout10DayStrategy" },
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

def cell_key_for(seed:, risk:)
  "#{seed}_rst_turtle_#{risk_tag(risk)}_shares_ts75_heat3_6_10_caps3x10_#{STAMP_DATE}"
end

def heat_for(risk)
  h = MODIFIED_TURTLE_HEAT.deep_dup
  h["unit_risk_fraction"] = risk
  h
end

def heat_enabled_of(run)
  rj = results_hash(run)
  heat = rj["heat"]
  if run.respond_to?(:heat_enabled?)
    !!run.heat_enabled?
  else
    heat.is_a?(Hash) && heat.present?
  end
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

def apply_shares_heat_dna!(run, cell_key:, risk:, ts:, seed:)
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

  heat = heat_for(risk)
  rj = results_hash(run)
  # Shares-only: omit leap_fulfillment entirely (IBKR Level 1 path)
  %w[leap_fulfillment leap_atr_offset leap_expiration_days].each { |k| rj.delete(k) }

  rj.merge!(
    "authorization" => AUTHZ,
    "experiment" => EXPERIMENT,
    "cell_key" => cell_key,
    "stamp_reason" => "shares_ts75_modified_heat_bakeoff_heat3_6_10_caps3x10",
    "book_seed" => seed,
    "fill_cadence" => "resting_stop_touch",
    "entry_fill_cadence" => "price_level_touch",
    "pyramid_fill_cadence" => "price_level_touch",
    "fill_arm" => "resting",
    "heat_mode" => "turtle",
    "heat" => heat,
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

def verify_shares_heat_on!(run, risk:)
  rj = results_hash(run)
  raise "VERIFY FAIL ##{run.id}: leap_fulfillment=#{rj['leap_fulfillment'].inspect}" if rj.key?("leap_fulfillment") && rj["leap_fulfillment"].present?
  heat = rj["heat"]
  unless heat.is_a?(Hash) && heat.present?
    raise "VERIFY FAIL ##{run.id}: heat hash blank/omitted (must ALWAYS write full heat)"
  end
  unless heat_enabled_of(run)
    raise "VERIFY FAIL ##{run.id}: heat_enabled?=false"
  end
  unless rj["heat_mode"].to_s == "turtle"
    raise "VERIFY FAIL ##{run.id}: heat_mode=#{rj['heat_mode'].inspect} expected turtle"
  end
  expect = {
    "max_units_per_market" => 3,
    "max_units_closely_correlated_same_direction" => 6,
    "max_units_loosely_correlated_same_direction" => 10,
    "max_units_single_direction" => 10,
  }
  expect.each do |k, v|
    got = heat[k].to_i
    raise "VERIFY FAIL ##{run.id}: heat[#{k}]=#{got} expected #{v}" unless got == v
  end
  urf = heat["unit_risk_fraction"].to_f
  unless (urf - risk).abs < 1e-9
    raise "VERIFY FAIL ##{run.id}: unit_risk_fraction=#{urf} expected #{risk}"
  end
  unless run.max_positions_per_symbol.to_i == MAX_PER_SYMBOL
    raise "VERIFY FAIL ##{run.id}: max_positions_per_symbol=#{run.max_positions_per_symbol}"
  end
  unless run.max_positions_per_portfolio.to_i == MAX_PER_PORTFOLIO
    raise "VERIFY FAIL ##{run.id}: max_positions_per_portfolio=#{run.max_positions_per_portfolio}"
  end
  true
end

puts "=== Shares-only TS75 modified-heat bakeoff stamp ==="
puts "DRY_RUN=#{DRY_RUN} experiment=#{EXPERIMENT}"
puts "caps=#{MAX_PER_SYMBOL}/#{MAX_PER_PORTFOLIO} heat=ON knobs=3/6/10/10 leap=OMITTED"
puts "factory methods=#{PortfolioBacktestRunFactory.singleton_methods(false).sort.inspect}"

cells = BOOKS.product(RISKS).map do |book, risk|
  {
    seed: book[:seed],
    portfolio_id: book[:portfolio_id],
    ts_id: TS_ID,
    risk: risk,
    cell_key: cell_key_for(seed: book[:seed], risk: risk),
  }
end

puts "planned_cells=#{cells.size}"
cells.each { |c| puts "  #{c[:cell_key]} p#{c[:portfolio_id]}" }
puts "heat_template_r01=#{heat_for(0.01).inspect}"

if DRY_RUN
  File.write(REPORT_PATH, JSON.pretty_generate(
    dry_run: true,
    planned: cells,
    heat_template: { r01: heat_for(0.01), r02: heat_for(0.02) },
    caps: { max_positions_per_symbol: MAX_PER_SYMBOL, max_positions_per_portfolio: MAX_PER_PORTFOLIO },
    at: Time.now.to_s
  ))
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
    verify_shares_heat_on!(existing, risk: c[:risk])
    enq = if %w[pending failed queued].include?(existing.status.to_s)
            enqueue!(existing)
          else
            "skip_enqueue:status=#{existing.status}"
          end
    puts "REUSE ##{existing.id} status=#{existing.status} heat_enabled=#{heat_enabled_of(existing)} #{enq}"
    rows << c.merge(pbr_id: existing.id, reused: true, enqueue: enq, status: existing.status.to_s)
    next
  end

  run = create_pbr!(portfolio: portfolio, ts: ts, risk: c[:risk])
  apply_shares_heat_dna!(run, cell_key: ck, risk: c[:risk], ts: ts, seed: c[:seed])
  verify_shares_heat_on!(run, risk: c[:risk])
  enq = enqueue!(run)
  puts "NEW ##{run.id} heat_enabled=#{heat_enabled_of(run)} #{enq}"
  rows << c.merge(pbr_id: run.id, reused: false, enqueue: enq, status: run.status.to_s)
end

report = {
  stamped_at: Time.now.to_s,
  experiment: EXPERIMENT,
  caps: { max_positions_per_symbol: MAX_PER_SYMBOL, max_positions_per_portfolio: MAX_PER_PORTFOLIO },
  heat: { mode: "turtle", knobs: "3/6/10/10", template: { r01: heat_for(0.01), r02: heat_for(0.02) } },
  leap_fulfillment: nil,
  fill: "resting_stop_touch",
  stop: "move_to_last_entry",
  atr_multiplier: 2.0,
  initial_capital: INITIAL,
  rows: rows,
}
File.write(REPORT_PATH, JSON.pretty_generate(report))

md = +""
md << "# Shares-only TS75 modified-heat bakeoff — stamp report\n\n"
md << "- **When:** #{Time.now}\n"
md << "- **Experiment:** `#{EXPERIMENT}`\n"
md << "- **Caps:** max_positions_per_symbol=#{MAX_PER_SYMBOL}, max_positions_per_portfolio=#{MAX_PER_PORTFOLIO}\n"
md << "- **Heat:** ON knobs 3/6/10/10 · heat_mode=turtle · **LEAP:** omitted · **Fill:** resting_stop_touch · **Stop:** move_to_last_entry 2N\n\n"
md << "| cell_key | PBR | portfolio | TS | risk | reused | enqueue |\n"
md << "|----------|-----|-----------|----|------|--------|---------|\n"
rows.each do |r|
  md << "| `#{r[:cell_key]}` | **##{r[:pbr_id]}** | p#{r[:portfolio_id]} | #{r[:ts_id]} | #{r[:risk]} | #{r[:reused]} | #{r[:enqueue]} |\n"
end
md << "\nReport JSON: `#{REPORT_PATH}`\n"
File.write(NOTE_PATH, md)

puts "=== done rows=#{rows.size} report=#{REPORT_PATH} ==="
