from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.login_vo import LoginVO


class UserVO(db.Model):
    __tablename__ = 'user_table'

    user_id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    user_firstname = db.Column('user_firstname', db.String(255), nullable=False)
    user_lastname = db.Column('user_lastname', db.String(255), nullable=False)
    user_gender = db.Column('user_gender', db.String(10), nullable=False)
    user_address = db.Column('user_address', db.String(255), nullable=False)
    user_hobby = db.Column('user_hobby', db.String(255), nullable=False)
    user_area_id = db.Column('user_area_id', db.Integer, db.ForeignKey(AreaVO.area_id, ondelete='CASCADE',
                                                                       onupdate='CASCADE'), nullable=False)
    user_login_id = db.Column('user_login_id', db.Integer, db.ForeignKey(LoginVO.login_id, ondelete='CASCADE',
                                                                         onupdate='CASCADE'), nullable=False)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'user_firstname': self.user_firstname,
            'user_lastname': self.user_lastname,
            'user_gender': self.user_gender,
            'user_address': self.user_address,
            'user_hobby': self.user_hobby,
            'user_area_id': self.user_area_id,
            'user_login_id': self.user_login_id
        }


db.create_all()
