(() => {
  'use strict';

  const experiment = 'phyllotaxis-utility-v1';
  const cookieName = 'anthesis_variant';
  const allowedVariants = new Set(['current', 'utility']);

  const readCookie = () => {
    const prefix = `${cookieName}=`;
    const match = document.cookie
      .split(';')
      .map((part) => part.trim())
      .find((part) => part.startsWith(prefix));
    if (!match) return null;
    const value = decodeURIComponent(match.slice(prefix.length));
    return allowedVariants.has(value) ? value : null;
  };

  const randomVariant = () => {
    if (globalThis.crypto?.getRandomValues) {
      const sample = new Uint32Array(1);
      globalThis.crypto.getRandomValues(sample);
      return sample[0] < 0x80000000 ? 'current' : 'utility';
    }
    return Math.random() < 0.5 ? 'current' : 'utility';
  };

  const requested = new URLSearchParams(globalThis.location.search).get('variant');
  const variant = allowedVariants.has(requested)
    ? requested
    : (readCookie() || randomVariant());

  const secure = globalThis.location.protocol === 'https:' ? '; Secure' : '';
  document.cookie =
    `${cookieName}=${encodeURIComponent(variant)}; Max-Age=2592000; Path=/; SameSite=Lax${secure}`;

  document.documentElement.dataset.experiment = experiment;
  document.documentElement.dataset.variant = variant;

  const theme = document.getElementById('site-theme');
  if (theme && variant === 'current') {
    theme.setAttribute('href', 'site-theme-current.css');
  }

  const track = (eventName) => {
    if (typeof eventName !== 'string' || !eventName) return;
    document.dispatchEvent(new CustomEvent('anthesis:experiment', {
      detail: Object.freeze({
        experiment,
        variant,
        event: eventName,
        surface: globalThis.location.pathname,
      }),
    }));
  };

  globalThis.AnthesisExperiment = Object.freeze({
    experiment,
    variant,
    track,
  });
})();
