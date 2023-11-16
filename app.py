from flask import Flask, render_template, url_for, request, redirect, send_file, session
from serp_api import fetch_data
import json
import os

app = Flask(__name__)
app.secret_key = "9773e89f69e69285cf11c10cbc44a37945f6abbc5d78d5e20c2b1b0f12d75ab7"

@app.route("/",methods=['GET', 'POST'])
def home():
    keyword = '' 
    type = ''
    if request.method == 'POST':
        keyword = request.form.get("keyword")
        type = request.form.get("type")
        print('keyword1',keyword)
        print('type1',type)        
        return redirect(url_for('keyword_search', keyword=keyword, type=type))
    return render_template('home.html', active_page='home')

@app.route('/<keyword>/<type>', methods=['GET', 'POST'])
def keyword_search(keyword,type):
    if request.method == 'POST':
        updated_keyword = request.form.get('keyword')
        updated_type = request.form.get('type') 
        return redirect(url_for('keyword_search', keyword=updated_keyword, type=updated_type))    
    
    data_list = fetch_data(keyword,type)
    image_filename = ''

    print('empytDataList: ',not data_list)
    print('fetched data',data_list)
    if len(data_list) > 0:
        image_filename = data_list[-1].get("image_filename")
        data_list = data_list[:-1]
    return render_template('home.html', data_list=data_list, image_filename=image_filename,type=type,keyword = keyword,active_page='home')

#@app.route('/')
def home():  # put application's code here
    username = session.get('username')
    if username:
        # User is logged in, retrieve other user-specific information if needed
        username = session.get('username')
        return render_template('home.html', logged_in=True, username=username)
    else:
        # User is not logged in
        return render_template('home.html', logged_in=False)
    
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

    return render_template('login.html')

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
                return "Username already exists", 400
    
        # Add the new user data to the existing users
        existing_users.append(user_data)

        # Write the updated user data back to the file
        with open(user_file_path, 'w') as file:
            json.dump(existing_users, file, indent=2)

        return redirect(url_for('login'))

    return render_template('signup.html')

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
            print (password)
            print (len(password))
            for user in existing_users:
                if user['username'] == username:
                    print (user['password'])
                    user['email'] = email
                    if len(password) == 0:
                        print ("liuyi2b")
                        newpassword = user['password']

                    else:
                        hashed_password = generate_password_hash(password, method='sha256')
                        newpassword = hashed_password
                    print (newpassword)
                    user['password'] = newpassword
            print (existing_users)
            with open(user_file_path, 'w') as file:
                json.dump(existing_users, file, indent=4)

            return redirect(url_for('home'))
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
            return render_template('update_info.html', username=username, email=email)
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
        return redirect(url_for('login'))
    else:
        # Redirect to the login page if not logged in
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug="True")