import enum

from pydantic import BaseModel


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 0


class UserInput(BaseModel):
    # # gender: Gender
    # age: str
    # healthy_life_style: str
    # left_eye_color: str

    # target group
    stress_level: float
    sleep_well: float
    average_sleep_time: float

    # # subgroup
    # coffee_nearby: str
    # chronic_diseases: str
    # smoking: str

    # # result
    # morning_drink: str
    #
    # wake_up_time: str
    # chronotype: str
    # gourmet: str
    # office_worker: str
    # homebody: str
    # write_hand: str
    # zodiac_sign: str
