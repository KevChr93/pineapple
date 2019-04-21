from project import db
from flask_login import UserMixin



from project import login_manager
 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


 

class Plans(db.Model):
    __tablename__ = 'Subscription Plans'

    id = db.Column(db.Integer, primary_key=True)
    plan_name= db.Column(db.String,nullable=False)
    price= db.Column(db.String)
    no_of_users =  db.Column(db.Integer) 
    storage = db.Column(db.Integer) 
    support = db.Column(db.String)
 
  
    def __init__(self,planName,Pprice,users, store,supp):
        self.plan_name = planName
        self.price = Pprice
        self.no_of_users = users
        self.storage=store
        self.support=supp
         
   
 


class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)

    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default='user')
    image_file = db.Column(db.String(20), nullable=False, default='user.png')

    sub_plan = db.Column(db.String(20),default='NONE')


    def __init__(self,FirstName,LastName, UserName, email, password, role):
        self.username = UserName
        self.firstname = FirstName
        self.lastname = LastName
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return '<User {0}>'.format(self.name)
 
 
    def toDict(self):
        return {
            'id': self.id,
            'first_name': self.firstname,
            'last_name': self.lastname,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'Plan':self.sub_plan
        }

 