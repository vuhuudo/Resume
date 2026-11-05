const $ = (id) => document.getElementById(id);
const val = (id) => $(id).value.trim();
let current = null;

const lines = (id) => $(id).value.split('\n').map((l) => l.trim()).filter(Boolean);
const split2 = (line) => line.split('|').map((x) => x.trim());

function fill(p) {
  current = p;
  const tx = (d, l, fb = '') => (d ? (d[l] ?? d.en ?? fb) : fb);
  $('nameEn').value = tx(p.name, 'en'); $('nameVi').value = tx(p.name, 'vi');
  $('phone').value = p.phone || ''; $('email').value = p.email || '';
  $('github').value = p.github || ''; $('linkedin').value = p.linkedin || '';
  $('locEn').value = tx(p.location, 'en'); $('locVi').value = tx(p.location, 'vi');
  $('availEn').value = tx(p.availability, 'en'); $('availVi').value = tx(p.availability, 'vi');
  const je = p.job?.en || {}, jv = p.job?.vi || {};
  $('jobTitleEn').value = je.title || ''; $('jobOrgEn').value = je.org || ''; $('jobMetaEn').value = je.meta || '';
  $('jobTitleVi').value = jv.title || ''; $('jobOrgVi').value = jv.org || ''; $('jobMetaVi').value = jv.meta || '';
  const ee = p.education?.en || {}, ev = p.education?.vi || {};
  $('eduEn').value = ee.strong || ''; $('schoolEn').value = ee.line || ''; $('yearsEn').value = ee.years || '';
  $('eduVi').value = ev.strong || ''; $('schoolVi').value = ev.line || ''; $('yearsVi').value = ev.years || '';
  $('avatar').value = p.avatar || '';
  $('exp').value = (p.experience || []).map((e) => [e.en || '', e.vi || ''].join(' | ').replace(/ \| $/, '')).join('\n');
  $('proj').value = (p.projects || []).map((x) =>
    [tx(x.n, 'en'), x.tech || '', x.en || '', tx(x.n, 'vi'), x.vi || ''].join(' | ')).join('\n');
  $('skills').value = (p.skills || []).map((g) => `${tx(g.g, 'en')}: ${(g.items || []).map((i) => i.n).join(', ')}`).join('\n');
  $('deny').value = (p.denylist || []).join('\n');
}

function unescapeHtml(s) {
  const d = document.createElement('textarea'); d.innerHTML = s || ''; return d.value;
}

function collect() {
  const mk = (en, vi) => ({ en: en || vi || '', vi: vi || en || '' });
  const p = JSON.parse(JSON.stringify(current || {}));
  const loc = mk(val('locEn'), val('locVi'));
  p.name = mk(val('nameEn'), val('nameVi'));
  p.phone = val('phone'); p.email = val('email');
  p.github = val('github'); p.linkedin = val('linkedin');
  p.location = loc;
  p.availability = mk(val('availEn'), val('availVi'));
  p.avatar = val('avatar');
  p.job = {
    en: { title: val('jobTitleEn'), org: val('jobOrgEn'), meta: val('jobMetaEn') },
    vi: { title: val('jobTitleVi'), org: val('jobOrgVi'), meta: val('jobMetaVi') },
  };
  p.education = {
    en: { strong: val('eduEn'), line: val('schoolEn'), years: val('yearsEn'),
          ats: [val('eduEn'), val('schoolEn'), val('yearsEn')].filter(Boolean).join(' — ') },
    vi: { strong: val('eduVi'), line: val('schoolVi'), years: val('yearsVi'),
          ats: [val('eduVi'), val('schoolVi'), val('yearsVi')].filter(Boolean).join(' — ') },
  };
  const items = (list) => list.length ? list : [['', '']];
  p.languages = p.languages || { en: { items: [] }, vi: { items: [] } };
  p.contacts = {};
  p.contactLine = {};
  for (const l of ['en', 'vi']) {
    const cs = [];
    if (loc[l]) cs.push(['pin', loc[l]]);
    if (p.phone) cs.push(['phone', p.phone]);
    if (p.email) cs.push(['mail', `<a href="mailto:${p.email}">${p.email}</a>`]);
    for (const [key, kind] of [['github', 'github'], ['linkedin', 'linkedin']]) {
      const u = p[key];
      if (u) cs.push([kind, `<a href="${u.startsWith('http') ? u : 'https://' + u}">${u}</a>`]);
    }
    p.contacts[l] = cs;
    p.contactLine[l] = cs.map((c) => c[1].replace(/<[^>]+>/g, '')).join(' • ');
  }
  p.experience = lines('exp').map((l) => {
    const [en, vi] = split2(l);
    return { w: 0, t: [], en: unescapeHtml(en), vi: unescapeHtml(vi || en) };
  });
  p.projects = lines('proj').map((l) => {
    const a = split2(l);
    const nameEn = unescapeHtml(a[0] || ''), tech = unescapeHtml(a[1] || '');
    const en = unescapeHtml(a[2] || ''), nameVi = unescapeHtml(a[3] || '') || nameEn;
    const vi = unescapeHtml(a[4] || '') || en;
    return { w: 0, t: [], n: { en: nameEn, vi: nameVi }, tech, en, vi };
  });
  p.skills = lines('skills').map((l) => {
    const i = l.indexOf(':');
    const g = i > 0 ? l.slice(0, i).trim() : 'Skills';
    const names = (i > 0 ? l.slice(i + 1) : l).split(',').map((s) => s.trim()).filter(Boolean);
    return { g: { en: g, vi: g }, items: names.map((n) => ({ n: unescapeHtml(n), t: [] })) };
  });
  p.denylist = lines('deny');
  return p;
}

async function api(path, opts) {
  const r = await fetch(path, opts);
  const body = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(body.error || `HTTP ${r.status}`);
  return body;
}

async function loadProfiles(selectId) {
  const ids = await api('/api/profiles');
  const sel = $('profileSel');
  sel.innerHTML = ids.map((i) => `<option value="${i}">${i}</option>`).join('') || '<option>(chưa có)</option>';
  if (selectId && ids.includes(selectId)) sel.value = selectId;
  if (ids.length) fill(await api('/api/profiles/' + encodeURIComponent(sel.value)));
}

$('profileSel').addEventListener('change', async () => {
  fill(await api('/api/profiles/' + encodeURIComponent($('profileSel').value)));
});

$('btnSave').addEventListener('click', async () => {
  try {
    const p = collect();
    const id = val('saveAs') || $('profileSel').value || 'default';
    await api('/api/profiles/' + encodeURIComponent(id), {
      method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(p),
    });
    $('saveMsg').textContent = `Đã lưu ${id}`;
    await loadProfiles(id);
  } catch (e) { $('saveMsg').textContent = 'Lỗi: ' + e.message; }
});

$('btnReload').addEventListener('click', () => loadProfiles($('profileSel').value));

$('btnGen').addEventListener('click', async () => {
  const langs = [];
  if ($('lEn').checked) langs.push('EN');
  if ($('lVi').checked) langs.push('VI');
  $('genMsg').textContent = 'Đang tạo...';
  $('files').innerHTML = ''; $('warnings').innerHTML = ''; $('gaps').innerHTML = '';
  try {
    const res = await api('/api/render', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ profileId: $('profileSel').value, profile: collect(), role: val('role'), title: val('title'), langs }),
    });
    $('genMsg').textContent = `${res.files.length} file`;
    $('files').innerHTML = res.files.map((f) =>
      `<a href="${f.url}" target="_blank" rel="noopener">
         <b>${f.name}</b><span class="kind">${f.kind === 'ats' ? 'máy đọc' : 'người đọc'} · ${f.lang.toUpperCase()} · ${f.pages} trang</span>
       </a>`).join('');
    $('warnings').innerHTML = (res.warnings || []).map((w) => `<div class="msg risk">${w}</div>`).join('');
    if ((res.gaps || []).length)
      $('gaps').innerHTML = `<div class="msg warn">JD đòi mà hồ sơ chưa có (không tự thêm):</div>
        <div class="chips">${res.gaps.map((g) => `<span class="chip">${g}</span>`).join('')}</div>`;
    if (!(res.warnings || []).length)
      $('warnings').innerHTML = '<div class="msg ok">Không phát hiện rò rỉ từ cấm hay lỗi font.</div>';
  } catch (e) { $('genMsg').textContent = 'Lỗi: ' + e.message; }
});

$('btnImprove').addEventListener('click', async () => {
  const f = $('cvFile').files[0];
  if (!f) { $('impMsg').textContent = 'Chọn file trước.'; return; }
  const fd = new FormData();
  fd.append('file', f);
  fd.append('profileId', $('profileSel').value);
  $('impMsg').textContent = 'Đang đọc...';
  try {
    const res = await api('/api/improve', { method: 'POST', body: fd });
    $('impMsg').textContent = `${res.chars} ký tự`;
    $('impText').value = res.text;
    $('findings').innerHTML = res.findings.map((x) =>
      `<div class="msg ${x.level}">${x.message}</div>`).join('') || '<div class="msg ok">Không thấy vấn đề rõ ràng.</div>';
  } catch (e) { $('impMsg').textContent = 'Lỗi: ' + e.message; }
});

loadProfiles();
