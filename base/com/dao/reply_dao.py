from base import db
from base.com.vo.login_vo import LoginVO
from base.com.vo.reply_vo import ReplyVO


class ReplyDAO:
    def insert_reply(self, reply_vo):
        db.session.add(reply_vo)
        db.session.commit()

    def view_reply(self):
        reply_vo_list = db.session.query(ReplyVO, LoginVO) \
            .filter(ReplyVO.reply_login_id == LoginVO.login_id) \
            .all()
        return reply_vo_list