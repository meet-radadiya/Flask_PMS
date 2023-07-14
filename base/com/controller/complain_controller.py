import datetime

from flask import render_template, redirect, request, url_for

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.complain_dao import ComplainDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.reply_dao import ReplyDAO
from base.com.vo.complain_vo import ComplainVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.reply_vo import ReplyVO


@app.route('/admin/view_complain')
def admin_view_complain():
    try:
        if admin_login_session() == "admin":
            complain_dao = ComplainDAO()
            complain_vo_list = complain_dao.admin_view_complain()
            return render_template('admin/viewComplain.html', complain_vo_list=complain_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_complain route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/load_complain_reply')
def admin_load_complain_reply():
    try:
        if admin_login_session() == "admin":
            complain_dao = ComplainDAO()
            complain_vo = ComplainVO()
            complain_id = request.args.get('complainId')
            complain_vo.complain_id = complain_id
            complain_vo_list = complain_dao.edit_complain(complain_vo)
            return render_template('admin/addReply.html', complain_vo_list=complain_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_reply_complain route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/insert_complain_reply', methods=['POST'])
def admin_insert_complain_reply():
    try:
        if admin_login_session() == "admin":
            complain_id = request.form.get('complainId')
            reply_description = request.form.get('complainReplyDescription')

            complain_dao = ComplainDAO()
            complain_vo = ComplainVO()
            login_vo = LoginVO()
            login_dao = LoginDAO()
            reply_vo = ReplyVO()
            reply_dao = ReplyDAO()

            login_vo.login_username = request.cookies.get('login_username')
            login_id = login_dao.find_login_id(login_vo)

            reply_vo.reply_login_id = login_id
            reply_vo.reply_datetime = datetime.datetime.now()
            reply_vo.reply_description = reply_description
            reply_vo.reply_complain_id = complain_id
            reply_dao.insert_reply(reply_vo)

            complain_vo.complain_id = complain_id
            complain_vo.complain_status = "Replied"
            complain_dao.update_complain(complain_vo)
            return redirect(url_for('admin_view_complain'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_replied_complain_reply route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/delete_complain')
def admin_delete_complain():
    try:
        if admin_login_session() == "admin":
            complain_dao = ComplainDAO()
            complain_vo = ComplainVO()
            complain_id = request.args.get('complainId')
            complain_vo.complain_id = complain_id
            complain_dao.delete_complain(complain_vo)
            return redirect(url_for('admin_view_complain'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_complain route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/user/insert_complain', methods=['POST'])
def user_insert_complain():
    try:
        if admin_login_session() == "user":
            complain_subject = request.form.get('complainSubject')
            complain_description = request.form.get('complainDescription')

            complain_dao = ComplainDAO()
            complain_vo = ComplainVO()
            login_vo = LoginVO()
            login_dao = LoginDAO()

            complain_date = datetime.datetime.now()
            complain_status = "Pending"
            login_vo.login_username = request.cookies.get('login_username')
            login_id = login_dao.find_login_id(login_vo)

            complain_vo.complain_subject = complain_subject
            complain_vo.complain_description = complain_description
            complain_vo.complain_datetime = complain_date
            complain_vo.complain_status = complain_status
            complain_vo.complain_login_id = login_id
            complain_dao.insert_complain(complain_vo)
            return redirect(url_for('user_view_complain'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_insert_complain route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)


@app.route('/user/view_complain')
def user_view_complain():
    try:
        if admin_login_session() == "user":
            complain_vo = ComplainVO()
            complain_dao = ComplainDAO()
            login_vo = LoginVO()
            login_dao = LoginDAO()
            reply_dao = ReplyDAO()

            login_vo.login_username = request.cookies.get('login_username')
            user_login_id = login_dao.find_login_id(login_vo)
            complain_vo.complain_login_id = user_login_id
            complain_vo_list = complain_dao.user_view_complain(complain_vo)

            reply_vo_list = reply_dao.view_reply()
            return render_template("user/addComplain.html", complain_vo_list=complain_vo_list,
                                   reply_vo_list=reply_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_view_complain route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)