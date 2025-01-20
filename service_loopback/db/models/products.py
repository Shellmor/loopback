import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db.base_class import Base

class Products(Base):
    """ Продукты магазина """
    localized_name = "Продукты магазина"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)
    price = sa.Column(sa.Float, nullable=False)
    stock_quantity = sa.Column(sa.Integer, nullable=False)
    place_shop_id = sa.Column(sa.Integer, sa.ForeignKey('place_shop.id'), nullable=False)

    order = relationship('OrderItem', back_populates='order')
    products = relationship('PlaceShop', back_populates='place_shop')
