import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, session



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:54321@localhost/recipe_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 데이터베이스 모델 정의
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisine.id'), nullable=False)
    food_img = db.Column(db.String(100))  # 이미지 파일 이름을 저장할 필드 추가

class FoodAni(db.Model):
    __tablename__ = 'food_ani'
    id = db.Column(db.Integer, primary_key=True)
    food_ani = db.Column(db.String(100), nullable=False)

 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 홈페이지 라우트
@app.route('/')
def index():
    cuisines = Cuisine.query.all()
    new_recipes = Recipe.query.order_by(Recipe.id.desc()).limit(5).all()
    food_ani_images = FoodAni.query.all()  # food_ani 테이블의 모든 데이터 가져오기
    return render_template('index.html', cuisines=cuisines, new_recipes=new_recipes, food_ani_images=food_ani_images)


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

# 회원가입 라우트
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('이미 존재하는 사용자 이름입니다.', 'danger')
            return render_template('signup.html')
        if User.query.filter_by(email=email).first():
            flash('이미 존재하는 이메일 주소입니다.', 'danger')
            return render_template('signup.html')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('signup.html')

# 로그인 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('잘못된 이메일 또는 비밀번호입니다.', 'danger')
    return render_template('login.html')

# 로그아웃 라우트
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(debug=True)