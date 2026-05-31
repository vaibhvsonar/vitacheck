/* ═══════════════════════════════════════════
   STATE
═══════════════════════════════════════════ */
let sessionHistory = [];
let apiBase = localStorage.getItem('vc_api') || 'http://localhost:5000';
let recognition = null;
let isRecording = false;
let analysisCount = 0;

/* ═══════════════════════════════════════════
   SETTINGS LOAD ON BOOT
═══════════════════════════════════════════ */
(function initSettings() {
  const theme = localStorage.getItem('vc_theme') || 'dark';
  applyThemeImmediate(theme);

  const accent = localStorage.getItem('vc_accent');
  const accent2 = localStorage.getItem('vc_accent2');
  if (accent) applyAccentImmediate(accent, accent2);

  const fs = localStorage.getItem('vc_font') || 'md';
  applyFontSizeImmediate(fs);

  if (localStorage.getItem('vc_compact') === 'true') {
    document.body.classList.add('compact');
  }
  if (localStorage.getItem('vc_bg') === 'false') {
    document.querySelector('.bg-canvas').style.display = 'none';
    document.querySelector('.bg-grid').style.display = 'none';
  }

  // API URL
  const savedApi = localStorage.getItem('vc_api');
  if (savedApi) apiBase = savedApi;
})();

/* ═══════════════════════════════════════════
   THEME
═══════════════════════════════════════════ */
function applyThemeImmediate(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  document.getElementById('themeToggleBtn').textContent = theme === 'dark' ? '🌙' : '☀️';
  localStorage.setItem('vc_theme', theme);
}
function setTheme(theme) {
  applyThemeImmediate(theme);
  document.getElementById('themeOptDark').classList.toggle('selected', theme === 'dark');
  document.getElementById('themeOptLight').classList.toggle('selected', theme === 'light');
  showToast(theme === 'dark' ? '🌙 Dark mode enabled' : '☀️ Light mode enabled');
}
function quickToggleTheme() {
  const cur = document.documentElement.getAttribute('data-theme');
  setTheme(cur === 'dark' ? 'light' : 'dark');
  // Sync modal
  document.getElementById('themeOptDark').classList.toggle('selected', cur !== 'dark');
  document.getElementById('themeOptLight').classList.toggle('selected', cur === 'dark');
}

/* ═══════════════════════════════════════════
   ACCENT COLOR
═══════════════════════════════════════════ */
function applyAccentImmediate(color, color2) {
  const root = document.documentElement;
  root.style.setProperty('--accent', color);
  root.style.setProperty('--accent2', color2 || color);
  root.style.setProperty('--accent-glow', color + '25');
  root.style.setProperty('--accent-glow2', color + '14');
  root.style.setProperty('--green', color);
  root.style.setProperty('--green-bg', color + '1a');
}
function setAccent(color, color2) {
  applyAccentImmediate(color, color2);
  localStorage.setItem('vc_accent', color);
  localStorage.setItem('vc_accent2', color2);
  document.querySelectorAll('.accent-swatch').forEach(s => {
    s.classList.toggle('selected', s.dataset.color === color);
  });
  showToast('🎨 Accent color updated');
}

/* ═══════════════════════════════════════════
   FONT SIZE
═══════════════════════════════════════════ */
function applyFontSizeImmediate(size) {
  document.body.classList.remove('font-sm','font-md','font-lg','font-xl');
  document.body.classList.add('font-' + size);
  localStorage.setItem('vc_font', size);
}
function setFontSize(size) {
  applyFontSizeImmediate(size);
  document.querySelectorAll('[id^="fsOpt-"]').forEach(el => el.classList.remove('selected'));
  document.getElementById('fsOpt-' + size).classList.add('selected');
  showToast('🔡 Text size updated');
}

/* ═══════════════════════════════════════════
   FEATURE TOGGLES
═══════════════════════════════════════════ */
function applyCompact(on) {
  document.body.classList.toggle('compact', on);
  localStorage.setItem('vc_compact', on);
  showToast(on ? '📐 Compact mode on' : '📐 Compact mode off');
}
function applyBg(on) {
  document.querySelector('.bg-canvas').style.display = on ? '' : 'none';
  document.querySelector('.bg-grid').style.display = on ? '' : 'none';
  localStorage.setItem('vc_bg', on);
}
function applyVoice(on) {
  document.getElementById('voiceRow').style.display = on ? 'flex' : 'none';
}
function applyHistory(on) {
  const hCard = document.getElementById('historyCard');
  if (!on) hCard.style.display = 'none';
  localStorage.setItem('vc_history', on);
}

/* ═══════════════════════════════════════════
   SETTINGS MODAL
═══════════════════════════════════════════ */
function openSettings() {
  const theme = document.documentElement.getAttribute('data-theme');
  document.getElementById('themeOptDark').classList.toggle('selected', theme === 'dark');
  document.getElementById('themeOptLight').classList.toggle('selected', theme === 'light');

  const savedAccent = localStorage.getItem('vc_accent') || '#00d4aa';
  document.querySelectorAll('.accent-swatch').forEach(s => s.classList.toggle('selected', s.dataset.color === savedAccent));

  const savedFs = localStorage.getItem('vc_font') || 'md';
  document.querySelectorAll('[id^="fsOpt-"]').forEach(el => el.classList.remove('selected'));
  document.getElementById('fsOpt-' + savedFs).classList.add('selected');

  document.getElementById('toggleCompact').checked = document.body.classList.contains('compact');
  document.getElementById('toggleBg').checked = document.querySelector('.bg-canvas').style.display !== 'none';
  document.getElementById('apiUrlInput').value = apiBase;

  document.getElementById('settingsModal').classList.add('open');
}
function closeSettingsBtn() { document.getElementById('settingsModal').classList.remove('open'); }
function closeSettings(e) { if (e.target === document.getElementById('settingsModal')) closeSettingsBtn(); }

function saveApiUrl() {
  apiBase = document.getElementById('apiUrlInput').value.trim() || 'http://localhost:5000';
  localStorage.setItem('vc_api', apiBase);
  showToast('🔌 API URL saved');
}

function resetSettings() {
  localStorage.clear();
  applyThemeImmediate('dark');
  applyAccentImmediate('#00d4aa','#00b894');
  applyFontSizeImmediate('md');
  document.body.classList.remove('compact');
  document.querySelector('.bg-canvas').style.display='';
  document.querySelector('.bg-grid').style.display='';
  apiBase = 'http://localhost:5000';
  showToast('↺ Settings reset');
  setTimeout(closeSettingsBtn, 800);
}

/* ═══════════════════════════════════════════
   EXPORT MODAL
═══════════════════════════════════════════ */
function openExport() { document.getElementById('exportModal').classList.add('open'); }
function closeExportBtn() { document.getElementById('exportModal').classList.remove('open'); }
function closeExport(e) { if (e.target === document.getElementById('exportModal')) closeExportBtn(); }

function exportAs(fmt) {
  if (sessionHistory.length === 0) { showToast('⚠️ No results to export yet'); return; }
  const now = new Date().toLocaleString();

  if (fmt === 'json') {
    const blob = new Blob([JSON.stringify({ exported: now, results: sessionHistory }, null, 2)], { type:'application/json' });
    downloadBlob(blob, 'vitacheck-results.json');
  } else if (fmt === 'csv') {
    const rows = [['Condition','Confidence','Tier','Query','Time']];
    sessionHistory.forEach(h => rows.push([h.label, h.conf.toFixed(1)+'%', h.tier, '"'+h.query.replace(/"/g,"'")+'"', h.time]));
    const blob = new Blob([rows.map(r=>r.join(',')).join('\n')], { type:'text/csv' });
    downloadBlob(blob, 'vitacheck-results.csv');
  } else if (fmt === 'txt') {
    let txt = 'VitaCheck — Session Report\n' + '='.repeat(40) + '\nExported: ' + now + '\n\n';
    sessionHistory.forEach((h,i) => {
      txt += `[${i+1}] ${h.label} (${h.conf.toFixed(1)}%, ${h.tier} confidence)\nQuery: ${h.query}\nTime: ${h.time}\n\n`;
    });
    txt += '\n⚠️ Educational use only. Not medical advice.';
    const blob = new Blob([txt], { type:'text/plain' });
    downloadBlob(blob, 'vitacheck-report.txt');
  } else if (fmt === 'print') {
    window.print();
  }
  closeExportBtn();
  showToast('✅ Exported as ' + fmt.toUpperCase());
}

function downloadBlob(blob, filename) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
}

/* ═══════════════════════════════════════════
   VOICE INPUT
═══════════════════════════════════════════ */
function toggleVoice() {
  if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    showToast('🎙 Voice not supported in this browser');
    return;
  }
  if (isRecording) {
    recognition.stop();
    return;
  }
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SR();
  recognition.lang = 'en-US';
  recognition.continuous = false;
  recognition.interimResults = true;

  recognition.onstart = () => {
    isRecording = true;
    document.getElementById('voiceBtn').classList.add('recording');
    document.getElementById('voiceBtn').textContent = '⏹ Recording…';
    document.getElementById('voiceHint').textContent = 'Speak now — click to stop';
  };
  recognition.onresult = (e) => {
    const transcript = Array.from(e.results).map(r => r[0].transcript).join('');
    document.getElementById('symptomInput').value = transcript;
    updateCharCount(document.getElementById('symptomInput'));
  };
  recognition.onend = () => {
    isRecording = false;
    document.getElementById('voiceBtn').classList.remove('recording');
    document.getElementById('voiceBtn').textContent = '🎙 Voice Input';
    document.getElementById('voiceHint').textContent = 'Click to speak your symptoms';
  };
  recognition.start();
}

/* ═══════════════════════════════════════════
   INPUT HELPERS
═══════════════════════════════════════════ */
function updateCharCount(el) {
  const len = el.value.length;
  const el2 = document.getElementById('charCount');
  el2.textContent = `${len} / 500`;
  el2.classList.toggle('warn', len > 400);
  if (len > 500) el.value = el.value.slice(0, 500);
}
function setChip(text) {
  document.getElementById('symptomInput').value = text;
  updateCharCount(document.getElementById('symptomInput'));
  document.getElementById('symptomInput').focus();
}
function appendTag(tag) {
  const ta = document.getElementById('symptomInput');
  ta.value = ta.value.trim() ? ta.value.trim() + ', ' + tag : 'I have ' + tag;
  updateCharCount(ta);
  ta.focus();
}

/* ═══════════════════════════════════════════
   ANALYSE
═══════════════════════════════════════════ */
function setLoading(on) {
  document.getElementById('analyseBtn').disabled = on;
  document.getElementById('btnSpinner').style.display = on ? 'block' : 'none';
  document.getElementById('btnText').textContent = on ? 'Analysing…' : '⚡ Analyse Symptoms';
}

function resetChat() {
  document.getElementById('chatArea').innerHTML = '';
  document.getElementById('resultCard').style.display = 'none';
  document.getElementById('symptomInput').value = '';
  updateCharCount(document.getElementById('symptomInput'));
  analysisCount = 0;
  document.getElementById('resultCount').textContent = '';
}

async function analyse() {
  const text = document.getElementById('symptomInput').value.trim();
  if (!text) { showToast('✏️ Please describe your symptoms first'); return; }

  setLoading(true);
  document.getElementById('resultCard').style.display = 'block';
  addUserMsg(text);

  try {
    const res = await fetch(`${apiBase}/analyse`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({text})
    });
    const data = await res.json();
    renderResponse(data, text);
  } catch(err) {
    addBotMsg(`<div class="info-card" style="border-color:rgba(229,62,90,0.2);">
      <strong style="color:var(--red);">⚡ Connection Error</strong><br>
      Cannot connect to VitaCheck backend at <code>${apiBase}</code><br><br>
      <strong>Run this in your terminal:</strong><br>
      <code style="display:block;margin-top:6px;padding:6px 10px;background:var(--card);border-radius:6px;font-size:0.78rem;">python app.py</code>
      <br>Then refresh and try again. You can also change the API URL in ⚙️ Settings.
    </div>`);
  }
  setLoading(false);
}

/* ═══════════════════════════════════════════
   RENDER RESPONSE
═══════════════════════════════════════════ */
function addUserMsg(text) {
  const area = document.getElementById('chatArea');
  const div = document.createElement('div');
  div.className = 'msg';
  div.innerHTML = `<div class="msg-label" style="text-align:right;color:var(--accent);font-size:0.65rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:4px;">You</div>
    <div class="msg-user-wrap"><div class="msg-user">${escHtml(text)}</div></div>`;
  area.appendChild(div);
}

function addBotMsg(html) {
  const area = document.getElementById('chatArea');
  const div = document.createElement('div');
  div.className = 'msg';
  div.innerHTML = `<div class="msg-label" style="color:var(--muted);font-size:0.65rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:4px;">VitaCheck</div>${html}`;
  area.appendChild(div);
  if (document.getElementById('toggleAutoscroll')?.checked !== false) {
    div.scrollIntoView({behavior:'smooth',block:'nearest'});
  }
  analysisCount++;
  document.getElementById('resultCount').textContent = analysisCount > 1 ? `${analysisCount} analyses` : '';
}

function escHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function renderResponse(data, userText) {
  if (data.type === 'emergency') {
    addBotMsg(`<div class="emergency-card">
      <div class="emg-icon">🚨</div>
      <div class="emg-title">Possible Emergency Detected</div>
      <div class="emg-body">Your symptoms may indicate a <strong>medical emergency</strong>. Please do not wait — seek immediate medical attention or call emergency services.</div>
      <div class="emg-number">📞 Emergency: 112 / 911</div>
    </div>`);
    return;
  }
  if (data.type === 'greeting') { addBotMsg(`<div class="info-card">👋 ${data.message}</div>`); return; }
  if (data.type === 'capability') {
    addBotMsg(`<div class="info-card">🤖 I'm <strong>VitaCheck</strong>, a BiomedBERT-powered symptom analyser. Describe your symptoms and I'll identify possible conditions with confidence scores and guidance.</div>`);
    return;
  }
  if (data.type === 'out_of_scope' || data.error) {
    addBotMsg(`<div class="info-card">${data.message || data.error}</div>`);
    return;
  }
  if (data.type === 'result') {
    const { label, confidence: conf, tier, top_k, guidance, disease_description } = data;
    const tierClass = tier==='high'?'rb-high':tier==='moderate'?'rb-moderate':'rb-low';
    const tierLabel = tier==='high'?'✦ High Confidence':tier==='moderate'?'◈ Moderate':'◌ Low Confidence';
    const fillClass = tier==='high'?'cf-high':tier==='moderate'?'cf-moderate':'cf-low';

    let topkHtml = '';
    if (top_k?.length) {
      const sorted = [...top_k].sort((a,b)=>b.confidence-a.confidence);
      topkHtml = `<div class="topk-title">Top Possible Conditions</div><div class="topk-list">
        ${sorted.map((item,i)=>`<div class="topk-row rank-${i+1}">
          <div class="topk-rank">${i+1}</div>
          <div class="topk-name">${item.label}</div>
          <div class="topk-mini-bar"><div class="topk-mini-fill" style="width:${item.confidence}%"></div></div>
          <div class="topk-pct">${typeof item.confidence==='number'?item.confidence.toFixed(1):item.confidence}%</div>
        </div>`).join('')}
      </div>`;
    }

    let guidanceHtml = '';
    if (guidance) {
      guidanceHtml = `<div class="guidance-block">
        ${guidance.next_steps?`<div class="guidance-row"><div class="guidance-ico">📋</div><div><div class="guidance-key">Next Steps</div><div class="guidance-val">${guidance.next_steps}</div></div></div>`:''}
        ${guidance.seek_help?`<div class="guidance-row"><div class="guidance-ico">🏥</div><div><div class="guidance-key">When to seek help</div><div class="guidance-val">${guidance.seek_help}</div></div></div>`:''}
      </div>`;
    }

    const uid = 'c' + Date.now();
    const html = `<div class="result-panel just-analysed">
      <div class="result-header"><span class="result-badge ${tierClass}">${tierLabel}</span></div>
      <div class="result-body">
        <div style="margin-bottom:14px;">
          <div class="condition-label">Most Likely Condition</div>
          <div class="condition-name">${label}</div>
          <div class="condition-note">Based on your described symptoms</div>
        </div>
        <div class="conf-meta"><span class="conf-label">Confidence Score</span><span class="conf-pct">${conf.toFixed(1)}%</span></div>
        <div class="conf-track"><div class="conf-fill ${fillClass}" id="${uid}" style="width:0%"></div></div>
        ${disease_description?`<div class="desc-box">${disease_description}</div>`:''}
        ${topkHtml}${guidanceHtml}
        <div class="share-row">
          <span class="share-label">Was this helpful?</span>
          <button class="fb-btn" onclick="this.classList.toggle('active')">👍</button>
          <button class="fb-btn" onclick="this.classList.toggle('active')">👎</button>
          <button class="share-btn" onclick="copyResult('${label}','${conf.toFixed(1)}')">📋 Copy</button>
        </div>
      </div>
    </div>`;

    addBotMsg(html);
    setTimeout(() => { const f = document.getElementById(uid); if(f) f.style.width = conf + '%'; }, 120);
    addHistory(label, conf, tier, userText);
  }
}

function copyResult(label, conf) {
  const text = `VitaCheck Analysis\nCondition: ${label}\nConfidence: ${conf}%\n\n⚠️ Educational only — not medical advice.`;
  navigator.clipboard.writeText(text).then(() => showToast('📋 Copied to clipboard'));
}

/* ═══════════════════════════════════════════
   SESSION HISTORY
═══════════════════════════════════════════ */
function addHistory(label, conf, tier, query) {
  if (localStorage.getItem('vc_history') === 'false') return;
  sessionHistory.unshift({ label, conf, tier, query, time: new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'}) });
  if (sessionHistory.length > 10) sessionHistory.pop();
  renderHistory();
}

function renderHistory() {
  const list = document.getElementById('historyList');
  const card = document.getElementById('historyCard');
  if (localStorage.getItem('vc_history') === 'false') return;
  card.style.display = 'block';
  list.innerHTML = sessionHistory.map((h,i) => `
    <div class="history-item">
      <span style="font-size:13px">${h.tier==='high'?'🟢':h.tier==='moderate'?'🟡':'⚪'}</span>
      <span class="hist-condition" onclick="loadHistory(${i})">${h.label}</span>
      <span class="hist-conf ${h.tier==='high'?'conf-high':h.tier==='moderate'?'conf-moderate':'conf-low'}">${h.conf.toFixed(0)}%</span>
      <span class="hist-time">${h.time}</span>
      <span class="hist-del" onclick="deleteHistory(${i})" title="Remove">✕</span>
    </div>`).join('');
}

function loadHistory(idx) {
  const h = sessionHistory[idx];
  document.getElementById('symptomInput').value = h.query;
  updateCharCount(document.getElementById('symptomInput'));
  document.getElementById('symptomInput').focus();
  showToast('📂 Query loaded — click Analyse to re-run');
}
function deleteHistory(idx) {
  sessionHistory.splice(idx, 1);
  renderHistory();
  if (sessionHistory.length === 0) document.getElementById('historyCard').style.display = 'none';
}
function clearHistory() {
  sessionHistory = [];
  document.getElementById('historyCard').style.display = 'none';
  showToast('🗑 History cleared');
}

/* ═══════════════════════════════════════════
   TOAST
═══════════════════════════════════════════ */
let toastTimer;
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2400);
}

/* ═══════════════════════════════════════════
   KEYBOARD SHORTCUT
═══════════════════════════════════════════ */
document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') analyse();
  if (e.key === 'Escape') {
    closeSettingsBtn();
    closeExportBtn();
  }
});
