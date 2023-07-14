from base import db
from base.com.vo.bucketfile_vo import BucketFileVO


class BucketFileDAO:
    def insert_bucketfile(self, bucketfile_vo):
        db.session.add(bucketfile_vo)
        db.session.commit()

    def view_bucketfile(self):
        bucketfile_vo_list = BucketFileVO.query.all()
        return bucketfile_vo_list

    def delete_bucketfile(self, bucketfile_vo):
        bucketfile_vo_list = BucketFileVO.query.get(bucketfile_vo.bucketfile_id)
        db.session.delete(bucketfile_vo_list)
        db.session.commit()
        return bucketfile_vo_list

    def search_bucketfile(self, bucketfile_vo):
        bucketfile_vo_list = BucketFileVO.query.filter_by(bucketfile_id=bucketfile_vo.bucketfile_id).all()
        return bucketfile_vo_list
