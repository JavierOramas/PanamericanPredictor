import temp
# import prediction
from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)
@app.route('/')
def init():
    return render_template('initial.html')
@app.route('/index', methods = ['POST'])
def index():
    year = request.form['year']
    medallas = temp.a.get_list(year)
    return render_template('index.html',array = medallas)
if __name__ == '__main__':
    app.run()