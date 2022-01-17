from sqlalchemy import sql, Column, Sequence

from utils.db_api.db_gino import db


class Item(db.Models):
    __tablename__ = 'items'
    query: sql.Select

    id = Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    start_city_code = Column(db.String(20))
    start_city_name = Column(db.String(50))

    day = Column(db.Integer)
    current_month_code = Column(db.Integer)
    current_month_name = Column(db.String(20))
    next_month1_code = Column(db.Integer)
    next_month1_name = Column(db.String(20))
    next_month2_code = Column(db.Integer)
    next_month2_name = Column(db.String(20))

    quantity_people_code = Column(db.Integer)
    quantity_people_name = Column(db.String(20))

    quantity_night_code = Column(db.Integer)
    quantity_night_name = Column(db.String(20))

    travel_country_code = Column(db.String(20))
    travel_country_name = Column(db.String(50))

    travel_city_code = Column(db.String(50))
    travel_city_name = Column(db.String(50))

    hotel_name = Column(db.String(100))
    rating = Column(db.String(20))
    stars = Column(db.String(20))
    price = Column(db.Integer)
    line = Column(db.String(20))
    beach_surface = Column(db.String(20))
    to_the_beach = Column(db.String(20))
    photo = Column(db.String(200))
    buy_url = Column(db.String(300))

    def __repr__(self):
        return f'''
{self.photo}
Рэйтинг: {self.rating}
Отель: {self.hotel_name}
Звезд: {self.stars} 
Цена: {self.price}
Линия {self.line}
{self.beach_surface}
До пляжа {self.to_the_beach}
'''




