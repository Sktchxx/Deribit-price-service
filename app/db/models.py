from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index, Integer, String, Numeric, BigInteger
from app.db.session import Base


class Price(Base):
    __tablename__ = 'prices'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    ticker: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Numeric(20, 8), nullable=False)
    timestamp: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True
    )

    __table_args__ = (
        Index(
            'ix_prices_ticker_timestamp',
            'ticker',
            'timestamp',
            unique=True),
    )
