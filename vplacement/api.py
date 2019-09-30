import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from ingestion.spoonacular import Spoonacular, RecipeId

load_dotenv(dotenv_path='config/.env')

app = flask.Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return '''<h1>Vplacement</h1>
<p>Whoop, whoop, coolest webapp ever!! </p>'''

@app.route('/recipeUrl')
@cross_origin()
def url_request():
    input_recipe_url = request.args.get('url')
    veg_option = request.args.get('diet')
    # Creating an object
    recipe = Spoonacular(input_recipe_url, veg_option)

    #Perform steps
    recipe.get_input_recipe()
    recipe.get_ingredients()
    recipe.get_output_recipes()
    recipe.remove_meat_recipes()

    return recipe.output_recipes_veg

@app.route('/recipeId')
@cross_origin()
def id_request():
    recipe_id = request.args.get('id')
    # Creating an object
    recipe = RecipeId(recipe_id)
    # Request info of that recipe
    recipe.get_recipe_info()

    return recipe.recipe_info

if __name__ == "__main__":
    app.run(host='0.0.0.0')

