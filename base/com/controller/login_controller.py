from flask import render_template, request, redirect, flash, session

from base import app
from base.com.dao.login_dao import LoginDAO
from base.com.dao.register_dao import RegisterDAO
from base.com.vo.login_vo import LoginVO
from base.com.vo.register_vo import RegisterVO

app.secret_key = 'detectionpage'


@app.route('/')
def login():
    try:
        return render_template('admin/login.html')
    except Exception as ex:
        return str(ex)


@app.route('/login')
def loginagain():
    try:
        return render_template('admin/login.html')
    except Exception as ex:
        return str(ex)


@app.route('/user/about')
def about():
    try:
        return render_template('user/about.html')
    except Exception as ex:
        return str(ex)


@app.route('/viewUsers')
def viewUsers():
    try:
        if "login_role" in session and session['login_role'] == "admin":
            register_dao = RegisterDAO()
            register_vo_view_all_list = register_dao.view_all_registered_users()
            view_history_list_1 = [log[LoginVO].as_dict() for
                                   log in register_vo_view_all_list]
            view_history_list_2 = [reg[RegisterVO].as_dict() for reg in \
                                   register_vo_view_all_list]

            return render_template('admin/viewUsers.html',
                                   view_history_list_1=view_history_list_1,
                                   view_history_list_2=view_history_list_2)
    except Exception as ex:
        return render_template('user/error.html')


@app.route('/admin_index')
def admin_index():
    try:
        if "login_role" in session and session['login_role'] == "admin":
            return render_template('admin/index.html')
    except Exception as ex:
        return render_template('user/error.html')


@app.route('/user_index')
def user_index():
    try:
        if "login_role" in session and session['login_role'] == "user":
            return render_template('user/index.html')
    except Exception as ex:
        return render_template('user/error.html')


@app.route('/load_login', methods=['POST', 'GET'])
def load_login():
    try:
        login_username = request.form.get("userName")
        login_password = request.form.get("password")

        login_vo = LoginVO()
        login_dao = LoginDAO()

        login_vo.login_username = login_username
        login_vo.login_password = login_password

        login_vo_list = login_dao.check_login(login_vo)

        if login_vo_list:

            login_vo_list = [login_obj.as_dict() for login_obj in
                             login_vo_list]
            login_dict = login_vo_list[0]
            login_username = login_dict.get("login_username")
            login_role = login_dict.get("login_role")

            if login_role == "admin":
                session['login_id'] = login_dict.get("login_id")
                session['login_role'] = login_role
                session['login_username'] = login_username
                return render_template("admin/index.html")

            elif login_role == "user":
                session['login_id'] = login_dict.get("login_id")
                session['login_role'] = login_role
                session['login_username'] = login_username
                return render_template("user/index.html")
        else:
            error_message = 'Username or Password is incorrect!!'
            flash(error_message)
            return redirect("/")

    except Exception as ex:
        return str(ex)
