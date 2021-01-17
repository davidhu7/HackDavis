from flask import Flask, render_template, request, make_response
import sqlite3

app = Flask(__name__)

TEAMS = {
    "1":"Chicago White Sox",
    "2":"Cleveland Indians",
    "3":"Detroit Tigers",
    "4":"Kansas City Royals",
    "5":"Minnesota Twins",
    "6":"Baltimore Orioles",
    "7":"Boston Red Sox",
    "8":"New York Yankees",
    "9":"Tampa Bay Rays",
    "10":"Toronto Blue Jays",
    "11":"Houston Astros",
    "12":"Los Angeles Angels",
    "13":"Oakland Athletics",
    "14":"Seattle Mariners",
    "15":"Texas Rangers",
    "16":"Chicago Cubs",
    "17":"Cincinnati Reds",
    "18":"Milwaukee Brewers",
    "19":"Pittsburgh Pirates",
    "20":"St. Louis Cardinals",
    "21":"Atlanta Braves",
    "22":"Miami Marlins",
    "23":"New York Mets",
    "24":"Philadelphia Phillies",
    "25":"Washington Nationals",
    "26":"Arizona Diamondbacks",
    "27":"Colorado Rockies",
    "28":"Los Angeles Dodgers",
    "29":"San Diego Padres",
    "30":"San Francisco Giants"
}

YEARS = {
    "1":"2015",
    "2":"2014",
    "3":"2013",
    "4":"2012",
    "5":"2011",
    "6":"2010",
    "7":"2009",
    "8":"2008",
    "9":"2007",
    "10":"2006",
    "11":"2005",
    "12":"2004",
    "13":"2003",
    "14":"2002",
    "15":"2001",
    "16":"2000"
}

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
