from flask import Flask, render_template, url_for, request, redirect, send_file, session
from serp_api import fetch_data
import json
import os
from demo_data_handler import jsonHandler,chart
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "9773e89f69e69285cf11c10cbc44a37945f6abbc5d78d5e20c2b1b0f12d75ab7"

@app.route("/",methods=['GET', 'POST'])
def home():
    keyword = '' 
    type = ''
    username = session.get('username')
    if request.method == 'POST':
        keyword = request.form.get("keyword")
        type = request.form.get("type")
        print('keyword1',keyword)
        print('type1',type)        
        return redirect(url_for('keyword_search', keyword=keyword, type=type))
    if username:
        # User is logged in, retrieve other user-specific information if needed
        username = session.get('username')
        return render_template('home.html', logged_in=True, username=username,active_page='home')
    else:
        # User is not logged in
        return redirect(url_for('demo'))

@app.route('/<keyword>/<type>', methods=['GET', 'POST'])
def keyword_search(keyword,type):
    username = session.get('username')
    if request.method == 'POST':
        updated_keyword = request.form.get('keyword')
        updated_type = request.form.get('type') 
        return redirect(url_for('keyword_search', keyword=updated_keyword, type=updated_type,logged_in=True,username=username))    
    
    data_list = fetch_data(keyword,type)
    if type == 'GEO_MAP_0':
        top3_data = [item['location'] for item in data_list[:3]]
    elif type == 'RELATED_QUERIES':
        top3_data = [item['queries_title'] for item in data_list[:3]]
    elif type == 'RELATED_TOPICS':
        top3_data = [item['title'] for item in data_list[:3]]
    image_filename = ''
    print('empytDataList: ',not data_list)
    print('fetched data',data_list)
    if len(data_list) > 0:
        image_filename = data_list[-1].get("image_filename")
        data_list = data_list[:-1]
    return render_template('home.html', data_list=data_list, image_filename=image_filename,type=type,keyword = keyword,top3_data=top3_data,active_page='home',logged_in=True,username=username)

@app.route("/demo",methods = ['GET','POST'])
def demo():
    demo_keyword = ''
    demo_type = ''
    if request.method == 'POST':
        demo_keyword = request.form.get("demo_keyword")
        demo_type = request.form.get("demo_type")
        print('demo_keyword',demo_keyword)
        print('demo_type',demo_type)
        return redirect(url_for('demo_keyword_search', demo_keyword=demo_keyword, demo_type=demo_type)) 
    return render_template('demo.html',active_page = 'demo',logged_in=False)

@app.route('/demo/<demo_keyword>/<demo_type>', methods=['GET', 'POST'])
def demo_keyword_search(demo_keyword,demo_type):
    if request.method == 'POST':
        updated_demo_keyword = request.form.get('demo_keyword')
        updated_demo_type = request.form.get("demo_type")
        return redirect(url_for('demo_keyword_search', demo_keyword=updated_demo_keyword, demo_type=updated_demo_type))
    demo_type_dict = {
    "GEO_MAP_0": "region",
    "RELATED_QUERIES": "queries",
    "RELATED_TOPICS": "topics"
    }
    if demo_type == 'GEO_MAP_0':
        demo_data = jsonHandler('cityu_region.json')
        demo_chart = chart('cityu_region.json')
        top3_demo_data = [item['location'] for item in demo_data[:3]]
    elif demo_type == 'RELATED_QUERIES':
        demo_data = jsonHandler('cityu_queries.json')
        demo_chart = chart('cityu_queries.json')
        top3_demo_data = [item['queries_title'] for item in demo_data[:3]]
    elif demo_type == 'RELATED_TOPICS':
        demo_data = jsonHandler('cityu_topics.json')
        demo_chart = chart('cityu_topics.json')
        top3_demo_data = [item['Topic'] for item in demo_data[:3]]
    return render_template('demo.html',active_page = 'demo',demo_data=demo_data,demo_chart=demo_chart,demo_keyword=demo_keyword,demo_type=demo_type,demo_type_dict=demo_type_dict,top3_demo_data=top3_demo_data)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Username and password are required", 400

        # Get the path to the user JSON file
        user_file_path = os.path.join(app.static_folder, 'users', 'users.json')

        existing_users = []
        if os.path.exists(user_file_path) and os.path.getsize(user_file_path) > 0:
            with open(user_file_path, 'r') as file:
                try:
                    existing_users = json.load(file)
                except json.decoder.JSONDecodeError:
                    pass

        for user in existing_users:
            if user['username'] == username and user['password'] == password:
                #session['username'] = user['username']
                session['username'] = user['username']
                return redirect(url_for('home'))

        return "Invalid username or password", 401

    return render_template('login.html',active_page = 'login')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the form data
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        # Validate the data (add more validation as needed)
        if not username or not password or not email:
            return "Username and password and email are required", 400
        # Create a dictionary with the user data
        user_data = {'username': username, 'password': password,'email':email}
        password = password
        # Create a dictionary with the user data
        user_data = {'username': username, 'password': password,'email':email}

        # Get the path to the user JSON file
        user_file_path = os.path.join(app.static_folder, 'users', 'users.json')

        # Load existing user data from the file
        existing_users = []
        if os.path.exists(user_file_path) and os.path.getsize(user_file_path) > 0:
            with open(user_file_path, 'r') as file:
                try:
                    existing_users = json.load(file)
                except json.decoder.JSONDecodeError:
                    pass  # Handle the case where the file is empty or not in valid JSON format

        # Check if the username already exists
        for user in existing_users:
            if user['username'] == username:
                #return "Username already exists", 400
                return render_template('signup.html',active_page='signup',username=username)
    
        # Add the new user data to the existing users
        existing_users.append(user_data)

        # Write the updated user data back to the file
        with open(user_file_path, 'w') as file:
            json.dump(existing_users, file, indent=2)

        return redirect(url_for('login'))

    return render_template('signup.html',active_page = 'signup')

@app.route('/signout')
def signout():
    # Clear user information from the session
    session.pop('username', None)

    # Redirect to the login page or any other desired page
    return redirect(url_for('login'))

@app.route('/update_info', methods=['GET', 'POST'])
def update_info():
    if 'username' in session:
        if request.method == 'POST':
            user_file_path = os.path.join(app.static_folder, 'users', 'users.json')
            
            # Read existing user data from the file
            existing_users = []
            if os.path.exists(user_file_path) and os.path.getsize(user_file_path) > 0:
                with open(user_file_path, 'r') as file:
                    try:
                        existing_users = json.load(file)
                    except json.decoder.JSONDecodeError:
                        pass
            username = session.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            print(password)
            print(len(password))
            for user in existing_users:
                if user['username'] == username:
                    print(user['password'])
                    user['email'] = email
                    if len(password) == 0:
                        print("liuyi2b")
                        newpassword = user['password']
                    else:
                        newpassword = password
                    print(newpassword)
                    user['password'] = newpassword
            print(existing_users)
            with open(user_file_path, 'w') as file:
                json.dump(existing_users, file, indent=4)

            return render_template('update_info.html',active_page='update_info',updated=True,logged_in=True,username=username,email=email)
        else:
            user_file_path = os.path.join(app.static_folder, 'users', 'users.json')
            username = session.get('username')
            existing_users = []
            if os.path.exists(user_file_path) and os.path.getsize(user_file_path) > 0:
                with open(user_file_path, 'r') as file:
                    try:
                        existing_users = json.load(file)
                    except json.decoder.JSONDecodeError:
                        pass
            for user in existing_users:
                if user['username'] == username:
                    email = user['email']
            return render_template('update_info.html', username=username, email=email,active_page = 'update_info',logged_in=True)
    else:
        return redirect(url_for('login'))

@app.route('/delete_account')
def delete_account():

    # Check if the user is logged in
    if 'username' in session:
        username_to_delete = session['username']
        
        # Get the path to the user JSON file
        user_file_path = os.path.join(app.static_folder, 'users', 'users.json')
        
        # Read existing user data from the file
        existing_users = []
        if os.path.exists(user_file_path) and os.path.getsize(user_file_path) > 0:
            with open(user_file_path, 'r') as file:
                try:
                    existing_users = json.load(file)
                except json.decoder.JSONDecodeError:
                    pass
        
        # Remove the user from the list based on the username
        updated_users = [user for user in existing_users if user['username'] != username_to_delete]
        
        # Write the updated user data back to the file
        with open(user_file_path, 'w') as file:
            json.dump(updated_users, file, indent=2)
        
        session.pop('username', None)
        
        # Redirect to the login page
        return redirect(url_for('home'))
    else:
        # Redirect to the login page if not logged in
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug="True")
