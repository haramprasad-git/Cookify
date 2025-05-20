const recipeCards = document.getElementsByClassName("recipe-card");
const filterForm = document.getElementById("filterForm");


filterForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const selectedCategory = document.getElementById("categorySelect").value;
    const selectedVeganity = document.getElementById("veganitySelect").value;
    const searchQuery = document.getElementById("recipeSearch").value;
    let hidden_recipes_count = 0;
    console.log("Count before: ", hidden_recipes_count)
    for (let i = 0; i < recipeCards.length; i++) {
        const card = recipeCards[i];
        const categories = card.dataset.categories.split(",")
        if (selectedCategory !== "0" && !(categories.includes(selectedCategory))) {
            card.style.display = "none";
            hidden_recipes_count++;
            continue;
        }
        if (selectedVeganity !== "0" && card.dataset.veganity !== selectedVeganity ) {
            card.style.display = "none";
            hidden_recipes_count++;
            continue;
        }
        if (searchQuery !== "" && !(card.dataset.name.includes(searchQuery))) {
            card.style.display = "none";
            hidden_recipes_count++;
            continue;
        }
        card.style.display = "initial";
    }
    console.log("Count After: ", hidden_recipes_count)
    if (!(hidden_recipes_count < recipeCards.length)) {
        document.getElementsByClassName("no-result-msg")[0].style.display = "initial";
    } else {
        document.getElementsByClassName("no-result-msg")[0].style.display = "none";
    }
});