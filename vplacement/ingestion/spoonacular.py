import requests
import pandas as pd
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='config/.env')

class Spoonacular:


    def __init__(self, input_recipe_url, veg_option, allergies):
        self.API_KEY = os.getenv('API_KEY')
        self.input_recipe_url = input_recipe_url
        self.input_recipe = {}
        self.original_df = pd.DataFrame
        self.ingredients = ''
        self.veg_option = veg_option
        self.output_recipes = []
        self.output_recipes_veg = []
        self.allergies = allergies
        self.meat_words = ['chicken', 'beef', 'meat', 'fish', 'salmon', 'cod', 'tuna', 'anchovies', 'tilapia',
                           'bacon', 'pork']
        self.nonvegan_words = ['honey', 'mayonnaise', 'milk', 'egg', 'cheese', 'butter']

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

    def get_output_recipes(self, number=50, ranking=1, ignore_pantry=True):
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
        self.output_recipes = response.json()
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
        df = df[df['aisle'] != 'Seafood']
        df = df[-(df['name'].apply(lambda x: any(word in x for word in self.meat_words)))]

        # Exclude allergies from dataframe
        if self.allergies is not None:
            allergies_list = self.allergies.split(",")
            df = df[-(df['name'].apply(lambda x: any(word in x for word in allergies_list)))]

        if self.veg_option is not 'vegetarian':
            df = df[-(df['aisle'].str.contains('Cheese'))]
            df = df[-(df['aisle'].str.contains('Dairy'))]
            df = df[-(df['name'].str.contains('mayonnaise'))]
            df = df[-(df['name'].str.contains('honey'))]

        # Turn the ingredients in a list and then a string
        ingredients_list = df['name'].tolist()
        self.ingredients = ','.join(ingredients_list)
        return self.ingredients

    def remove_meat_recipes(self):
        result_ids = []
        for recipe in range(0, len(self.output_recipes)):
            for word in self.meat_words:
                if ((word in self.output_recipes[recipe]['title']) &
                        (('vegan' or 'vegetarian' or 'veggie') not in self.output_recipes[recipe]['title'])):
                    result_ids.append(self.output_recipes[recipe]['id'])
            for ingredient in range(0, len(self.output_recipes[recipe]['missedIngredients'])):
                # Only continue when the recipe is not already found to have meat
                if self.output_recipes[recipe]['id'] not in (result_ids):
                    # Add recipe id to list if the recipe contains meat or seafood
                    if ((self.output_recipes[recipe]['missedIngredients'][ingredient]['aisle'] == 'Meat') |
                            (self.output_recipes[recipe]['missedIngredients'][ingredient]['aisle'] == 'Seafood')):
                        result_ids.append(self.output_recipes[recipe]['id'])
                if self.output_recipes[recipe]['id'] not in (result_ids):
                    for word in self.meat_words:
                        if word in self.output_recipes[recipe]['missedIngredients'][ingredient]['name']:
                            result_ids.append(self.output_recipes[recipe]['id'])
            if self.output_recipes[recipe]['id'] not in (result_ids):
                self.output_recipes_veg.append(self.output_recipes[recipe])
        return self.output_recipes_veg

    def remove_nonvegan_recipes(self):
        result_ids = []
        vegan_recipes = []
        for recipe in range(0, len(self.output_recipes_veg)):
            for ingredient in range(0, (len(self.output_recipes_veg[recipe]['missedIngredients']))):
                # Only continue when the recipe is not already found to have an allergy ingredient
                if self.output_recipes_veg[recipe]['id'] not in result_ids:
                    # Add recipe id to list if the recipe contains a nonvegan ingredient
                    if (('Dairy' in self.output_recipes_veg[recipe]['missedIngredients'][ingredient]['aisle']) |
                            ('Cheese' in self.output_recipes_veg[recipe]['missedIngredients'][ingredient]['aisle'])):
                        result_ids.append(self.output_recipes_veg[recipe]['id'])
                if self.output_recipes_veg[recipe]['id'] not in (result_ids):
                    for word in self.nonvegan_words:
                        if word in self.output_recipes_veg[recipe]['missedIngredients'][ingredient]['name']:
                            result_ids.append(self.output_recipes_veg[recipe]['id'])
            if self.output_recipes_veg[recipe]['id'] not in result_ids:
                vegan_recipes.append(self.output_recipes_veg[recipe])
        self.output_recipes_veg = vegan_recipes
        return self.output_recipes_veg

    def remove_allergies(self):
        result_ids = []
        allergy_free_recipes = []
        allergy_list = self.allergies.split(', ')
        for recipe in range(0, len(self.output_recipes_veg)):
            for ingredient in range(0, (len(self.output_recipes_veg[recipe]['missedIngredients']))):
                # Only continue when the recipe is not already found to have an allergy ingredient
                if self.output_recipes_veg[recipe]['id'] not in result_ids:
                    for word in allergy_list:
                        # Add recipe id to list if the recipe contains an allergy ingredient
                        if word in self.output_recipes_veg[recipe]['missedIngredients'][ingredient]['name']:
                            result_ids.append(self.output_recipes_veg[recipe]['id'])
            if self.output_recipes_veg[recipe]['id'] not in result_ids:
                allergy_free_recipes.append(self.output_recipes_veg[recipe])
        self.output_recipes_veg = allergy_free_recipes
        return self.output_recipes_veg

    def list_to_json(self):
        return {"output_recipes": self.output_recipes_veg}

class RecipeId:


    def __init__(self, recipe_id):
        self.API_KEY = os.getenv('API_KEY')
        self.recipe_id = recipe_id
        self.recipe_info = {}
        self.similar_recipes = {}

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

    def get_similar_recipes(self):
        """
        Function to get a similar recipe from recipe id

        Parameters:
        self.recipe_id (str): recipe id

        Returns:
        JSON: recipe information
        """
        base_url = "https://api.spoonacular.com/recipes/{}/similar".format(self.recipe_id)
        parameters = {"apiKey": self.API_KEY}
        response = requests.request("GET", base_url, params=parameters)
        self.similar_recipes = response.json()
        return self.similar_recipes

    def combine_info_similar(self):
        return {"recipe_info": self.recipe_info, "similar_recipes": self.similar_recipes}
