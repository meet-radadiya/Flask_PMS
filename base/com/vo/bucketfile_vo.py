from base import db


class BucketFileVO(db.Model):
    __tablename__ = 'bucketfile_table'
    bucketfile_id = db.Column('bucketfile_id', db.Integer, primary_key=True, autoincrement=True)
    bucketfile_name = db.Column('bucketfile_name', db.String(255), nullable=False)
    bucketfile_path = db.Column('bucketfile_path', db.String(255), nullable=False)
    bucketfile_object_url = db.Column('bucketfile_object_url', db.String(500), nullable=False)
    bucketfile_datetime = db.Column('bucketfile_datetime', db.DateTime, nullable=False)

    def as_dict(self):
        return {
            'bucketfile_id': self.bucketfile_id,
            'bucketfile_name': self.bucketfile_name,
            'bucketfile_path': self.bucketfile_path,
            'bucketfile_object_url': self.bucketfile_object_url,
            'bucketfile_datetime': self.bucketfile_datetime,
        }


db.create_all()
