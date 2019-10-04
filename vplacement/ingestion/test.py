import requests
import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='config/.env')

from spoonacular import Spoonacular, RecipeId

# Creating an object
recipe = Spoonacular("https://www.ricardocuisine.com/en/recipes/5762-classic-beef-chili", allergies='onion')

# Perform steps
recipe.get_input_recipe()
recipe.get_ingredients()
recipe.get_output_recipes(number=20)
#print(recipe.output_recipes[0]['missedIngredients'])
print(recipe.allergies)

recipe.remove_meat_recipes()


print(len(recipe.output_recipes_veg))

print(len(recipe.output_recipes_veg[0]['missedIngredients']))
print(len(recipe.output_recipes_veg[1]['missedIngredients']))

recipe.remove_allergies()
recipe.list_to_json()
print(recipe.output_recipes_veg)

# print(recipe.ingredients)
# print(recipe.original_df[['aisle', 'name', 'original']])

# recipe = RecipeId("716429")
# recipe.get_recipe_info()
# recipe.recipe_info
