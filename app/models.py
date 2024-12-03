from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    item: Mapped[str]
    category: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int]

    def as_dict(self):
        return {key: value for key, value in self.__dict__.items() if not str(key).startswith("_")}
