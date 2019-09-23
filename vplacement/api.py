import flask
from flask import request, jsonify
from dotenv import load_dotenv
from ingestion.spoonacular import Spoonacular

load_dotenv(dotenv_path='config/.env')

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Vplacement</h1>
<p>Whoop, whoop, coolest webapp ever!! </p>'''

@app.route('/recipe')
def url_request():
    input_recipe_url = request.args.get('url')
    # Creating an object
    recipe = Spoonacular(input_recipe_url)

    #Perform steps
    recipe.get_input_recipe()
    recipe.get_ingredients()
    recipe.get_output_recipes()

    return recipe.output_recipes

# A route to return the output recipes
@app.route('/results', methods=['GET'])
def api_all():
    return recipe.output_recipes

if __name__ == "__main__":
    app.run(host='0.0.0.0')

