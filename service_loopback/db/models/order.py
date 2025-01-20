import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db.base_class import Base


class OrderItem(Base):
    """ Связь заказов и продуктов """
    localized_name = "Связь заказов и продуктов"

    id = sa.Column(sa.Integer, primary_key=True)
    quantity = sa.Column(sa.Integer, nullable=False)
    price = sa.Column(sa.Float, nullable=False)
    place_shop_id = sa.Column(sa.Integer, sa.ForeignKey('place_shop.id'), nullable=False)
    product_id = sa.Column(sa.Integer, sa.ForeignKey('products.id'), nullable=False)

    order_items = relationship('Products', back_populates='order')