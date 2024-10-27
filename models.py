from copy import copy

from pandas.core.dtypes.cast import maybe_cast_to_integer_array
from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

# Определение таблицы
table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String)
)

if __name__ == '__main__':
    # table.c возвращает коллекцию колонок
    columns = [c for c in table.columns if c.name != "id"]
    print(columns)
