import random
import smtplib
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import bcrypt
from flask import render_template, redirect, request, url_for, make_response, flash, session

from base import app
from base.com.dao.complain_dao import ComplainDAO
from base.com.dao.feedback_dao import FeedbackDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.product_dao import ProductDAO
from base.com.dao.user_dao import UserDAO
from base.com.vo.login_vo import LoginVO

global_loginvo_list = []
global_login_secretkey_set = {0}


# @app.after_request
# def after_request(response):
#     response.headers["Cache-Control"] = "no-store"
#     return response


@app.route('/', methods=['GET'])
def admin_load_login():
    try:
        return render_template('user/login.html')
    except Exception as ex:
        print("admin_load_login route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)


@app.route("/admin/validate_login", methods=['POST'])
def admin_validate_login():
    try:
        global global_loginvo_list
        global global_login_secretkey_set

        login_username = request.form.get('loginUsername')
        login_password = request.form.get('loginPassword').encode("utf-8")

        login_vo = LoginVO()
        login_dao = LoginDAO()

        login_vo.login_username = login_username

        login_vo_list = login_dao.check_login_username(login_vo)
        login_list = [i.as_dict() for i in login_vo_list]
        len_login_list = len(login_list)
        if len_login_list == 0:
            error_message = 'username is incorrect !'
            flash(error_message)
            return redirect('/')
        elif not login_list[0]['login_status']:
            error_message = 'You have been temporarily blocked by website admin !'
            flash(error_message)
            return redirect('/')
        else:
            login_id = login_list[0]['login_id']
            login_username = login_list[0]['login_username']
            login_role = login_list[0]['login_role']
            login_secretkey = login_list[0]['login_secretkey']
            hashed_login_password = login_list[0]['login_password'].encode("utf-8")
            if bcrypt.checkpw(login_password, hashed_login_password):
                login_vo_dict = {
                    login_secretkey: {'login_username': login_username, 'login_role': login_role, 'login_id': login_id}}
                if len(global_loginvo_list) != 0:
                    for i in global_loginvo_list:
                        temp_list = list(i.keys())
                        global_login_secretkey_set.add(temp_list[0])
                    login_secretkey_list = list(global_login_secretkey_set)
                    if login_secretkey not in login_secretkey_list:
                        global_loginvo_list.append(login_vo_dict)
                else:
                    global_loginvo_list.append(login_vo_dict)
                if login_role == 'admin':
                    response = make_response(redirect(url_for('admin_load_dashboard')))
                    response.set_cookie('login_secretkey', value=login_secretkey, max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username, max_age=timedelta(minutes=30))
                    return response

                elif login_role == 'user':
                    response = make_response(redirect(url_for('user_load_dashboard')))
                    response.set_cookie('login_secretkey', value=login_secretkey, max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username, max_age=timedelta(minutes=30))
                    return response
                else:
                    return redirect(url_for('admin_logout_session'))
            else:
                error_message = 'password is incorrect !'
                flash(error_message)
                return redirect('/')
    except Exception as ex:
        print("admin_validate_login route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)


@app.route('/admin/load_dashboard', methods=['GET'])
def admin_load_dashboard():
    try:
        if admin_login_session() == 'admin':
            user_dao = UserDAO()
            complain_dao = ComplainDAO()
            feedback_dao = FeedbackDAO()
            product_dao = ProductDAO()
            count_user = user_dao.count_user()
            count_complain = complain_dao.count_complain()
            count_feedback = feedback_dao.count_feedback()
            count_product = product_dao.count_product()
            login_username = request.cookies.get('login_username')
            return render_template('admin/index.html', count_user=count_user, count_complain=count_complain,
                                   count_feedback=count_feedback, count_product=count_product,
                                   login_username=login_username)
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("admin_load_dashboard route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/user/load_dashboard', methods=['GET'])
def user_load_dashboard():
    try:
        if admin_login_session() == 'user':
            return render_template('user/index.html')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_load_dashboard route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)


@app.route('/admin/login_session')
def admin_login_session():
    try:
        global global_loginvo_list
        login_role_flag = ""
        login_secretkey = request.cookies.get('login_secretkey')
        if login_secretkey is None:
            return redirect('/')
        for i in global_loginvo_list:
            if login_secretkey in i.keys():
                if i[login_secretkey]['login_role'] == 'admin':
                    login_role_flag = "admin"
                elif i[login_secretkey]['login_role'] == 'user':
                    login_role_flag = "user"
        return login_role_flag
    except Exception as ex:
        print("admin_login_session route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)


@app.route("/admin/logout_session", methods=['GET'])
def admin_logout_session():
    try:
        global global_loginvo_list
        login_secretkey = request.cookies.get('login_secretkey')
        login_username = request.cookies.get('login_username')
        response = make_response(redirect('/'))
        if login_secretkey is not None and login_username is not None:
            response.set_cookie('login_secretkey', login_secretkey, max_age=0)
            response.set_cookie('login_username', login_username, max_age=0)
            for i in global_loginvo_list:
                if login_secretkey in i.keys():
                    global_loginvo_list.remove(i)
                    break
        return response
    except Exception as ex:
        print("admin_logout_session route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)


@app.route("/admin/block_user", methods=['GET'])
def admin_block_user():
    try:
        if admin_login_session() == 'admin':

            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_id = request.args.get('loginId')
            login_vo.login_id = login_id
            login_vo.login_status = False
            login_dao.update_login(login_vo)
            return redirect("/admin/view_user")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_block_user route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route("/admin/unblock_user", methods=['GET'])
def admin_unblock_user():
    try:
        if admin_login_session() == 'admin':

            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_id = request.args.get('loginId')
            login_vo.login_id = login_id
            login_vo.login_status = True
            login_dao.update_login(login_vo)
            return redirect('/admin/view_user')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_unblock_user route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/user/load_forget_password', methods=['GET'])
def user_load_forget_password():
    try:
        return render_template('user/forgetPassword.html')
    except Exception as ex:
        print("user_load_forget_password route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)


@app.route('/user/validate_login_username', methods=['post'])
def user_validate_login_username():
    try:
        login_username = request.form.get("loginUsername")
        login_dao = LoginDAO()
        login_vo = LoginVO()

        login_vo.login_username = login_username
        login_vo_list = login_dao.login_validate_username(login_vo)
        login_list = [i.as_dict() for i in login_vo_list]
        len_login_list = len(login_list)
        if len_login_list == 0:
            error_message = 'username is incorrect !'
            flash(error_message)
            return redirect(url_for('user_load_forget_password'))
        else:
            login_id = login_list[0]['login_id']
            session['session_login_id'] = login_id
            login_username = login_list[0]['login_username']
            sender = "pythondemodonotreply@gmail.com"
            receiver = login_username
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "PYTHON OTP"
            otp = random.randint(1000, 9999)
            session['session_otp_number'] = otp
            message = str(otp)
            msg.attach(MIMEText(message, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, "qazwsxedcrfvtgb1234567890")
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
            server.quit()
            return render_template('user/otpValidation.html')
    except Exception as ex:
        print("user_validate_login_username route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)


@app.route('/user/validate_otp_number', methods=['POST'])
def user_validate_otp_number():
    try:
        otp_number = int(request.form.get("otpNumber"))
        session_otp_number = session.get('session_otp_number')
        if otp_number == session_otp_number:
            return render_template('user/resetPassword.html')
        else:
            session.clear()
            error_message = 'otp is incorrect !'
            flash(error_message)
            return redirect(url_for('admin_load_forget_password'))
    except Exception as ex:
        print("user_validate_otp_number route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)


@app.route('/user/insert_reset_password', methods=['POST'])
def user_insert_reset_password():
    try:
        login_password = request.form.get("loginPassword")
        salt = bcrypt.gensalt(rounds=12)
        hashed_login_password = bcrypt.hashpw(login_password.encode("utf-8"), salt)
        login_id = session.get("session_login_id")
        login_dao = LoginDAO()
        login_vo = LoginVO()
        login_vo.login_id = login_id
        login_vo.login_password = hashed_login_password
        login_dao.update_login(login_vo)
        return redirect('/')
    except Exception as ex:
        print("user_insert_reset_password route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)