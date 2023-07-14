import datetime

from flask import render_template, redirect, request, url_for

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.feedback_dao import FeedbackDAO
from base.com.dao.login_dao import LoginDAO
from base.com.vo.feedback_vo import FeedbackVO
from base.com.vo.login_vo import LoginVO


@app.route('/admin/view_feedback')
def admin_view_feedback():
    try:
        if admin_login_session() == "admin":
            feedback_dao = FeedbackDAO()

            feedback_vo_list = feedback_dao.admin_view_feedback()
            return render_template('admin/viewFeedback.html', feedback_vo_list=feedback_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_feedback route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/delete_feedback')
def admin_delete_feedback():
    try:
        if admin_login_session() == "admin":

            feedback_dao = FeedbackDAO()
            feedback_vo = FeedbackVO()
            feedback_id = request.args.get('feedbackId')
            feedback_vo.feedback_id = feedback_id
            feedback_dao.delete_feedback(feedback_vo)
            return redirect(url_for('admin_view_feedback'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_feedback route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/user/insert_feedback', methods=['POST'])
def user_insert_feedback():
    try:
        if admin_login_session() == "user":
            feedback_rating = request.form.get('rating')
            feedback_description = request.form.get('feedbackDescription')
            feedback_date = datetime.datetime.now()

            feedback_dao = FeedbackDAO()
            feedback_vo = FeedbackVO()
            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_vo.login_username = request.cookies.get('login_username')
            login_id = login_dao.find_login_id(login_vo)

            feedback_vo.feedback_description = feedback_description
            feedback_vo.feedback_rating = feedback_rating
            feedback_vo.feedback_datetime = feedback_date
            feedback_vo.feedback_login_id = login_id
            feedback_dao.insert_feedback(feedback_vo)
            return redirect(url_for('user_view_feedback'))
        else:
            return admin_logout_session()

    except Exception as ex:
        print("user_insert_feedback route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)


@app.route('/user/view_feedback')
def user_view_feedback():
    try:
        if admin_login_session() == "user":

            feedback_dao = FeedbackDAO()
            feedback_vo = FeedbackVO()
            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_vo.login_username = request.cookies.get('login_username')
            login_id = login_dao.find_login_id(login_vo)
            feedback_vo.feedback_login_id = login_id

            feedback_vo_list = feedback_dao.user_view_feedback(feedback_vo)
            return render_template("user/addFeedback.html", feedback_vo_list=feedback_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_view_feedback route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)