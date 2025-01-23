import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, session
from datetime import datetime
from werkzeug.utils import secure_filename # secure_filename 추가

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:54321@localhost/recipe_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/img' # 업로드 폴더 경로 설정 (static/img) 업로드가즈아ㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏ
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 데이터베이스 모델 정의 (기존 코드와 동일)
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
    food_img = db.Column(db.String(100)) # 이미지 파일 경로 저장
    recommendation_count = db.Column(db.Integer, default=0)

class FoodAni(db.Model):
    __tablename__ = 'food_ani'
    id = db.Column(db.Integer, primary_key=True)
    food_ani = db.Column(db.String(100), nullable=False)

class RecipeRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 홈페이지 라우트 (기존 코드와 동일)
@app.route('/')
def index():
    cuisines = Cuisine.query.all()
    new_recipes = Recipe.query.order_by(Recipe.id.desc()).limit(5).all() # 이 코드로 최근에 올라온 음식 id 겟
    food_ani_images = FoodAni.query.all()
    return render_template('index.html', cuisines=cuisines, new_recipes=new_recipes, food_ani_images=food_ani_images)

# 음식 종류별 라우트 (기존 코드와 동일)
@app.route('/cuisine/<int:cuisine_id>')
def cuisine_recipes(cuisine_id):
    cuisine = Cuisine.query.get_or_404(cuisine_id)
    recipes = Recipe.query.filter_by(cuisine_id=cuisine_id).all()
    return render_template('recipes.html', cuisine=cuisine, recipes=recipes)

# 새로운 음식 정보 라우트 (기존 코드와 동일)
@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)

# 정보 페이지 라우트 추가 (기존 코드와 동일)
@app.route('/about')
def about():
    return render_template('about.html')

# 포스팅 페이지 라우트 (GET 요청 시 폼 표시, POST 요청 시 데이터 처리)
@app.route('/post', methods=['GET', 'POST'])
@login_required # 로그인Required 데코레이터 추가
def post():
    cuisines = Cuisine.query.all() # cuisine 데이터 가져오기

    if request.method == 'POST':
        name = request.form['name']
        cuisine_id = request.form['cuisine_id']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        food_img = request.files.get('food_img') # 파일 데이터 가져오기

        image_path = None # 기본적으로 None으로 설정

        if food_img and food_img.filename != '': # 파일이 업로드되었는지 확인
            filename = secure_filename(food_img.filename) # 파일 이름 안전하게 만들기
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # 저장 경로 설정
            food_img.save(image_path) # 파일 저장
            image_path = '/' + filename # DB에 저장할 웹 경로 (static/img/파일명) # 수정된 부분

        new_recipe = Recipe(
            name=name,
            cuisine_id=cuisine_id,
            ingredients=ingredients,
            instructions=instructions,
            food_img=image_path # 이미지 경로 저장
        )
        db.session.add(new_recipe)
        db.session.commit()

        flash('레시피가 성공적으로 포스팅되었습니다!', 'success') # 성공 메시지 flash
        return redirect(url_for('recipe_detail', recipe_id=new_recipe.id)) # 상세 페이지로 리다이렉트

    return render_template('post.html', cuisines=cuisines) # GET 요청 시 post.html 렌더링, cuisines 전달

# 회원가입 라우트 (기존 코드와 동일)
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

# 로그인 라우트 (기존 코드와 동일)
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

# 로그아웃 라우트 (기존 코드와 동일)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# 추천 기능 라우트 (기존 코드와 동일)
@app.route('/recommend_recipe', methods=['POST'])
def recommend_recipe():
    recipe_id = request.form.get('recipe_id')
    recipe = Recipe.query.get_or_404(recipe_id)

    if not current_user.is_authenticated:
        return jsonify({'message': '로그인을 하지 않았습니다'}), 401

    user_id = current_user.id
    existing_recommendation = RecipeRecommendation.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()

    if existing_recommendation:
        return jsonify({'message': '이미 추천을 눌렀습니다'}), 409

    new_recommendation = RecipeRecommendation(user_id=user_id, recipe_id=recipe_id)
    db.session.add(new_recommendation)

    recipe.recommendation_count += 1
    db.session.commit()

    return jsonify({'message': '추천 완료', 'recommendation_count': recipe.recommendation_count}), 200

# 검색 기능 라우트 추가
@app.route('/search')
def search():
    query = request.args.get('search') # 검색어 가져오기
    if query:
        search_results = Recipe.query.filter(Recipe.name.like(f'%{query}%')).all() # name 컬럼에서 검색어로 검색
    else:
        search_results = [] # 검색어가 없을 경우 빈 결과
    return render_template('search_results.html', results=search_results, query=query)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Cuisine 테이블 초기 데이터 추가 (필요한 경우)
        if not Cuisine.query.filter_by(id=1).first():
            cuisines_data = [
                {'id': 1, 'name': '한식'},
                {'id': 2, 'name': '양식'},
                {'id': 3, 'name': '중식'},
                {'id': 4, 'name': '일식'},
                {'id': 5, 'name': '기타'}
            ]
            for cuisine_data in cuisines_data:
                cuisine = Cuisine(**cuisine_data)
                db.session.add(cuisine)
            db.session.commit()

    app.run(debug=True)