require "json"

def rj_of(r)
  raw = r.respond_to?(:results_parsed) ? r.results_parsed : (JSON.parse(r.results_json.to_s) rescue {})
  raw = {} unless raw.is_a?(Hash)
  raw.respond_to?(:deep_stringify_keys) ? raw.deep_stringify_keys : raw.transform_keys(&:to_s)
end

def leap_of(rj)
  lf = rj["leap_fulfillment"]
  return lf if lf.is_a?(String) || lf == false || lf.nil?
  return lf["mode"] || lf["enabled"] || lf if lf.is_a?(Hash)
  rj["leap"] || rj["instrument"] || rj["instrument_mode"] || rj["packaging"]
end

rows = []
PortfolioBacktestRun.find_each do |r|
  rj = rj_of(r)
  ts = (rj["trading_strategy_id"] || rj.dig("config", "trading_strategy_id") || rj["ts_id"]).to_i
  next unless [75, 76, 77].include?(ts)
  leap = leap_of(rj)
  heat = rj["heat"]
  heat_on = heat.is_a?(Hash) && heat.present?
  dr = rj["date_range"] || rj["overlapping_date_range"] || r.overlapping_date_range
  start_d = rj["start_date"] || (dr.is_a?(Hash) ? (dr["start"] || dr["begin"]) : nil)
  end_d = rj["end_date"] || (dr.is_a?(Hash) ? (dr["end"] || dr["finish"]) : nil)
  # also peek packaging keys
  pack_keys = rj.keys.select { |k| k.to_s =~ /leap|packag|instrument|option|fulfill/i }
  rows << {
    id: r.id, status: r.status.to_s, pid: r.portfolio_id,
    ts: ts, risk: r.risk_percentage.to_f,
    max_sym: r.max_positions_per_symbol, max_port: r.max_positions_per_portfolio,
    leap: leap, heat_mode: rj["heat_mode"], heat_on: heat_on,
    heat_l1: heat_on ? heat["max_units_per_market"] : nil,
    cell: rj["cell_key"], experiment: rj["experiment"],
    fill: rj["fill_cadence"] || rj["fill_arm"],
    start: start_d, endd: end_d,
    tr: r.total_return, dd: r.max_drawdown,
    oa: r.option_aware_total_return, oa_dd: r.option_aware_max_drawdown,
    edge: r.edge_r || rj["edge_r"],
    trades: r.total_trades, pf: r.profit_factor,
    cagr: rj["cagr"] || rj.dig("metrics", "cagr"),
    stop: r.stop_strategy, atr: r.atr_multiplier,
    pack_keys: pack_keys,
    cell_has_leap: (rj["cell_key"].to_s.include?("leap") || rj["experiment"].to_s.include?("leap")),
    initial: r.initial_capital
  }
end

pnames = {}
Portfolio.where(id: rows.map { |x| x[:pid] }.uniq).each { |p| pnames[p.id] = p.name }

puts "TOTAL=#{rows.size}"
puts "STATUS_TALLY=#{rows.map { |x| x[:status] }.tally}"
puts "LEAP_TALLY=#{rows.map { |x| x[:leap].inspect }.tally}"
puts "TS_TALLY=#{rows.map { |x| x[:ts] }.tally}"

# True shares-only: leap nil/false AND cell does not say leap
true_shares = rows.select { |x| (x[:leap].nil? || x[:leap] == false) && !x[:cell_has_leap] }
# Ambiguous: leap nil but cell says leap
ambig = rows.select { |x| (x[:leap].nil? || x[:leap] == false) && x[:cell_has_leap] }
leap_all = rows.select { |x| x[:leap].to_s == "all" }

puts "TRUE_SHARES=#{true_shares.size} AMBIG_nil_but_leap_cell=#{ambig.size} LEAP_ALL=#{leap_all.size}"

puts "\n=== TRUE SHARES-ONLY (any status) ==="
true_shares.sort_by { |x| [-x[:id]] }.each do |x|
  name = pnames[x[:pid]] || "?"
  heat_s = x[:heat_on] ? "ON/#{x[:heat_mode]}" : "OFF/#{x[:heat_mode] || 'nil'}"
  edge = x[:edge] ? format("%.4f", x[:edge].to_f) : "n/a"
  tr = x[:tr] ? format("%.2f", x[:tr].to_f) : "n/a"
  dd = x[:dd] ? format("%.2f", x[:dd].to_f) : "n/a"
  mar = (x[:tr] && x[:dd] && x[:dd].to_f != 0) ? format("%.2f", x[:tr].to_f / x[:dd].to_f.abs) : "n/a"
  puts [
    "##{x[:id]}", x[:status], name, "p#{x[:pid]}", "TS#{x[:ts]}", "r#{x[:risk]}",
    heat_s, "caps=#{x[:max_sym]}/#{x[:max_port]}",
    "TR=#{tr}", "DD=#{dd}", "MAR=#{mar}", "Edge=#{edge}", "trades=#{x[:trades]}",
    "cell=#{x[:cell]}", "exp=#{x[:experiment]}", "range=#{x[:start]}..#{x[:endd]}",
    "stop=#{x[:stop]}", "fill=#{x[:fill]}", "init=#{x[:initial]}"
  ].join(" | ")
end

puts "\n=== AMBIG (leap field nil but cell/exp mentions leap) completed sample ==="
ambig.select { |x| x[:status] == "completed" }.sort_by { |x| -x[:id] }.first(25).each do |x|
  name = pnames[x[:pid]] || "?"
  edge = x[:edge] ? format("%.4f", x[:edge].to_f) : "n/a"
  puts ["##{x[:id]}", name, "TS#{x[:ts]}", "r#{x[:risk]}", "heat=#{x[:heat_on]}",
    "caps=#{x[:max_sym]}/#{x[:max_port]}", "Edge=#{edge}", "OA=#{x[:oa]}",
    "cell=#{x[:cell]}", "pack=#{x[:pack_keys].inspect}"].join(" | ")
end

puts "\n=== COMPLETED LEAP=all TS75/77 heat-OFF sample (contrast) ==="
leap_all.select { |x| x[:status] == "completed" && !x[:heat_on] }.sort_by { |x| -x[:id] }.first(20).each do |x|
  name = pnames[x[:pid]] || "?"
  edge = x[:edge] ? format("%.4f", x[:edge].to_f) : "n/a"
  puts ["##{x[:id]}", name, "TS#{x[:ts]}", "r#{x[:risk]}", "caps=#{x[:max_sym]}/#{x[:max_port]}",
    "Edge=#{edge}", "OA=#{x[:oa]}", "OADD=#{x[:oa_dd]}", "cell=#{x[:cell]}"].join(" | ")
end
