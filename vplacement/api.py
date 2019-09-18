import flask
from flask import request, jsonify
from dotenv import load_dotenv
from ingestion.spoonacular import Spoonacular

load_dotenv(dotenv_path='vplacement/config/.env')

#Creating an object
recipe = Spoonacular("https://www.delish.com/cooking/recipe-ideas/recipes/a57949/easy-shepherds-pie-recipe/")

recipe.get_input_recipe()
recipe.get_ingredients()
recipe.get_output_recipes()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Vplacement</h1>
<p>Whoop, whoop, coolest webapp ever!! </p>'''


# A route to return the output recipes
@app.route('/results', methods=['GET'])
def api_all():
    return recipe.output_recipes

app.run()
