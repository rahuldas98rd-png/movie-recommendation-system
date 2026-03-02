from features.load_data import load_movies
from features.preprocess import Preprocessor

import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from rake_nltk import Rake


class BuildFeatures:

    def __init__(self, data):
        self.df = data.fillna('')

        # initialize ONCE ✅
        self.stop_words = set(stopwords.words("english"))
        self.rake = Rake(stopwords=self.stop_words)
        self.lemmatizer = WordNetLemmatizer()

    # ---------------------------
    # TEXT CLEANING
    # ---------------------------
    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9 ]+', ' ', text)
        return text

    # ---------------------------
    # KEYWORD EXTRACTION
    # ---------------------------
    def text_extraction(self, text):
        self.rake.extract_keywords_from_text(text)
        keywords = self.rake.get_word_degrees().keys()
        return " ".join(keywords)

    # ---------------------------
    # LEMMATIZATION
    # ---------------------------
    def lemmatize_text(self, text):
        tokens = nltk.word_tokenize(text)
        lemmas = [self.lemmatizer.lemmatize(w) for w in tokens]
        return " ".join(lemmas)

    # ---------------------------
    # MAIN PIPELINE
    # ---------------------------
    def build_meta_data(self):

        # clean overview first
        self.df['overview'] = (
            self.df['overview']
            .astype(str)
            .apply(self.clean_text)
        )

        # extract keywords
        self.df['overview'] = self.df['overview'].apply(
            self.text_extraction
        )

        # clean categorical text
        self.df['genres_clean'] = (
            self.df['genres']
            .str.replace(',', ' ', regex=False)
            .str.lower()
        )

        self.df['keywords_clean'] = (
            self.df['keywords']
            .str.replace(',', ' ', regex=False)
            .str.lower()
        )

        # combine features
        self.df['meta_tags'] = (
            self.df['genres_clean'] + " " +
            self.df['keywords_clean'] + " " +
            self.df['overview']
        )

        # final normalization + lemmatization
        self.df['meta_tags'] = (
            self.df['meta_tags']
            .apply(self.clean_text)
            .apply(self.lemmatize_text)
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
        )

        return self.df[['title','meta_tags']]

if __name__ == "__main__":
    df = load_movies()

    preprocessor = Preprocessor(df)
    new_df = preprocessor.feature_extraction()

    build = BuildFeatures(new_df)
    meta_df = build.build_meta_data()
    print(meta_df.head())