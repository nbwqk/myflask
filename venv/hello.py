from flask import Flask,render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
app=Flask(__name__)
manager=Manager(app)
bootstrap=Bootstrap(app)

@app.route('/')
def index():
    return '<h1>hello,world!</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>hello,%s!</h1>' % name

@app.route('/work/<name>')
def work(name):
    return render_template('work.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
    manager.run()