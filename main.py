from flask import Flask, request, render_template, session, redirect
from flask_session import Session
from random import randint

app = Flask(__name__)
# configure my session stuff
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

# TODOS = []

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/roll")
def roll():
  dice_roll = [] #a list to hold all of our dice we will roll
  n = request.args.get("n", 2) # 2 is the default value if no n
  n = int(n) # make n an integer
  for i in range(n): # loop n number of times
    die = randint(9856,9861) # get a random #s of emoji codes
    dice_roll.append(chr(die)) # add the dice emoji to the roll list
  # print(dice_roll)
  return render_template("roll.html", number=n, dice_list=dice_roll)

@app.route("/todo", methods=["GET", "POST"])
def todo():
  # check if there is NOT a session for TODOS already
  if not session.get("TODOS"):
    session["TODOS"] = []
    
  # check what request method was used
  if request.method == "GET": # the user used a GET request
    # just show the todo list page
    return render_template("todo.html", todos=session["TODOS"])
  else: # they used the POST method (aka filled out the form)
    # grab all the data from the form
    task = request.form.get("task")
    priority = request.form.get("priority")
    # take the form data and build a dict
    task_dict = {
      "name": task,
      "priority": priority
    }

    # skip over the validation
    # add the dict to the TODOS list
    session.get("TODOS").append(task_dict)
    #now show the todos list page
    return render_template("todo.html", todos=session.get("TODOS"))
    

@app.route("/add")
def add():
  return render_template("add.html")

  
# we replaced this route with our new version of the /todo route
# left in the code for reference only 👇
@app.route("/add_task", methods=["POST"]) # only allows the POST request 
def add_task():
  # process the form
  # grab the new task from the form data
  new_task = request.form.get("task")
  priority = request.form.get("priority", "low")
  if new_task: # if there is a new task
    if new_task not in session.get("TODOS"): # check to see if it is a duplicate
      session.get("TODOS").append(new_task)
    return render_template("todo.html", todos=session.get("TODOS"), priority=priority)
  else: #no new task
    return "<h1>ERROR - No task given</h1><a href='/add'>Try again</a>"

    
if __name__ == "__main__":
  app.run("0.0.0.0", debug=True)