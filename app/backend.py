import json
import pandas as pd
from config_loader import *

class MovieRecommendation:
    def __init__(self):
        self.df = load_movies()
        self.model = load_model()

    def popular(self, k_pop=9):
        m = self.df['vote_count'].quantile(0.9).round(0)
        C = self.df['vote_average'].mean().round(1)
        v = self.df['vote_count']
        R = self.df['vote_average']

        self.df["weighted_rating"] = ((v / (v + m)) * R) + ((m / (v + m)) * C)

        # Sorting the data on the basis of weighted rating
        self.df.sort_values(by='weighted_rating', ascending=False, inplace=True)
        self.df.reset_index(drop=True, inplace=True)

        return list(self.df.loc[:k_pop, 'title']), list(self.df.loc[:k_pop, 'weighted_rating'])

    def text_extraction(self, x):
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

    def available_genres(self):
        self.df.loc[:, 'genres'] = self.df.loc[:, 'genres'].apply(lambda x: self.text_extraction(x))
        genres = set()
        for i in self.df['genres']:
            i = i.split(', ')
            genres.update(i)
        genres.remove('')
        return list(genres)

    def release_year(self):
        self.df['release_date'] = pd.to_datetime(self.df['release_date'])
        self.df['release_year'] = self.df['release_date'].dt.year
        years = sorted(set(self.df['release_year'].dropna(axis=0).astype(int)), reverse=True)
        return years

    def recommend(self, movie_title=None, k=6):
        if movie_title in list(self.df["title"].str.lower()):
            idx = self.df.loc[self.df["title"].str.lower() == movie_title].index[0]
            scores = list(enumerate(self.model[idx]))
            scores = sorted(scores, key=lambda x: x[1], reverse=True)

            movies_indices = [tpl[0] for tpl in scores[1:(k + 1)]]
            similarity_scores = [f"{round(tpl[1], 3) * 100}%" for tpl in scores[1:(k + 1)]]

            similar_movie_list = list(self.df["title"].iloc[movies_indices])
            date_list = list(self.df["release_date"].iloc[movies_indices])
            runtime_list = list(self.df["runtime"].astype(str).iloc[movies_indices])
            status_list = list(self.df["status"].iloc[movies_indices])
            description_list = list(self.df["overview"].iloc[movies_indices])


            genre_list = list(self.df["genres"].iloc[movies_indices])

            self.df.loc[:, 'spoken_languages'] = self.df.loc[:, 'spoken_languages'].apply(lambda x: self.text_extraction(x))
            language_list = list(self.df["spoken_languages"].iloc[movies_indices])

            ratings = list(self.df["vote_average"].iloc[movies_indices])

            return (similar_movie_list, date_list, runtime_list, status_list,
                    description_list, genre_list, language_list, ratings, similarity_scores)


        else:
            return [], [], [], [], [], [], [], [], []

if __name__ == "__main__":
    movie = MovieRecommendation()
    # movie_list, rating_list = movie.popular()
    # print("Top 10 rated Movie Recommendations: {}".format(movie_list))
    # print(rating_list)
    print(movie.recommend(movie_title="avatar"))