document.addEventListener("DOMContentLoaded", function () {

    // ==============================
    // FORM VALIDATION (SUBMIT PAGE)
    // ==============================
    const form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", function (e) {

            const name = form.querySelector("input[name='name']");
            const admission = form.querySelector("input[name='admission_number']");
            const file = form.querySelector("input[name='file']");

            // Basic validation checks
            if (!name.value.trim()) {
                alert("Name is required.");
                e.preventDefault();
                return;
            }

            if (!admission.value.trim()) {
                alert("Admission number is required.");
                e.preventDefault();
                return;
            }

            if (!file.value) {
                alert("Please upload a file.");
                e.preventDefault();
                return;
            }

        });
    }

    // ==============================
    // FILE SIZE WARNING (FRONTEND GUARD)
    // ==============================
    const fileInput = document.querySelector("input[type='file']");

    if (fileInput) {
        fileInput.addEventListener("change", function () {

            const file = this.files[0];

            if (file) {
                const sizeMB = file.size / (1024 * 1024);

                if (sizeMB > 10) {
                    alert("File is too large. Maximum allowed size is 10MB.");
                    this.value = "";
                }
            }

        });
    }

    // ==============================
    // UX ENHANCEMENT: BUTTON FEEDBACK
    // ==============================
    const buttons = document.querySelectorAll("button");

    buttons.forEach(btn => {
        btn.addEventListener("click", function () {
            btn.style.opacity = "0.7";
            setTimeout(() => {
                btn.style.opacity = "1";
            }, 200);
        });
    });

    // ==============================
    // AUTO FORMAT ADMISSION NUMBER
    // ==============================
    const admissionInput = document.querySelector("input[name='admission_number']");

    if (admissionInput) {
        admissionInput.addEventListener("input", function () {
            this.value = this.value.toUpperCase();
        });
    }

});
