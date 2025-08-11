from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_restful import Resource, Api, reqparse
import requests
import json

from azuresqlconnector import *

# Create the Flask app
app = Flask(__name__)


@app.route('/searchrecipes')
def recipes():
    return render_template('search_recipes.html')

@app.route('/search_recipe_api', methods=['POST'])
def api_search():
    q_string = "https://api.spoonacular.com/recipes/complexSearch?apiKey=b818cf7fb2d74a918fe080c4ff1799ab&instructionsRequired=True&addRecipeInformation=True&fillIngredients=True&query="+str(request.form['query'])

#    for i in data:
#        q_string=q_string+str("&"+i+"="+str(data[i]))

    r = requests.get(q_string).json()

    recipes=[]
    for i in r["results"]:
        name = i["title"]
        image=i['image']
        id = i["id"]
        summary = i["summary"]

        ingredients = []
        for j in i["extendedIngredients"]:
            ingredients.append([j["name"],j["original"]])

        instructions = []
        for j in i["analyzedInstructions"][0]["steps"]:
            instructions.append(j["step"])

        diets=i['diets']


        recipes.append({"RecipeName":name,"image":image,"ID":id,"Summary":summary,"diets":diets,"Ingredients":ingredients,"Instructions":instructions})

    #fix to keep data and render page
    return render_template('search_recipes.html', recipes=recipes)
    
@app.route('/save_recipe', methods=['GET'])
def saverecipe():
    parser = reqparse.RequestParser()
    parser.add_argument('recipe_id', type=str, location='args')
    arguments = parser.parse_args()
    id = arguments['recipe_id']

    q_string = "https://api.spoonacular.com/recipes/"+str(id)+"/information?apiKey=b818cf7fb2d74a918fe080c4ff1799ab&instructionsRequired=True&addRecipeInformation=True&number=1&fillIngredients=True"
    r = requests.get(q_string).json()

    name=r['title']
    name = name.replace("'", "''")
    image=r['image']
    image=image.replace("'", "''")
    summary=r['summary']
    summary=summary.replace("'", "''")
    summary = summary.split("<")
    summary_out = ""
    for i in summary:
        splitted = i.split(">")
        if len(splitted) <2:
            summary_out = summary_out+splitted[0]
        else:
            summary_out = summary_out+splitted[1]
    diets=''
    for i in r['diets']:
        diets = diets+(str(i)+', ')
    instructions=''
    increment=1
    for i in r['analyzedInstructions'][0]['steps']:
        instructions=instructions+'Step '+str(increment)+': '+i['step']+'\n'
        increment+=1
    instructions=instructions.replace("'", "''")
    ingredients=''
    for i in r['extendedIngredients']:
        ingredients=ingredients+i['original']+'\n'
    ingredients=ingredients.replace("'", "''")
    # Initialize SQL connection
    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()

    sql_query = f"""
        INSERT INTO FinalProject.Recipe
        (Recipe_ID, Recipe_Name, User_ID, Ingredients, Summary, Instructions, Recipe_image, Diets)
        VALUES ('{id}', '{name}', '{1}', '{ingredients}', '{summary_out}', '{instructions}', '{image}', '{diets}')
        """
    
    # Execute the SQL Query
    cursor.execute(sql_query)

    conn.commit()

    # Close the cursor
    cursor.close()

    return redirect(url_for('recipes'))

@app.route('/remove_recipe', methods=['GET'])
def removerecipe():
    parser = reqparse.RequestParser()
    parser.add_argument('recipe_id', type=str, location='args')
    arguments = parser.parse_args()
    recipe_id = arguments['recipe_id']
    user_id=1

    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()

    sql_query = f"""
        DELETE FROM FinalProject.Recipe WHERE
        Recipe_ID='{recipe_id}' AND User_ID='{user_id}';
        """
    
    # Execute the SQL Query
    cursor.execute(sql_query)

    conn.commit()

    # Close the cursor
    cursor.close()

    return redirect(url_for('cookbook'))


@app.route('/login')
def loginhome():
    return render_template('login.html')

@app.route('/adduser')
def addUser():
    return render_template('add_user.html')

@app.route('/updateuser')
def updateUser():
    return render_template('update_user.html')

@app.route('/')
def startpage():
    return render_template('homepage.html')

@app.route('/landing')
def landing():
    return render_template('landing_page.html')

@app.route('/savedrecipes')
def cookbook():
    id=1

    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()

    sql_query = f"""
        SELECT * FROM FinalProject.Recipe WHERE User_ID = '{id}';
        """

    cursor.execute(sql_query)

    recipes = cursor.fetchall()

    cursor.close()
    return render_template('view_recipes.html', recipes=recipes)

# This function handles adding a user to the database
@app.route('/register', methods=['POST'])
def add_user():
    user = str(request.form['username'])
    secret = str(request.form['password'])
    user_id = str(hash(user))

    # Initialize SQL connection
    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()

    sql_query = f"""
        INSERT INTO FinalProject.Customer
        (User_ID, Username, Pass)
        VALUES (
        '{user_id}',
        '{user}',
        '{secret}'
        );
        """
    
    cursor.execute(sql_query)

    conn.commit()

    cursor.close()

    # Redirect
    return render_template("login.html")

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login_user', methods=['POST'])
def login_attempt():
    if request.method == 'POST':
        # Extract form data
        username = str(request.form['username'])
        password = str(request.form['password'])

        try:
            # Establish Azure SQL connection
            conn = SQLConnection()
            conn = conn.getConnection()
            cursor = conn.cursor()

            # Query for Azure SQL for user credentials
            sql_login = f"""
            SELECT *
            FROM FinalProject.Customer
            WHERE Username = '{username}' AND Pass = '{password}'
            """

            cursor.execute(sql_login)
            user_id = cursor.fetchone()

            if user_id['password'] == password:
                # Store user_id in session
                session['username'] = user_id[0]
                cursor.close()
                conn.close()
                # Redirect to landing after successful login
                return redirect(url_for('landing'))
            else:
                return redirect(url_for('login'))
            
        except Exception as e:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

# Driver function
if __name__ == '__main__':

	app.run(debug = True)