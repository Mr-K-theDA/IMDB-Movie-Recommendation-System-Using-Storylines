import streamlit as st
import pandas as pd
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configure app settings
st.set_page_config(
    page_title="IMDb Magic Movie Finder",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Download NLTK data
nltk.download('stopwords')

# Custom CSS styling
st.markdown("""
<style>
    .recommendation-card {
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF4B4B;
        background-color: #1a1a1a;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .title-text {
        color: #FF4B4B !important;
        margin-bottom: 0.5rem !important;
    }
    .match-score {
        color: #00cc66;
        font-weight: bold;
    }
    .stTextArea textarea {
        background-color: #0E1117 !important;
        color: white !important;
    }
    .example-card {
        border-color: #4BFFB3 !important;
    }
</style>
""", unsafe_allow_html=True)

def preprocess(text):
    """Clean and preprocess text using NLP techniques"""
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(tokens)

@st.cache_resource
def load_resources():
    """Load data and models with caching"""
    try:
        df = pd.read_csv('imdb_2024_full.csv')
    except FileNotFoundError:
        st.error("Movie database not found. Please ensure 'imdb_2024_full.csv' exists.")
        return None, None, None
    
    df['Cleaned_Storyline'] = df['Storyline'].apply(preprocess)
    
    # Generate or load TF-IDF models
    try:
        tfidf = joblib.load('tfidf_vectorizer.joblib')
        tfidf_matrix = joblib.load('tfidf_matrix.joblib')
    except:
        st.warning("Building recommendation engine...")
        tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['Cleaned_Storyline'])
        joblib.dump(tfidf, 'tfidf_vectorizer.joblib')
        joblib.dump(tfidf_matrix, 'tfidf_matrix.joblib')
    
    return df, tfidf, tfidf_matrix

# Load data and models
df, tfidf, tfidf_matrix = load_resources()

# App Header
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg", width=120)
with col2:
    st.title("Magic Movie Finder")
    st.markdown("### Discover Similar Movies Through Storyline Magic")

# Initialize session state
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Main Content
main_col, sidebar_col = st.columns([3, 1])

with main_col:
    with st.form("main_form"):
        user_input = st.text_area(
            "**Describe a movie plot or enter an existing storyline:**",
            value=st.session_state.user_input,
            height=150,
            placeholder="Example: A young wizard begins his journey at a magical school...",
            help="Be as descriptive as possible for better results",
            key="main_input"
        )
        
        settings_col1, settings_col2 = st.columns(2)
        with settings_col1:
            num_recs = st.slider("Number of recommendations", 1, 10, 5)
        with settings_col2:
            min_score = st.slider("Minimum similarity score", 0.1, 1.0, 0.25)
        
        submitted = st.form_submit_button("Cast Recommendation Spell ✨", type="primary")
        
        if submitted:
            st.session_state.form_submitted = True

    if st.session_state.form_submitted:
        if not user_input.strip():
            st.warning("Please enter a movie description")
        elif df is not None:
            with st.spinner("Searching the magical database..."):
                # Process input
                cleaned_input = preprocess(user_input)
                input_vector = tfidf.transform([cleaned_input])
                
                # Calculate similarities
                sim_scores = cosine_similarity(input_vector, tfidf_matrix)[0]
                valid_indices = [i for i, score in enumerate(sim_scores) if score >= min_score]
                
                if not valid_indices:
                    st.warning("No magical matches found. Try a different description!")
                else:
                    # Get top recommendations
                    top_indices = sorted(valid_indices, 
                                       key=lambda i: sim_scores[i], 
                                       reverse=True)[:num_recs]
                    recommendations = df.iloc[top_indices].copy()
                    recommendations['Similarity'] = sim_scores[top_indices]
                    
                    # Display results
                    st.success(f"Found {len(recommendations)} magical matches!")
                    
                    for _, row in recommendations.iterrows():
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h3 class="title-text">{row['Movie Name']}</h3>
                            <p><span class="match-score">{row['Similarity']:.0%}</span> Match</p>
                            <p>{row['Storyline']}</p>
                        </div>
                        """, unsafe_allow_html=True)

# Sidebar Content
with sidebar_col:
    st.markdown("### Quick Access Spells")
    
    # Example Use Case
    with st.expander("✨ Example Spell", expanded=True):
        st.markdown("""
        **Input:**  
        `A young wizard begins his journey at a magical school...`
        """)
        if st.button("Use Example", key="example_button"):
            st.session_state.user_input = (
                "A young wizard begins his journey at a magical school "
                "where he makes friends and enemies, facing dark forces along the way."
            )
            st.session_state.form_submitted = True
            st.experimental_rerun()

    # Sample Movies
    st.markdown("### Recent Scrolls")
    if df is not None:
        sample_movies = df.sample(3)
        for _, movie in sample_movies.iterrows():
            with st.expander(movie['Movie Name']):
                st.write(movie['Storyline'])
                if st.button("Use This", key=f"sample_{movie['Movie Name']}"):
                    st.session_state.user_input = movie['Storyline']
                    st.session_state.form_submitted = True
                    st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("""
*Powered by magical algorithms and the IMDb spellbook*  
*Cauldron stirred with ❤️ by Movie Wizards*
""")