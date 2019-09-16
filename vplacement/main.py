import os
from dotenv import load_dotenv
from ingestion.spoonacular import Spoonacular

load_dotenv(dotenv_path='vplacement/config/.env')

#API_KEY = os.getenv('API_KEY')

recipe = Spoonacular("https://www.ricardocuisine.com/en/recipes/5762-classic-beef-chili")
recipe.get_input_recipe()
recipe.get_ingredients()
recipe.get_output_recipes()
print(recipe.output_recipes)