(function () {
    const backdrop = document.getElementById('imgPreviewBackdrop');
    const imgEl = document.getElementById('imgPreviewImg');
    const titleEl = document.getElementById('imgPreviewTitle');
    const closeBtn = document.getElementById('imgPreviewClose');

    if (!backdrop || !imgEl || !titleEl || !closeBtn) return;

    let lastActiveEl = null;

    function isOpen() {
      return backdrop.getAttribute('data-open') === 'true';
    }

    function openPreview(src, alt) {
      if (!src) return;
      lastActiveEl = document.activeElement;
      imgEl.src = src;
      imgEl.alt = alt || '图片预览';
      titleEl.textContent = alt || '图片预览';
      backdrop.setAttribute('data-open', 'true');
      backdrop.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      closeBtn.focus({ preventScroll: true });
    }

    function closePreview() {
      if (!isOpen()) return;
      backdrop.removeAttribute('data-open');
      backdrop.setAttribute('aria-hidden', 'true');
      imgEl.removeAttribute('src');
      imgEl.alt = '';
      titleEl.textContent = '图片预览';
      document.body.style.overflow = '';
      if (lastActiveEl && typeof lastActiveEl.focus === 'function') {
        lastActiveEl.focus({ preventScroll: true });
      }
      lastActiveEl = null;
    }

    document.addEventListener('click', function (e) {
      const target = e.target;
      if (target && target.classList && target.classList.contains('zoomable')) {
        openPreview(target.getAttribute('src'), target.getAttribute('alt'));
        return;
      }
      if (target === backdrop) {
        closePreview();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closePreview();
      if (e.key === 'Enter' || e.key === ' ') {
        const target = e.target;
        if (target && target.classList && target.classList.contains('zoomable')) {
          e.preventDefault();
          openPreview(target.getAttribute('src'), target.getAttribute('alt'));
        }
      }
    });

    closeBtn.addEventListener('click', closePreview);
  })();

  /* === 顶部导航：随滚动高亮当前章节（拆分后目录页、章节子页均跳过） === */
  (function () {
    if (document.body && document.body.id === 'manual-home') return;
    if (document.body && document.body.classList.contains('manual-chapter')) return;

    var nav = document.querySelector('.nav');
    if (!nav) return;

    var chain = [
      { id: 's0', href: '#s0' },
      { id: 's1', href: '#s1' },
      { id: 's2', href: '#s2' },
      { id: 's3', href: '#s3' },
      { id: 's4', href: '#s4' },
      { id: 's5', href: '#s5' },
      { id: 's6', href: '#s6' },
      { id: 's7', href: '#s7' },
      { id: 's8', href: '#s8' },
      { id: 's9', href: '#s9' },
      { id: 's10-motion', href: '#s10-motion' },
      { id: 's10-practice', href: '#s10-motion' },
      { id: 's10', href: '#s10-motion' },
      { id: 's11', href: '#s11' },
      { id: 's12', href: '#s12' },
      { id: 's-links', href: '#s10-motion' },
      { id: 's-appendix', href: '#s10-motion' }
    ];

    var ticking = false;
    function updateNavHighlight() {
      ticking = false;
      var navRect = nav.getBoundingClientRect();
      // 使用“导航下方的一条线”来判断当前所在章节，避免大卡片/长段落导致误判到上一章
      var lineY = Math.max(0, navRect.bottom + 14);

      var chosenHref = '#s0';
      var bestTop = -Infinity;

      // 优先：找到覆盖 lineY 的章节（top <= lineY < bottom）
      for (var i = 0; i < chain.length; i++) {
        var el = document.getElementById(chain[i].id);
        if (!el) continue;
        var r = el.getBoundingClientRect();
        if (r.top <= lineY && r.bottom > lineY) {
          chosenHref = chain[i].href;
          bestTop = r.top;
        }
      }

      // 兜底：如果没有任何章节覆盖 lineY，就退回到“最接近但在其上方”的章节
      if (bestTop === -Infinity) {
        for (var j = 0; j < chain.length; j++) {
          var el2 = document.getElementById(chain[j].id);
          if (!el2) continue;
          var r2 = el2.getBoundingClientRect();
          if (r2.top <= lineY && r2.top > bestTop) {
            bestTop = r2.top;
            chosenHref = chain[j].href;
          }
        }
      }

      nav.querySelectorAll('a[href^="#"]').forEach(function (a) {
        a.classList.toggle('nav-link--active', a.getAttribute('href') === chosenHref);
      });
    }

    function requestUpdate() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(updateNavHighlight);
    }

    window.addEventListener('scroll', requestUpdate, { passive: true });
    window.addEventListener('resize', requestUpdate);
    nav.addEventListener('click', function (e) {
      var t = e.target;
      if (t && t.closest && t.closest('a[href^="#"]')) {
        window.requestAnimationFrame(function () {
          window.requestAnimationFrame(updateNavHighlight);
        });
      }
    });
    window.addEventListener('hashchange', updateNavHighlight);
    updateNavHighlight();
  })();

  /* === 横向滑动步骤轮播 === */
  document.querySelectorAll('.step-carousel').forEach(function(carousel) {
    const track = carousel.querySelector('.step-carousel__track');
    const btnPrev = carousel.querySelector('.carousel-btn.prev');
    const btnNext = carousel.querySelector('.carousel-btn.next');
    const dots = carousel.querySelectorAll('.carousel-dot');
    const cards = carousel.querySelectorAll('.step-card');

    if (!track) return;

    // 提示是否可滚动，用于左右渐隐
    function updateCanScroll() {
      const canScroll = track.scrollWidth - track.offsetWidth > 10;
      carousel.setAttribute('data-can-scroll', canScroll ? 'true' : 'false');
    }

    function updateDots() {
      const cardWidth = cards[0] ? cards[0].offsetWidth + 20 : 300;
      const scrollLeft = track.scrollLeft;
      const index = Math.round(scrollLeft / cardWidth);
      dots.forEach(function(d, i) {
        d.classList.toggle('active', i === index);
      });
      if (btnPrev) btnPrev.disabled = scrollLeft <= 10;
      if (btnNext) btnNext.disabled = scrollLeft >= track.scrollWidth - track.offsetWidth - 10;
    }

    if (btnPrev) {
      btnPrev.addEventListener('click', function() {
        track.scrollBy({ left: -(cards[0] ? cards[0].offsetWidth + 20 : 300), behavior: 'smooth' });
      });
    }
    if (btnNext) {
      btnNext.addEventListener('click', function() {
        track.scrollBy({ left: cards[0] ? cards[0].offsetWidth + 20 : 300, behavior: 'smooth' });
      });
    }
    dots.forEach(function(dot, i) {
      dot.addEventListener('click', function() {
        const cardWidth = cards[0] ? cards[0].offsetWidth + 20 : 300;
        track.scrollTo({ left: i * cardWidth, behavior: 'smooth' });
      });
    });
    track.addEventListener('scroll', function () {
      updateDots();
      updateCanScroll();
    });
    window.addEventListener('resize', function () {
      updateDots();
      updateCanScroll();
    });
    updateDots();
    updateCanScroll();
  });
