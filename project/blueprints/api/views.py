from flask import redirect, render_template, Blueprint, request, flash, current_app, url_for, flash,jsonify


from project.extensions import  csrf





api= Blueprint('api', __name__, template_folder='templates', url_prefix='/api')


@api.route('/')
@csrf.exempt
def index():
    return 'hi'

@api.route('/lativ/homedata')
@csrf.exempt
def data():
    data=[{
      "url":'',
      "title":'',
      "price":'',
      "comments":'12'
    }]
    return jsonify(data)
