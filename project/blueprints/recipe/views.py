from flask import redirect, render_template, Blueprint, request, flash, url_for, jsonify, current_app
from project.blueprints.user.models import User
from datetime import datetime
from flask_login import login_required, login_user, current_user, logout_user
from project.blueprints.recipe.forms import RecipeForm
import os
from flask_dropzone import random_filename
from pymongo import MongoClient
from functools import reduce

from PIL import Image

client = MongoClient('mongodb://mongo:27017')
db = client.RecipeDB
RecipeCo = db['RecipeCo']

recipe = Blueprint('recipe', __name__, template_folder='templates' )

#utils section
def get_filename(f, filename, size):
    img = Image.open(f)
    print(img.size[0], img.size[1])
    if img.size[0] < size:
        return filename
    fileName, ext = os.path.splitext(filename)
    height = int((size / float(img.size[0]))*float(img.size[1]))
    img = img.resize((size, height), Image.ANTIALIAS)
    fileName = fileName+'_s' + ext
    img.save(os.path.join('/project/project/static/style/pics/recipes', fileName), optimize=True,quality=85)
    return fileName




#主页

@recipe.route('/recipe')
def index():
    return render_template('recipe-index.html')



@recipe.route('/new_recipe', methods=['POST', 'GET'])
def new():
    form = RecipeForm()
    if request.method =='POST':
        # x=db.RecipeCo.find()    #查看所有
        # for i in x:
        #     print(i)
        # db.RecipeCo.drop()      # 删除所有
        data = request.get_json()
        if len(data['steps'])<=1:
            length_steps = len(data['steps'])
        else:
            length_steps =int(reduce(lambda x, y:len(x)+len(y), data['steps']))

        if len(data['title']) > 125 or len(data['tags'])>10 or len(data['ingredients'])>30 or length_steps >1500:
            return jsonify('no')
        print('传送了', request.get_json())
        RecipeCo.insert(data)
        print('插入成功')
        return jsonify("saved")
    return render_template('new_recipe.html', form=form)

@recipe.route('/upload_pics', methods=['POST', 'GET'])
def test():
    if request.method =='POST' and 'file' in request.files:
        f = request.files.get('file')
        title = request.form.get('bind')
        filename = random_filename(f.filename)
        try:
            RecipeCo.update(
               {'title': title},
               {'$addToSet': {"files":"filename"}}
            )
        except:
            print('更新recipe数据库错误')
        f.save(os.path.join('/project/project/static/style/pics/recipes', filename))
        fileName = get_filename(f, filename, 400)
        print('保存成功')
    return render_template('test_upload.html')


@recipe.route('/get_pics')
def pics():
    pass

@recipe.route('/recipe/admin')
def admin():
    return render_template('recipe_admin.html')

@recipe.route('/recipe/admin/users')
def admin_user():
    return render_template('admin_user.html')

@recipe.route('/recipe/admin/all_recipes')
def all_recipes():
    return render_template('all_recipes.html')
