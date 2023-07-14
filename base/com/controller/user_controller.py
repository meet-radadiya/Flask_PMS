import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import bcrypt
from flask import render_template, request, flash, redirect

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.area_dao import AreaDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.user_dao import UserDAO
from base.com.vo.login_vo import LoginVO
from base.com.vo.user_vo import UserVO

login_secretkey = ""


@app.route('/user/load_user', methods=['GET'])
def user_load_user():
    try:
        area_dao = AreaDAO()
        area_vo_list = area_dao.view_area()
        return render_template('user/addUser.html', area_vo_list=area_vo_list)
    except Exception as ex:
        print("user_load_user route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)


@app.route('/user/insert_user', methods=['POST'])
def user_insert_user():
    try:
        global login_secretkey
        global login_secretkey_flag
        login_secretkey_flag = False

        login_vo = LoginVO()
        login_dao = LoginDAO()

        user_vo = UserVO()
        user_dao = UserDAO()

        login_username = request.form.get('loginUsername')
        user_firstname = request.form.get('userFirstname')
        user_lastname = request.form.get('userLastname')
        user_address = request.form.get('userAddress')
        user_gender = request.form.get('userGender')
        user_area = request.form.get('userArea')
        hobbies_list = request.form.getlist('userHobby')
        user_hobby = ",".join(hobbies_list)

        login_vo_list = login_dao.view_login()
        login_secretkey_list = [i.as_dict()['login_secretkey'] for i in login_vo_list]
        login_username_list = [i.as_dict()['login_username'] for i in login_vo_list]

        if login_username in login_username_list:
            error_message = "The username is already exists !"
            flash(error_message)
            return redirect('/user/load_user')

        while not login_secretkey_flag:
            login_secretkey = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(32))
            if login_secretkey not in login_secretkey_list:
                login_secretkey_flag = True
                break

        login_password = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
        salt = bcrypt.gensalt(rounds=12)
        hashed_login_password = bcrypt.hashpw(login_password.encode("utf-8"), salt)

        sender = "pythondemodonotreply@gmail.com"
        receiver = login_username
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = "YOUR SYSTEM GENERATED LOGIN PASSWORD IS:"
        msg.attach(MIMEText(login_password, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, "qazwsxedcrfvtgb1234567890")
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()

        login_vo.login_username = login_username
        login_vo.login_password = hashed_login_password
        login_vo.login_role = "user"
        login_vo.login_status = True
        login_vo.login_secretkey = login_secretkey
        login_dao.insert_login(login_vo)

        user_vo.user_firstname = user_firstname
        user_vo.user_lastname = user_lastname
        user_vo.user_gender = user_gender
        user_vo.user_address = user_address
        user_vo.user_area_id = user_area
        user_vo.user_hobby = user_hobby
        user_vo.user_login_id = login_vo.login_id
        user_dao.insert_user(user_vo)

        return redirect("/")
    except Exception as ex:
        print("user_insert_user route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)


@app.route('/admin/view_user')
def admin_view_user():
    try:
        if admin_login_session() == "admin":
            user_dao = UserDAO()
            user_vo_list = user_dao.view_user()
            return render_template('admin/viewUser.html', user_vo_list=user_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_user route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)