import requests
import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='config/.env')

from spoonacular import Spoonacular, RecipeId

# Creating an object
recipe = Spoonacular("https://www.ricardocuisine.com/en/recipes/5762-classic-beef-chili")

# Perform steps
recipe.get_input_recipe()
recipe.get_ingredients()
recipe.get_output_recipes(number=20)
print(recipe.output_recipes[0]['missedIngredients'])

recipe.remove_meat_recipes()

print(recipe.output_recipes_veg['output_recipes'])

# print(recipe.ingredients)
# print(recipe.original_df[['aisle', 'name', 'original']])

# recipe = RecipeId("716429")
# recipe.get_recipe_info()
# recipe.recipe_info
