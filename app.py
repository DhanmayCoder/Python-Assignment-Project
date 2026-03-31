from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def add_user_to_db(user, pwd):
    with open("users.txt", "a") as f:
        f.write(f"{user}:{pwd}\n")


def validate_credentials(user, pwd):
    try:
        with open("users.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
              
                stored_user, stored_pwd = line.strip().split(":")
                if user == stored_user and pwd == stored_pwd:
                    return True
    except FileNotFoundError:
        return False
    return False

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        add_user_to_db(u, p)
        return "<h1>Success!</h1><p>Account created. <a href='/login'>Go Login</a></p>"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        if validate_credentials(u, p):
            return f"<h1>Welcome, {u}!</h1><p>You are logged in.</p>"
        else:
            return "<h1>Error!</h1><p>Wrong username or password. <a href='/login'>Try again</a></p>"
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)