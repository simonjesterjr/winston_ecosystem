# frozen_string_literal: true

# Walnut #1428 unbind + Mode D #1585 DUT bind cutover on Winston v2.
# BINDING = bnd_3d6a5020d839c315583277d2 (IBKR paper DUT070450).
# Does NOT deactivate/archive Walnut. Does NOT mutate #1581.
# Does NOT Desk-Send or place orders. Does NOT touch winston_v2/BG source.
#
# Dry-run (default):
#   ./bin/compose exec -T winston_v2 bin/rails runner tmp/2026-09-24-walnut-unbind-1585-dut-bind.rb
# Apply:
#   ./bin/compose exec -T -e APPLY=1 winston_v2 bin/rails runner tmp/2026-09-24-walnut-unbind-1585-dut-bind.rb

require "json"

APPLY = ENV["APPLY"] == "1"
BINDING = "bnd_3d6a5020d839c315583277d2"
NICKNAME = "DUT070450"
WALNUT_ID = 1428
DUT_ID = 1585
KEPT_ID = 1581
IBKR = "interactive_broker_trader_api"
DUMMY = "dummy_sim"

def snap(portfolio)
  {
    "id" => portfolio.id,
    "name" => portfolio.name,
    "active" => portfolio.active,
    "execution_mode" => portfolio.execution_mode,
    "fulfillment_adapter_key" => portfolio.fulfillment_adapter_key,
    "broker_binding_id" => portfolio.broker_binding_id,
    "fulfillment_mode" => portfolio.fulfillment_mode,
    "leap_fulfillment" => portfolio.leap_fulfillment,
    "fingerprint" => portfolio.fingerprint,
    "trading_strategy_id" => portfolio.trading_strategy_id,
    "updated_at" => portfolio.updated_at.iso8601(6)
  }
end

def claimants
  Portfolio.where(broker_binding_id: BINDING).order(:id).pluck(:id)
end

walnut = Portfolio.find(WALNUT_ID)
dut = Portfolio.find(DUT_ID)
kept = Portfolio.find(KEPT_ID)

before = {
  "walnut_1428" => snap(walnut),
  "dut_1585" => snap(dut),
  "kept_1581" => snap(kept),
  "claimants" => claimants
}

raise "refusing: ##{WALNUT_ID} is not Walnut (#{walnut.name})" unless walnut.name.to_s.include?("Walnut")
raise "refusing: Walnut ##{WALNUT_ID} is not active" unless walnut.active
raise "refusing: Walnut execution_mode is #{walnut.execution_mode}, expected paper" unless walnut.execution_mode == "paper"
raise "refusing: Walnut is not the BINDING claimant (#{walnut.broker_binding_id})" unless walnut.broker_binding_id == BINDING
raise "refusing: Walnut adapter is #{walnut.fulfillment_adapter_key}, expected #{IBKR}" unless walnut.fulfillment_adapter_key == IBKR

raise "refusing: ##{DUT_ID} is not the Mode D Copper book (#{dut.name})" unless dut.name.to_s.include?("mode-d-from-wut-794")
raise "refusing: ##{DUT_ID} is not active" unless dut.active
raise "refusing: ##{DUT_ID} fulfillment_mode is #{dut.fulfillment_mode}, expected mode_d" unless dut.fulfillment_mode == "mode_d"
raise "refusing: ##{DUT_ID} leap_fulfillment is #{dut.leap_fulfillment}, expected none" unless dut.leap_fulfillment == "none"
raise "refusing: ##{DUT_ID} already bound to #{dut.broker_binding_id}" if dut.broker_binding_id.present?
raise "refusing: ##{DUT_ID} adapter is #{dut.fulfillment_adapter_key}, expected #{DUMMY}" unless dut.fulfillment_adapter_key == DUMMY

raise "refusing: ##{KEPT_ID} fulfillment_mode is #{kept.fulfillment_mode}, expected mode_c" unless kept.fulfillment_mode == "mode_c"
raise "refusing: ##{KEPT_ID} leap_fulfillment is #{kept.leap_fulfillment}, expected all" unless kept.leap_fulfillment == "all"
raise "refusing: ##{KEPT_ID} is bound (#{kept.broker_binding_id})" if kept.broker_binding_id.present?
raise "refusing: ##{KEPT_ID} adapter is #{kept.fulfillment_adapter_key}, expected #{DUMMY}" unless kept.fulfillment_adapter_key == DUMMY

raise "refusing: unexpected BINDING claimants #{before['claimants'].inspect}" unless before["claimants"] == [WALNUT_ID]

plan = {
  "apply" => APPLY,
  "binding" => BINDING,
  "nickname" => NICKNAME,
  "actions" => [
    "Walnut ##{WALNUT_ID}: fulfillment_adapter_key=#{DUMMY}, broker_binding_id=nil (stay active paper)",
    "##{DUT_ID}: fulfillment_adapter_key=#{IBKR}, broker_binding_id=#{BINDING} (keep mode_d / leap none)",
    "##{KEPT_ID}: unchanged"
  ],
  "before" => before
}
puts JSON.pretty_generate(plan)

unless APPLY
  puts "DRY_RUN no writes"
  exit 0
end

kept_before = before["kept_1581"]

ActiveRecord::Base.transaction do
  walnut.update!(
    fulfillment_adapter_key: DUMMY,
    broker_binding_id: nil
  )
  walnut.reload
  raise "Walnut deactivated" unless walnut.active == true
  raise "Walnut execution_mode drifted to #{walnut.execution_mode}" unless walnut.execution_mode == "paper"
  raise "Walnut still bound to #{walnut.broker_binding_id}" unless walnut.broker_binding_id.nil?
  raise "Walnut adapter is #{walnut.fulfillment_adapter_key}" unless walnut.fulfillment_adapter_key == DUMMY

  dut.update!(
    fulfillment_adapter_key: IBKR,
    broker_binding_id: BINDING
  )
  dut.reload
  raise "##{DUT_ID} adapter is #{dut.fulfillment_adapter_key}" unless dut.fulfillment_adapter_key == IBKR
  raise "##{DUT_ID} binding is #{dut.broker_binding_id}" unless dut.broker_binding_id == BINDING
  raise "##{DUT_ID} fulfillment_mode drifted to #{dut.fulfillment_mode}" unless dut.fulfillment_mode == "mode_d"
  raise "##{DUT_ID} leap_fulfillment drifted to #{dut.leap_fulfillment}" unless dut.leap_fulfillment == "none"
  raise "##{DUT_ID} deactivated" unless dut.active == true
  raise "##{DUT_ID} execution_mode drifted to #{dut.execution_mode}" unless dut.execution_mode == "paper"

  kept_now = snap(Portfolio.find(KEPT_ID))
  raise "##{KEPT_ID} changed: before=#{kept_before.inspect} after=#{kept_now.inspect}" unless kept_now == kept_before

  now_claimants = claimants
  raise "BINDING claimants are #{now_claimants.inspect}, expected [#{DUT_ID}]" unless now_claimants == [DUT_ID]
end

after = {
  "walnut_1428" => snap(Portfolio.find(WALNUT_ID)),
  "dut_1585" => snap(Portfolio.find(DUT_ID)),
  "kept_1581" => snap(Portfolio.find(KEPT_ID)),
  "claimants" => claimants
}

report = {
  "applied_at" => Time.now.utc.iso8601,
  "binding" => BINDING,
  "nickname" => NICKNAME,
  "before" => before,
  "after" => after,
  "guards" => {
    "walnut_active_paper_dummy_unbound" => after["walnut_1428"]["active"] == true &&
      after["walnut_1428"]["execution_mode"] == "paper" &&
      after["walnut_1428"]["fulfillment_adapter_key"] == DUMMY &&
      after["walnut_1428"]["broker_binding_id"].nil?,
    "dut_ibkr_bound_mode_d" => after["dut_1585"]["fulfillment_adapter_key"] == IBKR &&
      after["dut_1585"]["broker_binding_id"] == BINDING &&
      after["dut_1585"]["fulfillment_mode"] == "mode_d" &&
      after["dut_1585"]["leap_fulfillment"] == "none",
    "kept_1581_unchanged" => after["kept_1581"] == before["kept_1581"],
    "sole_claimant_1585" => after["claimants"] == [DUT_ID]
  }
}

out = "/app/tmp/2026-09-24-walnut-unbind-1585-dut-bind.json"
File.write(out, JSON.pretty_generate(report))
puts JSON.pretty_generate(report)
puts "WROTE #{out}"
