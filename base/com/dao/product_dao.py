from base import db
from base.com.vo.category_vo import CategoryVO
from base.com.vo.product_vo import ProductVO
from base.com.vo.subcategory_vo import SubCategoryVO


class ProductDAO:
    def insert_product(self, product_vo):
        db.session.add(product_vo)
        db.session.commit()

    def view_product(self):
        product_vo_list = (db.session.query(CategoryVO, SubCategoryVO, ProductVO).filter(
            CategoryVO.category_id == ProductVO.product_category_id).filter(
            SubCategoryVO.subcategory_id == ProductVO.product_subcategory_id).all())
        return product_vo_list

    def delete_product(self, product_id):
        product_vo_list = ProductVO.query.get(product_id)
        db.session.delete(product_vo_list)
        db.session.commit()
        return product_vo_list

    def edit_product(self, product_vo):
        product_vo_list = ProductVO.query.filter_by(product_id=product_vo.product_id)
        return product_vo_list

    def update_product(self, product_vo):
        db.session.merge(product_vo)
        db.session.commit()

    def count_product(self):
        count_product = ProductVO.query.count()
        return count_product