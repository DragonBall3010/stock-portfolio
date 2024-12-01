from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask app, database, and login manager
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # You should change this to a more secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sql123@localhost/stock_portfolio'  # Change your DB credentials here
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

# Set login_view so that users are redirected to login page if not logged in
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Define the user loader function
@login_manager.user_loader
def load_user(user_id):
    # Assuming 'User' is a model class that fetches a user by ID
    # You can replace this with database query logic to fetch the user from your database
    return User(user_id)

# Database Model for User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

# Initialize database tables (if they don't exist)
with app.app_context():
    db.create_all()

# Home route for testing
@app.route('/')
def home():
    return render_template('index.html')  # Make sure to create index.html if you want to display something

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))

        flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# Dashboard Route (after login)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)
