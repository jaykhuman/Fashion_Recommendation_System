from base import db
from base.com.vo.login_vo import LoginVO
from base.com.vo.register_vo import RegisterVO


class RegisterDAO:
    def insert_register(self, register_vo):
        db.session.add(register_vo)
        db.session.commit()

    def view_all_registered_users(self):
        # register_vo_view_all_list = RegisterVO.query.all()
        register_vo_view_all_list = db.session.query(RegisterVO, LoginVO).join(
            LoginVO, RegisterVO.register_login_id == LoginVO.login_id).all()
        return register_vo_view_all_list
