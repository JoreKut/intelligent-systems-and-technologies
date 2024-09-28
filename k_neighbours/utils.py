import collections
import copy

import pandas
from sklearn import preprocessing
from sklearn.metrics.pairwise import cosine_similarity

from models import UserInput


class RecSys:
    """
        fit - load_data, prepare df
        predict(input)
            - does not change target_df
            - calculate similarity based on df and get k-neighbour
    """
    __n_neighbour: int
    __ranked_list: pandas.DataFrame
    __target_df: pandas.DataFrame

    __target_columns: list[str] = [
        "stress_level",
        "sleep_well",
        "average_sleep_time",
    ]

    def __init__(
            self,
            df,
            n_neighbour: int
    ):
        self.__n_neighbour = n_neighbour
        self.df = df

    @staticmethod
    def to_df(user_model: UserInput):
        return pandas.DataFrame(
            dict(
                stress_level=[user_model.stress_level],
                sleep_well=[user_model.sleep_well],
                average_sleep_time=[user_model.average_sleep_time]
            )
        )

    def fit(self):
        """"""
        target_df = self.df[self.__target_columns]

        # Prepare enums to number
        target_df.loc[target_df['sleep_well'] == 'Да', 'sleep_well'] = 1
        target_df.loc[target_df['sleep_well'] == 'Нет', 'sleep_well'] = 0

        # Cast values to float
        target_df = target_df.astype(float)
        # min-max scale data
        self.__target_df = self.normalize_data(target_df)

    @staticmethod
    def normalize_data(df) -> pandas.DataFrame:
        """Scale columns to 0..1 range"""
        scaler = preprocessing.Normalizer()
        df.iloc[:, :] = scaler.fit_transform(df.iloc[:, :].to_numpy())
        return df

    def predict(self, user_input: UserInput):
        user_df = self.to_df(user_input)
        normalized_user_df = self.normalize_data(user_df)

        user_vector = normalized_user_df.values
        target_vectors = self.__target_df.values

        # find similarity values
        diffs = cosine_similarity(target_vectors, user_vector)
        result_df = pandas.DataFrame(diffs, columns=['similarity_rate'])

        # join asserted results to similarity rates
        joined_result_df = copy.copy(self.df[["morning_drink"]])
        joined_result_df[['similarity_rate']] = result_df

        # sort df by similarity rates
        sorted_list = joined_result_df.sort_values(by="similarity_rate", ascending=False)

        # get top 5 by similarity
        head_neighbours = sorted_list.head(self.__n_neighbour)
        target_values = head_neighbours['morning_drink'].values
        # find the most frequent value
        m = dict(collections.Counter(target_values))
        predicted_answer = max(m, key=m.get)
        return predicted_answer
