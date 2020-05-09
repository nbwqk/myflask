from flask import Flask,render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

app=Flask(__name__)
app.config['SECRET_KEY']='hard to guess string'
manager=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)

class NameForm(Form):
    name=StringField('What is your name?',validators=[Required()])
    submit=SubmitField('Submit')

@app.route('/')
def index():
    return '<h1>hello,world!</h1>'

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
    name=None
    form=NameForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
    return render_template('about.html',form=form,name=name)

if __name__ == '__main__':
    manager.run()