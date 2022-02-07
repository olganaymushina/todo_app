import sqlite3 
from flask import Flask, render_template, request, redirect
from forms import NewTask, DelTask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/all-tasks')
def tasks():
    con = sqlite3.connect("todo.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT tasks.completed, tasks.id, tasks.name, roommates.name AS roommate_name, tasks.date FROM tasks LEFT JOIN roommates ON roommates.user_id=tasks.user_id")
    rows = cur.fetchall()
    con.commit()
    con.close
    return render_template("all_tasks.html", rows=rows)

@app.route('/add-task')
def add_task():
    new_task = NewTask(csrf_enabled = False)
    return render_template("add_new_task.html", template_form = new_task)

@app.route('/added_task', methods = ["GET", "POST"])
def task():
    new_task = NewTask(csrf_enabled = False)
    if request.method == "POST":
        con = sqlite3.connect("todo.db")
        name = request.form['name']
        user_name = request.form['user_id']
        due = request.form['date']
        con.execute("INSERT INTO tasks (name, user_id, date) VALUES (?,?,?)",(name, user_name, due))
        con.commit()
        con.close
    return render_template('message.html', template_form = new_task)

@app.route('/complete_task', methods = ["GET", "POST"])
def complete_task():
    if request.method == "POST":
        con = sqlite3.connect("todo.db")
        task_id = request.form["task_id"]
        completed_value = request.form["completed_value"]
        con.execute("UPDATE tasks SET completed = ? WHERE id = ? ", (completed_value, task_id))
        con.commit()
        con.close
    return redirect('/all-tasks')

@app.route('/delete-task')
def del_task():
    del_task = DelTask(csrf_enabled = False)
    return render_template("del_task.html", template_form = del_task)

@app.route('/deleted', methods = ["GET", "POST"])
def delete():
    del_task = DelTask(csrf_enabled = False)
    if request.method == "POST":
        con = sqlite3.connect("todo.db")
        name = request.form['name']
        cur = con.cursor()
        cur.execute("DELETE FROM tasks WHERE name = ? ", [name])
        con.commit()
        con.close
    return render_template("message2.html", template_form = del_task)


# cursor.execute('INSERT INTO images VALUES(?)', (img,))
# Without the comma, (img) is just a grouped expression, not a tuple, 
# and thus the img string is treated as the input sequence. If that string is 74 characters long, 
# then Python sees that as 74 separate bind values, each one character long.

# >>> len(img)
# 74
# >>> len((img,))
# 1
                # OR

                
# You need to use a list as the second argument to conn.execute(...)!

# Since you only gave the function a string, the string is being interpreted as list of characters.

# In our example from above, you just need to wrap name in square brackets to read [name]: