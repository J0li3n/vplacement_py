import os
from dotenv import load_dotenv
from ingestion.spoonacular import Spoonacular

load_dotenv(dotenv_path='vplacement/config/.env')

#recipe = Spoonacular("https://www.ricardocuisine.com/en/recipes/5762-classic-beef-chili")
#recipe = Spoonacular("https://natashaskitchen.com/fish-tacos-recipe/")
recipe = Spoonacular("https://www.delish.com/cooking/recipe-ideas/recipes/a57949/easy-shepherds-pie-recipe/")

recipe.get_input_recipe()
recipe.get_ingredients()
recipe.get_output_recipes()
print(recipe.output_recipes)
print(recipe.ingredients)