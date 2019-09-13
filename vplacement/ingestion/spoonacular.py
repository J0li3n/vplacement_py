import requests
import pandas as pd
import json

#Make Spoonacular class

def get_input_recipe(url):
    """
    Function to retrieve the information about the input recipe.

    Parameters:
    url (str): URL of the recipe of interest

    Returns:
    JSON: Recipe characteristics

    """
    base_url = "https://api.spoonacular.com/recipes/extract"
    parameters = {"apiKey": API_key,
                  "url": url}
    response = requests.request("GET", base_url, params=parameters)
    response_json = response.json()
    return response_json


def get_output_recipes(ingredients, veg_option='vegetarian'):
    """
    Function return output recipe based on original ingredients

    Parameters:
    ingredients (str): ingredients of the recipe

    Returns:
    JSON: Recipes

    """
    base_url = "https://api.spoonacular.com/recipes/search"
    parameters = {"apiKey": API_key,
                  "query": ingredients,
                  "diet": veg_option}
    response = requests.request("GET", base_url, params=parameters)
    response_json = response.json()
    return response_json

#response_json = get_input_recipe("https://www.ricardocuisine.com/en/recipes/5762-classic-beef-chili")
#get_output_recipes(ingredients_str)


def get_ingredients(response_json):
    # Get ingredients
    ingredients = response_json['extendedIngredients']
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

    # Take the top 5 ingredients
    ingredients_list5 = ingredients_list[0:5]
    ingredients_str = ','.join(ingredients_list5)
    return ingredients_str


