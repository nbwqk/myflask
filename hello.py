from flask import Flask,render_template,session,url_for,redirect,flash
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
import os

basedir=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
manager=Manager(app)
app.config['SECRET_KEY']='hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db=SQLAlchemy(app)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)



class Role(db.Model):
    __tablename__ = 'roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    users=db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


bootstrap=Bootstrap(app)
moment=Moment(app)

def make_shell_context(): # 把对象添加到导入列表中，我们要为 shell 命令注册一个 make_context 回调函数
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command("shell",Shell(make_context=make_shell_context()))


class NameForm(FlaskForm):
    name=StringField('What is your name?',validators=[DataRequired()])
    submit=SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            session['know']=False
        else:
            session['know']=True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),know=session.get('know',False))

@app.route('/user/<name>')
def user(name):
    return '<h1>hello,%s!</h1>' % name

@app.route('/work/<name>')
def work(name):
    return render_template('work.html',name=name,current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route('/about',methods=['GET','POST'])
def about():
    form=NameForm()
    if form.validate_on_submit():
        old_name=session.get('name')
        if old_name is not None and old_name!=form.name.data:
            flash('Looks like you have changed your name!')
        session['name']=form.name.data
        return redirect(url_for('about'))
    return render_template('about.html',form=form,name=session.get('name'))

if __name__ == '__main__':
    manager.run()