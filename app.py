from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# render_template is used to generate output from a template file based on the 
# Jinja2 engine that is found in the application's templates folder

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #relative path
db = SQLAlchemy(app) #initializing database

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow) 
        # .utcnow -  Greenwich Mean Time time zone 
        # .now - the current time in your location
    
    def __repr__(self): 
        return '<Task %r>' % self.id


@app.route('/', methods = ['POST','GET']) #creating index route; GET - default; 
def index():
    if request.method == 'POST':
        task_content = request.form['content']  #adding the task in here
        new_task = Todo(content = task_content) #passing the content to the class "to_do"
        try:
            db.session.add(new_task) #adding to the database
            db.session.commit() #commiting to the database
            return redirect('/') #redirecting back to the index
        except:
            return "Oops! Error while adding your task."
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #to display all the current tasks in the table.
        #This line will be looking at all of the database contents in the order of their 
        #creation, i.e., newest to oldest and will return all of them
        return render_template('index.html',tasks = tasks) #passing 'tasks' to template

@app.route('/delete/<int:id>') #unique element of task is the 'id'; 'content' can't be unique and hence can't be used.
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) #if not present, 404!
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Oops! Error while deleting your task." 
    
@app.route('/update/<int:id>', methods = ['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Oops! Error while updating your task." 
    else:
        return render_template('update.html',task = task)
    
@app.route('/show')
def show_site():
    return render_template('about_me.html')    
    

if __name__ == "__main__":
    app.run(debug = True) #(debug=True) if any errors, it pops up on web page.