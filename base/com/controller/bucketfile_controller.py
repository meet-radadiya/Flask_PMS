import os
import pathlib
from datetime import datetime

import boto3
from flask import request, redirect, render_template, url_for
from werkzeug.utils import secure_filename

from base import app
from base.com.controller.login_controller import \
    admin_login_session, \
    admin_logout_session
from base.com.dao.bucketfile_dao import BucketFileDAO
from base.com.vo.bucketfile_vo import BucketFileVO

aws_access_key_id = 'aws_access_key_id'
aws_secret_access_key = 'aws_secret_access_keyg'
bucket_name = 'bucket_name'
region_name = "region_name"

local_folder = 'base/static/adminResources/local/'
app.config['local_folder'] = local_folder

storage_folder = 'base/static/adminResources/storage/'
app.config['storage_folder'] = storage_folder


@app.route('/admin/load_bucket')
def admin_load_bucket():
    try:
        if admin_login_session() == 'admin':
            return render_template('admin/addBucket.html')
        else:
            admin_logout_session()
    except Exception as ex:
        print("admin_load_bucket route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/insert_bucket', methods=['POST'])
def admin_insert_bucket():
    try:
        if admin_login_session() == 'admin':
            bucket_name = request.form.get('bucketName')
            bucket_resource = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                                           aws_secret_access_key=aws_secret_access_key, region_name=region_name)
            bucket_response = bucket_resource.create_bucket(ACL='public-read-write',
                                                            Bucket=bucket_name)
            return redirect('/admin/view_bucket')
        else:
            admin_logout_session()
    except Exception as ex:
        print("admin_insert_bucket route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/view_bucket')
def admin_view_bucket():
    try:
        if admin_login_session() == 'admin':
            s3_resource = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key)
            bucket_list = s3_resource.list_buckets()
            return render_template('admin/viewBucket.html', bucket_list=bucket_list)
        else:
            admin_logout_session()
    except Exception as ex:
        print("admin_view_bucket route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/load_bucketfile')
def admin_load_bucketfile():
    try:
        if admin_login_session() == 'admin':
            return render_template('admin/addBucketFile.html')
        else:
            admin_logout_session()
    except Exception as ex:
        print("admin_load_bucketfile route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/insert_bucketfile', methods=['POST'])
def admin_insert_bucketfile():
    try:
        if admin_login_session() == 'admin':
            bucketfile_vo = BucketFileVO()
            bucketfile_dao = BucketFileDAO()

            file = request.files.get('file')
            login_username = request.cookies.get('login_username')
            bucketfolder_name = (login_username).replace("@gmail.com", "")
            bucketfile_name = secure_filename(file.filename)
            bucketfile_path = os.path.join(app.config['local_folder'] + bucketfolder_name + "/")
            file_path = pathlib.Path(bucketfile_path)
            if not file_path.exists():
                os.mkdir(bucketfile_path)
            file.save(os.path.join(bucketfile_path, bucketfile_name))
            s3_resource = boto3.resource('s3', aws_access_key_id=aws_access_key_id,
                                         aws_secret_access_key=aws_secret_access_key)
            s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key)
            # to keep file public
            # s3_client.put_object(Bucket=bucket_name, Key=(bucketfolder_name), ACL='public-read')
            s3_client.put_object(Bucket=bucket_name, Key=(bucketfolder_name))
            s3_resource.meta.client.upload_file(Filename=bucketfile_path + bucketfile_name,
                                                Bucket=bucket_name,
                                                Key=bucketfolder_name + "/" + bucketfile_name)
            bucketfile_object_url = f"https://{bucket_name}.s3.amazonaws.com/{bucketfolder_name}/{bucketfile_name}"
            # expiration = 3600
            # bucketfile_object_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name,'Key': bucketfolder_name + "/" + bucketfile_name},ExpiresIn=expiration)
            bucketfile_vo.bucketfile_name = bucketfile_name
            bucketfile_vo.bucketfile_path = bucketfile_path.replace('base', '..')
            bucketfile_vo.bucketfile_datetime = datetime.now()
            bucketfile_vo.bucketfile_object_url = bucketfile_object_url
            bucketfile_dao.insert_bucketfile(bucketfile_vo)
            return redirect('/admin/view_bucketfile')
        else:
            admin_logout_session()
    except Exception as ex:
        print("admin_insert_bucketfile route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/view_bucketfile')
def admin_view_bucketfile():
    try:
        if admin_login_session() == 'admin':
            bucketfile_dao = BucketFileDAO()
            bucketfile_vo_list = bucketfile_dao.view_bucketfile()
            return render_template('admin/viewBucketFile.html', bucketfile_vo_list=bucketfile_vo_list)
        else:
            admin_logout_session()
    except Exception as ex:
        print("admin_view_bucketfile route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/download_bucketfile')
def admin_download_bucketfile():
    try:
        if admin_login_session() == 'admin':
            bucketfile_vo = BucketFileVO()
            bucketfile_dao = BucketFileDAO()
            login_username = request.cookies.get('login_username')
            bucketfile_id = request.args.get('bucketfileId')
            bucketfolder_name = (login_username).replace("@gmail.com", "")
            bucketfile_vo.bucketfile_id = bucketfile_id
            bucketfile_vo_list = bucketfile_dao.search_bucketfile(bucketfile_vo)
            bucketfile_name = bucketfile_vo_list[0].bucketfile_name
            bucketfile_path = os.path.join(app.config['storage_folder'] + bucketfolder_name + "/")
            file_path = pathlib.Path(bucketfile_path)
            if not file_path.exists():
                os.mkdir(bucketfile_path)
            s3Resource = boto3.resource('s3', aws_access_key_id=aws_access_key_id,
                                        aws_secret_access_key=aws_secret_access_key)
            s3Resource.Bucket(bucket_name).download_file(bucketfolder_name + "/" + bucketfile_name,
                                                         bucketfile_path + "/" + bucketfile_name)

            download_file_path = storage_folder.replace("base", "..") + bucketfolder_name + "/" + bucketfile_name
            return render_template('admin/downloadBucketFile.html', download_file_path=download_file_path)
        else:
            admin_logout_session()
    except Exception as ex:
        print("admin_download_bucketfile route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)


@app.route('/admin/delete_bucketfile')
def admin_delete_bucketfile():
    try:
        if admin_login_session() == 'admin':
            bucketfile_vo = BucketFileVO()
            bucketfile_dao = BucketFileDAO()

            bucketfile_id = request.args.get('bucketfileId')
            login_username = request.cookies.get('login_username')
            bucketfile_vo.bucketfile_id = bucketfile_id
            bucketfile_vo_list = bucketfile_dao.delete_bucketfile(bucketfile_vo)
            bucketfolder_name = (login_username).replace("@gmail.com", "")
            bucketfile_name = bucketfile_vo_list.bucketfile_name
            bucketfile_path = bucketfile_vo_list.bucketfile_path.replace("..", "base")
            bucket_file = bucketfile_path + "/" + bucketfile_name
            os.remove(bucket_file)
            s3 = boto3.resource("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
            object = s3.Object(bucket_name, bucketfolder_name + "/" + bucketfile_name)
            object.delete()
            return redirect(url_for('admin_view_bucketfile'))
        else:
            admin_logout_session()
    except Exception as ex:
        print("admin_delete_bucketfile route exception occured>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)