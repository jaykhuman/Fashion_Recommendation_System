from base import db
from base.com.vo.login_vo import LoginVO


class RegisterVO(db.Model):
    __tablename__ = 'register_table'
    register_id = db.Column('register_id', db.Integer, primary_key=True,
                            autoincrement=True)
    register_firstname = db.Column('register_firstname', db.String(255),
                                   nullable=False)
    register_lastname = db.Column('register_lastname', db.String(255),
                                  nullable=False)
    register_login_id = db.Column('register_login_id', db.Integer,
                                  db.ForeignKey(LoginVO.login_id),
                                  nullable=False)

    def as_dict(self):
        return {
            'register_id': self.register_id,
            'register_firstname': self.register_firstname,
            'register_lastname': self.register_lastname,
            'register_login_id': self.register_login_id
        }


db.create_all()
