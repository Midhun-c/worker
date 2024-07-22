from flask import Flask, render_template, redirect, url_for, request, flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import User, Worker

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/migrant_worker_db'
app.config['SECRET_KEY'] = 'your_secret_key'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(username):
    return User.get_by_username(username)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save_to_db()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_by_username(username)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Login failed. Check your username and/or password.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    workers = Worker.get_all_workers_by_user(current_user.get_id())
    return render_template('dashboard.html', workers=workers)

@app.route('/add_worker', methods=['GET', 'POST'])
@login_required
def add_worker():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        photo = request.form['photo']
        employment_history = request.form['employment_history']
        worker = Worker(name, location, photo, employment_history, current_user.get_id())
        worker.save_to_db()
        flash('Worker added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_worker.html')

@app.route('/edit_worker/<worker_id>', methods=['GET', 'POST'])
@login_required
def edit_worker(worker_id):
    worker = Worker.get_worker_by_id(worker_id)
    if request.method == 'POST':
        updated_data = {
            'name': request.form['name'],
            'location': request.form['location'],
            'photo': request.form['photo'],
            'employment_history': request.form['employment_history']
        }
        Worker.update_worker(worker_id, updated_data)
        flash('Worker updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_worker.html', worker=worker)

@app.route('/delete_worker/<worker_id>', methods=['POST'])
@login_required
def delete_worker(worker_id):
    Worker.delete_worker(worker_id)
    flash('Worker deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
