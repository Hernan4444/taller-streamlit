import re
import string

import altair as alt
import nltk
import pandas as pd
from nltk.corpus import stopwords

import streamlit as st

nltk.download('stopwords')

st.markdown(
    """
    <style>
    .stActionButton{
        visibility: hidden;
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def remove_numbers_and_punctuation(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    text = ' '.join(filtered_words)
    return text


def load_data(data_path):
    mc_df = pd.read_csv('McDonald_s_Reviews.csv', encoding="latin-1")
    mc_df = mc_df.dropna()
    mc_df['rating'] = mc_df['rating'].apply(lambda x: int(x.split()[0]))
    mc_df['latitude'] = mc_df['latitude'].astype(float)
    mc_df['longitude'] = mc_df['longitude'].astype(float)
    mc_df['review'] = mc_df['review'].str.lower()
    return mc_df


def add_title_and_description():
    st.title('Taller Streamlit')
    st.markdown('Con este taller pondremos a prueba **algunas** de las funcionalidades de Streamlit.')


def should_show_data(mc_df):
    checkbox = st.checkbox('¿Mostrar todos los datos?', value=False)
    if checkbox:
        search_term = st.text_input('Buscar por palabra')
        if search_term:
            results = mc_df[mc_df['review'].str.contains(search_term)]
            st.write(results)
            return results
        else:
            st.write(mc_df)
            return mc_df
    return mc_df


def create_two_columns():
    return st.columns(2)


def plot_rating_histogram(mc_df, column):
    column.header('Histograma de valoraciones')
    altair_chart = alt.Chart(mc_df).mark_bar().encode(
        x=alt.X('rating:N', bin=alt.Bin(binned=True)),
        y='count()',
    )
    column.altair_chart(altair_chart)


def plot_word_frequency_bar_chart(mc_df, column):
    column.header('20 Palabras más frecuentes en reviews')
    word_frequency = mc_df['review'].apply(
        lambda x: remove_numbers_and_punctuation(x)
    ).str.split(expand=True).stack().value_counts()
    word_frequency = word_frequency.reset_index()[0:20]
    word_frequency.columns = ['word', 'amount']
    altair_chart = alt.Chart(word_frequency).mark_bar().encode(
        x=alt.X('word', sort='-y'),
        y='amount'
    )
    column.altair_chart(altair_chart)


def add_mcdonalds_map(mc_df):
    st.header('Mapa de McDonald\'s con reviews')
    unique_locations = mc_df[['latitude', 'longitude']].drop_duplicates()
    st.map(unique_locations)


add_title_and_description()
mc_data = load_data('McDonald_s_Reviews.csv')
filtered_mc_df = should_show_data(mc_data)
column_1, column_2 = create_two_columns()
plot_rating_histogram(filtered_mc_df, column_1)
plot_word_frequency_bar_chart(filtered_mc_df, column_2)
add_mcdonalds_map(filtered_mc_df)

