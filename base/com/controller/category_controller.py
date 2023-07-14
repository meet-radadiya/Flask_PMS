from flask import request, render_template, redirect

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.category_dao import CategoryDAO
from base.com.vo.category_vo import CategoryVO


@app.route('/admin/load_category')
def admin_load_category():
    try:
        if admin_login_session() == "admin":
            return render_template('admin/addCategory.html')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_category route exception occured>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/insert_category', methods=['POST'])
def admin_insert_category():
    try:
        if admin_login_session() == "admin":
            category_name = request.form.get('categoryName')
            category_description = request.form.get('categoryDescription')

            category_vo = CategoryVO()
            category_dao = CategoryDAO()

            category_vo.category_name = category_name
            category_vo.category_description = category_description

            category_dao.insert_category(category_vo)

            return redirect('/admin/view_category')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_insert_category route exception occured>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/view_category')
def admin_view_category():
    try:
        if admin_login_session() == "admin":
            category_dao = CategoryDAO()
            category_vo_list = category_dao.view_category()
            return render_template('admin/viewCategory.html', category_vo_list=category_vo_list)
        else:
            return admin_logout_session()

    except Exception as ex:
        print("admin_view_category route exception occured>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/delete_category')
def admin_delete_category():
    try:
        if admin_login_session() == "admin":
            category_vo = CategoryVO()
            category_dao = CategoryDAO()
            category_id = request.args.get('categoryId')
            category_vo.category_id = category_id
            category_dao.delete_category(category_vo)
            return redirect('/admin/view_category')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_category route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/edit_category', methods=['GET'])
def admin_edit_category():
    try:
        if admin_login_session() == "admin":
            category_vo = CategoryVO()
            category_dao = CategoryDAO()

            category_id = request.args.get('categoryId')
            category_vo.category_id = category_id
            category_vo_list = category_dao.edit_category(category_vo)
            return render_template('admin/editCategory.html', category_vo_list=category_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_category route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/update_category', methods=['POST'])
def admin_update_category():
    try:
        if admin_login_session() == "admin":
            category_id = request.form.get('categoryId')
            category_name = request.form.get('categoryName')
            category_description = request.form.get('categoryDescription')

            category_vo = CategoryVO()
            category_dao = CategoryDAO()

            category_vo.category_id = category_id
            category_vo.category_name = category_name
            category_vo.category_description = category_description
            category_dao.update_category(category_vo)
            return redirect('/admin/view_category')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_update_category route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)