from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm,LoginFOrm,Posts,Coments,LoginFOrm1
from flask_login import UserMixin,LoginManager,login_user,logout_user,login_required,current_user
app = Flask(__name__)
app.config['SECRET_KEY']='1234'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'
db= SQLAlchemy(app)
migrate=Migrate(app,db)
login = LoginManager(app)
login.login_view='loginFOrm'

class Coment(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False, unique=True)
    create_att = db.Column(db.DateTime, default=datetime.utcnow)
    user=db.Column(db.Integer,db.ForeignKey('user.id'))
    post = db.Column(db.Integer, db.ForeignKey('post.id'))


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1=db.Column (db.Integer, db.ForeignKey("user.id"))
    user2 = db.Column (db. Integer, db.ForeignKey('user.id'))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    create_att = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat = db.Column(db.Integer, db.ForeignKey('chat.id'))

class User(db.Model,UserMixin):
    id= db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.Integer, nullable=False)
    email = db.Column(db.Integer,nullable=False,unique=True)
    create_att=db.Column(db.DateTime, default=datetime.utcnow)

    def hash_password(self,password):
        self.password= generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

@login.user_loader
def user_loader(id):
    return User.query.get(id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    image=db.Column(db.String, nullable=False)
    create_att = db.Column(db.DateTime, default=datetime.utcnow)
    user=db.Column(db.Integer,db.ForeignKey('user.id'))





@app.route('/')
def main():
    forms= Post.query.all()

    return render_template('home.html',forms=forms)

@app.route('/my_user',methods=['GET','POST'])
def my_user():
    if request.method=="POST":
        my_user=request.form["name"]
        my_password=request.form["password"]
        my_email=request.form["email"]
        name=User.query.get(current_user.id)
        name.name=my_user
        name.hash_password(my_password)
        name.email = my_email
        db.session.commit()
        return render_template("my_user.html",curent_user=current_user,user=my_user)
    return render_template('my_user.html',curent_user=current_user)


@app.route('/send_message/<int:id>')
def start_chat(id):
    chat = Chat.query.filter_by(user1=current_user.id, user2=id).first()
    chat1 = Chat.query.filter_by(user2=current_user.id, user1=id).first()
    if chat is None and chat1 is None:
        c = Chat(user1=current_user.id, user2=id)
        db.session.add(c)
        db.session.commit()
        return redirect(f'/chat/{c.id}')
    elif chat is not None and chat1 is None:
        return redirect(f'/chat/{chat.id}')
    elif chat is None and chat1 is not None:
        return redirect(f'/chat/{chat1.id}')

@app.route('/chat/<int:id>',methods=['GET','POST'])
def chat(id):
    text= Chat.query.get(id)
    chatik=Message.query.filter_by(chat=id)
    user=[]
    for i in chatik:
        name=User.query.get(i.user)
        user.append([name,i])
    form=Coments()
    if form.validate_on_submit():
        text_chat=form.text.data
        message=Message(text=text_chat,user=current_user.id,chat=id)
        db.session.add(message)
        db.session.commit()
        return redirect(f'/chat/{id}')
    return render_template('chat.html',text=text,chat=user,form=form)




@app.route('/RegistrationForm',methods=['GET','POST'])
def registration():
    form=RegistrationForm()
    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        password=form.password.data
        user=User(name=username,email=email)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/LoginFOrm')
    return render_template('RegistrationForm.html',form=form)

@app.route('/LoginFOrm',methods=['GET','POST'])
def loginFOrm():
    form=LoginFOrm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        check=form.remember_me.data
        username1=User.query.filter_by(name=username).first()
        if username1 is None or not username1.check_password(password):
            return redirect ('/LoginFOrm')
        login_user (username1,remember=check)
        return redirect('/')
    return render_template('LoginFOrm.html',form=form)

@app.route('/logout',methods=['GET','POST'])
def logout():
    logout_user()
    return redirect('/LoginFOrm')



@app.route('/create_post',methods=['GET','POST'])
@login_required
def create_post():
    form=Posts()
    if form.validate_on_submit():
        text = form.text.data
        post = Post(text=text,user=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    return render_template('create_post.html',form=form)

@app.route('/profile')
@login_required
def profile():

    return render_template('profile.html',user=current_user)

@app.route('/post/<int:id>',methods=['GET','POST'])
def post(id):
    p=Post.query.get(id)
    form=Coments()
    comentairs=Coment.query.filter_by(post=id)
    if form.validate_on_submit():
        text = form.text.data
        coment = Coment(text=text,user = current_user.id,post=id)
        db.session.add(coment)
        db.session.commit()
        return redirect(f'/post/{id}')
    return render_template('post.html',post=p,form=form,comentairs=comentairs)


@app.route('/get_user/<int:id>')
def post_user(id):
    p=User.query.get(id)

    return render_template('user.html',p=p)

@app.route('/css')
def css():
    return render_template('baze.html',)




#название сата MovieVibe большая буква м логотип