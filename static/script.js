document.addEventListener("DOMContentLoaded", function () {
  const dropdownOptions = document.getElementById("dropdown_options");
  const arrowIcon = document.getElementById("arrow_icon");
  const realValueInput = document.getElementById("real_value");
  const displayText = document.getElementById("display_text");
  const dropdownButton = document.querySelector(
    'button[onclick="toggleDropdown()"]'
  );

  window.toggleDropdown = function () {
    dropdownOptions.classList.toggle("hidden");
    arrowIcon.classList.toggle("rotate-180");
  };

  window.selectOption = function (value, text) {
    realValueInput.value = value;
    displayText.innerText = text;
    toggleDropdown();
  };

  window.addEventListener("click", function (e) {
    if (
      !dropdownButton.contains(e.target) &&
      !dropdownOptions.contains(e.target)
    ) {
      if (!dropdownOptions.classList.contains("hidden")) {
        toggleDropdown();
      }
    }
  });
});
