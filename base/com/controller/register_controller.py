from flask import render_template, request, redirect

from base import app
from base.com.dao.login_dao import LoginDAO
from base.com.dao.register_dao import RegisterDAO
from base.com.vo.login_vo import LoginVO
from base.com.vo.register_vo import RegisterVO


@app.route('/')
def home():
    return render_template("admin/login.html")


@app.route('/index')
def index():
    return render_template('admin/index.html')


@app.route('/register')
def register():
    return render_template('admin/register.html')


@app.route('/load_register')
def load_register():
    try:
        return render_template('admin/register.html')
    except Exception as ex:
        return str(ex)


@app.route('/insert_register', methods=['POST'])
def insert_register():
    try:
        register_vo = RegisterVO()
        register_dao = RegisterDAO()

        login_vo = LoginVO()
        login_dao = LoginDAO()

        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        user_name = request.form.get("userName")
        password = request.form.get("passWord")

        login_vo.login_username = user_name
        login_vo.login_password = password
        login_vo.login_role = "user"

        login_dao.insert_login(login_vo)

        register_vo.register_firstname = first_name
        register_vo.register_lastname = last_name
        register_vo.register_login_id = login_vo.login_id

        register_dao.insert_register(register_vo)

        return redirect("/")

    except Exception as ex:
        return str(ex)
