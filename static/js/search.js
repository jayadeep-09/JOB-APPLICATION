(function () {
    const form = document.querySelector("[data-filter-form]");
    const cards = Array.from(document.querySelectorAll(".job-card-wrap"));
    const count = document.querySelector("[data-result-count]");
    const empty = document.querySelector("[data-empty-state]");
    const skeleton = document.querySelector("[data-skeleton]");

    const normalize = (value) => String(value || "").toLowerCase().trim();
    const applyFilters = () => {
        if (!form || !cards.length) return;
        skeleton?.classList.remove("d-none");
        window.setTimeout(() => {
            const data = new FormData(form);
            const query = normalize(data.get("q"));
            const location = normalize(data.get("location"));
            const category = normalize(data.get("category"));
            const type = normalize(data.get("type"));
            const salary = Number(data.get("salary") || 0);
            let visible = 0;
            cards.forEach((card) => {
                const haystack = normalize([card.dataset.title, card.dataset.company, card.dataset.location, card.dataset.skills].join(" "));
                const matchesQuery = !query || haystack.includes(query);
                const matchesLocation = !location || normalize(card.dataset.location).includes(location);
                const matchesCategory = !category || normalize(card.dataset.category) === category;
                const matchesType = !type || normalize(card.dataset.type) === type;
                const matchesSalary = !salary || Number(card.dataset.salary || 0) >= salary;
                const shouldShow = matchesQuery && matchesLocation && matchesCategory && matchesType && matchesSalary;
                card.classList.toggle("d-none", !shouldShow);
                if (shouldShow) visible += 1;
            });
            if (count) count.textContent = visible;
            empty?.classList.toggle("d-none", visible !== 0);
            skeleton?.classList.add("d-none");
        }, 180);
    };

    form?.addEventListener("submit", (event) => {
        event.preventDefault();
        applyFilters();
    });
    form?.querySelectorAll("input, select").forEach((control) => {
        control.addEventListener("input", applyFilters);
        control.addEventListener("change", applyFilters);
    });
    document.querySelector("[data-clear-filters]")?.addEventListener("click", () => {
        form?.reset();
        applyFilters();
    });
    if (form) applyFilters();

    const applicantSearch = document.querySelector("[data-applicant-search]");
    applicantSearch?.addEventListener("input", () => {
        const query = normalize(applicantSearch.value);
        document.querySelectorAll(".applicant-row").forEach((row) => {
            row.classList.toggle("d-none", !normalize(row.dataset.applicant).includes(query));
        });
    });
})();
