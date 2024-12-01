import os

class Config:
    SECRET_KEY = 'your_secret_key'  # Change this to a secure key
    SQLALCHEMY_DATABASE_URI = 'mysql://root:sql123@localhost/stock_portfolio'  # Update with your DB credentials
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FINNHUB_API_KEY = 'cl4ssi9r01qrlanq468gcl4ssi9r01qrlanq4690'  # Replace with your actual API key from Finnhub
