from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    quantity = Column(Integer)
    price = Column(Float)

engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# adicionar um novo produto
new_product = Product(name='Produto 1', quantity=5, price=10.5)
session.add(new_product)
session.commit()

# consultar todos os produtos
products = session.query(Product).all()

# imprimir os nomes dos produtos
for product in products:
    print(product.name)