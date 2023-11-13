from flask import Flask, render_template, url_for, jsonify, request, redirect, send_file
from serp_api import fetch_data

app = Flask(__name__)

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
        return redirect(url_for('keyword_search', keyword=keyword, type=type))     
    data_list = fetch_data(keyword,type)
    print('empytDataList: ',not data_list)
    image_filename = ''
    if len(data_list) > 0:
        image_filename = data_list[-1].get("image_filename")
        data_list = data_list[:-1]
    return render_template('home.html', data_list=data_list, image_filename=image_filename,type=type,keyword = keyword,active_page='home')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form, active_page='login')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form, active_page='signup')

@app.route('/download')
def download_file():
    p = "cityu_queries.png"
    return send_file(p,as_attachment=True)

if __name__ == '__main__':
    app.run(debug="True")

