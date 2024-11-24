from flask import Flask, render_template, redirect, url_for, request
from forms.forms import RegForm, LogForm, ProductForm, SearchForm
from db_work.db_con import User, db, Product
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SK')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    form = SearchForm()
    all_products = Product.query.all()
    return render_template('index.html', products=all_products, form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegForm()
    # проверка отправляет ли пользователь данные через форму / проверка метода POST
    if form.validate_on_submit():
        new_user = User(user_name=form.user_name.data, user_email=form.user_email.data,
                        user_password=form.user_password.data)
        new_user.set_password(form.user_password.data)
        db.session.add(new_user)
        db.session.commit()
        print('reg ok')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LogForm()
    if form.validate_on_submit():
        # запрос к БД на получение пользователя по email
        user = User.query.filter_by(user_email=form.user_email.data).first()  # аутентификация
        if user and user.check_password(form.user_password.data):
            login_user(user)  # авторизация
            return redirect(url_for('dashboard'))
        else:
            print('Bad password')
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated:
        user_products = Product.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard.html', products=user_products)
    return redirect(url_for('login'))


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = ProductForm()
    if form.validate_on_submit():
        product_name = form.product_name.data
        product_desc = form.product_desc.data
        product_price = form.product_price.data
        product_img = request.files['product_img']
        filename = product_img.filename
        product_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(product_name, product_img)
        new_product = Product(user_id=current_user.id, product_name=product_name, product_desc=product_desc, product_price=product_price,
                              product_image=filename, product_category='pizza')
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('new_product.html', form=form)


@app.route('/product_detail/<int:id>')
def product_detail(id):
    product = Product.query.get(id)
    return render_template('product_detail.html', product=product)


@app.route('/product_remove/<int:id>')
def product_remove(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/product_search', methods=['GET', 'POST'])
def product_search():
    form_data = request.form['search']
    # search_products = Product.query.filter_by(product_name=form_data).all()
    search_products = Product.query.filter(Product.product_name.ilike(f'%{form_data}%')).all()
    return render_template('search.html', products=search_products)


@app.route('/product_update/<int:id>', methods=['GET', 'POST'])
def product_update(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form_update = ProductForm()
    product = Product.query.get(id)
    if form_update.validate_on_submit():
        product_name = form_update.product_name.data
        product_desc = form_update.product_desc.data
        product_price = form_update.product_price.data
        product_img = request.files['product_img']
        product.product_name = product_name
        product.product_desc = product_desc
        product.product_price = product_price
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], product.product_image))
        product.product_image = product_img.filename
        product_img.save(os.path.join(app.config['UPLOAD_FOLDER'], product_img.filename))
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('product_update.html', form=form_update, product=product)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('index'))
    return redirect(url_for('index'))


# точка входа в программу
if __name__ == '__main__':
    with app.app_context(): # создание БД в контексте приложения
        db.create_all()
    app.run(debug=True)  # здесь нужно указывать порт, port='5001'
