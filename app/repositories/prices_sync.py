from sqlalchemy.orm import Session
from app.db.models import Price


class PriceRepositorySync:
    def __init__(self, db: Session):
        self.db = db

    def bulk_insert(self, prices: list[Price]):
        self.db.add_all(prices)
        self.db.commit()
