import requests
import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='config/.env')

from spoonacular import Spoonacular, RecipeId

# Creating an object
#recipe = Spoonacular("https://www.ricardocuisine.com/en/recipes/5762-classic-beef-chili", allergies='onion')
#recipe = Spoonacular("https://www.chicken.ca/recipes/one-pan-chicken-and-mushroom-tagliatelle", veg_option='vegan')
# recipe = Spoonacular("https://www.ricardocuisine.com/en/recipes/407-fish-and-chips", veg_option='vegan')
# recipe = Spoonacular("https://www.beefitswhatsfordinner.com/recipes/recipe/55558/classic-beef-meatloaf", veg_option = 'vegan')
recipe = Spoonacular("https://www.thekitchn.com/how-to-make-meatballs-cooking-lessons-from-the-kitchn-108048")

# Perform steps
recipe.get_input_recipe()
recipe.get_ingredients()

print(recipe.ingredients)

recipe.get_output_recipes(number=50)
#print(recipe.output_recipes[0]['missedIngredients'])
print(recipe.allergies)

print(len(recipe.output_recipes))
recipe.remove_meat_recipes()
print(len(recipe.output_recipes_veg))
recipe.remove_nonvegan_recipes()
print(len(recipe.output_recipes_veg))
# recipe.remove_allergies()
# print(len(recipe.output_recipes_veg))

for recipies in range(0, len(recipe.output_recipes_veg)):
    for ingredient in range(0, len(recipe.output_recipes_veg[recipies]['missedIngredients'])):
        print(recipe.output_recipes_veg[recipies]['id'],
              recipe.output_recipes_veg[recipies]['missedIngredients'][ingredient]['aisle'],
              recipe.output_recipes_veg[recipies]['missedIngredients'][ingredient]['name'])

# print(recipe.output_recipes_veg[0]['missedIngredients'][0]['name'])
# # print(len(recipe.output_recipes_veg[1]['missedIngredients']))

# recipe.remove_allergies()
# recipe.list_to_json()
# print(recipe.output_recipes_veg)

# print(recipe.ingredients)
print(recipe.original_df[['aisle', 'name', 'original']])
# print(recipe.original_df)


# recipe = RecipeId("716429")
# recipe.get_recipe_info()
# recipe.get_similar_recipes()
# print(recipe.combine_info_similar())

