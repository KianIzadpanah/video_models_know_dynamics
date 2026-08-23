/* Video Models Know Dynamics — site behaviour.
   Pure vanilla, no dependencies. Everything degrades to a usable page if JS
   fails: the sidebar is server-rendered and clips fall back to their posters. */
(function () {
  'use strict';

  var STORE = {
    get: function (k, d) { try { var v = localStorage.getItem('vmkd-' + k); return v === null ? d : v; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem('vmkd-' + k, v); } catch (e) {} }
  };

  /* ------------------------------------------------------------------ theme */
  var themeBtn = document.querySelector('.themebtn');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var root = document.documentElement;
      var cur = root.dataset.theme;
      if (cur !== 'dark' && cur !== 'light') {
        cur = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }
      var next = cur === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      STORE.set('theme', next);
    });
  }

  /* ------------------------------------------------------------------- nav */
  /* The sidebar state lives in localStorage and is applied before first paint by
     the inline script in the page head. It has to be persisted: every nav link is
     a real page load, so an in-memory flag would reset on each navigation and the
     sidebar would spring back open every time you picked a page. */
  var root = document.documentElement;
  var burger = document.querySelector('.burger');
  var scrim = document.querySelector('.scrim');

  function navState() {
    return root.getAttribute('data-nav') === 'open' ? 'open' : 'closed';
  }

  function setNav(state, remember) {
    root.setAttribute('data-nav', state);
    if (burger) burger.setAttribute('aria-expanded', String(state === 'open'));
    if (remember !== false) STORE.set('nav', state);
  }

  setNav(navState(), false);          // sync aria to whatever the head script chose

  if (burger) {
    burger.addEventListener('click', function () {
      setNav(navState() === 'open' ? 'closed' : 'open');
    });
  }
  if (scrim) scrim.addEventListener('click', function () { setNav('closed'); });

  /* Picking a page collapses the sidebar, so the clips get the full width on the
     page you actually wanted to look at. Only page links do this -- the group
     headers expand and collapse an experiment and must leave the sidebar open. */
  var sideEl = document.getElementById('sidebar');
  if (sideEl) {
    sideEl.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a) return;
      if (a.closest('.exp-pages') || a.classList.contains('side-home')) {
        setNav('closed');
      }
    });
  }

  /* ------------------------------------------------- sidebar groups + filter */
  document.querySelectorAll('.exp-h').forEach(function (h) {
    h.addEventListener('click', function () {
      var group = h.closest('.exp');
      var open = group.classList.toggle('open');
      h.setAttribute('aria-expanded', String(open));
    });
  });

  var filter = document.getElementById('navfilter');
  if (filter) {
    filter.addEventListener('input', function () {
      var q = filter.value.trim().toLowerCase();
      document.querySelectorAll('.exp').forEach(function (group) {
        var expText = (group.querySelector('.exp-h') || {}).textContent || '';
        var expHit = expText.toLowerCase().indexOf(q) > -1;
        var any = false;
        group.querySelectorAll('.exp-pages li').forEach(function (li) {
          var hit = !q || expHit || li.textContent.toLowerCase().indexOf(q) > -1;
          li.hidden = !hit;
          if (hit) any = true;
        });
        group.hidden = !!q && !any && !expHit;
        if (q && (any || expHit)) group.classList.add('open');
      });
      if (!q) {
        document.querySelectorAll('.exp').forEach(function (g) {
          if (!g.querySelector('a.on')) g.classList.remove('open');
          else g.classList.add('open');
        });
      }
    });
  }

  // keep the active sidebar item in view on load
  var active = document.querySelector('.exp-pages a.on');
  if (active) {
    var side = document.getElementById('sidebar');
    var top = active.offsetTop - side.clientHeight / 2;
    if (top > 0) side.scrollTop = top;
  }

  /* ----------------------------------------------------------------- clips */
  var clips = Array.prototype.slice.call(document.querySelectorAll('.clip:not(.miss)'));
  var state = {
    seed: STORE.get('seed', null),
    rate: parseFloat(STORE.get('rate', '1')) || 1,
    paused: false
  };

  function videos() {
    return clips.map(function (c) { return c.querySelector('video'); }).filter(Boolean);
  }

  function visibleClips() {
    return clips.filter(function (c) { return !c.hidden; });
  }

  /* Lazy attach: a <video> only gets its src once it is near the viewport, and
     playback pauses whenever it scrolls away. With ~80 clips on a page this is
     the difference between a usable page and a stalled one. */
  var io = null;
  if ('IntersectionObserver' in window) {
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var v = e.target.querySelector('video');
        if (!v) return;
        if (e.isIntersecting) {
          attach(v);
          if (!state.paused) play(v);
        } else if (!v.paused) {
          v.pause();
        }
      });
    }, { rootMargin: '350px 0px', threshold: 0.01 });
  }

  function attach(v) {
    if (!v.src && v.dataset.src) v.src = v.dataset.src;
  }

  function play(v) {
    attach(v);
    v.playbackRate = state.rate;
    var p = v.play();
    if (p && p.catch) p.catch(function () {});
  }

  function applySeed() {
    if (!clips.length) return;
    clips.forEach(function (c) {
      var on = !state.seed || state.seed === 'all' || c.dataset.seed === state.seed;
      c.hidden = !on;
      var v = c.querySelector('video');
      if (v && !on) v.pause();
    });
    document.querySelectorAll('[data-seed][type="button"]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.seed === (state.seed || '')));
    });
    // newly revealed clips that are already on screen should start
    if (io) {
      clips.forEach(function (c) { io.unobserve(c); if (!c.hidden) io.observe(c); });
    } else {
      visibleClips().forEach(function (c) { if (!state.paused) play(c.querySelector('video')); });
    }
  }

  function applyRate() {
    videos().forEach(function (v) { v.playbackRate = state.rate; });
    document.querySelectorAll('[data-rate]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(parseFloat(b.dataset.rate) === state.rate));
    });
  }

  function syncReplay() {
    state.paused = false;
    updatePlayLabel();
    visibleClips().forEach(function (c) {
      var v = c.querySelector('video');
      if (!v) return;
      attach(v);
      try { v.currentTime = 0; } catch (e) {}
      play(v);
    });
  }

  function updatePlayLabel() {
    var b = document.querySelector('[data-toggleplay]');
    if (b) b.textContent = state.paused ? 'Play all' : 'Pause all';
  }

  function togglePlay() {
    state.paused = !state.paused;
    updatePlayLabel();
    visibleClips().forEach(function (c) {
      var v = c.querySelector('video');
      if (!v) return;
      if (state.paused) v.pause(); else play(v);
    });
  }

  var toolbar = document.querySelector('[data-toolbar]');
  if (toolbar) {
    // default the seed selector to the first available option
    var first = toolbar.querySelector('[data-seed]');
    var opts = Array.prototype.slice.call(toolbar.querySelectorAll('[data-seed]'))
      .map(function (b) { return b.dataset.seed; });
    if (!state.seed || opts.indexOf(state.seed) === -1) state.seed = first ? first.dataset.seed : null;

    toolbar.addEventListener('click', function (e) {
      var s = e.target.closest('[data-seed]');
      if (s) { state.seed = s.dataset.seed; STORE.set('seed', state.seed); applySeed(); return; }
      var r = e.target.closest('[data-rate]');
      if (r) { state.rate = parseFloat(r.dataset.rate); STORE.set('rate', r.dataset.rate); applyRate(); return; }
      if (e.target.closest('[data-sync]')) syncReplay();
      if (e.target.closest('[data-toggleplay]')) togglePlay();
    });
  }

  if (clips.length) {
    applySeed();
    applyRate();
    updatePlayLabel();
    if (io) clips.forEach(function (c) { if (!c.hidden) io.observe(c); });
    else clips.forEach(function (c) { if (!c.hidden) play(c.querySelector('video')); });
  }

  /* -------------------------------------------------------------- lightbox */
  var lb = document.querySelector('.lightbox');
  if (lb && clips.length) {
    var lbv = lb.querySelector('.lb-video');
    var lbi = lb.querySelector('.lb-img');
    var seek = lb.querySelector('.lb-seek');
    var timeEl = lb.querySelector('.lb-time');
    var capEl = lb.querySelector('.lb-cap');
    var playBtn = lb.querySelector('.lb-play');
    var FRAME = 1 / 24;   // clips here are 20-24 fps; one step reads as one frame
    var lastFocus = null;
    var scrubbing = false;

    function open(clip) {
      var src = clip.dataset.src;
      var img = clip.dataset.img;
      if (!src && !img) return;
      lastFocus = document.activeElement;
      capEl.textContent = clip.dataset.label || '';
      // Stills (timing strips, keyframe checks) reuse the same overlay, minus
      // the transport bar — there is nothing to play or step through.
      lb.classList.toggle('is-img', !!img);
      if (img) {
        lbv.hidden = true;
        lbv.removeAttribute('src');
        lbi.hidden = false;
        lbi.src = img;
        lbi.alt = clip.dataset.label || '';
      } else {
        lbi.hidden = true;
        lbi.removeAttribute('src');
        lbv.hidden = false;
        lbv.src = src;
        lbv.playbackRate = state.rate;
      }
      lb.hidden = false;
      document.body.style.overflow = 'hidden';
      setRateButtons();
      if (!img) lbv.play().catch(function () {});
      lb.querySelector('.lb-close').focus();
    }

    function close() {
      lb.hidden = true;
      lbv.pause();
      lbv.removeAttribute('src');
      lbv.load();
      lbi.removeAttribute('src');
      document.body.style.overflow = '';
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    function setRateButtons() {
      lb.querySelectorAll('[data-lbrate]').forEach(function (b) {
        b.setAttribute('aria-pressed', String(parseFloat(b.dataset.lbrate) === lbv.playbackRate));
      });
    }

    function step(dir) {
      lbv.pause();
      var d = lbv.duration || 0;
      var t = lbv.currentTime + dir * FRAME;
      lbv.currentTime = Math.max(0, Math.min(d ? d - 0.001 : t, t));
      syncPlayBtn();
    }

    function syncPlayBtn() { playBtn.innerHTML = lbv.paused ? '▶' : '❘❘'; }

    document.addEventListener('click', function (e) {
      var z = e.target.closest('.clip .zoom');
      if (z) { e.preventDefault(); open(z.closest('.clip')); return; }
      var c = e.target.closest('.clip');
      if (c && (c.dataset.src || c.dataset.img) && !e.target.closest('.lightbox')) { open(c); return; }
      if (e.target.closest('.lb-back') || e.target.closest('.lb-close')) close();
      var st = e.target.closest('.lb-step');
      if (st) step(parseInt(st.dataset.step, 10));
      if (e.target.closest('.lb-play')) {
        if (lbv.paused) lbv.play().catch(function () {}); else lbv.pause();
        syncPlayBtn();
      }
      var lr = e.target.closest('[data-lbrate]');
      if (lr) { lbv.playbackRate = parseFloat(lr.dataset.lbrate); setRateButtons(); }
    });

    lbv.addEventListener('timeupdate', function () {
      if (scrubbing || !lbv.duration) return;
      seek.value = String(Math.round((lbv.currentTime / lbv.duration) * 1000));
      timeEl.textContent = lbv.currentTime.toFixed(2) + 's';
    });
    lbv.addEventListener('play', syncPlayBtn);
    lbv.addEventListener('pause', syncPlayBtn);
    seek.addEventListener('pointerdown', function () { scrubbing = true; });
    seek.addEventListener('pointerup', function () { scrubbing = false; });
    seek.addEventListener('input', function () {
      if (!lbv.duration) return;
      lbv.currentTime = (parseInt(seek.value, 10) / 1000) * lbv.duration;
      timeEl.textContent = lbv.currentTime.toFixed(2) + 's';
    });

    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') { close(); return; }
      if (lb.classList.contains('is-img')) return;
      if (e.key === 'ArrowRight' || e.key === '.') { e.preventDefault(); step(1); }
      else if (e.key === 'ArrowLeft' || e.key === ',') { e.preventDefault(); step(-1); }
      else if (e.key === ' ') {
        e.preventDefault();
        if (lbv.paused) lbv.play().catch(function () {}); else lbv.pause();
      }
    });
  }

  /* ------------------------------------------------------------------ keys */
  document.addEventListener('keydown', function (e) {
    if (e.target.matches('input,textarea,select') || e.metaKey || e.ctrlKey || e.altKey) return;
    if (!document.querySelector('.lightbox[hidden]')) return;   // lightbox owns keys
    if (e.key === '/') { e.preventDefault(); if (filter) { filter.focus(); filter.select(); } }
    else if (e.key === 'r' && toolbar) { syncReplay(); }
    else if (e.key === 'p' && toolbar) { togglePlay(); }
    else if (e.key === 'n') { setNav(navState() === 'open' ? 'closed' : 'open'); }
    else if (e.key === 'Escape') { setNav('closed'); }
  });
})();
