// Optional enhancements. Project links and disclosure controls work without JavaScript.
(() => {
  const galleryViewer = document.querySelector('[data-gallery-viewer]');
  if (galleryViewer) {
    const content = galleryViewer.querySelector('div');
    document.querySelectorAll('[data-gallery-card]').forEach(card => card.addEventListener('click', () => {
      content.replaceChildren(...[...card.querySelectorAll('.aether-gallery-media img')].map(image => image.cloneNode()));
      galleryViewer.showModal();
    }));
    galleryViewer.querySelector('button').addEventListener('click', () => galleryViewer.close());
    galleryViewer.addEventListener('click', event => { if (event.target === galleryViewer) galleryViewer.close(); });
  }

  document.querySelectorAll('[data-grass-comparison]').forEach(comparison => {
    const image = comparison.querySelector('[data-comparison-image]');
    const map = comparison.querySelector('[data-comparison-map]');
    const caption = comparison.querySelector('[data-comparison-caption]');
    const tabs = [...comparison.querySelectorAll('[data-view]')];
    const handles = [...comparison.querySelectorAll('[data-divider]')];
    const labels = [...image.querySelectorAll('.grass-label')];
    const names = {basecolor: 'Base color', normal: 'Tangent-space normal', roughness: 'Roughness', ao: 'Ambient occlusion', height: 'Height'};
    let positions = [33.333, 66.667], active = null;
    const update = () => {
      image.style.setProperty('--first', `${positions[0]}%`);
      image.style.setProperty('--second', `${positions[1]}%`);
      handles.forEach((handle, i) => {
        handle.setAttribute('aria-valuenow', Math.round(positions[i]));
        handle.setAttribute('aria-valuemin', i ? Math.round(positions[0]) : 0);
        handle.setAttribute('aria-valuemax', i ? 100 : Math.round(positions[1]));
      });
      const widths = [positions[0], positions[1] - positions[0], 100 - positions[1]];
      labels.forEach((label, i) => { label.hidden = widths[i] < 13; });
    };
    const setPosition = (index, value) => {
      positions[index] = Math.max(index ? positions[0] : 0, Math.min(index ? 100 : positions[1], value));
      update();
    };
    const move = event => {
      if (active === null) return;
      const rect = image.getBoundingClientRect();
      setPosition(active, 100 * (event.clientX - rect.left) / rect.width);
    };
    image.addEventListener('pointerdown', event => {
      if (image.dataset.mode !== 'compare' || event.button !== 0) return;
      const rect = image.getBoundingClientRect();
      const x = 100 * (event.clientX - rect.left) / rect.width;
      const handle = event.target.closest('[data-divider]');
      active = handle ? handles.indexOf(handle) : (Math.abs(x - positions[0]) <= Math.abs(x - positions[1]) ? 0 : 1);
      handles[active].focus({preventScroll: true});
      image.setPointerCapture(event.pointerId);
      move(event); event.preventDefault();
    });
    image.addEventListener('pointermove', move);
    image.addEventListener('pointerup', () => { active = null; });
    image.addEventListener('pointercancel', () => { active = null; });
    image.addEventListener('lostpointercapture', () => { active = null; });
    handles.forEach((handle, i) => handle.addEventListener('keydown', event => {
      const delta = event.shiftKey ? 10 : 1;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowDown') setPosition(i, positions[i] - delta);
      else if (event.key === 'ArrowRight' || event.key === 'ArrowUp') setPosition(i, positions[i] + delta);
      else if (event.key === 'Home') setPosition(i, i ? positions[0] : 0);
      else if (event.key === 'End') setPosition(i, i ? 100 : positions[1]);
      else return;
      event.preventDefault();
    }));
    tabs.forEach(tab => tab.addEventListener('click', () => {
      const view = tab.dataset.view;
      tabs.forEach(button => button.setAttribute('aria-pressed', String(button === tab)));
      const isMap = Object.hasOwn(names, view);
      image.dataset.mode = isMap ? 'map' : view;
      map.hidden = !isMap;
      if (isMap) { map.src = `assets/aether-gallery/grass-map-${view}.jpg`; map.alt = `${names[view]} map captured orthographically in Aether`; }
      handles.forEach(handle => { handle.hidden = view !== 'compare'; });
      caption.textContent = isMap ? `${names[view]}: orthographic Aether capture, shown independently of the angled Plush views.` : view === 'compare' ? 'Drag the dividers on the image, or use the arrow keys when a divider is focused. Tabs show each view on its own.' : 'Fixed-camera capture from the Plush player. Select Compare to sweep between the three views.';
    }));
    update();
  });

  const printButton = document.querySelector('.print-resume');
  if (printButton) {
    printButton.hidden = false;
    printButton.addEventListener('click', () => window.print());
  }

  // A link to footage opens its native disclosure without starting playback.
  function openLinkedDetail() {
    if (!location.hash) return;
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (target?.tagName === 'DETAILS') target.open = true;
  }
  openLinkedDetail();
  addEventListener('hashchange', openLinkedDetail);

  const stage = document.querySelector('[data-plush-peek]');
  if (!stage || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const eye = stage.querySelector('.peek-eye');
  const upper = stage.querySelector('[data-eye-upper]');
  const lower = stage.querySelector('[data-eye-lower]');
  const clip = stage.querySelector('[data-eye-clip]');
  const iris = stage.querySelector('[data-eye-iris]');
  const pupil = stage.querySelector('[data-eye-pupil]');
  const ring = stage.querySelector('.peek-iris');
  let dilation = 8;
  const links = [...stage.querySelectorAll('.peek-link')];
  let mouse = null, gx = 0, gy = -10, visible = true, raf = 0;
  let last = performance.now(), blinkAt = -1, nextBlink = last + 4200;
  const ease = v => v * v * (3 - 2 * v);
  const clamp = v => Math.max(0, Math.min(1, v));
  const point = (x,y) => `${x.toFixed(2)} ${y.toFixed(2)}`;
  function frame(now) {
    if (!visible || document.hidden) { raf = 0; return; }
    const dt = Math.min(.05, (now-last)/1000); last = now;
    const r = eye.getBoundingClientRect();
    const tx = mouse ? 38*Math.tanh((mouse[0]-r.left-r.width/2)/300) : 0;
    const ty = mouse ? 20*Math.tanh((mouse[1]-r.top-r.height/2)/240)-5 : -10;
    const k = 1-Math.exp(-dt*9); gx+=(tx-gx)*k; gy+=(ty-gy)*k;
    if (now>nextBlink && blinkAt<0) blinkAt=now;
    let open=1;
    if (blinkAt>=0) {
      const t=now-blinkAt;
      open=t<80 ? 1-ease(t/80) : t<125 ? 0 : ease(clamp((t-125)/180));
      if (t>305) { blinkAt=-1; nextBlink=now+4200+Math.random()*2400; }
    }
    const y1=36+(-62+gy*.55-36)*open, y2=38+(-66+gy*.55-38)*open;
    const top=`M-100 4C-52 ${y1.toFixed(2)} 46 ${y2.toFixed(2)} 100-6`;
    const bottom=`C50 ${(42+gy*.2).toFixed(2)} -46 ${(40+gy*.2).toFixed(2)} -100 4`;
    upper.setAttribute('d',top); lower.setAttribute('d',`M100-6${bottom}`);
    clip.setAttribute('d',`${top}${bottom}Z`);
    iris.setAttribute('transform',`translate(${point(gx,gy)})`);
    const distanceToEye = mouse ? Math.hypot(mouse[0]-r.left-r.width/2,mouse[1]-r.top-r.height/2) : 400;
    const attention = stage.matches(':focus-within') ? 1 : clamp(1-distanceToEye/300);
    const targetDilation = 7.5+attention*7+.5*Math.sin(now*.0012);
    dilation += (targetDilation-dilation)*k;
    pupil.setAttribute('r',dilation.toFixed(2));
    ring.setAttribute('r',(27+attention*2).toFixed(2));
    for (const a of links) {
      const box=a.getBoundingClientRect();
      const distance=mouse ? Math.hypot(mouse[0]-box.left-box.width/2,mouse[1]-box.top-box.height/2) : 240;
      a.style.setProperty('--interest',clamp(1-distance/220).toFixed(2));
    }
    raf=requestAnimationFrame(frame);
  }
  function start() { if (!raf && visible && !document.hidden) { last=performance.now(); raf=requestAnimationFrame(frame); } }
  addEventListener('pointermove',e=>{mouse=[e.clientX,e.clientY];},{passive:true});
  document.addEventListener('pointerleave',()=>{mouse=null;});
  document.addEventListener('visibilitychange',start);
  if ('IntersectionObserver' in window) new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;start();}).observe(stage);
  start();
})();
