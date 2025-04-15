document.addEventListener("DOMContentLoaded", () => {
    // Get the max acres from the hidden div
    const maxAcresElement = document.getElementById("max-acres");
    const maxAcres = parseInt(maxAcresElement.dataset.maxAcres);

    // Select all crop checkboxes and the submit button
    const checkboxes = document.querySelectorAll(".crop-checkbox");
    const submitButton = document.getElementById("submit-button");

    // Error message element
    const errorMessage = document.getElementById("error-message");

    // Validate selection on form submission
    submitButton.addEventListener("click", (event) => {
        let totalAcres = 0;

        // Calculate the total acres for selected checkboxes
        checkboxes.forEach((checkbox) => {
            if (checkbox.checked) {
                totalAcres += parseInt(checkbox.dataset.acres);
            }
        });

        // Check if the total exceeds maxAcres
        if (totalAcres > maxAcres) {
            errorMessage.textContent = `Error: Selected acres (${totalAcres}) exceed the available acres (${maxAcres}).`;
            event.preventDefault(); // Prevent form submission
        } else {
            errorMessage.textContent = ""; // Clear error message
        }
    });
});