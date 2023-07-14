import os

from flask import request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

from base import app
from base.com.controller.login_controller import admin_logout_session, admin_login_session
from base.com.dao.category_dao import CategoryDAO
from base.com.dao.product_dao import ProductDAO
from base.com.dao.subcategory_dao import SubCategoryDAO
from base.com.vo.product_vo import ProductVO
from base.com.vo.subcategory_vo import SubCategoryVO

PRODUCT_FOLDER = 'base/static/adminResources/product/'
app.config['PRODUCT_FOLDER'] = PRODUCT_FOLDER


@app.route('/admin/load_product')
def admin_load_product():
    try:
        if admin_login_session() == "admin":
            category_dao = CategoryDAO()
            category_vo_list = category_dao.view_category()
            return render_template('admin/addProduct.html', category_vo_list=category_vo_list)

        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_product route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/ajax_subcategory_product')
def admin_ajax_subcategory_product():
    try:
        if admin_login_session() == "admin":
            subcategory_vo = SubCategoryVO()
            subcategory_dao = SubCategoryDAO()
            subcategory_category_id = request.args.get('productCategoryId')
            subcategory_vo.subcategory_category_id = subcategory_category_id
            subcategory_vo_list = subcategory_dao.view_ajax_subcategory_product(subcategory_vo)
            ajax_product_subcategory = [i.as_dict() for i in subcategory_vo_list]
            return jsonify(ajax_product_subcategory)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_ajax_subcategory_product route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/insert_product', methods=['POST'])
def admin_insert_product():
    try:
        if admin_login_session() == "admin":
            product_category_id = request.form.get('productCategoryId')
            product_subcategory_id = request.form.get('productSubcategoryId')
            product_name = request.form.get('productName')
            product_description = request.form.get('productDescription')
            product_price = request.form.get('productPrice')
            product_quantity = request.form.get('productQuantity')
            product_image = request.files.get('productImage')

            product_image_name = secure_filename(product_image.filename)
            product_image_path = os.path.join(app.config['PRODUCT_FOLDER'])
            product_image.save(os.path.join(product_image_path, product_image_name))

            product_vo = ProductVO()
            product_dao = ProductDAO()

            product_vo.product_name = product_name
            product_vo.product_description = product_description
            product_vo.product_price = product_price
            product_vo.product_quantity = product_quantity
            product_vo.product_image_name = product_image_name
            product_vo.product_image_path = product_image_path.replace("base", "..")
            product_vo.product_category_id = product_category_id
            product_vo.product_subcategory_id = product_subcategory_id
            product_dao.insert_product(product_vo)
            return redirect(url_for('admin_view_product'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_insert_product route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/view_product')
def admin_view_product():
    try:
        if admin_login_session() == "admin":
            product_dao = ProductDAO()
            product_vo_list = product_dao.view_product()
            return render_template('admin/viewProduct.html', product_vo_list=product_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_product route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/delete_product')
def admin_delete_product():
    try:
        if admin_login_session() == "admin":
            product_dao = ProductDAO()
            product_vo = ProductVO()
            product_id = request.args.get('productId')
            product_vo.product_id = product_id
            product_vo_list = product_dao.delete_product(product_id)
            file_path = product_vo_list.product_image_path.replace("..", "base") + product_vo_list.product_image_name
            os.remove(file_path)
            return redirect(url_for('admin_view_product'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_product route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)