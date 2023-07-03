from base import db
from base.com.vo.detection_vo import DetectionVO
from base.com.vo.login_vo import LoginVO


class DetectionDAO:
    def insert_detection(self, detection_vo):
        db.session.add(detection_vo)
        db.session.commit()

    def user_view_detection(self, detection_vo):
        detection_vo_list = db.session.query(DetectionVO).filter_by(
            detection_login_id=detection_vo.detection_login_id).all()
        return detection_vo_list

    def admin_view_detection(self):
        view_history_list = db.session.query(DetectionVO, LoginVO).join(
            LoginVO, DetectionVO.detection_login_id == LoginVO.login_id).all()
        return view_history_list

    def delete_detection(self, detection_vo):
        detection_vo_list = DetectionVO.query.get(
            detection_vo.detection_id)
        db.session.delete(detection_vo_list)
        db.session.commit()

    def ajax_view(self,login_id):
        detection_data_list = DetectionVO.query.filter(DetectionVO.detection_login_id== login_id).all()
        return detection_data_list