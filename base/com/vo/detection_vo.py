from base import db
from base.com.vo.login_vo import LoginVO


class DetectionVO(db.Model):
    __tablename__ = 'detection_table'
    detection_id = db.Column('detection_id', db.Integer, primary_key=True,
                             autoincrement=True, nullable=False)

    detection_input_file = db.Column('detection_input_file', db.String(255),
                                     nullable=False)
    detection_output_file = db.Column('detection_output_file', db.String(255),
                                      nullable=False)

    detection_datetime = db.Column('detection_datetime', db.DATETIME(255),
                                   nullable=False)

    detection_login_id = db.Column('detection_login_id',
                                   db.ForeignKey(LoginVO.login_id),
                                   nullable=False)

    def as_dict(self):
        return {
            'detection_id': self.detection_id,
            'detection_input_file': self.detection_input_file,
            'detection_output_file': self.detection_output_file,
            'detection_datetime': self.detection_datetime,
            'detection_login_id': self.detection_login_id
        }


db.create_all()
