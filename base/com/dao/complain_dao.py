from base import db
from base.com.vo.complain_vo import ComplainVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.reply_vo import ReplyVO


class ComplainDAO:
    def insert_complain(self, complain_vo):
        db.session.add(complain_vo)
        db.session.commit()

    def user_view_complain(self, complain_vo):
        complain_vo_list = db.session.query(ComplainVO, LoginVO) \
            .filter_by(complain_login_id=complain_vo.complain_login_id) \
            .filter(ComplainVO.complain_login_id == LoginVO.login_id) \
            .all()
        return complain_vo_list

    def admin_view_complain(self):
        complain_vo_list = db.session.query(ComplainVO, ReplyVO, LoginVO) \
            .join(LoginVO, ComplainVO.complain_login_id == LoginVO.login_id) \
            .join(ReplyVO, ComplainVO.complain_id == ReplyVO.reply_complain_id, isouter=True) \
            .all()
        return complain_vo_list

    def delete_complain(self, complain_vo):
        complain_vo_list = ComplainVO.query.get(complain_vo.complain_id)
        db.session.delete(complain_vo_list)
        db.session.commit()

    def edit_complain(self, complain_vo):
        complain_vo_list = ComplainVO.query.get(complain_vo.complain_id)
        return complain_vo_list

    def update_complain(self, complain_vo):
        db.session.merge(complain_vo)
        db.session.commit()

    def count_complain(self):
        count_complain = ComplainVO.query.count()
        return count_complain