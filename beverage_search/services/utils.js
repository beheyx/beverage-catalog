const DIVIDER = "-----------------------------\n";
const NOT_FOUND_ERR_MSG = 'not found';

const searchByName = (name, beverages) => {
    const recipe = beverages.find(beverage => beverage.name.toLowerCase() === name.toLowerCase());

    if (!recipe) {
      return NOT_FOUND_ERR_MSG;
    }

    const favoriteMark = recipe.favorite === "*" ? " [*]" : ""; // Add favorite indicator
    const namePrint = `Name: ${recipe.name}${favoriteMark}`;
    const ingredientsPrint = `Ingredients: ${recipe.ingredients.join(', ')}`;
    const instructionsPrint = `Instructions:\n${recipe.instructions.map((instruction, idx) => `${idx + 1}. ${instruction}`).join('\n')}`;

    return `${DIVIDER}${namePrint}\n${ingredientsPrint}\n${instructionsPrint}`;
}

const filterByCategory = (category, beverages) => {
    const recipes = beverages.filter(beverage => beverage.category.toLowerCase() === category.toLowerCase());

    if (recipes.length === 0) {
        return NOT_FOUND_ERR_MSG;
    }

    const result = recipes.map(({ name, category, description, favorite }) => {
        const favoriteMark = favorite === "*" ? " [*]" : ""; // Add favorite indicator
        const namePrint = `Name: ${name}${favoriteMark}`;
        const categoryPrint = `Category: ${category}`;
        const descriptionPrint = `Description: ${description}`;

        return `${DIVIDER}${namePrint}\n${categoryPrint}\n${descriptionPrint}`;
    }).join('\n\n');

    return `${result}`;
}

const filterByIngredients = (ingredient, beverages) => {
    const recipes = beverages.filter(beverage => 
        beverage.ingredients.map(i => i.toLowerCase()).includes(ingredient.toLowerCase())
    );

    if (recipes.length === 0) {
        return NOT_FOUND_ERR_MSG;
    }

    const result = recipes.map(({ name, ingredients, description, favorite }) => {
        const favoriteMark = favorite === "*" ? " [*]" : ""; // Add favorite indicator
        const namePrint = `Name: ${name}${favoriteMark}`;
        const ingredientsPrint = `Ingredients: ${ingredients.join(', ')}`;
        const descriptionPrint = `Description: ${description}`;

        return `${DIVIDER}${namePrint}\n${ingredientsPrint}\n${descriptionPrint}`;
    }).join('\n\n');

    return `${result}`;
}

module.exports = {
    searchByName,
    filterByCategory,
    filterByIngredients
};
