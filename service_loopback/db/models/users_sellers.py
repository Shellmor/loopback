import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db.base_class import Base


class UsersSellers(Base):
    """ Пользователи продавцы """
    localized_name = "Пользователи продавцы"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, nullable=False)
    first_name = sa.Column(sa.String, nullable=True)
    last_name = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, nullable=False)
    created = sa.Column(sa.DateTime(timezone=True), default=sa.func.now())
    status = sa.Column(sa.String, nullable=False)
    context = sa.Column(sa.String, nullable=False)
    place_shop_id = sa.Column(sa.Integer, sa.ForeignKey('place_shop.id'), nullable=False)

    staff = relationship('PlaceShop', back_populates='staff_shop')
