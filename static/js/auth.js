(function () {
    document.querySelectorAll(".password-toggle").forEach((button) => {
        button.addEventListener("click", () => {
            const input = button.closest(".password-field")?.querySelector("input");
            if (!input) return;
            const isHidden = input.type === "password";
            input.type = isHidden ? "text" : "password";
            button.innerHTML = isHidden ? '<i class="fa-regular fa-eye-slash"></i>' : '<i class="fa-regular fa-eye"></i>';
        });
    });

    document.querySelectorAll(".needs-client-validation").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const confirmInput = form.querySelector("[data-confirm-password]");
            if (confirmInput) {
                const passwordInput = form.querySelector(confirmInput.dataset.confirmPassword);
                confirmInput.setCustomValidity(passwordInput && confirmInput.value !== passwordInput.value ? "Passwords must match" : "");
            }
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                form.querySelector(".btn-loading")?.classList.remove("loading");
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
        resetForm.querySelector(".btn-loading")?.classList.remove("loading");
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

    // Application form submission is handled by main.js — no duplicate handler here.
})();
