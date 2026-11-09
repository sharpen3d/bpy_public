// API pages: the sidebar tree, search over types and members, and copy buttons on code.
(() => {
  const data = window.PLUSH_API;
  const body = document.body;
  const apiRoot = body.dataset.api || '';
  const current = body.dataset.page || '';
  const tree = document.getElementById('tree');
  const input = document.getElementById('q');
  const browseToggle = document.getElementById('api-browse-toggle');
  const browserContent = document.getElementById('api-browser-content');
  const mobile = matchMedia('(max-width: 860px)');

  function setBrowserOpen(open) {
    browserContent.hidden = !open;
    browseToggle.setAttribute('aria-expanded', String(open));
    browseToggle.textContent = open ? 'Close API browser' : 'Browse API';
  }

  function syncBrowserLayout() {
    browseToggle.hidden = !mobile.matches;
    setBrowserOpen(!mobile.matches);
  }

  syncBrowserLayout();
  mobile.addEventListener('change', syncBrowserLayout);
  browseToggle.addEventListener('click', () => {
    setBrowserOpen(browserContent.hidden);
    if (!browserContent.hidden && !input.value) scrollCurrentItem();
  });
  tree.addEventListener('click', event => {
    if (mobile.matches && event.target.closest('a') && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey) {
      setBrowserOpen(false);
      input.blur();
    }
  });
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* private window */ } },
  };
  const groupItems = g => g.c ? g.c.flatMap(c => c.i) : g.i;
  const itemLink = e => {
    const kind = ({ c: 'class', r: 'record', s: 'struct', e: 'enum', i: 'interface' })[e.k];
    const badge = e.k ? `<span class="badge ${e.k}" title="${kind}">${e.k.toUpperCase()}</span>` : '';
    return `<a class="item${e.u === current ? ' on' : ''}" href="${apiRoot}${e.u}" title="${esc(e.s || '')}">${badge}<span>${esc(e.n)}</span></a>`;
  };

  function renderTree() {
    const open = new Set(store.get('aether-api-open') || []);
    let html = '';
    for (const sec of data.sections) {
      const flat = sec.g.length === 1 && !sec.g[0].a;
      html += `<div class="sec${flat ? ' flat' : ''}"><div class="label">${esc(sec.t)}</div>`;
      for (const g of sec.g) {
        const all = groupItems(g);
        const items = all.map(itemLink).join('');
        if (flat) { html += items; continue; }
        const key = sec.t + '/' + g.a;
        const here = all.some(e => e.u === current);
        html += `<details class="grp" data-key="${esc(key)}"${here || open.has(key) ? ' open' : ''}><summary>${esc(g.a)}<span class="count">${all.length}</span></summary>`;
        if (g.c) {
          for (const c of g.c) {
            const conceptKey = `${key}/${c.n}`;
            const conceptHere = c.i.some(e => e.u === current);
            html += `<details class="concept" data-key="${esc(conceptKey)}"${conceptHere || open.has(conceptKey) ? ' open' : ''}><summary><span>${esc(c.n)}</span><span class="count">${c.i.length}</span></summary>${c.i.map(itemLink).join('')}</details>`;
          }
        } else html += items;
        html += '</details>';
      }
      html += '</div>';
    }
    tree.innerHTML = html;
    tree.querySelectorAll('details').forEach(d => d.addEventListener('toggle', () => {
      const keys = [...tree.querySelectorAll('details[open]')].map(x => x.dataset.key);
      store.set('aether-api-open', keys);
    }));
    scrollCurrentItem();
  }

  function scrollCurrentItem() {
    const on = tree.querySelector('.item.on');
    // Scroll the tree itself, so opening a reference never moves the article.
    if (on && !browserContent.hidden) {
      tree.scrollTop += on.getBoundingClientRect().top - tree.getBoundingClientRect().top - tree.clientHeight / 2;
    }
  }

  // Search index: every type and every member heading.
  const index = [];
  for (const sec of data.sections) for (const g of sec.g) {
    const concepts = g.c || [{ n: '', i: g.i }];
    for (const c of concepts) for (const e of c.i) {
      const parts = [sec.t, g.a, c.n].filter(Boolean);
      const where = parts.join(' · ');
      index.push({ name: e.n, lower: e.n.toLowerCase(), url: e.u, summary: e.s || '', where, type: true });
      for (const [m, anchor] of e.m || []) index.push({ name: `${e.n}.${m}`, lower: m.toLowerCase(), full: `${e.n}.${m}`.toLowerCase(), url: `${e.u}#${anchor}`, summary: e.s || '', where });
    }
  }

  let hits = [], selected = 0;
  function search(q) {
    q = q.trim().toLowerCase();
    if (!q) { renderTree(); return; }
    const words = q.split(/\s+/);
    hits = [];
    for (const it of index) {
      const hay = it.full || it.lower;
      const context = `${it.where} ${it.summary}`.toLowerCase();
      if (!words.every(w => hay.includes(w) || context.includes(w))) continue;
      let score = it.type ? 0 : 6;
      if (it.lower === q) score -= 4;
      else if (it.lower.startsWith(q)) score -= 2;
      else if (!hay.includes(q)) score += 4;
      hits.push([score, it.name.length, it]);
    }
    hits.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    hits = hits.slice(0, 80).map(h => h[2]);
    selected = 0;
    tree.innerHTML = '<div class="results">' + (hits.length ? hits.map((h, i) =>
      `<a class="hit${i === 0 ? ' sel' : ''}" href="${apiRoot}${h.url}" title="${esc(h.summary)}"><b>${esc(h.name)}</b><small>${esc(h.where)}</small></a>`).join('')
      : '<div class="none">Nothing matches.</div>') + '</div>';
  }

  function move(by) {
    const links = tree.querySelectorAll('.hit');
    if (!links.length) return;
    links[selected].classList.remove('sel');
    selected = (selected + by + links.length) % links.length;
    links[selected].classList.add('sel');
    links[selected].scrollIntoView({ block: 'nearest' });
  }

  input.addEventListener('input', () => search(input.value));
  input.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    else if (e.key === 'Enter') { const a = tree.querySelectorAll('.hit')[selected]; if (a) location.href = a.href; }
    else if (e.key === 'Escape') { input.value = ''; search(''); input.blur(); }
  });
  addEventListener('keydown', e => {
    const editing = e.target?.closest('input, textarea, select, [contenteditable="true"]');
    if (e.key === '/' && !editing && !e.metaKey && !e.ctrlKey && !e.altKey) {
      e.preventDefault(); setBrowserOpen(true); input.focus(); input.select();
    } else if (e.key === 'Escape' && mobile.matches && !browserContent.hidden) {
      setBrowserOpen(false); browseToggle.focus();
    }
  });

  document.querySelectorAll('.code').forEach(block => {
    const button = document.createElement('button');
    button.className = 'copy';
    button.textContent = 'Copy';
    button.type = 'button';
    button.addEventListener('click', async () => {
      const code = block.querySelector('code');
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(code.innerText);
        button.textContent = 'Copied';
        setTimeout(() => { button.textContent = 'Copy'; }, 1200);
      } catch {
        const selection = getSelection();
        const range = document.createRange();
        range.selectNodeContents(code);
        selection?.removeAllRanges();
        selection?.addRange(range);
        button.textContent = 'Select and copy';
      }
    });
    block.appendChild(button);
  });

  renderTree();
})();
