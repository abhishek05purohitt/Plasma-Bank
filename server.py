from flask import render_template
import sqlite3
import requests
from flask import Flask
from flask import request,redirect,url_for,session,flash,jsonify
from flask_wtf import Form
from wtforms import TextField

import pandas as pd
import pickle
from sklearn.externals import joblib
import numpy as np

from bs4 import BeautifulSoup
import plyer
import time,datetime



app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def hel():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, addr TEXT, city TEXT, pin TEXT, bg TEXT,email TEXT UNIQUE, pass TEXT)')
    print( "Table created successfully")
    conn.close()
    if session.get('username')==True:
        messages = session['username']

    else:
        messages = ""
    user = {'username': messages}
    return redirect(url_for('index',user=user))


@app.route('/reg')
def add():
    return render_template('register.html')


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   msg = ""
   #con = None
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         bg = request.form['bg']
         email = request.form['email']
         passs = request.form['pass']

         with sqlite3.connect("database.db") as con:
             cur = con.cursor()
             cur.execute("INSERT INTO users (name,addr,city,pin,bg,email,pass) VALUES (?,?,?,?,?,?,?)",(nm,addr,city,pin,bg,email,passs) )
             con.commit()
             msg = "Record successfully added"



      except:
             con.rollback()
             msg = "error in insert operation"

      finally:
             flash('done')
             return redirect(url_for('index'))
             con.close()





@app.route('/index',methods = ['POST','GET'])
def index():



    if request.method == 'POST':
        if session.get('username') is not None:
            messages = session['username']

        else:
            messages = ""
        user = {'username': messages}
        print(messages)
        val = request.form['search']
        print(val)
        type = request.form['type']
        print(type)
        if type=='blood':
            con = sqlite3.connect('database.db')
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("select * from users where bg=?",(val,))
            search = cur.fetchall();
            cur.execute("select * from users ")

            rows = cur.fetchall();


            return render_template('index.html', title='Home', user=user,rows=rows,search=search)

        if type=='donorname':
            con = sqlite3.connect('database.db')
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("select * from users where name=?",(val,))
            search = cur.fetchall();
            cur.execute("select * from users ")

            rows = cur.fetchall();


            return render_template('index.html', title='Home', user=user,rows=rows,search=search)



    if session.get('username') is not None:
        messages = session['username']

    else:
        messages = ""
    user = {'username': messages}
    print(messages)
    if request.method=='GET':
        con = sqlite3.connect('database.db')
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("select * from users ")

        rows = cur.fetchall();
        return render_template('index.html', title='Home', user=user, rows=rows)

    #messages = request.args['user']




@app.route('/list')
def list():
   con = sqlite3.connect('database.db')
   con.row_factory = sqlite3.Row

   cur = con.cursor()
   cur.execute("select * from users")

   rows = cur.fetchall();
   print(rows)
   return render_template("list.html",rows = rows)

@app.route('/drop')
def dr():
        con = sqlite3.connect('database.db')
        con.execute("DROP TABLE request")
        return "dropped successfully"

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('/login.html')
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['pass']
        if email == 'admin@bloodbank.com' and password == 'admin':
            a = 'yes'
            session['username'] = email
            #session['logged_in'] = True
            session['admin'] = True
            return redirect(url_for('index'))
        #print((password,email))
        con = sqlite3.connect('database.db')
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("select email,pass from users where email=?",(email,))
        rows = cur.fetchall();
        for row in rows:
            print(row['email'],row['pass'])
            a = row['email']
            session['username'] = a
            session['logged_in'] = True
            print(a)
            u = {'username': a}
            p = row['pass']
            print(p)

            if email == a and password == p:
                return redirect(url_for('index'))
            else:
                return render_template('/login.html')
        return render_template('/login.html')
    else:
        return render_template('/')


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session.pop('logged_in',None)
   try:
       session.pop('admin',None)
   except KeyError as e:
       print("I got a KeyError - reason " +str(e))


   return redirect(url_for('login'))


@app.route('/dashboard',methods =['POST','GET'])
def dashboard():
   totalblood=0
   #otype=0
   #qt=0
   
   con = sqlite3.connect('database.db')
   con.row_factory = sqlite3.Row

   cur = con.cursor()
   cur.execute("select * from blood")
   
   #if request.method == 'POST':
    #    otype = request.form['blood_group']
   #     qt = request.form['qt']
    
  # btypes=[otype]

   rows = cur.fetchall();
   for row in rows:
       totalblood  += int(row['qty'])
   
   cur.execute("select * from users")
   users = cur.fetchall();

   Apositive=0
   #for x in btypes:
    #   if x=='A+':
     #      Apositive=Apositive-int(qt)
       #totalblood=totalblood-int(qt)
  # with sqlite3.connect("database.db") as con:
   #    cur = con.cursor()
    #   a=types[0]
     #  cur.execute("UPDATE blood SET type = ?, donorname = ?, donorsex = ?, qty = ?,dweight = ?, donoremail = ?,phone = ? WHERE id = ?",(type,donorname,donorsex,qty,) )
      # con.commit()


   Opositive=0
   #for x in btypes:
    #   if x=='O+':
     #      Opositive=Opositive-int(qt)
       #totalblood=totalblood-int(qt)
   
   
   Bpositive=0
   #for x in btypes:
    #   if x=='B+':
     #      Bpositive=Bpositive-int(qt)
       #totalblood=totalblood-int(qt)

   Anegative=0
   #for x in btypes:
    #   if x=='A-':
     #      Anegative=Anegative-int(qt)
       #totalblood=totalblood-int(qt)

   Onegative=0
   #for x in btypes:
       #if x=='O-':
      #     Onegative=Onegative-int(qt)
       #totalblood=totalblood-int(qt)


   Bnegative=0
   #for x in btypes:
    #   if x=='B-':
     #      Bnegative=Bnegative-int(qt)
       #totalblood=totalblood-int(qt)

   ABpositive=0
   #for x in btypes:
    #   if x=='AB+':
     #      ABpositive=ABpositive-int(qt)
       #totalblood=totalblood-int(qt)


   ABnegative = 0
   




   cur.execute("select * from blood where type=?",('A+',))
   type = cur.fetchall();
   for a in type:
       Apositive += int(a['qty'])
       


   cur.execute("select * from blood where type=?",('A-',))
   type = cur.fetchall();
   for a in type:
       Anegative += int(a['qty'])

   

   cur.execute("select * from blood where type=?",('O+',))
   type = cur.fetchall();
   for a in type:
       Opositive += int(a['qty'])
       
    
    
   
   

           
    

   cur.execute("select * from blood where type=?",('O-',))
   type = cur.fetchall();
   for a in type:
       Onegative += int(a['qty'])

   cur.execute("select * from blood where type=?",('B+',))
   type = cur.fetchall();
   for a in type:
       Bpositive += int(a['qty'])


   cur.execute("select * from blood where type=?",('B-',))
   type = cur.fetchall();
   for a in type:
       Bnegative += int(a['qty'])



   cur.execute("select * from blood where type=?",('AB+',))
   type = cur.fetchall();
   for a in type:
       ABpositive += int(a['qty'])


   cur.execute("select * from blood where type=?",('AB-',))
   type = cur.fetchall();
   for a in type:
       ABnegative += int(a['qty'])

    

   
   bloodtypestotal = {'apos': Apositive,'aneg':Anegative,'opos':Opositive,'oneg':Onegative,'bpos':Bpositive,'bneg':Bnegative,'abpos':ABpositive,'abneg':ABnegative}






   return render_template("requestdonors.html",rows = rows,totalblood = totalblood,users=users,bloodtypestotal=bloodtypestotal)


@app.route('/bloodbank')
def bl():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS blood (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, donorname TEXT, donorsex TEXT, qty TEXT, dweight TEXT, donoremail TEXT, phone TEXT)')
    print( "Table created successfully")
    conn.close()
    return render_template('/adddonor.html')


@app.route('/addb',methods =['POST','GET'])
def addb():
    msg = ""
    if request.method == 'POST':
        try:
           type = request.form['blood_group']
           donorname = request.form['donorname']
           donorsex = request.form['gender']
           qty = request.form['qty']
           dweight = request.form['dweight']
           email = request.form['email']
           phone = request.form['phone']



           with sqlite3.connect("database.db") as con:
              cur = con.cursor()
              cur.execute("INSERT INTO blood (type,donorname,donorsex,qty,dweight,donoremail,phone) VALUES (?,?,?,?,?,?,?)",(type,donorname,donorsex,qty,dweight,email,phone) )
              con.commit()
              msg = "Record successfully added"
        except:
           con.rollback()
           msg = "error in insert operation"

        finally:
            flash("added new entry!")
            return redirect(url_for('dashboard'))
            con.close()

    else:
        return render_template("rest.html",msg=msg)

@app.route("/editdonor/<id>", methods=('GET', 'POST'))
def editdonor(id):
    msg =""
    if request.method == 'GET':
        con = sqlite3.connect('database.db')
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("select * from blood where id=?",(id,))
        rows = cur.fetchall();
        return render_template("editdonor.html",rows = rows)
    if request.method == 'POST':
        try:
           type = request.form['blood_group']
           donorname = request.form['donorname']
           donorsex = request.form['gender']
           qty = request.form['qty']
           dweight = request.form['dweight']
           email = request.form['email']
           phone = request.form['phone']



           with sqlite3.connect("database.db") as con:
              cur = con.cursor()
              cur.execute("UPDATE blood SET type = ?, donorname = ?, donorsex = ?, qty = ?,dweight = ?, donoremail = ?,phone = ? WHERE id = ?",(type,donorname,donorsex,qty,dweight,email,phone,id) )
              con.commit()
              msg = "Record successfully updated"
        except:
           con.rollback()
           msg = "error in insert operation"

        finally:
            flash('saved successfully')
            return redirect(url_for('dashboard'))
            con.close()

@app.route("/myprofile/<email>", methods=('GET', 'POST'))
def myprofile(email):
    msg =""
    if request.method == 'GET':


        con = sqlite3.connect('database.db')
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("select * from users where email=?",(email,))
        rows = cur.fetchall();
        return render_template("myprofile.html",rows = rows)
    if request.method == 'POST':
        try:
           name = request.form['name']
           addr = request.form['addr']
           city = request.form['city']
           pin = request.form['pin']
           bg = request.form['bg']
           emailid = request.form['email']

           print(name,addr)



           with sqlite3.connect("database.db") as con:
              cur = con.cursor()
              cur.execute("UPDATE users SET name = ?, addr = ?, city = ?, pin = ?,bg = ?, email = ? WHERE email = ?",(name,addr,city,pin,bg,emailid,email) )
              con.commit()
              msg = "Record successfully updated"
        except:
           con.rollback()
           msg = "error in insert operation"

        finally:
           flash('profile saved')
           return redirect(url_for('index'))
           con.close()



@app.route('/contactforblood/<emailid>', methods=('GET', 'POST'))
def contactforblood(emailid):
    if request.method == 'GET':
        conn = sqlite3.connect('database.db')
        print("Opened database successfully")
        conn.execute('CREATE TABLE IF NOT EXISTS request (id INTEGER PRIMARY KEY AUTOINCREMENT, toemail TEXT, formemail TEXT, toname TEXT, toaddr TEXT)')
        print( "Table created successfully")
        fromemail = session['username']
        name = request.form['nm']
        addr = request.form['add']

        print(fromemail,emailid)
        conn.execute("INSERT INTO request (toemail,formemail,toname,toaddr) VALUES (?,?,?,?)",(emailid,fromemail,name,addr) )
        conn.commit()
        conn.close()
        flash('request sent')
        return redirect(url_for('index'))
    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        print("Opened database successfully")
        conn.execute('CREATE TABLE IF NOT EXISTS request (id INTEGER PRIMARY KEY AUTOINCREMENT, toemail TEXT, formemail TEXT, toname TEXT, toaddr TEXT)')
        print( "Table created successfully")
        fromemail = session['username']
        name = request.form['nm']
        addr = request.form['add']

        print(fromemail,emailid)
        conn.execute("INSERT INTO request (toemail,formemail,toname,toaddr) VALUES (?,?,?,?)",(emailid,fromemail,name,addr) )
        conn.commit()
        conn.close()
        flash('request sent')
        return redirect(url_for('index'))



@app.route('/notifications',methods=('GET','POST'))
def notifications():
    if request.method == 'GET':


            conn = sqlite3.connect('database.db')
            print("Opened database successfully")
            conn.row_factory = sqlite3.Row

            cur = conn.cursor()
            cor = conn.cursor()
            cur.execute('select * from request where toemail=?',(session['username'],))
            cor.execute('select * from request where toemail=?',(session['username'],))
            row = cor.fetchone();
            rows = cur.fetchall();
            if row==None:
                return render_template('notifications.html')
            else:
                return render_template('notifications.html',rows=rows)


@app.route('/deleteuser/<useremail>',methods=('GET', 'POST'))
def deleteuser(useremail):
    if request.method == 'GET':
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('delete from users Where email=?',(useremail,))
        flash('deleted user:'+useremail)
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))


@app.route('/deletebloodentry/<id>',methods=('GET', 'POST'))
def deletebloodentry(id):
    if request.method == 'GET':
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('delete from blood Where id=?',(id,))
        flash('deleted entry:'+id)
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

@app.route('/deleteme/<useremail>',methods=('GET', 'POST'))
def deleteme(useremail):
    if request.method == 'GET':
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('delete from users Where email=?',(useremail,))
        flash('deleted user:'+useremail)
        conn.commit()
        conn.close()
        session.pop('username', None)
        session.pop('logged_in',None)
        return redirect(url_for('index'))

@app.route('/deletenoti/<id>',methods=('GET', 'POST'))
def deletenoti(id):
    if request.method == 'GET':
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('delete from request Where id=?',(id,))
        flash('deleted notification:'+id)
        conn.commit()
        conn.close()
        return redirect(url_for('notifications'))


@app.route("/cpd")
def cpd():
    return render_template('cpd.html',title='cpd')

model = pickle.load(open('model.pkl', 'rb'))


@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('cpd.html', prediction_text='   your Corona Prone Score is  {}/10'.format(output))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)



@app.route("/liveupdate")
def liveupdate():
    url= "https://www.worldometers.info/coronavirus/country/india/"
    req=requests.get(url)
    bsobj=BeautifulSoup(req.text,"html.parser")
    
    data=bsobj.find_all("div",class_="maincounter-number")

    total=data[0].text.strip()
    totald=data[1].text.strip()
    recovered=data[2].text.strip()

    urluk="https://coronaclusters.in/uttarakhand"
    requk=requests.get(urluk)
    bsobjuk=BeautifulSoup(requk.content,'html.parser')
    datauk=bsobjuk.find_all("div",class_="card-body")
    totaluk=datauk[0].text.strip()
    totalduk=datauk[1].text.strip()
    totalruk=datauk[2].text.strip()
    totalauk=datauk[3].text.strip()
    
    


    
    return render_template('liveupdate.html',total=total,totald=totald,recovered=recovered,totalruk=totalruk,totaluk=totaluk,totalduk=totalduk,totalauk=totalauk)



@app.route('/updateplasma')
def updateplasma():
        return render_template('/updateplasma.html')


@app.route('/addc',methods =['POST','GET'])
def addc():
    msg = ""
    

    if request.method == 'POST':
        try:
           type = request.form['blood_group']
           qt = request.form['qt']
           
           qty=0
           qty-=int(qt)
           donorname = 'Abc'
           donorsex = 'female'
           dweight = 80
           email = 'abc@gmail.com'
           phone = 9410326265
    

           with sqlite3.connect("database.db") as con:
              cur = con.cursor()
              cur.execute("INSERT INTO blood (type,donorname,donorsex,qty,dweight,donoremail,phone) VALUES (?,?,?,?,?,?,?)",(type,donorname,donorsex,qty,dweight,email,phone) )
              con.commit()
              msg = "Record successfully added"
        except:
           con.rollback()
           msg = "error in insert operation"

        finally:
            flash("updated entry!")
            return redirect(url_for('dashboard'))
            con.close()

    else:
        return render_template("rest.html",msg=msg)




    
                    
if __name__ == '__main__':
    app.run(debug=True)
