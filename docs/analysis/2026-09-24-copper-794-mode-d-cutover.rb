# frozen_string_literal: true

# Mint a new Winston v2 paper book from Winston Unit Test Portfolio Backtest Run 794.
# Mode D is fulfillment_packaging_policy["fulfillment_mode"] = "mode_d".
# Does not update Portfolio 1581, TradingStrategy 341, or any broker binding.
#
# Dry-run (default):
#   ./bin/compose exec -T winston_v2 bin/rails runner tmp/2026-09-24-copper-794-mode-d-cutover.rb
# Apply:
#   ./bin/compose exec -T -e APPLY=1 winston_v2 bin/rails runner tmp/2026-09-24-copper-794-mode-d-cutover.rb

APPLY = ENV["APPLY"] == "1"
NAME = "Portfolio Copper · mode-d-from-wut-794"
SYMBOLS = %w[AMZN GLD GOOGL JNJ MSFT PG TSLA TSM WMT XLE XLV].freeze
KEPT_ID = 1581
TS_ID = 341
HEAT_KNOBS = {
  "max_units_per_market" => 3,
  "max_units_closely_correlated_same_direction" => 6,
  "max_units_loosely_correlated_same_direction" => 10,
  "max_units_single_direction" => 10
}.freeze

def symbol_set(portfolio)
  portfolio.markets.map { |m| m.trading_symbol.to_s.upcase }.sort
end

def kept_snapshot(portfolio)
  {
    "id" => portfolio.id,
    "name" => portfolio.name,
    "seed_name" => portfolio.seed_name,
    "active" => portfolio.active,
    "trading_strategy_id" => portfolio.trading_strategy_id,
    "risk_percentage" => portfolio.risk_percentage.to_s,
    "atr_multiplier" => portfolio.atr_multiplier.to_s,
    "stop_strategy" => portfolio.stop_strategy,
    "max_positions_per_symbol" => portfolio.max_positions_per_symbol,
    "max_positions_per_portfolio" => portfolio.max_positions_per_portfolio,
    "max_pyramid" => portfolio.max_pyramid,
    "leap_fulfillment" => portfolio.leap_fulfillment,
    "fulfillment_adapter_key" => portfolio.fulfillment_adapter_key,
    "broker_binding_id" => portfolio.broker_binding_id,
    "wut_backtest_run_id" => portfolio.wut_backtest_run_id,
    "successor_of_id" => portfolio.successor_of_id,
    "fingerprint" => portfolio.fingerprint,
    "fulfillment_packaging_policy" => portfolio.fulfillment_packaging_policy,
    "fulfillment_mode" => portfolio.fulfillment_mode,
    "markets" => symbol_set(portfolio),
    "updated_at" => portfolio.updated_at.iso8601
  }
end

def heat_knobs(heat)
  return {} unless heat.is_a?(Hash)

  HEAT_KNOBS.keys.index_with { |key| heat[key].to_i }
end

kept = Portfolio.find(KEPT_ID)
ts = TradingStrategy.find(TS_ID)
before = kept_snapshot(kept)
raise "refusing: TradingStrategy #{TS_ID} is #{ts.name}" unless ts.name == "TurtleV1 S1 Breakout20/10"
raise "refusing: TradingStrategy #{TS_ID} already has a heat hash" if ts.heat_enabled?
raise "refusing: kept book #{KEPT_ID} is not Mode C" unless kept.fulfillment_mode == "mode_c"
raise "refusing: kept book markets drifted" unless symbol_set(kept) == SYMBOLS.sort

markets = SYMBOLS.map { |sym| Market.find_by!(trading_symbol: sym) }
active_same_books = Portfolio.active.includes(:markets).select { |row| symbol_set(row) == SYMBOLS.sort }
unexpected = active_same_books.reject { |row| row.id == KEPT_ID || row.name == NAME }
raise "refusing: unexpected active book with these markets: #{unexpected.map(&:id)}" if unexpected.any?

attrs = {
  name: NAME,
  seed_name: NAME,
  color: "#9a3412",
  active: false,
  execution_mode: "paper",
  trading_strategy_id: TS_ID,
  risk_percentage: 1.0,
  atr_multiplier: 2.0,
  stop_strategy: "move_to_last_entry",
  risk_evaluation_strategy: "static",
  pyramid_atr_multiplier: 0.5,
  max_pyramid: 4,
  max_positions_per_symbol: 3,
  max_positions_per_portfolio: 10,
  max_leverage: 3.0,
  always_in_market: false,
  primary_entry_strategy: ts.primary_entry_strategy,
  confirmational_entry_strategy_ids: Array(ts.confirmational_entry_strategy_names),
  exit_strategy_ids: Array(ts.exit_strategy_names),
  fulfillment_adapter_key: "dummy_sim",
  broker_binding_id: nil,
  leap_fulfillment: "none",
  fulfillment_packaging_policy: { "fulfillment_mode" => "mode_d" },
  wut_backtest_run_id: 794,
  successor_of_id: nil
}

existing = Portfolio.find_by(name: NAME)
plan = {
  apply: APPLY,
  name: NAME,
  kept_id: KEPT_ID,
  kept_unchanged_preview: before.slice("id", "name", "leap_fulfillment", "fulfillment_mode", "risk_percentage", "broker_binding_id"),
  active_same_books: active_same_books.map { |row| { id: row.id, name: row.name } },
  existing_id: existing&.id,
  attrs: attrs
}
puts JSON.pretty_generate(plan)

unless APPLY
  puts "DRY_RUN no writes"
  exit 0
end

portfolio = nil
activation = nil
ActiveRecord::Base.transaction do
  portfolio = existing || Portfolio.create!(attrs)
  raise "refusing: #{NAME} resolved to kept book #{KEPT_ID}" if portfolio.id == KEPT_ID

  if existing
    drift = attrs.except(:active).select { |key, value| portfolio.public_send(key) != value && portfolio.public_send(key).to_s != value.to_s }
    # jsonb / decimal: compare the fields that define the DNA
    dna_ok = portfolio.trading_strategy_id == TS_ID &&
             portfolio.risk_percentage.to_d == BigDecimal("1.0") &&
             portfolio.max_positions_per_symbol == 3 &&
             portfolio.max_positions_per_portfolio == 10 &&
             portfolio.leap_fulfillment == "none" &&
             portfolio.fulfillment_mode == "mode_d" &&
             portfolio.broker_binding_id.nil? &&
             portfolio.fulfillment_adapter_key == "dummy_sim" &&
             portfolio.wut_backtest_run_id == 794 &&
             symbol_set(portfolio) == SYMBOLS.sort
    raise "existing #{NAME} ##{portfolio.id} does not match 794 DNA #{drift.inspect}" unless dna_ok
  else
    markets.each { |market| portfolio.books.create!(market: market) }
    portfolio.cash_events.create!(
      amount: 30_000,
      event_type: "initial",
      event_date: Date.current,
      notes: "Mode D shares seed $30k from WUT PBR 794 / Copper 413. Not a successor of Wv2 1581."
    )
  end

  raise "books drifted" unless symbol_set(portfolio.reload) == SYMBOLS.sort

  resolved = Operations::PortfolioHeat.resolve(portfolio)
  knobs = heat_knobs(resolved.heat)
  unless knobs == HEAT_KNOBS && (resolved.heat["unit_risk_fraction"].to_f - 0.01).abs < 1e-9
    raise "runtime heat #{resolved.heat.inspect} source=#{resolved.source} is not 3/6/10/10 at 1%"
  end

  activation = Operations::PortfolioActivationService.activate!(portfolio: portfolio, force: true)
  raise activation.message unless activation.ok?

  kept_now = kept_snapshot(Portfolio.find(KEPT_ID))
  raise "kept book #{KEPT_ID} changed" unless kept_now == before

  portfolio.reload
  raise "binding set" if portfolio.broker_binding_id.present?
  raise "not mode_d" unless portfolio.fulfillment_mode == "mode_d"
  raise "leap not none" unless portfolio.leap_fulfillment == "none"
end

packed_long = Operations::FulfillmentPackagingSelector.call(
  portfolio: portfolio, symbol: "AMZN", signal_share_units: 237, direction: "long"
)
packed_short = Operations::FulfillmentPackagingSelector.call(
  portfolio: portfolio, symbol: "AMZN", signal_share_units: 80, direction: "short"
)
raise "long packaging #{packed_long.inspect}" unless packed_long[:fulfillment_type] == "stock" && packed_long[:units] == 200
raise "short packaging #{packed_short.inspect}" unless packed_short[:fulfillment_type] == "stock" && packed_short[:units] == 80

resolved = Operations::PortfolioHeat.resolve(portfolio)
report = {
  portfolio_id: portfolio.id,
  name: portfolio.name,
  seed_name: portfolio.seed_name,
  active: portfolio.active,
  trading_strategy_id: portfolio.trading_strategy_id,
  risk_percentage: portfolio.risk_percentage.to_s,
  caps: [portfolio.max_positions_per_symbol, portfolio.max_positions_per_portfolio],
  leap_fulfillment: portfolio.leap_fulfillment,
  fulfillment_mode: portfolio.fulfillment_mode,
  fulfillment_packaging_policy: portfolio.fulfillment_packaging_policy,
  fulfillment_adapter_key: portfolio.fulfillment_adapter_key,
  broker_binding_id: portfolio.broker_binding_id,
  wut_backtest_run_id: portfolio.wut_backtest_run_id,
  successor_of_id: portfolio.successor_of_id,
  markets: symbol_set(portfolio),
  capital_base: portfolio.capital_base,
  heat_source: resolved.source,
  heat: resolved.heat,
  activation: {
    ok: activation.ok?,
    forced: activation.forced,
    reasons: activation.reasons,
    conflicts: activation.conflicts,
    message: activation.message
  },
  packaging_long_237: { type: packed_long[:fulfillment_type], units: packed_long[:units], details: packed_long[:details] },
  packaging_short_80: { type: packed_short[:fulfillment_type], units: packed_short[:units] },
  kept_1581: kept_snapshot(Portfolio.find(KEPT_ID)),
  container_sha: `git -C /app rev-parse HEAD`.strip
}
File.write("/app/tmp/copper_794_mode_d_cutover.json", JSON.pretty_generate(report))
puts JSON.pretty_generate(report)
