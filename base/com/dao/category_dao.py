from base import db
from base.com.vo.category_vo import CategoryVO


class CategoryDAO:
    def insert_category(self, category_vo):
        db.session.add(category_vo)
        db.session.commit()

    def view_category(self):
        category_vo_list = CategoryVO.query.all()
        return category_vo_list

    def delete_category(self, category_vo):
        category_vo_list = CategoryVO.query.get(category_vo.category_id)
        db.session.delete(category_vo_list)
        db.session.commit()

    def edit_category(self, category_vo):
        category_vo_list = CategoryVO.query. \
            filter_by(category_id=category_vo.category_id).all()
        return category_vo_list

    def update_category(self, category_vo):
        db.session.merge(category_vo)
        db.session.commit()
