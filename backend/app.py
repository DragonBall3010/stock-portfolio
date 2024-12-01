from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Stock, Portfolio, Transaction
import finnhub

# Initialize the Flask app, database, and login manager
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

# Flask-Login's user_loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes and app logic


# Initialize the Finnhub client
finnhub_client = finnhub.Client(api_key="cl4ssi9r01qrlanq468gcl4ssi9r01qrlanq4690")

@app.route('/')
def home():
    stock_data = fetch_stock_data('AAPL')  # Example: Fetch Apple stock data
    return render_template('index.html', stock_data=stock_data)

def fetch_stock_data(symbol):
    data = finnhub_client.quote(symbol)
    if data:
        return {
            'symbol': symbol,
            'current_price': data['c'],
            'high': data['h'],
            'low': data['l'],
            'open': data['o'],
            'previous_close': data['pc']
        }
    else:
        return None

# Register route for new users
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        new_user = User(username=username, email=email, password_hash=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error registering user. Try again.', 'danger')
            db.session.rollback()

    return render_template('register.html')

# Login route for users
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('login.html')

# Logout route for users
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
