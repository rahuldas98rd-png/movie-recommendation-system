import json
import pandas as pd
from features.load_data import load_movies

pd.set_option('display.max_columns', 200)

class Preprocessor:
    def __init__(self, data):
        self.df = data

    def missing_value_imputation(self):
        """
        impute missing values in "overview" feature with empty string
        :return: updated dataframe
        """
        self.df["overview"] = self.df["overview"].fillna("")
        return self.df

    def filter_required_columns(self):
        """
        filter out unnecessary columns
        :return: filtered dataframe
        """
        self.df = self.missing_value_imputation()
        self.df = self.df[["title", "genres", "keywords", "overview"]]
        return self.df

    def test_extraction(self, x):
        """
        convert each data of a feature from string to json format and extract
        only required data
        :param x:
        :return: filtered data
        """
        data_list = []
        x = json.loads(x)
        for i, item in enumerate(x):
            data_list.append(x[i]['name'])
        final_data = ', '.join(data_list)
        return final_data

    def feature_extraction(self):
        """
        update "genres" & "keywords"
        :return: updated dataframe
        """
        self.df = self.filter_required_columns()
        self.df.loc[:, 'genres'] = self.df.loc[:, 'genres'].apply(lambda x: self.test_extraction(x))
        self.df.loc[:, 'keywords'] = self.df.loc[:, 'keywords'].apply(lambda x: self.test_extraction(x))
        return self.df


if __name__ == "__main__":
    df = load_movies()

    preprocessor = Preprocessor(df)
    new_df = preprocessor.feature_extraction()
    print(new_df.isnull().sum())
    print(new_df.head())