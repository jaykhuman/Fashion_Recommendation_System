from datetime import datetime
from flask import render_template, session, request, redirect,jsonify
from werkzeug.utils import secure_filename

from base import app
from base.com.dao.detection_dao import DetectionDAO
from base.com.dao.login_dao import LoginDAO
from base.com.service.detection_service import ai_interface
from base.com.vo.detection_vo import DetectionVO


@app.route('/user/loadImage', methods=["GET"])
def user_load_image():
    try:
        if "login_role" in session and session['login_role'] == "user":
            return render_template('user/uploadImg.html')
    except Exception as ex:
        return render_template('user/error.html')


@app.route('/user/uploadImage', methods=["POST"])
def user_upload_image():
    try:
        if "login_role" in session and session['login_role'] == "user":
            detection_image = request.files.get("detectionImage")
            input_filepath = "base/static/adminResourses/inputImage/"
            input_filename = secure_filename(detection_image.filename)
            input_file = input_filepath + input_filename
            detection_image.save(input_file)

            image_name_list = ai_interface(input_file)

            detection_dao = DetectionDAO()
            detection_vo = DetectionVO()

            detection_vo.detection_input_file = input_file.replace("base",
                                                                   "..")
            image_name_list = [image_name.replace("\\", "/") for
                               image_name in
                               image_name_list]
            image_name_list_temp = []
            output_filepath = "../static/adminResourses/"
            for img in image_name_list:
                img1 = output_filepath + img
                image_name_list_temp.append(img1)

            image_name_str = ",".join(image_name_list_temp)
            detection_vo.detection_output_file = image_name_str
            detection_vo.detection_login_id = session.get("login_id")
            detection_vo.detection_datetime = datetime.now()
            detection_dao.insert_detection(detection_vo)

            return user_view_detection()
    except Exception as ex:
        return render_template('user/error.html')


@app.route('/admin/view-user')
def admin_view_user():
    try:
        login_dao = LoginDAO()
        login_vo_list = login_dao.view_all_users()
        print(login_vo_list)
        # ajax_login_vo_list = [i.as_dict() for i in login_vo_list]
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>",ajax_login_vo_list)
        return render_template('admin/viewDetection.html',
                               login_vo_list=login_vo_list)
    except Exception as ex:
        return render_template('user/error.html')


@app.route('/admin/ajax_view_user')
def admin_ajax_view_user():
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>..")
    login_id = request.args.get("loginId")
    print("login_id",login_id)
    # detection_vo = DetectionVO()
    detection_dao = DetectionDAO()
    detection_data_list = detection_dao.ajax_view(login_id)
    print(">>>>>>>",detection_data_list)
    dict_detection_data_list = [i.as_dict() for i in detection_data_list]
    print(">>>>>>>", dict_detection_data_list)
    return jsonify(dict_detection_data_list)
#
# @app.route('/admin_viewDetection')
# def admin_viewDetection():
#     try:
#         if "login_role" in session and session['login_role'] == "admin":
#
#             detection_dao = DetectionDAO()
#             view_history_list = detection_dao.admin_view_detection()
#             view_history_list_1 = [detection[0].as_dict() for
#                                    detection in view_history_list]
#             view_history_list_2 = [detection[1].as_dict() for
#                                    detection in view_history_list]
#             print(view_history_list_1)
#             print(view_history_list_2)
#             for data in view_history_list_1:
#                 data['detection_output_file'] = data[
#                     'detection_output_file'].split(",")
#             return render_template('admin/viewDetection.html',
#                                    view_history_list_1=view_history_list_1,
#                                    view_history_list_2=view_history_list_2)
#     except Exception as ex:
#         return render_template('user/error.html')


@app.route('/user/viewDetection')
def user_view_detection():
    try:
        if "login_role" in session and session['login_role'] == "user":
            detection_vo = DetectionVO()
            detection_dao = DetectionDAO()
            detection_vo.detection_login_id = session.get("login_id")
            detection_vo_list = detection_dao.user_view_detection(detection_vo)
            detection_vo_list = [detection.as_dict() for detection in
                                 detection_vo_list]
            detect_list = []
            for detection in detection_vo_list:
                detection['detection_output_file'] = detection[
                    'detection_output_file'].split(",")
                detect_list.append(detection)

            return render_template('user/viewDetection.html',
                                   detection_vo_list=detect_list)
    except Exception as ex:
        return render_template('user/error.html')


@app.route('/user/deletedetection')
def deletedetection():
    try:
        if "login_role" in session and session['login_role'] == "user":
            detection_vo = DetectionVO()
            detection_dao = DetectionDAO()

            detection_id = request.args.get('detection_id')

            detection_vo.detection_id = detection_id
            detection_dao.delete_detection(detection_vo)
            return redirect("/user/viewDetection")

    except Exception as ex:
        return render_template('user/error.html')
