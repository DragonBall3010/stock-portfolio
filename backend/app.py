from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sql123'
app.config['MYSQL_DB'] = 'stock_portfolio'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/test-db')
def test_db():
    cur = mysql.connection.cursor()
    cur.execute("SHOW DATABASES;")
    databases = cur.fetchall()
    return {"databases": [db[0] for db in databases]}

if __name__ == "__main__":
    app.run(debug=True)


