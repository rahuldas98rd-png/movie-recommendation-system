import os
from dotenv import load_dotenv
from src.features.load_data import load_movies
from src.utils.helper import save_object
from features.preprocess import Preprocessor
from src.features.build_features import BuildFeatures
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

load_dotenv()
export_file_path = os.getenv("MODEL_EXPORT_PATH")

class TrainingPipeline:

    def __init__(self, data=load_movies()):
        self.df = data

    def run(self):

        preprocessor = Preprocessor(self.df)
        clean_df = preprocessor.feature_extraction()

        builder = BuildFeatures(clean_df)
        meta_df = builder.build_meta_data()

        cv_obj = CountVectorizer(analyzer='word', lowercase=True, stop_words='english')
        cvt = cv_obj.fit_transform(meta_df['meta_tags'])

        similarity_matrix_cs = cosine_similarity(cvt, cvt)

        print("✅ Training completed successfully")

        save_object(obj=similarity_matrix_cs, path=export_file_path+"cosine_model.pkl")


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run()