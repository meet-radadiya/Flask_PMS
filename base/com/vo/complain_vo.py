from base import db
from base.com.vo.login_vo import LoginVO


class ComplainVO(db.Model):
    __tablename__ = "complain_table"
    complain_id = db.Column("complain_id", db.Integer, primary_key=True, autoincrement=True)
    complain_subject = db.Column("complain_subject", db.String(255), nullable=False)
    complain_description = db.Column("complain_description", db.Text, nullable=False)
    complain_datetime = db.Column("complain_datetime", db.DateTime, nullable=False)
    complain_status = db.Column("complain_status", db.String(100), nullable=False)
    complain_login_id = db.Column("complain_login_id", db.Integer,
                                  db.ForeignKey(LoginVO.login_id, ondelete='CASCADE', onupdate='CASCADE'),
                                  nullable=False)

    def as_dict(self):
        return {
            "complain_id": self.complain_id,
            "complain_subject": self.complain_subject,
            "complain_description": self.complain_description,
            "complain_datetime": self.complain_datetime,
            "complain_status": self.complain_status,
            "complain_login_id": self.complain_login_id,
        }


db.create_all()