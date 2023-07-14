from base import db
from base.com.vo.complain_vo import ComplainVO
from base.com.vo.login_vo import LoginVO


class ReplyVO(db.Model):
    __tablename__ = "reply_table"
    reply_id = db.Column("reply_id", db.Integer, primary_key=True, autoincrement=True)
    reply_description = db.Column("reply_description", db.Text, nullable=False)
    reply_datetime = db.Column("reply_datetime", db.DateTime, nullable=False)
    reply_login_id = db.Column("reply_login_id", db.Integer,
                               db.ForeignKey(LoginVO.login_id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    reply_complain_id = db.Column("reply_complain_id", db.Integer,
                                  db.ForeignKey(ComplainVO.complain_id, ondelete='CASCADE', onupdate='CASCADE'),
                                  nullable=False)

    def as_dict(self):
        return {
            "reply_id": self.reply_id,
            "reply_description": self.reply_description,
            "reply_datetime": self.reply_datetime,
            "reply_login_id": self.reply_login_id,
            "reply_complain_id": self.reply_complain_id,
        }


db.create_all()
