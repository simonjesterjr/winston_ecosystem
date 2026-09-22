# Probe-before-promote

- **When:** 2026-09-21 22:29:34 MT
- **Overall:** FAIL
- **PBRs:** 727, 743, 763, 764

## PBR #727 — FAIL
- **PASS** `identity` (v1): {:portfolio_id=>412, :portfolio_name=>"Teal_WUT_evolved", :status=>"completed", :trading_strategy_id=>75, :trading_strategy_name=>"TurtleV1 S1 Breakout20/10", :risk_percentage=>0.02, :fill_cadence=>"resting_stop_touch", :leap_fulfillment=>"all", :cell_key=>"teal_rst_turtle_r02_leap30k_ts75_evolved", :experiment=>"mode_c_evolve_indigo_teal"}
- **FAIL** `heat_intent_vs_reality` (v1): {:heat_mode=>"turtle", :heat_present=>false, :heat_enabled=>false, :cell_key=>"teal_rst_turtle_r02_leap30k_ts75_evolved", :expected=>"turtle ⇒ heat hash present and heat_enabled"}
- **PASS** `position_caps` (v1): {:available=>true, :peak=>11, :breaches=>0, :cap=>12, :max_positions_per_symbol=>4}
- **PASS** `packaging_contracts` (v1): {:leap_fulfillment=>"all", :prefers_option=>true, :share_units=>nil, :contracts_floor=>nil, :m_band_allow_one=>false, :available=>true, :entries=>0, :option_entries=>0, :stock_entries=>0, :zero_contracts_smell=>false, :stock_only_despite_leap_pref=>false}
- **PASS** `edge_r_present` (v2): {:edge_r=>17.6998, :n=>nil}
- **PASS** `oa_dd_sanity` (v2): {:skipped=>true, :reason=>"oa_dd not stamped on results_json"}
- **PASS** `runner_sha` (v2): {:container_or_cwd_sha=>"0902707", :note=>"informational — compare to expected WUT merge when heat-ON"}

## PBR #743 — PASS
- **PASS** `identity` (v1): {:portfolio_id=>412, :portfolio_name=>"Teal_WUT_evolved", :status=>"completed", :trading_strategy_id=>75, :trading_strategy_name=>"TurtleV1 S1 Breakout20/10", :risk_percentage=>0.02, :fill_cadence=>"resting_stop_touch", :leap_fulfillment=>"all", :cell_key=>"teal_rst_legacy_r02_leap30k_ts75_evolved", :experiment=>"mode_c_evolve_indigo_teal_matrix"}
- **PASS** `heat_intent_vs_reality` (v1): {:heat_mode=>"legacy", :heat_present=>false, :heat_enabled=>false, :expected=>"legacy/off ⇒ heat_enabled false"}
- **PASS** `position_caps` (v1): {:available=>true, :peak=>11, :breaches=>0, :cap=>12, :max_positions_per_symbol=>4}
- **PASS** `packaging_contracts` (v1): {:leap_fulfillment=>"all", :prefers_option=>true, :share_units=>nil, :contracts_floor=>nil, :m_band_allow_one=>false, :available=>true, :entries=>0, :option_entries=>0, :stock_entries=>0, :zero_contracts_smell=>false, :stock_only_despite_leap_pref=>false}
- **PASS** `edge_r_present` (v2): {:edge_r=>17.0985, :n=>nil}
- **PASS** `oa_dd_sanity` (v2): {:skipped=>true, :reason=>"oa_dd not stamped on results_json"}
- **PASS** `runner_sha` (v2): {:container_or_cwd_sha=>"0902707", :note=>"informational — compare to expected WUT merge when heat-ON"}

## PBR #763 — FAIL
- **PASS** `identity` (v1): {:portfolio_id=>412, :portfolio_name=>"Teal_WUT_evolved", :status=>"completed", :trading_strategy_id=>75, :trading_strategy_name=>"TurtleV1 S1 Breakout20/10", :risk_percentage=>0.02, :fill_cadence=>"resting_stop_touch", :leap_fulfillment=>"all", :cell_key=>"teal_rst_turtle_r02_leap30k_ts75_heat_on_restamp727_20260921", :experiment=>"mode_c_evolve_indigo_teal_heat_on_restamp"}
- **PASS** `heat_intent_vs_reality` (v1): {:heat_mode=>"turtle", :heat_present=>true, :heat_enabled=>true, :cell_key=>"teal_rst_turtle_r02_leap30k_ts75_heat_on_restamp727_20260921", :expected=>"turtle ⇒ heat hash present and heat_enabled"}
- **FAIL** `position_caps` (v1): {:available=>true, :peak=>16, :breaches=>32, :cap=>12, :max_positions_per_symbol=>4}
- **PASS** `packaging_contracts` (v1): {:leap_fulfillment=>"all", :prefers_option=>true, :share_units=>nil, :contracts_floor=>nil, :m_band_allow_one=>false, :available=>true, :entries=>0, :option_entries=>0, :stock_entries=>0, :zero_contracts_smell=>false, :stock_only_despite_leap_pref=>false}
- **PASS** `edge_r_present` (v2): {:edge_r=>7.7087, :n=>nil}
- **PASS** `oa_dd_sanity` (v2): {:skipped=>true, :reason=>"oa_dd not stamped on results_json"}
- **PASS** `runner_sha` (v2): {:container_or_cwd_sha=>"0902707", :note=>"informational — compare to expected WUT merge when heat-ON"}

## PBR #764 — FAIL
- **PASS** `identity` (v1): {:portfolio_id=>412, :portfolio_name=>"Teal_WUT_evolved", :status=>"completed", :trading_strategy_id=>75, :trading_strategy_name=>"TurtleV1 S1 Breakout20/10", :risk_percentage=>0.02, :fill_cadence=>"resting_stop_touch", :leap_fulfillment=>"all", :cell_key=>"teal_rst_turtle_r02_leap30k_ts75_heat_on_restamp743_20260921", :experiment=>"mode_c_evolve_indigo_teal_heat_on_restamp"}
- **PASS** `heat_intent_vs_reality` (v1): {:heat_mode=>"turtle", :heat_present=>true, :heat_enabled=>true, :cell_key=>"teal_rst_turtle_r02_leap30k_ts75_heat_on_restamp743_20260921", :expected=>"turtle ⇒ heat hash present and heat_enabled"}
- **FAIL** `position_caps` (v1): {:available=>true, :peak=>16, :breaches=>32, :cap=>12, :max_positions_per_symbol=>4}
- **PASS** `packaging_contracts` (v1): {:leap_fulfillment=>"all", :prefers_option=>true, :share_units=>nil, :contracts_floor=>nil, :m_band_allow_one=>false, :available=>true, :entries=>0, :option_entries=>0, :stock_entries=>0, :zero_contracts_smell=>false, :stock_only_despite_leap_pref=>false}
- **PASS** `edge_r_present` (v2): {:edge_r=>7.7087, :n=>nil}
- **PASS** `oa_dd_sanity` (v2): {:skipped=>true, :reason=>"oa_dd not stamped on results_json"}
- **PASS** `runner_sha` (v2): {:container_or_cwd_sha=>"0902707", :note=>"informational — compare to expected WUT merge when heat-ON"}

