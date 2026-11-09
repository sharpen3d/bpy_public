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

})();
