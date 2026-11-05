// Optional enhancements. Project links and disclosure controls work without JavaScript.
(() => {
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
