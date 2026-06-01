(function () {
    const navbar = document.querySelector(".app-navbar");
    const setNavbarState = () => {
        navbar?.classList.toggle("nav-scrolled", window.scrollY > 12);
    };
    setNavbarState();
    window.addEventListener("scroll", setNavbarState, { passive: true });

    const currentPath = window.location.pathname.replace(/\/$/, "") || "/";
    document.querySelectorAll(".navbar .nav-link").forEach((link) => {
        const linkPath = new URL(link.href, window.location.origin).pathname.replace(/\/$/, "") || "/";
        link.classList.toggle("active", linkPath === currentPath);
    });

    const navCollapse = document.getElementById("primaryNav");
    document.querySelectorAll(".navbar .nav-link, .navbar .btn").forEach((link) => {
        link.addEventListener("click", () => {
            if (!navCollapse?.classList.contains("show") || !window.bootstrap) return;
            bootstrap.Collapse.getOrCreateInstance(navCollapse).hide();
        });
    });

    const toastHost = document.getElementById("toastHost");
    window.showToast = function showToast(message, type = "primary") {
        if (!toastHost || !window.bootstrap) return;
        const toast = document.createElement("div");
        toast.className = "toast align-items-center text-bg-" + type + " border-0";
        toast.setAttribute("role", "status");
        toast.innerHTML = '<div class="d-flex"><div class="toast-body">' + message + '</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button></div>';
        toastHost.appendChild(toast);
        const instance = new bootstrap.Toast(toast, { delay: 2600 });
        instance.show();
        toast.addEventListener("hidden.bs.toast", () => toast.remove());
    };

    const revealItems = document.querySelectorAll(".fade-up");
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("in-view");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.16 });
        revealItems.forEach((item) => observer.observe(item));
    } else {
        revealItems.forEach((item) => item.classList.add("in-view"));
    }

    const animateCounter = (counter) => {
        const target = Number(counter.dataset.counter || 0);
        const suffix = target === 94 ? "%" : target === 48 ? "h" : "+";
        let value = 0;
        const step = Math.max(1, Math.ceil(target / 64));
        const tick = () => {
            value = Math.min(target, value + step);
            counter.textContent = value.toLocaleString() + suffix;
            if (value < target) requestAnimationFrame(tick);
        };
        tick();
    };
    const counters = document.querySelectorAll("[data-counter]");
    if ("IntersectionObserver" in window) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.45 });
        counters.forEach((counter) => counterObserver.observe(counter));
    } else {
        counters.forEach(animateCounter);
    }

    document.querySelectorAll(".save-job").forEach((button) => {
        button.addEventListener("click", () => {
            const saved = button.classList.toggle("saved");
            const icon = button.querySelector("i");
            if (icon) icon.className = saved ? "fa-solid fa-bookmark" : "fa-regular fa-bookmark";
            window.showToast?.(saved ? "Job saved." : "Job removed.");
        });
    });

    document.querySelectorAll(".password-toggle").forEach((button) => {
        button.addEventListener("click", () => {
            const input = button.closest(".password-shell")?.querySelector("input");
            if (!input) return;
            const showing = input.type === "text";
            input.type = showing ? "password" : "text";
            button.innerHTML = showing ? '<i class="fa-regular fa-eye"></i>' : '<i class="fa-regular fa-eye-slash"></i>';
        });
    });

    document.querySelectorAll(".validated-form").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const confirmInput = form.querySelector("[data-confirm-password]");
            if (confirmInput) {
                const passwordInput = form.querySelector(confirmInput.dataset.confirmPassword);
                confirmInput.setCustomValidity(passwordInput && confirmInput.value !== passwordInput.value ? "Passwords do not match" : "");
            }
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                window.showToast?.("Please check the highlighted fields.", "danger");
            }
            form.classList.add("was-validated");
        });
    });

    const strengthInput = document.querySelector("[data-password-strength]");
    if (strengthInput) {
        const meter = document.querySelector(".strength-meter");
        const text = document.querySelector(".strength-text");
        strengthInput.addEventListener("input", () => {
            const value = strengthInput.value;
            const score = Number(value.length >= 8) + Number(/[A-Z]/.test(value)) + Number(/[0-9]/.test(value)) + Number(/[^A-Za-z0-9]/.test(value));
            meter?.classList.remove("medium", "strong");
            if (score >= 4) {
                meter?.classList.add("strong");
                if (text) text.textContent = "Password strength: strong";
            } else if (score >= 2) {
                meter?.classList.add("medium");
                if (text) text.textContent = "Password strength: medium";
            } else if (text) {
                text.textContent = "Password strength: weak";
            }
        });
    }

    const resetForm = document.querySelector("[data-reset-form]");
    resetForm?.addEventListener("submit", (event) => {
        event.preventDefault();
        if (!resetForm.checkValidity()) return;
        document.querySelector("[data-reset-success]")?.classList.remove("d-none");
        window.showToast?.("Reset instructions sent.");
    });

    const dropzone = document.querySelector("[data-dropzone]");
    const fileInput = dropzone?.querySelector("input[type='file']");
    if (dropzone && fileInput) {
        ["dragenter", "dragover"].forEach((eventName) => {
            dropzone.addEventListener(eventName, (event) => {
                event.preventDefault();
                dropzone.classList.add("dragover");
            });
        });
        ["dragleave", "drop"].forEach((eventName) => {
            dropzone.addEventListener(eventName, (event) => {
                event.preventDefault();
                dropzone.classList.remove("dragover");
            });
        });
        dropzone.addEventListener("drop", (event) => {
            fileInput.files = event.dataTransfer.files;
            const fileName = event.dataTransfer.files[0]?.name;
            if (fileName) dropzone.querySelector("strong").textContent = fileName;
        });
        fileInput.addEventListener("change", () => {
            const fileName = fileInput.files[0]?.name;
            if (fileName) dropzone.querySelector("strong").textContent = fileName;
        });
    }

    const applicationForm = document.querySelector("[data-application-form]");
    applicationForm?.addEventListener("submit", (event) => {
        if (!applicationForm.checkValidity()) {
            event.preventDefault();
            window.showToast?.("Please fill in all required fields.", "danger");
            applicationForm.classList.add("was-validated");
            return;
        }
        // Let the form submit normally to Django
    });

    const filterForm = document.querySelector("[data-filter-form]");
    const jobCards = Array.from(document.querySelectorAll("[data-job-list] .job-card"));
    const resultCounts = document.querySelectorAll("[data-result-count]");
    const emptyState = document.querySelector("[data-empty-state]");
    const normalize = (value) => String(value || "").toLowerCase().trim();

    const updateJobResults = () => {
        if (!filterForm || !jobCards.length) return;
        const data = new FormData(filterForm);
        const query = normalize(data.get("q"));
        const location = normalize(data.get("location"));
        const category = normalize(data.get("category"));
        const type = normalize(data.get("type"));
        const salary = Number(data.get("salary") || 0);
        let visible = 0;

        jobCards.forEach((card) => {
            const searchable = normalize([card.dataset.title, card.dataset.company, card.dataset.location, card.dataset.skills].join(" "));
            const isVisible =
                (!query || searchable.includes(query)) &&
                (!location || normalize(card.dataset.location).includes(location)) &&
                (!category || normalize(card.dataset.category) === category) &&
                (!type || normalize(card.dataset.type) === type) &&
                (!salary || Number(card.dataset.salary || 0) >= salary);

            card.classList.toggle("d-none", !isVisible);
            if (isVisible) visible += 1;
        });

        resultCounts.forEach((item) => {
            item.textContent = visible;
        });
        emptyState?.classList.toggle("d-none", visible !== 0);
    };

    filterForm?.addEventListener("submit", (event) => {
        event.preventDefault();
        updateJobResults();
    });
    filterForm?.querySelectorAll("input, select").forEach((field) => {
        field.addEventListener("input", updateJobResults);
        field.addEventListener("change", updateJobResults);
    });
    document.querySelector("[data-clear-filters]")?.addEventListener("click", () => {
        filterForm?.reset();
        updateJobResults();
    });
    updateJobResults();

    const homeSearch = document.querySelector("[data-home-search]");
    homeSearch?.addEventListener("submit", () => {
        window.showToast?.("Searching roles...");
    });

    const applicantSearch = document.querySelector("[data-applicant-search]");
    applicantSearch?.addEventListener("input", () => {
        const query = normalize(applicantSearch.value);
        document.querySelectorAll("[data-applicant]").forEach((row) => {
            row.classList.toggle("d-none", !normalize(row.dataset.applicant).includes(query));
        });
    });
})();
