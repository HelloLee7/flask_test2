from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL 데이터베이스 연결 설정 (본인의 정보로 변경!)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:54321@localhost/recipe_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # recipes = db.relationship('Recipe', backref='cuisine', lazy=True)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisine.id'), nullable=False)

# 홈페이지 라우트
@app.route('/')
def index():
    cuisines = Cuisine.query.all()
    new_recipes = Recipe.query.order_by(Recipe.id.desc()).limit(5).all() # 최근 5개 음식
    return render_template('index.html', cuisines=cuisines, new_recipes=new_recipes)

# 음식 종류별 라우트
@app.route('/cuisine/<int:cuisine_id>')
def cuisine_recipes(cuisine_id):
    cuisine = Cuisine.query.get_or_404(cuisine_id)
    recipes = Recipe.query.filter_by(cuisine_id=cuisine_id).all()
    return render_template('recipes.html', cuisine=cuisine, recipes=recipes)

# 새로운 음식 정보 라우트
@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)

# 정보 페이지 라우트 추가
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)