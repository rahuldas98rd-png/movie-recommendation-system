import os
from dotenv import load_dotenv
from src.utils.helper import load_object
from src.features.load_data import load_movies

load_dotenv()

file_import_path = os.getenv("MODEL_IMPORT_PATH")

class Recommendation:
    def __init__(self, dataset):
        self.model = load_object(file_import_path+"cosine_model.pkl")
        self.df = dataset

    def recommend(self, movie_title=None, k=5):
        try:
            idx = self.df.loc[self.df["title"].str.lower() == movie_title].index[0]
            scores = list(enumerate(self.model[idx]))
            scores = sorted(scores, key=lambda x: x[1], reverse=True)

            movies_indices = [tpl[0] for tpl in scores[1:(k + 1)]]
            similarity_scores = [f"{round(tpl[1], 3) * 100}%" for tpl in scores[1:(k + 1)]]

            similar_movie_list = list(self.df["title"].str.lower().iloc[movies_indices])
            return similar_movie_list, similarity_scores
        except IndexError:
            return False

if __name__ == "__main__":
    dataset = load_movies()
    recommendation = Recommendation(dataset)
    movie_title = input("Enter your favorite movie: ").strip().lower()
    if recommendation.recommend():
        print("\nTop5 matches using Cosine Similarity:")
        movies, similar = recommendation.recommend(movie_title=movie_title, k=6)
        for i, movie in enumerate(movies):
            print("{} --> with {} similarity".format(movie, similar[i]))

    else:
        print("❌ Movie not found")