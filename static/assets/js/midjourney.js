document.addEventListener("DOMContentLoaded", function () {
    const categoryDropdown = document.querySelectorAll(".category-dropdown");
    const categoryButtons = document.querySelectorAll(".category-button");
    const subcategoryContainers = document.querySelectorAll(".subcategory");
    const subcategoryButtons = document.querySelectorAll(".subcategory-button");
    const inputField = document.getElementById("input-field");

    categoryButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        // Ausgewählten Button hervorheben
        categoryButtons.forEach(function (button) {
          button.classList.remove("selected");
        });
        this.classList.add("selected");

        // Alle Unter-Kategorie-Container ausblenden
        subcategoryContainers.forEach(function (container) {
          container.style.display = "none";
        });
        subcategoryButtons.forEach(function (button) {
          button.addEventListener("click", function () {
        // Ausgewählten Button hervorheben
        subcategoryButtons.forEach(function (button) {
          button.classList.remove("selected");
        });
        this.classList.add("selected");
        });
        });

        // Entsprechenden Unter-Kategorie-Container anzeigen
        const selectedCategory = this.dataset.category;
        const selectedSubcategoryContainer = document.getElementById(selectedCategory);
        selectedSubcategoryContainer.style.display = "block";
      });
    });

    subcategoryButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      // Button-Namen in das Textfeld eintragen
      const selectedCategoryButton = document.querySelector(".category-button.selected");
      const categoryDropdown = document.getElementById("category-dropdown");
      const categoryDropdownName = categoryDropdown.options[categoryDropdown.selectedIndex].text;
      const categoryButtonName = selectedCategoryButton ? selectedCategoryButton.innerText : "";
      const subcategoryButtonName = this.innerText;
      const value = "Ein " + categoryDropdownName + " im " + categoryButtonName + " Stil in einem " + subcategoryButtonName + " Material.";
          inputField.value = value.toLowerCase();
      });
    });
    });