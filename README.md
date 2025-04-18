```
# IMDB Movie Recommendation System Using Storylines

## Project Overview

This project develops a content-based movie recommendation system that suggests similar films based on their storylines. By leveraging web scraping, Natural Language Processing (NLP), and machine learning techniques, the system allows users to input a movie plot and receive recommendations for the top 5 most similar movies.

## Skills Takeaway

- Selenium (Web Scraping)
- Python
- Pandas (Data Manipulation)
- Streamlit (User Interface Development)
- NLP (Natural Language Processing)
- TF-IDF (Text Representation)
- Cosine Similarity (Similarity Calculation)
- Machine Learning
- Data Cleaning
- Data Analysis
- Visualization

## Problem Statement

To build a system that can recommend movies to users based on the similarity of their storylines. This involves scraping movie data from IMDb (2024 releases), processing the text of the storylines using NLP, and employing Cosine Similarity to identify and suggest the top 5 most similar movies to a user-provided storyline.

## Business Use Cases

- **Movie Recommendation:** Users can input a movie storyline and receive the top 5 most similar movie suggestions.
- **Entertainment Suggestions:** Provides personalized movie recommendations based on narrative preferences.

## Approach

1.  **Data Scraping and Storage:**
    -   Scrape movie data (Movie Name, Storyline) for 2024 releases from IMDb using Selenium.
    -   Store the scraped data in a CSV file (`imdb_movies_2024.csv`).

2.  **Data Preprocessing and Analysis:**
    -   **Text Cleaning (NLP):** Remove stop words, punctuation, and non-alphanumeric characters from the storylines using NLTK or SpaCy. Tokenize the cleaned text.
    -   **Text Representation:** Convert the processed storylines into numerical vectors using the TF-IDF (Term Frequency-Inverse Document Frequency) Vectorizer from Scikit-learn.
    -   **Cosine Similarity:** Calculate the pairwise Cosine Similarity between the TF-IDF vectors of all movie storylines to determine similarity scores.

3.  **Recommendation System:**
    -   Implement a function that takes a user-input storyline.
    -   Preprocess and vectorize the input storyline using the same TF-IDF Vectorizer fitted on the scraped data.
    -   Calculate the Cosine Similarity between the input storyline vector and all movie storyline vectors.
    -   Rank the movies based on their similarity scores to the input storyline.
    -   Return the top 5 most similar movies (Movie Name and Storyline).

4.  **Streamlit Interface:**
    -   Develop an interactive web application using Streamlit.
    -   Create an input field where users can enter a movie storyline.
    -   Implement the recommendation logic to process the input and retrieve the top 5 similar movies.
    -   Display the recommended movies with their names and storylines in a user-friendly format.

## Dataset

-   Scraped IMDb Data for 2024 Movies.
-   Columns: `Movie Name`, `Storyline`.
-   Format: CSV file (`imdb_movies_2024.csv`).

## Technical Tags

-   **Languages:** Python
-   **Libraries/Tools:**
    -   Web Scraping: Selenium
    -   NLP: NLTK, Scikit-learn (TF-IDF)
    -   Recommendation Algorithms: Cosine Similarity
    -   Web Framework: Streamlit
    -   Data Manipulation: Pandas

## Project Deliverables

-   `imdb_movies_2024.csv`: CSV file containing the scraped IMDb 2024 movie data (Movie Name, Storyline).
-   `scraper.py`: Python script for extracting movie data from IMDb using Selenium.
-   `recommendation.py`: Python script containing the NLP processing and recommendation logic using TF-IDF and Cosine Similarity.
-   `app.py`: Python script for building the interactive user interface using Streamlit.
-   `requirements.txt`: File listing the project dependencies.
-   `README.md`: Project documentation (this file).

## Setup Instructions

1.  **Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Download ChromeDriver:**
    -   Download the ChromeDriver executable that matches your Chrome browser version from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).
    -   Place the `chromedriver` executable in the project directory or ensure it's in your system's PATH.

3.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

    The Streamlit application will open in your web browser.

## Example Use Case

**Input Storyline:** "A group of friends on a summer road trip encounter strange and supernatural events in a remote area."

**Expected Output (Example):**

1.  **Movie Name:** Spooky Roads (Storyline: A group of college students driving across the country find themselves haunted by a malevolent entity.)
2.  **Movie Name:** Summer of Fear (Storyline: During their vacation, a group of teens uncovers a terrifying secret in a small town.)
3.  **Movie Name:** Highway Horrors (Storyline: Travelers on a lonely highway face a series of terrifying encounters with the unknown.)
4.  **Movie Name:** The Lost Highway (Storyline: Friends taking a detour on their road trip stumble upon a mysterious and dangerous phenomenon.)
5.  **Movie Name:** Ghost Trails (Storyline: A summer adventure turns sinister when a group of young adults discovers a haunted trail.)

## Project Guidelines

-   Follow Python coding conventions (PEP 8).
-   Ensure the web scraping process is respectful and adheres to IMDb's terms of service.
-   Implement efficient text processing and similarity calculation methods.
-   Provide clear and concise comments in the code.
-   Document any challenges faced and solutions implemented.

## Contact

For questions or support, please feel free to reach out.

## License

MIT License - see the `LICENSE` file for details.
```
