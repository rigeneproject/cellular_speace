/** SPEACE T101 — Local Organism Monitor Frontend */
(function () {
  'use strict';

  const WS_URL = 'ws://127.0.0.1:8787/ws/state';
  const API_URL = 'http://127.0.0.1:8787/api/state';
  const POLL_INTERVAL = 2000;

  const els = {
    headerMeta: document.getElementById('header-meta'),
    connStatus: document.getElementById('conn-status'),
    connText: document.getElementById('conn-text'),
    errorBanner: document.getElementById('error-banner'),
  };

  let ws = null;
  let pollTimer = null;
  let _health = null;

  function fmtNum(n, d) {
    if (n === null || n === undefined || Number.isNaN(n)) return '—';
    return Number(n).toFixed(d);
  }

  function fmtBytes(b) {
    if (!b || Number.isNaN(b)) return '0 B';
    const u = ['B', 'KB', 'MB', 'GB', 'TB'];
    let i = 0;
    while (b >= 1024 && i < u.length - 1) { b /= 1024; i++; }
    return b.toFixed(1) + ' ' + u[i];
  }

  function setConn(ok, text) {
    els.connStatus.style.background = ok ? 'var(--accent-green)' : 'var(--accent-red)';
    els.connText.textContent = text;
    if (ok) {
      els.errorBanner.style.display = 'none';
    } else {
      els.errorBanner.style.display = 'block';
      els.errorBanner.textContent = text;
    }
  }

  function setBar(id, val, max) {
    const el = document.getElementById(id);
    if (!el) return;
    const pct = Math.max(0, Math.min(100, (val / max) * 100));
    el.style.width = pct + '%';
    el.className = 'gauge-bar-inner ' + (pct > 80 ? 'red' : pct > 50 ? 'yellow' : 'green');
  }

  function setBadge(id, level) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = level;
    el.className = 'badge ' + level;
  }

  function setPanelStatus(panelId, status) {
    const panel = document.getElementById(panelId);
    if (!panel) return;
    panel.classList.remove('critical', 'warning');
    if (status === 'critical') panel.classList.add('critical');
    else if (status === 'high' || status === 'warning') panel.classList.add('warning');
  }

  // ------------------------------------------------------------------ //
  // Render helpers
  // ------------------------------------------------------------------ //

  function renderList(containerId, items, mapper) {
    const c = document.getElementById(containerId);
    if (!c) return;
    if (!Array.isArray(items) || items.length === 0) {
      c.innerHTML = '<li>—</li>';
      return;
    }
    c.innerHTML = items.slice().reverse().map(mapper).join('');
  }

  function renderDrives(drives) {
    const c = document.getElementById('dr-list');
    if (!c) return;
    if (!Array.isArray(drives) || drives.length === 0) {
      c.innerHTML = '<div class="drive-item"><span class="drive-name">No drives</span></div>';
      return;
    }
    c.innerHTML = drives.map(d => {
      const lvl = Math.max(0, Math.min(1, d.level || 0));
      const pct = (lvl * 100).toFixed(0);
      const color = lvl > 0.7 ? 'var(--accent-red)' : lvl > 0.4 ? 'var(--accent-yellow)' : 'var(--accent-green)';
      return `<div class="drive-item">` +
        `<span class="drive-name">${d.name || 'unknown'}</span>` +
        `<div class="drive-bar"><div class="drive-bar-inner" style="width:${pct}%; background:${color}"></div></div>` +
        `<span class="drive-value">${pct}%</span>` +
        `</div>`;
    }).join('');
  }

  function renderAnomalies(anomalies) {
    const c = document.getElementById('a-list');
    if (!c) return;
    if (!Array.isArray(anomalies) || anomalies.length === 0) {
      c.innerHTML = '<li><span class="anomaly-type">No anomalies detected</span></li>';
      return;
    }
    c.innerHTML = anomalies.map(a => {
      const sev = a.severity || 'warning';
      return `<li>` +
        `<span class="anomaly-type">${a.type || 'unknown'}</span>` +
        `<span class="anomaly-severity ${sev}">${sev.toUpperCase()}</span>` +
        `</li>`;
    }).join('');
  }

  // ------------------------------------------------------------------ //
  // Apply state
  // ------------------------------------------------------------------ //

  function applyState(s) {
    // Body
    const b = s.body || {};
    document.getElementById('b-cpu').textContent = fmtNum(b.cpu, 1) + '%';
    setBar('bb-cpu', b.cpu, 100);
    const memGB = (b.memory_bytes || 0) / (1024 * 1024 * 1024);
    document.getElementById('b-ram').textContent = fmtNum(memGB, 2) + ' GB';
    setBar('bb-ram', memGB, 16);
    const diskGB = (b.disk_bytes || 0) / (1024 * 1024 * 1024);
    document.getElementById('b-disk').textContent = fmtNum(diskGB, 2) + ' GB';
    setBar('bb-disk', diskGB, 500);
    document.getElementById('b-net').textContent = fmtBytes(b.network_bytes);
    setBar('bb-net', b.network_bytes || 0, 1e9);
    document.getElementById('b-temp').textContent = fmtNum(b.temperature, 1) + ' C';
    setBar('bb-temp', b.temperature, 100);
    document.getElementById('b-batt').textContent = fmtNum(b.battery, 1) + '%';
    setBar('bb-batt', b.battery, 100);

    // Cognition
    const c = s.cognition || {};
    const gw = c.global_workspace || {};
    document.getElementById('c-gw').textContent = gw.global_state || gw.state || '—';
    document.getElementById('c-focus').textContent = c.attention_focus || '—';
    document.getElementById('c-awareness').textContent = fmtNum(gw.awareness_level || gw.awareness || 0, 3);
    const sm = c.self_model || {};
    document.getElementById('c-stage').textContent = sm.developmental_stage || '—';
    document.getElementById('c-phi').textContent = fmtNum(sm.coherence_phi || 0, 3);
    const goals = Array.isArray(c.active_goals) ? c.active_goals.join(', ') : '—';
    document.getElementById('c-goals').textContent = goals;
    renderList('c-narrative', c.narrative_trace || [], it => {
      let txt = it.title || it.event || (typeof it === 'string' ? it : JSON.stringify(it).slice(0, 80));
      return `<li>${txt}</li>`;
    });

    // Dynamics
    const d = s.dynamics || {};
    document.getElementById('d-chaos').textContent = fmtNum(d.chaos_score, 3);
    document.getElementById('d-rigidity').textContent = fmtNum(d.rigidity_score, 3);
    document.getElementById('d-drift').textContent = fmtNum(d.drift, 4);
    document.getElementById('d-attractors').textContent = d.attractor_count || 0;
    const crit = d.criticality || {};
    document.getElementById('d-branching').textContent = fmtNum(crit.branching_ratio, 3);
    document.getElementById('d-critical').textContent = crit.near_critical ? 'true' : 'false';
    const li = d.stabilizer && d.stabilizer.last_intervention ? d.stabilizer.last_intervention : {};
    const liTxt = li.tick !== undefined ? `tick ${li.tick}: ${li.pattern || '—'} → ${li.modulation || '—'}` : '—';
    document.getElementById('d-intervention').textContent = liTxt;
    setPanelStatus('panel-dynamics', d.chaos_score > 0.7 ? 'critical' : d.chaos_score > 0.4 ? 'warning' : 'normal');

    // Prediction Error
    const e = s.embodiment || {};
    document.getElementById('p-acc').textContent = fmtNum(e.prediction_accuracy, 3);
    document.getElementById('p-err').textContent = fmtNum(e.prediction_error, 3);

    // Embodiment
    document.getElementById('e-depth').textContent = fmtNum(e.depth, 3);
    document.getElementById('e-latency').textContent = fmtNum(e.loop_latency_ms, 1) + ' ms';
    document.getElementById('e-success').textContent = fmtNum(e.action_success_rate, 3);
    document.getElementById('e-sensor').textContent = e.sensor_status || 'unknown';
    document.getElementById('e-actuator').textContent = e.actuator_status || 'unknown';

    // Identity
    const i = s.identity || {};
    document.getElementById('i-count').textContent = i.node_count || 0;
    document.getElementById('i-hash').textContent = (i.consensus_identity_hash || '').slice(0, 16) || '—';
    document.getElementById('i-divergence').textContent = i.divergence_detected ? 'true' : 'false';
    renderList('i-nodes', i.distributed_nodes || [], n => `<li>${n.node_id || '?'} (trust ${fmtNum(n.trust_score, 2)})</li>`);
    renderList('i-narrative', i.narrative_sync || [], it => `<li>${it.title || it.event || JSON.stringify(it).slice(0, 60)}</li>`);

    // Drives
    const dr = s.drives || {};
    document.getElementById('dr-tendency').textContent = dr.action_tendency || 'idle';
    document.getElementById('dr-dominant').textContent = dr.dominant_drive || '—';
    renderDrives(dr.drives);

    // Safety
    const safe = s.safety || {};
    const risk = safe.risk_level || 'low';
    setBadge('s-badge', risk);
    document.getElementById('s-mode').textContent = safe.governance_mode || 'observation_only';
    document.getElementById('s-revert').textContent = safe.revert_available ? 'true' : 'false';
    document.getElementById('s-patches').textContent = safe.pending_patches || 0;
    const blockedCount = Array.isArray(safe.blocked_actions) ? safe.blocked_actions.length : 0;
    document.getElementById('s-blocked').textContent = blockedCount;
    const flags = Array.isArray(safe.anomaly_flags) ? safe.anomaly_flags : (Array.isArray(safe.flags) ? safe.flags : []);
    renderList('s-flags', flags, f => `<li>${f.type || 'unknown'}${f.tick !== undefined ? ' @ tick ' + f.tick : ''}</li>`);
    setPanelStatus('panel-safety', risk);

    // Anomaly Panel
    const ap = s.anomaly_panel || {};
    const overall = ap.overall_status || 'normal';
    setBadge('a-badge', overall);
    document.getElementById('a-status').textContent = overall;
    document.getElementById('a-count').textContent = ap.anomaly_count || 0;
    renderAnomalies(ap.anomalies || []);
    setPanelStatus('panel-anomaly', overall);

    // T102 — Alert Telemetry
    const al = s.alert_engine || {};
    const alAlerts = Array.isArray(al.alerts) ? al.alerts : [];
    document.getElementById('al-health').textContent = fmtNum(al.health_score, 3);
    document.getElementById('al-count').textContent = alAlerts.length;
    const alCrit = alAlerts.filter(a => a.severity === 'critical').length;
    const alWarn = alAlerts.filter(a => a.severity === 'warning').length;
    document.getElementById('al-critical').textContent = alCrit;
    document.getElementById('al-warning').textContent = alWarn;
    const alMaxSev = alCrit > 0 ? 'critical' : alWarn > 0 ? 'warning' : 'normal';
    setBadge('al-badge', alMaxSev);
    renderList('al-timeline', alAlerts, a => {
      const t = a.timestamp ? new Date(a.timestamp * 1000).toISOString().split('T')[1].replace('Z', '').slice(0, 8) : '—';
      return `<li><span class="anomaly-type">${a.alert_type || 'unknown'}</span><span class="anomaly-severity ${a.severity || 'warning'}">${(a.severity || 'warning').toUpperCase()}</span><span class="meta">${t}</span></li>`;
    });
    setPanelStatus('panel-alerts', alMaxSev);

    // Header meta from health (if loaded separately)
    if (s.timestamp) {
      const ts = new Date(s.timestamp * 1000).toISOString().split('T')[1].replace('Z', '');
      // optionally update something
    }
  }

  // ------------------------------------------------------------------ //
  // Transport
  // ------------------------------------------------------------------ //

  function connectWS() {
    try {
      ws = new WebSocket(WS_URL);
      ws.onopen = () => { setConn(true, 'live'); };
      ws.onmessage = (ev) => {
        try {
          const data = JSON.parse(ev.data);
          applyState(data);
        } catch (e) { /* ignore malformed */ }
      };
      ws.onerror = () => { setConn(false, 'ws error'); fallbackPoll(); };
      ws.onclose = () => { setConn(false, 'ws closed'); fallbackPoll(); };
    } catch (e) {
      fallbackPoll();
    }
  }

  async function fetchState() {
    try {
      const r = await fetch(API_URL);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const data = await r.json();
      setConn(true, 'polling');
      applyState(data);
    } catch (e) {
      setConn(false, e.message || 'disconnected');
    }
  }

  function fallbackPoll() {
    if (pollTimer) return;
    fetchState();
    pollTimer = setInterval(() => {
      fetchState();
    }, POLL_INTERVAL);
  }

  function stopPoll() {
    if (pollTimer) {
      clearInterval(pollTimer);
      pollTimer = null;
    }
  }

  // ------------------------------------------------------------------ //
  // Boot
  // ------------------------------------------------------------------ //

  fetchState().then(() => connectWS());
})();
