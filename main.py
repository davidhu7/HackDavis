from flask import Flask, render_template, request, make_response
import sqlite3

app = Flask(__name__)

def logged_in(cur, username, password):
    sql = """
        SELECT username,password FROM users WHERE username=? and password=?;
    """
    cur.execute(sql, (username, password))
    rows = cur.fetchall()
    if len(list(rows)) == 0:
        return False
    else:
        return True

@app.route('/')
def index():
    if logged_in:
        return render_template(
            'content.html',
            username=request.cookies.get('username'),
        )
    else:
        return render_template(
            'content.html'
        )

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        print(request.form.get('team1'))
        print(request.form.get('team2'))
        print(request.form.get('year1'))
        print(request.form.get('year2'))
    else:
        print("GET")


@app.route('/login', methods=['get', 'post'])
def login():
    if request.form.get('username'):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        login_successful = logged_in(
            cur=cur,
            username=request.form.get('username'),
            password=request.form.get('password'),
        )
        if login_successful:
            res = make_response(render_template(
                'login.html',
                login_successful=True,
                username=request.form.get('username'),
            ))
            res.set_cookie('username', request.form.get('username'))
            res.set_cookie('password', request.form.get('password'))
            return res
        else:
            return render_template(
                'login.html',
                login_unsuccessful=True,
            )
    else:
        return render_template(
            'login.html',
            login_default=True,
        )

@app.route('/create_user', methods=['get', 'post'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    username = request.form.get('username')
    password = request.form.get('password')
    repeatpassword = request.form.get('repeatpassword')
    if password == repeatpassword:
        if len(username) == 0:
            create_user_successful = False
            length_error = True
            if length_error and create_user_successful == False:
                res = make_response(render_template(
                    'create_user.html',
                    password_error=True
                ))
                return res
        elif len(password) == 0:
            create_user_successful = False
            length_error = True
            if length_error and create_user_successful == False:
                res = make_response(render_template(
                    'create_user.html',
                    length_error=True
                ))
                return res
        else:
            create_user_successful=True
            if len(username) != 0 and len(password) != 0:
                try:
                    sql = """
                        INSERT INTO users (username, password) values (?,?);
                    """
                    cur.execute(sql, (username, password))
                    con.commit()
                except sqlite3.IntegrityError:
                    username_error=True
                    if username_error:
                        res = make_response(render_template(
                            'create_user.html',
                            username_error=True
                        ))
                        return res
                if create_user_successful:
                    res = make_response(render_template(
                        'create_user.html',
                        create_user_successful=True,
                    ))
                    return res
                else:
                    return render_template(
                        'create_user.html',
                        create_user_unsuccessful=True
                    )
    else:
        password_error=True
        if password_error:
            res = make_response(render_template(
                'create_user.html',
                password_error=True
            ))
            return res

@app.route('/logout')
def logout():
    res = make_response(render_template(
        'logout.html'
    ))
    res.set_cookie('username', '', expires=0)
    res.set_cookie('password', '', expires=0)
    return res

@app.route('/delete_user/<username>')
def delete_user(username):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    if logged_in(
        cur=cur,
        username=request.cookies.get('username'),
        password=request.cookies.get('password'),
    ):
        sql = """
            DELETE FROM users WHERE username=?;
        """
        cur.execute(sql, (username,))
        con.commit
        res = make_response(render_template(
            'delete_user.html',
        ))
        res.set_cookie('username', '', expires=0)
        res.set_cookie('password', '', expires=0)
        return res
    return render_template('content.html')


app.run()
