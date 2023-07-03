from base import db
from base.com.vo.login_vo import LoginVO


class LoginDAO:
    def insert_login(self, login_vo):
        db.session.add(login_vo)
        db.session.commit()

    def check_login(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(
            login_username=login_vo.login_username,
            login_password=login_vo.login_password).all()
        return login_vo_list

    def view_login(self, login_vo):
        login_vo_view_list = LoginVO.query.filter_by(
            login_username=login_vo.login_username.all())
        return login_vo_view_list

    def view_all_users(self):
        login_vo_list = LoginVO.query.filter(LoginVO.login_role
                                             != "admin").all()
        return login_vo_list
