# Movie Recommendation System Dataset -- Documentation

## 📌 Overview

This repository contains structured datasets commonly used for:
- **movie analytics**
- **content-based filtering**
- **collaborative filtering recommendation systems**.

The datasets combine:

✅ Movie metadata\
✅ Cast & crew relationships\
✅ User rating behavior

Datasets included:

-   `movies.csv` --- Full movie metadata
-   `credits.csv` --- Cast and crew information
-   `ratings.csv` --- User--movie interaction data
-   `movies_small.csv` --- Reduced subset of movie metadata

------------------------------------------------------------------------

## 📊 Dataset Summary

  File               Records   Description
  ------------------ --------- -------------------------------
  movies.csv         4,803     Complete movie metadata
  credits.csv        4,803     Cast and crew JSON attributes
  ratings.csv        100,004   User rating interactions
  movies_small.csv   6         Sample subset for testing

------------------------------------------------------------------------

## 1. 🎥 movies.csv

### Description

Contains primary descriptive metadata for movies sourced from TMDB-style
datasets.

### Columns

  Column                 Type      Description
  ---------------------- --------- -------------------------
  budget                 Integer   Production budget
  genres                 JSON      List of genre objects
  homepage               String    Official movie website
  id                     Integer   Unique movie identifier
  keywords               JSON      Thematic keywords
  original_language      String    Language code
  original_title         String    Original movie title
  overview               Text      Movie synopsis
  popularity             Float     Popularity score
  production_companies   JSON      Producing companies
  production_countries   JSON      Country of production
  release_date           Date      Movie release date
  revenue                Integer   Box office revenue
  runtime                Float     Duration in minutes
  spoken_languages       JSON      Languages spoken
  status                 String    Release status
  tagline                String    Promotional tagline
  title                  String    Display title
  vote_average           Float     Average rating
  vote_count             Integer   Number of votes

------------------------------------------------------------------------

### Notes

-   `genres`, `keywords`, `production_companies`, `production_countries` and `spoken_languages` fields are JSON-encoded arrays.
-   Requires parsing using `json.loads()` during preprocessing.

## 2. 👥 credits.csv

### Description

Provides detailed **cast** and **crew** information associated with each
movie.

### Columns

  Column     Type      Description
  ---------- --------- -----------------------------------
  movie_id   Integer   Foreign key referencing movies.id
  title      String    Movie title
  cast       JSON      Actor list with roles
  crew       JSON      Crew members and job roles

### Notes

-   `cast` and `crew` fields are JSON-encoded arrays.
-   Requires parsing using `json.loads()` during preprocessing.

------------------------------------------------------------------------

## 3. ⭐ ratings.csv

### Description

Represents explicit user feedback used for collaborative filtering.

### Columns

  Column      Type      Description
  ----------- --------- ----------------------------
  userId      Integer   Unique user identifier
  movieId     Integer   Movie identifier
  rating      Float     User rating (0.5--5 scale)
  timestamp   Integer   Unix timestamp

### Typical Usage

-   Matrix factorization
-   User--item interaction modeling
-   Implicit/explicit recommendation pipelines

------------------------------------------------------------------------

## 4. ⚡ movies_small.csv

### Description

A lightweight subset of `movies.csv` intended for experimentation or
debugging.

### Characteristics

-   Same schema as `movies.csv`
-   Uses **semicolon (`;`) delimiter**
-   Useful for rapid prototyping

------------------------------------------------------------------------

## 🔗 Dataset Relationships

    movies.id  = credits.movie_id
    movies.id  = ratings.movieId

This relational structure enables:

-   Content-based recommendation
-   Hybrid recommender systems
-   Actor/director similarity modeling
-   User preference learning

------------------------------------------------------------------------

## ⚙️ Recommended Preprocessing Steps

1.  Parse JSON columns:
    -   genres
    -   keywords
    -   production_companies
    -   cast
    -   crew
2.  Handle Missing Values:
    -   runtime
    -   homepage
    -   tagline
3.  Feature Engineering:
    -   Extract director from crew
    -   Build combined metadata ("tags")
    -   Normalize popularity and ratings
4.  Merge datasets:

``` python
movies.merge(credits, left_on="id", right_on="movie_id")
```

------------------------------------------------------------------------

## 🚀 Example Use Cases

-   🎯 Movie Recommendation Engine
-   🧩 NLP Similarity Modeling
-   👨‍🎬 Actor/Director Network Analysis
-   📈 Popularity Prediction
-   📊 Movie Trend Analytics

------------------------------------------------------------------------

## 📂 Directory Structure

    .
    ├── movies.csv
    ├── credits.csv
    ├── ratings.csv
    ├── movies_small.csv
    └── README.md

------------------------------------------------------------------------

## 📈 Suggested Tech Stack

  Task              Tools
  ----------------- -------------------------------
  Data Processing   Pandas, NumPy
  NLP               Scikit-learn
  Visualization     Matplotlib, Seaborn
  Modeling          Surprise, TensorFlow, PyTorch

------------------------------------------------------------------------

## 📜 License

Dataset licensing depends on the original source (e.g.,
TMDB/MovieLens).\
Verify redistribution permissions before commercial use.

------------------------------------------------------------------------

## 🤝 Contributions

Pull requests and improvements are welcome.

If you build a recommender system using this dataset, consider sharing
your approach 🚀

------------------------------------------------------------------------

## Author Notes

This README is designed for data science workflows including: 
- Exploratory Data Analysis (EDA) 
- Machine Learning pipelines 
- Recommendation system research

------------------------------------------------------------------------

## ⭐ Support

If this dataset helps your project, consider giving the repository a
**star** ⭐