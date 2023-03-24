import json
import os
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route('/')
def Mainpage():
    return render_template('Mainpage.html', create_recipe_url='/create_recipe')



@app.route('/recipes/<category>')
def recipes_by_category(category):
    images = []
    for root, dirs, files in os.walk("data"):
        for name in files:
            file = open("data/" + name, encoding = 'utf-8')
            data = json.load(file)
            if data["category"] == category:
                images.append({'title': data["name"],'url': data["image"], 'time': data["preptime"], 'portions': data["portions"], 'link': data["link"]})
            file.close()

    return render_template('recipes.html', images=images)

@app.route('/recipes/<category>/<subcategory>')
def recipes_by_subcategory(category, subcategory):
    images = []
    for root, dirs, files in os.walk("data"):
        for name in files:
            file = open("data/" + name, encoding = 'utf-8')
            data = json.load(file)
            if data["category"] == category and data["subcategory"] == subcategory:
                images.append({'title': data["name"],'url': data["image"], 'time': data["preptime"], 'portions': data["portions"], 'link': data["link"]})
            file.close()

    return render_template('recipes.html', images=images)
    
#Recipes
@app.route('/recipe/<name>')
def recipe(name):
    f = open('data/' + name + '.json', encoding = 'utf-8')
    data = json.load(f)
    return render_template('recipe.html', recipe = data)
    f.close()

@app.route('/create_recipe', methods=['POST', 'GET'])
def create_recipe():
    recipe_data = {
        'name': request.form['name'],
        'category': request.form['category'],
        'subcategory': request.form['subcategory'],
        'image': request.form['image'],
        'preptime': request.form['preptime'],
        'portions': request.form['portions'],
        'link': request.form['link']
    }

    # Generate a unique filename for the new recipe JSON document
    filename = recipe_data['name'].replace(' ', '_').lower() + '.json'

    # Save the recipe data to a new JSON document
    with open('data/' + filename, 'w') as f:
        json.dump(recipe_data, f)

    # Redirect the user to the new recipe page
    return redirect('/recipe/' + filename[:-5])    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')