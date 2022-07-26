# from asyncio.windows_events import NULL
import os
import csv
from unicodedata import name
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from matplotlib.pyplot import table
from werkzeug.utils import secure_filename

import sqlite3 as sq
listoftables=[]


app = Flask(__name__)

conn = sq.connect('database.db',check_same_thread=False)
Cur = conn.cursor()

# app.config['SQLALCHEMY_DATABASE_URI'] =\
#         'sqlite:///' + os.path.join(basedir, 'database.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class MOSS(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     Rno1 = db.Column(db.Integer, nullable=False)
#     Rno2 = db.Column(db.Integer, nullable=False)
#     Queslist = db.Column(db.String(100),nullable=False)

# db.create_all()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/uploading', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        table = request.form['table']
        listoftables.append(table)
        f = request.files['file']
        f.save(secure_filename(f.filename))  # this will secure the file

        command1 = """CREATE TABLE IF NOT EXISTS '{}' (Sno VARCHAR(20),Rno1 DECIMAL(8,2),
            Rno2 DECIMAL(8,2), MossQ VARCHAR(20))"""
        Cur.execute(command1.format(table))

        with open(f.filename, 'r', newline="") as file:
            fn = csv.reader(file)
            next(fn)
            for row in fn:
                id = row[0]
                Rno1 = row[1]
                Rno2 = row[2]
                Queslist = row[3]

                # print(row)
                Cur.execute("""INSERT INTO '{}' VALUES('{}','{}','{}','{}')""".format(table,id,Rno1,Rno2,Queslist))
                conn.commit()
    conn.commit()
    return render_template("updated.html")

@app.route("/updatecol", methods=['GET', 'POST'])
def rendering():
    return render_template("update.html")

@app.route("/updatecollegedb", methods=['GET', 'POST'])
def updatecoldb():
    if request.method == 'POST':
        # table = request.form['table']
        f = request.files['file1']
        f.save(secure_filename(f.filename))  # this will secure the file
        # print(f.filename)

        command1 = """CREATE TABLE IF NOT EXISTS '{}' (Rno VARCHAR(20),Names VARCHAR(20))"""
        Cur.execute(command1.format("COLLEGEDB"))


        # Cur.execute(command1)

        with open(f.filename, 'r', newline="") as file:
            fn = csv.reader(file)
            next(fn)
            for row in fn:
                Rno = row[0]
                Name = row[1]
                Cur.execute("""INSERT INTO COLLEGEDB VALUES(?,?)""",(Rno,Name))
                conn.commit()
            conn.commit()
        D={}
        Cur.execute("SELECT * FROM COLLEGEDB")
        for row in Cur:
            D[int(row[0])]=row[1]
    # return "ok"
        print(D)
    return render_template("updated.html")

@app.route("/redirect",methods=["GET","POST"])
def redirecting():
    return render_template("index.html")

@app.route('/search',methods=['GET','POST'])
def display():
    Cur.execute("""SELECT name FROM sqlite_master 
    WHERE type='table';""")
    
    for row in Cur:
        for j in row:
            if j not in listoftables:
                listoftables.append(j)
    # print(listoftables)
    return render_template('search.html',listoftables=listoftables)

@app.route('/db',methods=['GET','POST'])
def showres():
    if request.method == "POST":
        choice=request.form['dropdown']
        rno1 = request.form['rno1']
        rno2 = request.form['rno2']
        print(listoftables)
        Assignments=[]
        for i in listoftables:
            if i != "ALL":
                Assignments.append(i)
        print(Assignments)
        command1 = """SELECT * FROM '{}' """
        Cur.execute(command1.format(choice))
        print(rno1)
        print(rno2)
        if choice != "ALL":
            # if int(rno2) == None: This doesnt work
            if rno2 == '':
                for j in Cur:
                    # print(j[1])
                    if j[1] == int(rno1) or j[2] == int(rno1):
                        print("Got Mossed in Question",end=" ")
                        print(j[3],end=" ")
                        print("in",end=" ")
                        print(choice)
            elif rno1 == '':
                for j in Cur:
                    # print(j[1])
                    if j[1] == int(rno2) or j[2] == int(rno2):
                        print("Got Mossed in Question",end=" ")
                        print(j[3],end=" ")
                        print("in",end=" ")
                        print(choice)
            else:
                check=0
                for j in Cur:
                    # print(j[1])
                    if ((j[1] == int(rno1) or j[2] == int(rno1)) and (j[2] == int(rno2) or j[1] == int(rno2))):
                        print("They both Got Mossed in Question",end=" ")
                        print(j[3],end=" ")
                        print("in",end=" ")
                        print(choice)
                        check=1
                if check == 0:
                    print("The students entered weren't mossed with each other in this Assignment.")
        else:
            for i in Assignments:
                    command1 = """SELECT * FROM '{}' """
                    Cur.execute(command1.format(i))
                    if rno2 == '':
                        for j in Cur:
                            # print(j[1])
                            if j[1] == int(rno1) or j[2] == int(rno1):
                                print("Got Mossed in Question",end=" ")
                                print(j[3],end=" ")
                                print("in",end=" ")
                                print(i)
                    elif rno1 == '':
                        for j in Cur:
                            # print(j[1])
                            if j[1] == int(rno2) or j[2] == int(rno2):
                                print("Got Mossed in Question",end=" ")
                                print(j[3],end=" ")
                                print("in",end=" ")
                                print(i)
                    else:
                        check=0
                        for j in Cur:
                            # print(j[1])
                            if ((j[1] == int(rno1) or j[2] == int(rno1)) and (j[2] == int(rno2) or j[1] == int(rno2))):
                                print("They both Got Mossed in Question",end=" ")
                                print(j[3],end=" ")
                                print("in",end=" ")
                                print(i)
                                check=1
                        if check == 0:
                            print("The students entered weren't mossed with each other in this Assignment.")
        return "hello"
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
