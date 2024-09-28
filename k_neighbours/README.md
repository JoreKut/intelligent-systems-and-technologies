# K-neighbours.


У нас есть модель ввода:
```python
class UserInput(BaseModel):
    # gender: Gender
    age: str
    healthy_life_style: str
    left_eye_color: str

    # target group
    stress_level: float
    sleep_well: float
    average_sleep_time: float

    # subgroup
    coffee_nearby: str
    chronic_diseases: str
    smoking: str

    # result
    morning_drink: str

    wake_up_time: str
    chronotype: str
    gourmet: str
    office_worker: str
    homebody: str
    write_hand: str
    zodiac_sign: str

```


Для определения вектора, будем использовать данные:

```python
class UserInput(BaseModel):
    ...
    # target group
    stress_level: float
    sleep_well: float
    average_sleep_time: float
    ...
```


Образование вектора пользовательских данных

```python
class RecSys:
    @staticmethod
    def to_df(user_model: UserInput):
        return pandas.DataFrame(
            dict(
                stress_level=[user_model.stress_level],
                sleep_well=[user_model.sleep_well],
                average_sleep_time=[user_model.average_sleep_time]
            )
        )
```

```python
# find similarity values
diffs = cosine_similarity(target_vectors, user_vector)
result_df = pandas.DataFrame(diffs, columns=['similarity_rate'])

```

## Preview

[> Jupiter file with list code](recsys,ipynb)
