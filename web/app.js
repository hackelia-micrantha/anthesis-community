document.documentElement.classList.add('js');

const reveals = document.querySelectorAll('.reveal');

// Use IntersectionObserver when available; otherwise fall back to making all
// reveal elements visible so content remains accessible in older or
// restricted environments.
if ('IntersectionObserver' in window) {
  try {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry, index) => {
          if (entry.isIntersecting) {
            entry.target.style.transitionDelay = `${index * 0.08}s`;
            entry.target.classList.add('visible');
          }
        });
      },
      { threshold: 0 }
    );

    reveals.forEach((section) => observer.observe(section));
  } catch (err) {
    // If IntersectionObserver can't be constructed or used, reveal everything so
    // the page content isn't hidden.
    reveals.forEach((section) => section.classList.add('visible'));
  }
} else {
  // No support: reveal everything.
  reveals.forEach((section) => section.classList.add('visible'));
}

const nav = document.querySelector('.nav');
const navToggle = document.querySelector('.nav-toggle');

if (nav && navToggle) {
  const links = nav.querySelector('.nav-links');
  const closeMenu = () => {
    nav.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
  };

  navToggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  nav.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && nav.classList.contains('open')) {
      closeMenu();
      navToggle.focus();
    }
  });

  links?.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });

  window.matchMedia('(min-width: 901px)').addEventListener('change', (event) => {
    if (event.matches) closeMenu();
  });
}
