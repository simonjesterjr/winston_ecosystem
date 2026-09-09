(function () {
  const $ = (id) => document.getElementById(id);

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function chip(health) {
    const h = health || "UNKNOWN";
    return '<span class="chip ' + esc(h) + '">' + esc(h) + "</span>";
  }

  function table(headers, rows) {
    if (!rows || !rows.length) return "<p class='muted'>none / UNKNOWN</p>";
    const th = headers.map((h) => "<th>" + esc(h) + "</th>").join("");
    const body = rows.map((r) => "<tr>" + r.map((c) => "<td>" + c + "</td>").join("") + "</tr>").join("");
    return "<table><thead><tr>" + th + "</tr></thead><tbody>" + body + "</tbody></table>";
  }

  function renderContainers(data) {
    const list = (data && data.containers) || [];
    $("containers").innerHTML = table(
      ["id", "parent", "health", "status", "ports"],
      list.map((c) => [
        esc(c.id), esc(c.parent), chip(c.health), esc(c.status), esc(c.ports_live || "")
      ])
    );
  }

  function renderQueues(data) {
    const list = (data && data.queues) || [];
    $("queues").innerHTML = table(
      ["monolith", "queue", "depth", "retry", "dead", "health", "alerts"],
      list.map((q) => [
        esc(q.owning_monolith), esc(q.name), esc(q.depth), esc(q.retry), esc(q.dead),
        chip(q.health), esc((q.alerts || []).join("; "))
      ])
    );
  }

  function renderCron(data) {
    const list = (data && data.cron) || [];
    $("cron").innerHTML = table(
      ["owner", "id", "schedule", "class", "last_ok"],
      list.map((c) => [
        esc(c.owner || c.service), esc(c.id), esc(c.schedule), esc(c.class),
        esc(typeof c.last_ok === "object" ? (c.last_ok && c.last_ok.status) : c.last_ok)
      ])
    );
  }

  function opsList(data) {
    if (!data) return [];
    if (Array.isArray(data.ops)) return data.ops;
    if (Array.isArray(data.operational_portfolios)) return data.operational_portfolios;
    const http = data.http_list && data.http_list.portfolios;
    return Array.isArray(http) ? http.map((p) => Object.assign({ execution_mode: "UNKNOWN" }, p)) : [];
  }

  function band(op) {
    if (op.attention_band) return op.attention_band;
    if (op.closed || op.closed_at) return "inactive";
    if (!op.active) return "inactive";
    return op.execution_mode === "real" ? "real" : "paper";
  }

  function renderOps(data) {
    const list = opsList(data);
    $("op-table").innerHTML = table(
      ["id", "name", "mode", "band", "export_kind", "active", "markets", "ts"],
      list.map((op) => [
        esc(op.id),
        esc(op.name),
        esc(op.execution_mode || "UNKNOWN"),
        esc(band(op)),
        esc(op.export_kind || ""),
        esc(op.active),
        esc((op.markets || []).join(" ")),
        esc(op.trading_strategy || (op.trading_strategy && op.trading_strategy.name) || "")
      ])
    );
    renderRack(list);
  }

  function renderRack(list) {
    const el = $("op-rack");
    el.innerHTML = "";
    const planes = { real: 0, paper: 1, inactive: 2 };
    const counts = { 0: 0, 1: 0, 2: 0 };
    list.forEach((op) => {
      const p = planes[band(op)] ?? 2;
      const i = counts[p]++;
      const slab = document.createElement("button");
      slab.type = "button";
      slab.className = "slab " + band(op);
      slab.textContent = (op.seed_name || op.name || op.id) + " #" + op.id;
      slab.style.left = (16 + i * 110) + "px";
      slab.style.top = (16 + p * 72) + "px";
      slab.style.transform = "translate(" + (p * 18) + "px, 0) skewX(-18deg)";
      slab.title = "OP " + op.id + " execution_mode=" + (op.execution_mode || "UNKNOWN");
      el.appendChild(slab);
    });
    const cap = document.createElement("p");
    cap.className = "muted";
    cap.textContent = "Near = Active real. Mid = Active paper. Far = inactive/closed. Numbers match the table.";
    el.appendChild(cap);
  }

  async function load() {
    const paths = ["../snapshots/latest.json", "/operations/ecosystem.json"];
    let data = null;
    for (const p of paths) {
      try {
        const res = await fetch(p, { cache: "no-store" });
        if (res.ok) { data = await res.json(); break; }
      } catch (e) { /* try next */ }
    }
    $("as-of").textContent = data && data.generated_at
      ? ("snapshot " + data.generated_at)
      : "snapshot UNKNOWN — run inventory";
    if (!data) return;
    renderContainers(data.containers || data);
    renderQueues(data.queues || data);
    renderCron(data.cron || data);
    renderOps(data.operational_portfolios || data);
  }

  document.querySelectorAll("input[name=proj]").forEach((el) => {
    el.addEventListener("change", () => {
      const rack = el.value === "rack";
      $("op-table").classList.toggle("hidden", rack);
      $("op-rack").classList.toggle("hidden", !rack);
      $("op-rack").setAttribute("aria-hidden", rack ? "false" : "true");
    });
  });
  $("refresh").addEventListener("click", load);
  if (window.matchMedia("(max-width: 900px)").matches) {
    document.querySelector("input[value=table]").checked = true;
    $("op-rack").classList.add("hidden");
  }
  load();
})();
