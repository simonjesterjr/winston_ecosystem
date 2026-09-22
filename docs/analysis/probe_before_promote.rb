# frozen_string_literal: true
# Probe-before-promote v1+v2 — host Definition of Done (DoD) gate for Portfolio Backtest Runs (PBRs).
#
# Usage (sawtooth, Winston Unit Test container):
#   ./bin/compose exec -T winston_unit_test \
#     bin/rails runner /ecosystem/scripts/probe_before_promote.rb 727 743 763 764
# Optional ENV:
#   PROBE_OUT=/ecosystem/docs/analysis/probe-before-promote-LAST.json
#   PROBE_STRICT=1  (default) exit 2 if any FAIL
#
# Owner: Sawtooth Ops (Chief of Staff fallback). Ticket: 2026-09-21-probe-before-promote.md

require "json"

IDS = ARGV.map { |a| Integer(a) rescue nil }.compact
abort "usage: rails runner probe_before_promote.rb ID [ID…]" if IDS.empty?

OUT = ENV.fetch("PROBE_OUT", "/ecosystem/docs/analysis/probe-before-promote-last.json")
STRICT = ENV.fetch("PROBE_STRICT", "1") != "0"

def results_hash(run)
  raw = run.respond_to?(:results_parsed) ? run.results_parsed : run.try(:results_json)
  h = raw.is_a?(Hash) ? raw : (JSON.parse(raw.to_s) rescue {})
  h = {} unless h.is_a?(Hash)
  h.respond_to?(:deep_stringify_keys) ? h.deep_stringify_keys : h.transform_keys(&:to_s)
end

def heat_enabled_of(run, rj)
  if run.respond_to?(:heat_enabled?)
    !!run.heat_enabled?
  else
    heat = rj["heat"]
    heat.is_a?(Hash) && !heat.empty?
  end
end

def peak_open_stats(rj, cap)
  events = rj["cash_events"]
  return { available: false, peak: nil, breaches: nil, cap: cap } unless events.is_a?(Array)
  peak = 0
  breaches = 0
  events.each do |e|
    next unless e.is_a?(Hash)
    n = e["open_positions"]
    next if n.nil?
    n = n.to_i
    peak = n if n > peak
    breaches += 1 if cap.positive? && n > cap
  end
  { available: true, peak: peak, breaches: breaches, cap: cap }
end

def option_entry_stats(rj)
  events = rj["cash_events"]
  return { available: false } unless events.is_a?(Array)
  # WUT cash_events are mostly "close" rows with is_option; also accept entry-like events if present
  rows = events.select { |e|
    e.is_a?(Hash) && (
      e.key?("is_option") ||
      e["event"].to_s.downcase.include?("entry") ||
      e["event"].to_s.downcase.include?("close")
    )
  }
  opt = rows.count { |e| e["is_option"] == true || e["is_option"].to_s == "true" }
  stock = rows.count { |e| e["is_option"] == false || e["is_option"].to_s == "false" || e["is_option"].nil? }
  # Prefer option-flagged closes as evidence of LEAP/call packaging in sim
  { available: true, events_scanned: rows.size, option_events: opt, stock_or_unflagged_events: stock,
    option_entries: opt, stock_entries: stock, entries: rows.size }
end

def packaging_intent(rj, run)
  leap = (rj["leap_fulfillment"] || run.try(:leap_fulfillment)).to_s
  cell = rj["cell_key"].to_s
  prefers_option = %w[all preferred required].include?(leap) ||
                   cell.include?("leap") ||
                   rj["fulfillment_plan_a"].to_s == "leap" ||
                   Array(rj.dig("packaging_preference")).first.to_s == "leap"
  # Share units for contract floor — prefer stamped signal_share_units / units hints
  share_units = [
    rj["signal_share_units"],
    rj["share_units"],
    rj["adjusted_share_units"],
  ].compact.map(&:to_f).find { |x| x.positive? }
  contracts_floor = share_units ? (share_units / 100.0).floor : nil
  {
    leap_fulfillment: leap,
    prefers_option: prefers_option,
    share_units: share_units,
    contracts_floor: contracts_floor,
    m_band_allow_one: rj["m_band_allow_one_contract"] == true,
  }
end

def check_heat(rj, run)
  mode = rj["heat_mode"].to_s
  cell = rj["cell_key"].to_s
  heat = rj["heat"]
  heat_present = heat.is_a?(Hash) && !heat.empty?
  enabled = heat_enabled_of(run, rj)
  wants_turtle = mode == "turtle" || cell.include?("_turtle_") || cell.include?("heat_on")
  wants_off = mode == "legacy" || cell.include?("_legacy_") || mode.empty? && !wants_turtle

  if wants_turtle
    ok = heat_present && enabled
    {
      id: "heat_intent_vs_reality",
      version: "v1",
      pass: ok,
      detail: {
        heat_mode: mode,
        heat_present: heat_present,
        heat_enabled: enabled,
        cell_key: cell,
        expected: "turtle ⇒ heat hash present and heat_enabled",
      },
    }
  elsif wants_off || mode == "legacy"
    # legacy/off: hash should be absent (label-only turtle already caught above)
    ok = !enabled
    {
      id: "heat_intent_vs_reality",
      version: "v1",
      pass: ok,
      detail: {
        heat_mode: mode.presence || "(blank)",
        heat_present: heat_present,
        heat_enabled: enabled,
        expected: "legacy/off ⇒ heat_enabled false",
      },
    }
  else
    {
      id: "heat_intent_vs_reality",
      version: "v1",
      pass: true,
      detail: { heat_mode: mode, note: "no clear turtle/legacy intent; informational only", heat_present: heat_present, heat_enabled: enabled },
    }
  end
end

def check_caps(rj, run)
  cap = run.max_positions_per_portfolio.to_i
  stats = peak_open_stats(rj, cap)
  unless stats[:available]
    return { id: "position_caps", version: "v1", pass: false, detail: { error: "cash_events missing — cannot measure peak open" } }
  end
  ok = stats[:breaches].to_i.zero? && (cap <= 0 || stats[:peak].to_i <= cap)
  {
    id: "position_caps",
    version: "v1",
    pass: ok,
    detail: stats.merge(max_positions_per_symbol: run.max_positions_per_symbol),
  }
end

def check_packaging(rj, run)
  intent = packaging_intent(rj, run)
  opts = option_entry_stats(rj)
  # System One smell: prefers LEAP/call but floor(N/100)==0
  zero_contracts = intent[:prefers_option] && !intent[:m_band_allow_one] &&
                   intent[:contracts_floor] == 0
  # If share_units unknown but leap-all and zero option entries on a completed run with many stock entries → soft fail
  soft = false
  if intent[:prefers_option] && intent[:contracts_floor].nil? && opts[:available] && run.status.to_s == "completed"
    if opts[:entries].to_i.positive? && opts[:option_events].to_i.zero? && opts[:stock_or_unflagged_events].to_i.positive?
      soft = true
    end
  end
  ok = !zero_contracts && !soft
  {
    id: "packaging_contracts",
    version: "v1",
    pass: ok,
    detail: intent.merge(opts).merge(
      zero_contracts_smell: zero_contracts,
      stock_only_despite_leap_pref: soft,
    ),
  }
end

def check_identity(rj, run)
  {
    id: "identity",
    version: "v1",
    pass: true,
    detail: {
      portfolio_id: run.portfolio_id,
      portfolio_name: run.portfolio&.try(:name),
      status: run.status.to_s,
      trading_strategy_id: rj["trading_strategy_id"],
      trading_strategy_name: rj["trading_strategy_name"],
      risk_percentage: run.try(:risk_percentage) || rj["risk_percentage"],
      fill_cadence: rj["fill_cadence"],
      leap_fulfillment: rj["leap_fulfillment"],
      cell_key: rj["cell_key"],
      experiment: rj["experiment"],
    },
  }
end

def check_edge_v2(rj, run)
  # Expect Edge card / edge_r when completed and not barren n=0
  edge_r = run.try(:edge_r)
  edge_r = rj["edge_r"] if edge_r.nil?
  status = run.status.to_s
  if status != "completed"
    return { id: "edge_r_present", version: "v2", pass: true, detail: { skipped: true, reason: "not completed", status: status } }
  end
  # barren allowed if explicitly n=0 in edge snapshot
  snap = rj["edge"] || rj["edge_snapshot"] || {}
  n = snap.is_a?(Hash) ? (snap["n"] || snap["trade_count"]) : nil
  if edge_r.nil? && n.to_i == 0
    return { id: "edge_r_present", version: "v2", pass: true, detail: { barren: true, n: 0 } }
  end
  ok = !edge_r.nil?
  { id: "edge_r_present", version: "v2", pass: ok, detail: { edge_r: edge_r, n: n } }
end

def check_oa_dd_sanity_v2(rj, run)
  # Flag catastrophic OA DD when heat supposedly on (informational FAIL if OA DD > 50 and heat_enabled)
  oa_dd = rj["option_aware_max_drawdown"] || rj["oa_max_drawdown"] || rj.dig("summary", "option_aware_max_drawdown")
  # sometimes nested in metrics
  if oa_dd.nil? && rj["option_aware_equity_history"].is_a?(Array)
    # skip heavy recompute — leave informational
    return { id: "oa_dd_sanity", version: "v2", pass: true, detail: { skipped: true, reason: "oa_dd not stamped on results_json" } }
  end
  return { id: "oa_dd_sanity", version: "v2", pass: true, detail: { skipped: true, reason: "no oa_dd field" } } if oa_dd.nil?

  dd = oa_dd.to_f.abs
  # normalize if fraction
  dd = dd * 100.0 if dd <= 1.5
  heat_on = heat_enabled_of(run, rj)
  # FAIL smell: heat on AND OA DD >= 50%
  ok = !(heat_on && dd >= 50.0)
  { id: "oa_dd_sanity", version: "v2", pass: ok, detail: { oa_dd_pct: dd, heat_enabled: heat_on, threshold_pct: 50.0 } }
end

def check_runner_sha_v2
  sha = begin
    `git -C /app rev-parse --short HEAD 2>/dev/null`.to_s.strip
  rescue
    ""
  end
  sha = `git rev-parse --short HEAD 2>/dev/null`.to_s.strip if sha.empty?
  {
    id: "runner_sha",
    version: "v2",
    pass: true,
    detail: { container_or_cwd_sha: sha.presence || "unknown", note: "informational — compare to expected WUT merge when heat-ON" },
  }
end

# --- build report ---
rows = []
IDS.each do |id|
  run = PortfolioBacktestRun.find_by(id: id)
  unless run
    rows << { pbr_id: id, found: false, checks: [], overall_pass: false }
    next
  end
  rj = results_hash(run)
  checks = [
    check_identity(rj, run),
    check_heat(rj, run),
    check_caps(rj, run),
    check_packaging(rj, run),
    check_edge_v2(rj, run),
    check_oa_dd_sanity_v2(rj, run),
    check_runner_sha_v2,
  ]
  # System One state facts for Jev
  heat_c = checks.find { |c| c[:id] == "heat_intent_vs_reality" }
  caps_c = checks.find { |c| c[:id] == "position_caps" }
  pack_c = checks.find { |c| c[:id] == "packaging_contracts" }
  jev_state = {
    pbr_id: id,
    heat_mode: heat_c.dig(:detail, :heat_mode),
    heat_present: heat_c.dig(:detail, :heat_present),
    heat_enabled: heat_c.dig(:detail, :heat_enabled),
    peak_open: caps_c.dig(:detail, :peak),
    max_positions_per_portfolio: caps_c.dig(:detail, :cap),
    open_gt_cap_events: caps_c.dig(:detail, :breaches),
    leap_fulfillment: pack_c.dig(:detail, :leap_fulfillment),
    prefers_option_packaging: pack_c.dig(:detail, :prefers_option),
    share_units: pack_c.dig(:detail, :share_units),
    contracts_floor: pack_c.dig(:detail, :contracts_floor),
    zero_contracts_smell: pack_c.dig(:detail, :zero_contracts_smell),
    stock_only_despite_leap_pref: pack_c.dig(:detail, :stock_only_despite_leap_pref),
  }
  overall = checks.all? { |c| c[:pass] }
  rows << {
    pbr_id: id,
    found: true,
    overall_pass: overall,
    checks: checks,
    jev_state: jev_state,
  }
end

report = {
  at: Time.now.getlocal("-06:00").strftime("%Y-%m-%d %H:%M:%S MT"),
  tool: "probe_before_promote",
  versions: %w[v1 v2],
  ticket: "2026-09-21-probe-before-promote.md",
  pbr_ids: IDS,
  rows: rows,
  overall_pass: rows.all? { |r| r[:overall_pass] },
}

File.write(OUT, JSON.pretty_generate(report))
puts JSON.pretty_generate(report)
puts "Wrote #{OUT}"

# Markdown summary
md_path = OUT.sub(/\.json\z/, ".md")
lines = []
lines << "# Probe-before-promote"
lines << ""
lines << "- **When:** #{report[:at]}"
lines << "- **Overall:** #{report[:overall_pass] ? "PASS" : "FAIL"}"
lines << "- **PBRs:** #{IDS.join(", ")}"
lines << ""
rows.each do |r|
  lines << "## PBR ##{r[:pbr_id]} — #{r[:found] ? (r[:overall_pass] ? "PASS" : "FAIL") : "NOT FOUND"}"
  next unless r[:found]
  r[:checks].each do |c|
    mark = c[:pass] ? "PASS" : "FAIL"
    lines << "- **#{mark}** `#{c[:id]}` (#{c[:version]}): #{c[:detail].inspect}"
  end
  lines << ""
end
File.write(md_path, lines.join("\n") + "\n")
puts "Wrote #{md_path}"

exit(report[:overall_pass] || !STRICT ? 0 : 2)
