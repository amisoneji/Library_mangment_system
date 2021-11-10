from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
#from flask_cors import CORS,cross_origin

app = Flask(__name__)
app.secret_key = 'Authetication'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'Task'
mysql = MySQL(app)



#home page
@app.route('/')  # route for redirecting to the home page
#@cross_origin()
def home():
    return render_template('index.html')

# signup html rendering
@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    #return redirect(url_for('index'))
    return render_template('index.html')

#signup form action
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form["username"]
        emailaddress = request.form["emailaddress"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s   OR username=% s ', (emailaddress,username ))
        login = cursor.fetchone()
        if login:
            msg = 'Either user name is  not available or account already exists with this Email !'
        elif not username or not password or not emailaddress:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s)', (username, password, emailaddress, ))
            mysql.connection.commit()
            msg = 'You have successfully registered, Please login now!'
            mysql.connection.commit()
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('index.html', msg = msg)


#login and verification
@app.route('/logintomainpage', methods =['GET', 'POST'])
def logintomainpage():
    msg = ''
    if request.method == 'POST':
        emailadd = request.form['email_address']


        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (emailadd, password, ))
        login = cursor.fetchone()

        if login:
            session['loggedin'] = True
            session['id'] =login['id']
            session['username'] = login['username']
            msg = 'Logged in successfully !'
            cursor.execute("SELECT * FROM books2 ")

            data = cursor.fetchall()
            print(data)
            mysql.connection.commit()

            return render_template('home.html', data =data)
        else:
            msg = 'Incorrect Email Address / password !'
    return render_template('index.html', msg = msg)

@app.route('/newentryrender')
def newentryrender():
    return render_template("newentry.html")

@app.route('/newentry', methods =['GET', 'POST'])
def newentry():
    msg = ''
    if request.method == 'POST':
        bookid = int(request.form['bookid'])
        print(bookid)
        booktitle = request.form['booktitle']
        author = request.form['author']
        category = request.form['category']
        avaibility =int( request.form['avaibility'])

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            mySql_insert_query = """INSERT INTO books2 (Id, booktitle, author, category,avaibility) 
                                            VALUES (%s, %s, %s, %s,%s) """
            print("1")
            record = (bookid, booktitle, author, category, avaibility)
            cursor.execute(mySql_insert_query, record)
            msg = "New Entry Added Successfully"
            mysql.connection.commit()
            print("3")
            return render_template('newentry.html', msg=msg)
        except Exception as e:
            msg=e
            return render_template('newentry.html', msg=msg)

@app.route('/updaterender')
def updaterender():
    return render_template("update.html")

@app.route('/updateentry', methods =['GET', 'POST'])
def updateentry():
    msg = ''
    if request.method == 'POST':
        bookid =int( request.form['bookid'])

        change_column = request.form['change_column']
        newvalue = request.form['newvalue']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            if change_column=="Avaibility Count":
                newvalue=int(newvalue)
                cursor.execute('UPDATE books2 SET avaibility =%s where Id= %s', (newvalue, bookid))
                mysql.connection.commit()

            elif change_column == "Book Title":
                cursor.execute('UPDATE books2 SET booktitle = %s where Id= %s', (newvalue, bookid))
                mysql.connection.commit()
            elif change_column == "Author":
               cursor.execute('UPDATE books2 SET author = %s where Id= %s', (newvalue, bookid))
               mysql.connection.commit()
            elif change_column == "Category":
                cursor.execute('UPDATE books2 SET category = %s where Id= %s', (newvalue, bookid))
                mysql.connection.commit()

            cursor.execute("SELECT * FROM books2 ")

            data = cursor.fetchall()
            print(data)
            mysql.connection.commit()

            return render_template('home.html', data=data)
        except Exception as e:
            msg=e
            return render_template('update.html', msg=msg)

@app.route('/deleterendering')
def deleterendering():
    return render_template("delete.html")

@app.route('/deleteentry', methods =['GET', 'POST'])
def deleteentry():
    if request.method == 'POST':
        bookid =int( request.form['bookid'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            sql_delete = "DELETE FROM books2 WHERE id = %s"
            sql_data = (bookid,)

            cursor.execute(sql_delete, sql_data)
            cursor.execute("SELECT * FROM books2 ")

            data = cursor.fetchall()
            print(data)
            mysql.connection.commit()

            return render_template('home.html',data=data)
        except Exception as e:
            msg=e
            return render_template('delete.html', msg=msg)


@app.route('/serch', methods =['GET', 'POST'])
def serch():
    if request.method == 'POST':
        serchname =( request.form['serchname'])
        print(serchname)


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM books2 WHERE booktitle LIKE %s ", ("%" + serchname + "%",))

            data = cursor.fetchall()
            print(data)
            mysql.connection.commit()

            return render_template('home.html',data=data)
        except Exception as e:
            msg=e
            return render_template('delete.html', msg=msg)

@app.route('/lms', methods =['GET', 'POST'])
def lms():

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM books2 ")

            data = cursor.fetchall()
            print(data)
            mysql.connection.commit()

            return render_template('home.html',data=data)
        except Exception as e:
            msg=e
            return render_template('home.html', msg=msg)






if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8000) # port to run on local machine
    app.run(debug=True)