import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db.base_class import Base


class PlaceShop(Base):
    """ Площадка магазинов """
    localized_name = "Площадка магазинов"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, nullable=False)
    context = sa.Column(sa.String, nullable=False)
    create_date = sa.Column(sa.DateTime(timezone=True), default=sa.func.now())
    description = sa.Column(sa.String, nullable=True)

    place_shop = relationship('Product', back_populates='products')
    staff_shop = relationship('UsersSellers', back_populates='staff')

