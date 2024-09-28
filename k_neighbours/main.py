import pandas

from models import UserInput
from utils import RecSys

if __name__ == '__main__':
    file = pandas.read_csv("result.csv", sep=";")
    r = RecSys(df=file, n_neighbour=1)
    r.fit()
    input_data_1 = UserInput(
        stress_level=55,
        sleep_well=1,
        average_sleep_time=8
    )
    input_data_2 = UserInput(
        stress_level=4.9,
        sleep_well=1,
        average_sleep_time=7.8
    )
    result = r.predict(input_data_1)
    print(result)  # Coffee
    result = r.predict(input_data_2)
    print(result)  # Tea
