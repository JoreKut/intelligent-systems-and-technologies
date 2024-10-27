from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

# Определение таблицы
table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String)
)
