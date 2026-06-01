(function () {
    const reveals = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("in-view");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });
        reveals.forEach((item) => observer.observe(item));
    } else {
        reveals.forEach((item) => item.classList.add("in-view"));
    }

    const counters = document.querySelectorAll(".counter");
    const animateCounter = (counter) => {
        const target = Number(counter.dataset.target || 0);
        const suffix = target === 96 ? "%" : target === 48 ? "h" : "+";
        let value = 0;
        const step = Math.max(1, Math.ceil(target / 70));
        const tick = () => {
            value = Math.min(target, value + step);
            counter.textContent = value.toLocaleString() + suffix;
            if (value < target) requestAnimationFrame(tick);
        };
        tick();
    };
    if ("IntersectionObserver" in window) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.4 });
        counters.forEach((counter) => counterObserver.observe(counter));
    } else {
        counters.forEach(animateCounter);
    }
})();
