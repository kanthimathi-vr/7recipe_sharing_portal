from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)
RECIPE_FILE = 'recipes.json'

def load_recipes():
    try:
        with open(RECIPE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_recipes(recipes):
    with open(RECIPE_FILE, 'w') as f:
        json.dump(recipes, f, indent=2)

@app.route('/')
def index():
    recipes = load_recipes()
    category = request.args.get('category', '').lower()
    if category:
        recipes = [r for r in recipes if r['category'].lower() == category]
    categories = sorted(set(r['category'] for r in load_recipes()))
    return render_template('index.html', recipes=recipes, categories=categories)

@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    recipes = load_recipes()
    recipe = next((r for r in recipes if r['id'] == recipe_id), None)
    return render_template('recipe.html', recipe=recipe)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        recipes = load_recipes()
        new_recipe = {
            'id': len(recipes) + 1,
            'title': request.form['title'],
            'category': request.form['category'],
            'ingredients': request.form['ingredients'],
            'instructions': request.form['instructions'],
            'image': request.form['image'],
            'date': datetime.now().strftime('%B %d, %Y')
        }
        recipes.insert(0, new_recipe)
        save_recipes(recipes)
        return redirect(url_for('index'))
    return render_template('add_recipe.html')

if __name__ == '__main__':
    app.run(debug=True)
