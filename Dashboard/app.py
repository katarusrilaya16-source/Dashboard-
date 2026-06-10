from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import errors
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',                
    'password': '1234', 
    'database': 'dashboard_db'
}
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('login.html')



@app.route('/login', methods=['POST'])
def login():
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    try:
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True) 
        
       
        cursor.execute("SELECT id, username, email, created_at FROM users")
        all_users = cursor.fetchall() 
        
        cursor.close()
        conn.close()
        
        
        return render_template('dashboard.html', users=all_users)

    except Exception as e:
        print(f"Dashboard Error: {e}")
        return "Could not load dashboard data.", 500

@app.route('/mail')
def mail():
    return render_template('mail.html')


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    try:
        
        username = request.form.get('username') 
        email = request.form.get('email')
        password = request.form.get('password')

       
        print(f"DEBUGGING VALUES RECEIVED: Username={username}, Email={email},Password={password}")
        
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, password))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return "User added successfully!"

    except errors.DatabaseError as err:
        print(f"Database Error: {err}")
        return f"Database failed: {err}", 500
    except Exception as e:
        print(f"General Error: {e}")
        return f"General Error: {e}", 500

        

@app.route('/logout')
def logout():
    return redirect('/')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
