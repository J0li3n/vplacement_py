import requests
import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='vplacement/config/.env')

#API_KEY = os.getenv('API_KEY')

class Spoonacular:
    def __init__(self, input_recipe_url):
        self.API_KEY = os.getenv('API_KEY')
        self.input_recipe_url = input_recipe_url
        self.input_recipe = {}
        self.ingredients = ''
        self.veg_option = 'vegetarian'
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


    def get_output_recipes(self):
        """
        Function return output recipe based on original ingredients

        Parameters:
        ingredients (str): ingredients of the recipe

        Returns:
        JSON: Recipes

        """
        base_url = "https://api.spoonacular.com/recipes/search"
        parameters = {"apiKey": self.API_KEY,
                      "query": self.ingredients,
                       "diet": self.veg_option}
        response = requests.request("GET", base_url, params=parameters)
        self.output_recipes = response.json()
        return self.output_recipes

    #Improve this function and cut into different functions
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
        df = pd.DataFrame(ingredients)
        # Exclude meat from dataframe
        df = df[df['aisle'] != 'Meat']
        df = df[-((df['name'].str.contains('meat')) |
                  (df['name'].str.contains('beef')) |
                  (df['name'].str.contains('chicken')))]
        # Select only some ingredients
        df = df[df['aisle'].str.contains('Produce') |
                df['aisle'].str.contains('Canned') |
                df['aisle'].str.contains('Pasta')]

        ingredients_list = df['name'].tolist()
        #Take only the last word of the ingredients to prevent too specific ingredients
        ingredients_list = [ingredient.split()[-1] for ingredient in ingredients_list]

        # Take the top 5 ingredients
        ingredients_list5 = ingredients_list[0:5]
        self.ingredients = ','.join(ingredients_list5)
        return self.ingredients

