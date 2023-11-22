from flask import Flask, render_template, url_for, request, redirect, send_file, session
from serp_api import fetch_data
import json
import os
from demo_data_handler import jsonHandler,chart

app = Flask(__name__)

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
    logged_in = True
    if request.method == 'POST':
        updated_keyword = request.form.get('keyword')
        updated_type = request.form.get('type') 
        return redirect(url_for('keyword_search', keyword=updated_keyword, type=updated_type))    
    
    queries = None
    locations = None
    titles = None
    num_locations = None
    num_queries = None
    num_titles = None
    data_list = fetch_data(keyword,type)
    if type == 'GEO_MAP_0':
        locations = [item.get('location') for item in data_list if 'location' in item]
        num_locations = len(locations)
        print(locations)
        #handle if the returned location value is less than 3
        top3_data = locations[:3] if num_locations >= 3 else locations
    elif type == 'RELATED_QUERIES':
        queries = [item.get('queries_title') for item in data_list if 'queries_title' in item]
        num_queries = len(queries)
        #handle if the returned queries value is less than 3
        top3_data = queries[:3] if num_queries >= 3 else queries
    elif type == 'RELATED_TOPICS':
        titles = [item.get('title') for item in data_list if 'title' in item]
        num_titles = len(titles)
        top3_data = titles[:3] if num_titles >= 3 else titles
    image_filename = ''
    search_result = ''
    if (data_list):
        search_result = 'Yes'
    elif (not data_list):
        search_result = 'No'
    print('empytDataList: ',not data_list)
    print('fetched data',data_list)
    if len(data_list) > 0:
        image_filename = data_list[-1].get("image_filename")
        data_list = data_list[:-1]
    user_file_path = os.path.join(app.static_folder, 'users', 'users.json')
    existing_users = []
    if os.path.exists(user_file_path) and os.path.getsize(user_file_path) > 0:
        with open(user_file_path, 'r') as file:
            try:
                existing_users = json.load(file)
            except json.decoder.JSONDecodeError:
                pass
    for user in existing_users:
        if user['username'] == username:
            # Append keyword, type, and image path to the JSON file
            user_search_record = {
                "keyword": keyword,
                "type": type,
                "keywords_data":search_result,
                "image": image_filename
            }
            user.setdefault('data', []).append(user_search_record)
            with open(user_file_path, 'w') as file:
                json.dump(existing_users, file, indent=2)
            break
    return render_template('home.html', 
                           data_list=data_list, image_filename=image_filename,type=type,keyword = keyword,top3_data=top3_data,active_page='home',logged_in=logged_in, username=username,locations=locations,queries=queries,titles=titles,num_locations=num_locations,num_queries=num_queries,num_titles=num_titles)

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
    print('demo keyword: ',demo_keyword)
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

        if not username and not password:
            error_message = "Username and password are required"
            return render_template('login.html',active_page='login',username=username,password=password,error_message=error_message)
        elif not username and password:
            error_message = "Username is required"
            return render_template('login.html',active_page='login',username=username,password=password,error_message=error_message)
        elif not password and username:
            error_message = "Password is required"
            return render_template('login.html',active_page='login',username=username,password=password,error_message=error_message)
        else:
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
                    session['username'] = user['username']
                    return redirect(url_for('home'))
            error_message = "Invalid username or password"
            return render_template('login.html',active_page='login',username=username,password=password,error_message=error_message)

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
            signup_error = "Username, password and email are required"
            return render_template('signup.html',active_page='signup',username=username,password=password,email=email,signup_error=signup_error)
        # Create a dictionary with the user data
        user_data = {'username': username, 'password': password,'email':email}
        password = password

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
        user_file_path = os.path.join(app.static_folder, 'users', 'users.json')
        existing_users = []
        
        if os.path.exists(user_file_path) and os.path.getsize(user_file_path) > 0:
            with open(user_file_path, 'r') as file:
                try:
                    existing_users = json.load(file)
                except json.decoder.JSONDecodeError:
                    pass
        
        username = session['username']
        email = None
        password = None
        keyword = None
        keyword_type = None
        result = None
        image_filename = None
        user_data = None

        if request.method == 'POST':
            if 'delete_account' in request.form:
                # Delete account functionality
                username_to_delete = session['username']
                updated_users = [user for user in existing_users if user['username'] != username_to_delete]
                
                with open(user_file_path, 'w') as file:
                    json.dump(updated_users, file, indent=2)
                
                session.pop('username', None)
                
                return redirect(url_for('login'))

            # Update info functionality
            email = request.form.get('email')
            password = request.form.get('password')
            
            for user in existing_users:
                if user['username'] == username:
                    if email:
                        user['email'] = email
                    if password:
                        user['password'] = password
                    if 'data' in user:
                        user_data = user['data']
                        if len(user['data']) > 0:
                            keyword = user['data'][-1]['keyword']
                            keyword_type = user['data'][-1]['type']
                            result = user['data'][-1]['keywords_data']
                            image_filename = user['data'][-1]['image']
                        break
            with open(user_file_path, 'w') as file:
                json.dump(existing_users, file, indent=4)
            return render_template('update_info.html', active_page='update_info', updated=True, logged_in=True,
                                   username=username, email=email,keyword=keyword,keyword_type=keyword_type,result=result,image_filename=image_filename,user_data=user_data)
        else:
            for user in existing_users:
                # print('User:',user)
                # print('UserName:',username)
                # print('username: ',user['username'])
                # print('existing_user:',existing_users)
                if user['username'] == username:
                    email = user['email']                   
                    if 'data' in user:
                        user_data = user['data']
                        if len(user_data) > 0:
                            keyword = user['data'][-1]['keyword']
                            keyword_type = user['data'][-1]['type']
                            result = user['data'][-1]['keywords_data']
                            image_filename = user['data'][-1]['image']
                        break
            return render_template('update_info.html', username=username,email=email, active_page='update_info',
                                   logged_in=True,keyword=keyword,keyword_type=keyword_type,result=result,image_filename=image_filename,user_data=user_data)
    else:
        return redirect(url_for('login'))

@app.route('/delete_account', methods=['GET', 'POST'])
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
