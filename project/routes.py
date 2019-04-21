from flask import Flask,request, render_template, flash, url_for, redirect
import json
from project.models import User
from project import app,host,db
from project.forms import RegForm,LoginForm,subForm
from project import bcrypt
from flask_login import login_user, current_user,logout_user,login_required




@app.before_first_request
def setup():

   db.create_all()
   db.session.commit()

   User.query.filter(User.username == "Admin").delete()
   Admin_pw = bcrypt.generate_password_hash("password").decode('utf-8')
   admin = User("admin","admin", "Admin","admin@admin.com",Admin_pw, "Admin")
   admin.id=1
   db.session.add(admin)
   db.session.commit()
   logout_user()


 

                  



@app.route("/")
def home():
   if current_user.is_authenticated:
      return render_template("index.html",host=host)
   else:
      return render_template("index.html",host=host)


@app.route("/plans")
def plans():
   return render_template("subs.html",host=host)


@app.route("/login", methods=['GET', 'POST'])
def login():
   if current_user.is_authenticated:
         return redirect(url_for('home'))
   else:
      form = LoginForm()
      if form.validate_on_submit():
         user = User.query.filter_by(email = form.email.data).first()
         if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect (next_page) if next_page else redirect(url_for('home'))
         else:     
            flash('Login Unsuccessful. Please check username and password', 'danger')
      return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
   if current_user.is_authenticated:
      return redirect(url_for('home'))
   else:
      form = RegForm()
      if form.validate_on_submit():
         hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         u = User( form.firstname.data,form.lastname.data,form.username.data, form.email.data,hashed_pw, "user")
        # save p to the dtabase
         db.session.add(u)
         db.session.commit()
        # return p's record in the response
         msgstr = 'Account created for '+form.username.data+'!'
        #print(p.username)
         flash(msgstr, 'success')
         return redirect(url_for('login'))
   return render_template('reg.html', title='Register', form=form)


@app.route("/logout")
def logout():
   logout_user()
   return redirect(url_for('home'))


@app.route("/analytics")
@login_required
def analytics():

   if current_user.role =="Admin":
      records = User.query.all()
      image_file = url_for('static', filename='propics/' + current_user.image_file)

      return render_template('analytics.html', Users=records,title='analytics',image_file=image_file)
   else:
      return redirect(url_for('home'))

   





@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  form=subForm()
  if request.method=='POST':
      current_user.sub_plan=form.plan.data
      db.session.commit()
  image_file = url_for('static', filename='propics/' + current_user.image_file)
  return render_template('account.html',form=form, title='Account',image_file=image_file)