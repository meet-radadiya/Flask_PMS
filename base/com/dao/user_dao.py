from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.user_vo import UserVO


class UserDAO:
    def insert_user(self, user_vo):
        db.session.add(user_vo)
        db.session.commit()

    def view_user(self):
        user_vo_list = db.session.query(UserVO, LoginVO, AreaVO) \
            .join(LoginVO, UserVO.user_login_id == LoginVO.login_id) \
            .join(AreaVO, UserVO.user_area_id == AreaVO.area_id) \
            .all()
        return user_vo_list

    def edit_user(self, user_vo):
        user_vo_list = db.session.query(UserVO) \
            .filter_by(user_login_id=user_vo.user_login_id) \
            .all()
        return user_vo_list

    def update_user(self, user_vo):
        db.session.merge(user_vo)
        db.session.commit()

    def count_user(self):
        count_user = UserVO.query.count()
        return count_user