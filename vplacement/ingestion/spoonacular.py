import requests
import pandas as pd
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='config/.env')

class Spoonacular:

    def __init__(self, input_recipe_url, veg_option='vegetarian'):
        self.API_KEY = os.getenv('API_KEY')
        self.input_recipe_url = input_recipe_url
        self.input_recipe = {}
        self.original_df = pd.DataFrame
        self.ingredients = ''
        self.veg_option = veg_option
        self.output_recipes = {}

    def get_input_recipe(self):
        """
        Function to retrieve the information about the input recipe.

        Parameters:
        url (str): URL of the recipe of interest

        Returns:
        JSON: Recipe characteristics
        """
        base_url = "https://api.spoonacular.com/recipes/extract"
        parameters = {"apiKey": self.API_KEY,
                      "url": self.input_recipe_url}
        response = requests.request("GET", base_url, params=parameters)
        self.input_recipe = response.json()
        return self.input_recipe

    def get_output_recipes(self, number=20, ranking=1, ignore_pantry=True):
        """
        Function return output recipe based on original ingredients

        Parameters:
        ingredients (str): ingredients of the recipe

        Returns:
        JSON: Recipes
        """
        base_url = "https://api.spoonacular.com/recipes/findByIngredients"
        parameters = {"apiKey": self.API_KEY,
                      "ingredients": self.ingredients,
                      "number": number,
                      "ranking": ranking,
                      "ignorePantry": ignore_pantry,
                      }
        response = requests.request("GET", base_url, params=parameters)
        self.output_recipes = json.dumps({"output_recipes": response.json()})
        self.output_recipes = json.loads(self.output_recipes)
        return self.output_recipes

    # Improve this function and cut into different functions
    def get_ingredients(self):
        """
        Function to get ingredients from input recipes

        Parameters:
        response_json (dict): json file of recipes

        Returns:
        str: ingredients
        """
        # Get ingredients
        ingredients = self.input_recipe['extendedIngredients']
        # Create dataframe
        self.original_df = pd.DataFrame(ingredients)

        # Exclude meat and seafood from dataframe
        df = self.original_df[self.original_df['aisle'] != 'Meat']
        df = self.original_df[self.original_df['aisle'] != 'Seafood']
        df = df[-((df['name'].str.contains('meat')) |
                  (df['name'].str.contains('beef')) |
                  (df['name'].str.contains('chicken')))]

        if(self.veg_option == 'vegan'):
            df = df[-(df['aisle'].str.contains('Cheese'))]

        #Turn the ingredients in a list and then a string
        ingredients_list = df['name'].tolist()
        self.ingredients = ','.join(ingredients_list)
        return self.ingredients

class RecipeId:

    def __init__(self, recipe_id):
        self.API_KEY = os.getenv('API_KEY')
        self.recipe_id = recipe_id
        self.recipe_info = {}

    def get_recipe_info(self):
        """
        Function to get recipe information from recipe id

        Parameters:
        self.recipe_id (str): recipe id

        Returns:
        JSON: recipe information
        """
        base_url = "https://api.spoonacular.com/recipes/{}/information".format(self.recipe_id)
        parameters = {"apiKey": self.API_KEY}
        response = requests.request("GET", base_url, params=parameters)
        self.recipe_info = response.json()
        return self.recipe_info
