#now we run our application

from flask import Flask, render_template, request, redirect, url_for
import Recommendations as rc
from flask_sqlalchemy import SQLAlchemy
#import logging

app = Flask(__name__,template_folder="templates")

#logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# /// = relative path, //// = absolute path
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

#get_list = []
final_list = []
user = 671

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))


@app.route("/")
def home():
    user_list = Movie.query.all()
    rc_list = final_list
    #app.logger.info('Info level log')
    #app.logger.warning('Warning level log')
    return render_template("base.html", user_list = user_list, rc_list = rc_list)


@app.route("/add", methods=["POST"])
def add():
    global get_list
    title = request.form.get("title")
    
    new_movie = Movie(title=title)
    db.session.add(new_movie)
    db.session.commit()
    
    #get_list.append(title)
    return redirect(url_for("home")) 


@app.route("/delete/<int:i>")
def delete(i):
    movie = Movie.query.filter_by(id=i).first()
    db.session.delete(movie)
    db.session.commit()
    #get_list.pop(i)
    return redirect(url_for("home"))

@app.route("/recommendation")#, methods=["POST"])
def recommendation():
    global final_list
    #global get_list
    get_list = []
    movies = Movie.query.all()
    for i in movies:
        get_list.append(i.title)
        
    try:
        final = rc.get_top_recommendations(10, get_list, user)
        final_list = final.tolist()
        #print(final_list)
        return redirect(url_for("home"))
        #return render_template('result.html', variety=final_list)
    except Exception as e:
        print(e)
        return redirect(url_for("recommendation"))
        

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
