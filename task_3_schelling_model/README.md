# Schelling Model

Inspired by [topic by Adil Moujahid](https://adilmoujahid.com/posts/2020/05/streamlit-python-schelling/)

## Вывод
![](media/output.png)


## Code structure

![](media/class_structure.png)

### Принип работы программы:
```python
model = SchellingModel(...)

while True:
    model.do_iteration()
    model.recalculate_ranks()

    if model.is_everyone_satisfied():
        break

model.print_info()
```

## Tests
У нас также есть unit-tests на логику определение таблицы удовлетворенности сущностей.

/[test_rank.py](test_rank.py)