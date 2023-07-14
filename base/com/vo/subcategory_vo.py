from base import db
from base.com.vo.category_vo import CategoryVO


class SubCategoryVO(db.Model):
    __tablename__ = 'subcategory_table'
    subcategory_id = db.Column('subcategory_id', db.Integer, primary_key=True, autoincrement=True)
    subcategory_name = db.Column('subcategory_name', db.String(255), nullable=False)
    subcategory_description = db.Column('subcategory_description', db.Text, nullable=False)
    subcategory_category_id = db.Column('subcategory_category_id', db.Integer,
                                        db.ForeignKey(CategoryVO.category_id, ondelete='CASCADE', onupdate='CASCADE'),
                                        nullable=False)

    def as_dict(self):
        return {
            'subcategory_id': self.subcategory_id,
            'subcategory_name': self.subcategory_name,
            'subcategory_description': self.subcategory_description,
            'subcategory_category_id': self.subcategory_category_id
        }


db.create_all()
