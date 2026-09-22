# frozen_string_literal: true
# Loop B overnight refresh 2026-09-21 — read-only WUT pull
# Host:
#   cd /home/johnkoisch/Documents/com/sawtooth
#   ./bin/compose cp ecosystem/docs/analysis/_loop_b_overnight_refresh_2026-09-21.rb winston_unit_test:/tmp/loop_b_refresh.rb
#   ./bin/compose exec -T winston_unit_test bin/rails runner /tmp/loop_b_refresh.rb

require "json"
require "date"

BOOKS = {
  "Walnut" => { pid: 223, cohort: "diversifier_contrast" },
  "Mint"   => { pid: 110, cohort: "promote_screen_hold" },
  "Yellow" => { pid: 111, cohort: "promote_screen_hold" },
  "Red"    => { pid: 6,   cohort: "mode_c_parent_solvent" },
  "Blue"   => { pid: 7,   cohort: "mode_c_parent_solvent" },
  "Mango"  => { pid: 65,  cohort: "mode_c_parent_solvent" },
  "Orange" => { pid: 35,  cohort: "mode_c_parent_solvent" },
  "Rust"   => { pid: 66,  cohort: "promote_screen_hold" },
  "Indigo" => { pid: 411, cohort: "mode_c_wv2_promoted" },
  "Teal"   => { pid: 412, cohort: "mode_c_wv2_promoted" },
  "Copper" => { pid: 413, cohort: "mode_c_wv2_promoted" },
  "Slate"  => { pid: 414, cohort: "mode_c_wv2_promoted" }
}.freeze

def regime(pcs)
  return nil if pcs.nil?
  v = pcs.to_f
  return "ultra_high_pcs" if v > 90
  return "high_mid_band" if v > 72 && v <= 90
  return "mid_band_corridor" if v >= 60 && v <= 72
  return "below_gate" if v >= 40 && v < 60
  "low_pcs_cluster"
end

def trading_days_between(d0, d1)
  return 0 if d0.nil? || d1.nil?
  a = d0.to_date
  b = d1.to_date
  return 0 if b < a
  n = 0
  cur = a
  while cur < b
    cur += 1
    n += 1 if cur.wday.between?(1, 5)
  end
  n
end

def parse_rj(r)
  raw = r.results_json
  raw.is_a?(String) ? JSON.parse(raw) : JSON.parse(raw.to_json)
rescue
  {}
end

# Equity slice helpers
def equity_dates(hist)
  return [] if hist.nil? || hist.empty?
  arr = hist.is_a?(String) ? JSON.parse(hist) : hist
  arr = arr["equity"] || arr["history"] || arr if arr.is_a?(Hash)
  return [] unless arr.is_a?(Array)
  arr.map do |pt|
    if pt.is_a?(Hash)
      d = pt["date"] || pt["as_of"] || pt["t"] || pt.keys.first
      v = pt["equity"] || pt["value"] || pt["oa"] || pt["v"] || pt.values.last
      [Date.parse(d.to_s), v.to_f] rescue nil
    elsif pt.is_a?(Array) && pt.size >= 2
      [Date.parse(pt[0].to_s), pt[1].to_f] rescue nil
    end
  end.compact.sort_by(&:first)
rescue
  []
end

def fwd_slice(points, as_of, want_td)
  return { status: "no_equity" } if points.empty?
  start_i = points.index { |d, _| d >= as_of } || points.index { |d, _| d > as_of }
  return { status: "no_equity_at_as_of" } unless start_i
  window = points[start_i, want_td + 1] || []
  have = [window.size - 1, 0].max
  if have < want_td
    return { status: "insufficient_forward", have_td: have, end: window.last&.first&.to_s }
  end
  e0 = window.first[1]
  e1 = window[want_td][1]
  peak = e0
  max_dd = 0.0
  window[0..want_td].each do |_, eq|
    peak = eq if eq > peak
    dd = peak.zero? ? 0.0 : (peak - eq) / peak.abs * 100.0
    max_dd = dd if dd > max_dd
  end
  oa_pct = e0.zero? ? nil : ((e1 - e0) / e0.abs) * 100.0
  { status: "ok", oa_pct: oa_pct&.round(4), oa_dd_pct: max_dd.round(4), end: window[want_td][0].to_s, have_td: want_td }
end

def fwd_available(points, as_of, max_td = 60)
  return { status: "no_equity" } if points.empty?
  start_i = points.index { |d, _| d >= as_of }
  return { status: "no_equity_at_as_of" } unless start_i
  remain = points.size - start_i - 1
  take = [remain, max_td].min
  return { status: "insufficient_forward", have_td: remain } if take <= 0
  window = points[start_i, take + 1]
  e0 = window.first[1]
  e1 = window.last[1]
  peak = e0
  max_dd = 0.0
  window.each do |_, eq|
    peak = eq if eq > peak
    dd = peak.zero? ? 0.0 : (peak - eq) / peak.abs * 100.0
    max_dd = dd if dd > max_dd
  end
  oa_pct = e0.zero? ? nil : ((e1 - e0) / e0.abs) * 100.0
  { status: "ok", td: take, oa_pct: oa_pct&.round(4), oa_dd_pct: max_dd.round(4), end: window.last[0].to_s }
end

def stub_for(row)
  pcs = row[:pcs_latest].to_f
  d_first = row[:delta_pcs_since_first].to_f
  d20 = row[:delta_pcs_20d]
  full_oa = row[:pbr_full_oa_pct]
  avail = row.dig(:fwd_available, :oa_pct)
  regime = row[:regime_tag_latest]

  # Walnut diversifier special
  return "watch" if row[:book] == "Walnut"

  collapse = (d_first <= -20) || (d20 && d20.to_f <= -15)
  insolvent = full_oa && full_oa.to_f < -50
  outside = !%w[mid_band_corridor high_mid_band].include?(regime.to_s) &&
            !(pcs >= 60 && pcs <= 90)

  if collapse && (insolvent || (avail && avail.to_f <= 0))
    "reweight_candidate"
  elsif collapse || outside
    # Orange paradox: collapse but OA strong → still candidate for geometry
    if collapse
      "reweight_candidate"
    else
      "watch"
    end
  elsif regime == "mid_band_corridor"
    "hold"
  elsif regime == "high_mid_band"
    "hold_diversifier_watch"
  else
    "hold"
  end
end

today = Date.today
rows = []
depth_summary = []

BOOKS.each do |book, meta|
  pid = meta[:pid]
  port = Portfolio.find_by(id: pid)
  next unless port

  snaps = PortfolioCorrelationSnapshot
            .where(portfolio_id: pid, methodology_version: "corr_v2")
            .order(:as_of_date)
  n = snaps.count
  first = snaps.first
  latest = snaps.last
  # latest daily_job vs any
  latest_daily = snaps.where(source: "daily_job").order(:as_of_date).last
  sources = snaps.map(&:source).tally

  # 20d lookback snap
  target_20 = latest&.as_of_date&.-(28) # calendar slack; pick closest <=
  snap_20 = nil
  if latest
    snap_20 = snaps.where("as_of_date <= ?", latest.as_of_date - 20).order(as_of_date: :desc).first
    snap_20 ||= snaps.where("as_of_date <= ?", latest.as_of_date - 14).order(as_of_date: :desc).first
  end

  pcs_latest = latest&.score
  pcs_first = first&.score
  delta_since_first = (pcs_latest && pcs_first) ? (pcs_latest.to_f - pcs_first.to_f).round(2) : nil
  delta_20 = (pcs_latest && snap_20) ? (pcs_latest.to_f - snap_20.score.to_f).round(2) : nil
  delta_max_r_20 = (latest && snap_20) ? (latest.max_abs_correlation.to_f - snap_20.max_abs_correlation.to_f).round(4) : nil

  days_outside = snaps.count { |s| s.score.to_f < 60 || s.score.to_f > 90 }

  # Best LEAP PBR
  pbrs = PortfolioBacktestRun.where(portfolio_id: pid, status: "completed").order(id: :desc).limit(120)
  scored = pbrs.map do |r|
    rj = parse_rj(r)
    leap = rj["leap_fulfillment"].to_s
    next unless leap == "all" || r.option_aware_total_return.present?
    {
      id: r.id,
      risk: r.risk_percentage,
      oa: r.option_aware_total_return,
      oa_dd: r.option_aware_max_drawdown,
      edge: r.try(:edge_r),
      edge_n: r.try(:edge_n) || rj["edge_n"],
      cell: rj["cell_key"],
      ts: rj["trading_strategy_id"],
      leap: leap.presence || (r.option_aware_total_return ? "oa_present" : nil),
      heat: rj["heat_mode"],
      end_date: r.try(:end_date) || rj["end_date"] || rj["current_date"] || r.try(:period_end),
      hist: rj["option_aware_equity_history"] || rj[:option_aware_equity_history]
    }
  end.compact
  leap_all = scored.select { |x| x[:leap] == "all" && x[:oa] }
  best = (leap_all.any? ? leap_all : scored.select { |x| x[:oa] }).max_by { |x| x[:oa].to_f }

  # Highlight Teal #743 / exciting cells if present
  highlight_ids = [743, 727, 767, 768, 769, 770]
  highlights = PortfolioBacktestRun.where(id: highlight_ids, portfolio_id: pid).map do |r|
    rj = parse_rj(r)
    { id: r.id, status: r.status, oa: r.option_aware_total_return, edge: r.try(:edge_r),
      cell: rj["cell_key"], heat: rj["heat_mode"], leap: rj["leap_fulfillment"] }
  end

  feature_as_of = first&.as_of_date
  points = best ? equity_dates(best[:hist]) : []
  fwd20 = feature_as_of ? fwd_slice(points, feature_as_of, 20) : { status: "no_feature" }
  fwd60 = feature_as_of ? fwd_slice(points, feature_as_of, 60) : { status: "no_feature" }
  fwd_av = feature_as_of ? fwd_available(points, feature_as_of, 60) : { status: "no_feature" }

  pbr_end = begin
    best && best[:end_date] ? Date.parse(best[:end_date].to_s) : (points.last&.first)
  rescue
    points.last&.first
  end

  td_first_to_pbr_end = trading_days_between(feature_as_of, pbr_end)
  td_first_to_today = trading_days_between(feature_as_of, today)
  td_latest_to_need60 = feature_as_of ? [60 - td_first_to_today, 0].max : nil

  row = {
    book: book,
    portfolio_id: pid,
    cohort: meta[:cohort],
    pcs_latest: pcs_latest&.to_f&.round(2),
    pcs_as_of_latest: latest&.as_of_date&.to_s,
    mean_abs_r_latest: latest&.mean_abs_correlation&.to_f&.round(4),
    max_abs_r_latest: latest&.max_abs_correlation&.to_f&.round(4),
    high_pair_count_latest: latest&.high_pair_count,
    delta_pcs_20d: delta_20,
    delta_max_r_20d: delta_max_r_20,
    delta_pcs_since_first: delta_since_first,
    pcs_first: pcs_first&.to_f&.round(2),
    pcs_first_as_of: first&.as_of_date&.to_s,
    n_snapshots: n,
    days_outside_60_90: days_outside,
    snapshot_source_latest: latest&.source,
    snapshot_sources: sources,
    latest_daily_job_as_of: latest_daily&.as_of_date&.to_s,
    latest_daily_job_pcs: latest_daily&.score&.to_f&.round(2),
    regime_tag_latest: regime(pcs_latest),
    feature_as_of: feature_as_of&.to_s,
    fwd_20d: fwd20,
    fwd_60d: fwd60,
    fwd_available: fwd_av,
    td_first_snap_to_pbr_end: td_first_to_pbr_end,
    td_first_snap_to_today: td_first_to_today,
    td_still_needed_for_60d_from_first: td_latest_to_need60,
    best_pbr_id: best&.dig(:id),
    pbr_cell: best&.dig(:cell),
    pbr_full_oa_pct: best&.dig(:oa)&.to_f&.round(4),
    pbr_full_edge_r: best&.dig(:edge)&.to_f&.round(4),
    pbr_edge_n: best&.dig(:edge_n),
    pbr_end_date: pbr_end&.to_s,
    highlight_pbrs: highlights,
    mid_band_corridor_member: regime(pcs_latest) == "mid_band_corridor"
  }
  row[:membership_recommendation_stub] = stub_for(row)
  rows << row

  depth_summary << {
    book: book,
    pid: pid,
    n_snaps: n,
    sources: sources,
    first: first&.as_of_date&.to_s,
    latest: latest&.as_of_date&.to_s,
    latest_src: latest&.source,
    pcs: pcs_latest&.to_f&.round(2),
    delta_since_first: delta_since_first,
    td_to_today: td_first_to_today,
    td_to_pbr_end: td_first_to_pbr_end,
    fwd60_status: fwd60[:status],
    fwd60_have: fwd60[:have_td],
    regime: regime(pcs_latest),
    stub: row[:membership_recommendation_stub],
    best_edge: best&.dig(:edge),
    best_oa: best&.dig(:oa)&.to_f&.round(1),
    best_pbr: best&.dig(:id)
  }
end

# Teal #743 Edge specifically (mid-band anchor)
teal743 = PortfolioBacktestRun.find_by(id: 743)
teal743_info = if teal743
  rj = parse_rj(teal743)
  { id: 743, status: teal743.status, oa: teal743.option_aware_total_return,
    edge_r: teal743.try(:edge_r), cell: rj["cell_key"], heat: rj["heat_mode"],
    leap: rj["leap_fulfillment"], portfolio_id: teal743.portfolio_id }
else
  { id: 743, missing: true }
end

out = {
  generated_at_mt: Time.now.getlocal("-06:00").strftime("%Y-%m-%d %H:%M:%S MT"),
  purpose: "Loop B overnight refresh — PCS depth + mid-band + interim fwd labels",
  prior_seed: "2026-09-21-loop-b-60d-forward-labels-seed.json",
  today: today.to_s,
  teal_743_anchor: teal743_info,
  depth_summary: depth_summary,
  rows: rows,
  unlock_fwd_60d: depth_summary.any? { |d| d[:fwd60_status] == "ok" },
  max_td_first_to_today: depth_summary.map { |d| d[:td_to_today].to_i }.max,
  mode_c_daily_job: depth_summary.select { |d| %w[Indigo Teal Copper Slate].include?(d[:book]) }.map { |d|
    { book: d[:book], sources: d[:sources], latest: d[:latest], latest_src: d[:latest_src], n: d[:n_snaps] }
  }
}

puts "REFRESH_JSON_BEGIN"
puts JSON.pretty_generate(out)
puts "REFRESH_JSON_END"
