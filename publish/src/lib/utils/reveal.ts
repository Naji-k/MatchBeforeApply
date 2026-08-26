export interface RevealOptions {
  delay?: number;
  y?: number;
}

/**
 * Svelte action: fades/slides an element in the first time it enters the viewport.
 * Respects prefers-reduced-motion (element is simply left visible) and
 * degrades gracefully when IntersectionObserver is unavailable.
 */
export function reveal(node: HTMLElement, options: RevealOptions = {}) {
  const { delay = 0, y = 18 } = options;

  if (typeof window === "undefined") return;

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced || !("IntersectionObserver" in window)) return;

  node.style.opacity = "0";
  node.style.transform = `translateY(${y}px)`;
  node.style.transition = [
    `opacity 0.5s ease-out ${delay}ms`,
    `transform 0.5s ease-out ${delay}ms`,
  ].join(", ");

  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          node.style.opacity = "1";
          node.style.transform = "translateY(0)";
          observer.disconnect();
        }
      }
    },
    { threshold: 0.15 },
  );
  observer.observe(node);

  return {
    destroy() {
      observer.disconnect();
    },
  };
}
