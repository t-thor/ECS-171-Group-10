import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import sys
import os.path
from pydub import AudioSegment
from PIL import Image


# Paths
sys.path.insert(1, './preprocessing')
sys.path.insert(1, './model')
import wav_splitter
import generate_spectrograms
import song_predict

# imgs & audio path
img_path = os.path.dirname(__file__) + '/output/images/'
audio_path = os.path.dirname(__file__) + '/output/audio/'

st.write("""
# Music Genre Classification App
## ECS171 Group 8 Spring 2021
This app analyzes a song and classifies it into one of the 10 genres
""")

col1 = st.sidebar
col2, col3 = st.columns((2,1))

col1.header('User Input Features')

# Collects user input 
uploaded_file = col1.file_uploader("Upload your wave file", type=["wav"])

choice = col1.selectbox('Chart',('Mel Spectrogram', 'Chroma', 'Tonnetz'))
choice2 = col1.selectbox('Sampling Method', ('Beg/Mid/End', 'Quartiles', 'Sample x3(nondeterministic)', 'Random x8(nondeterministic)'))

if uploaded_file is not None:

    num_samples = 1
    if choice2 == 'Sample x3(nondeterministic)':
        num_samples = 3

    wav_splitter.wav_split(uploaded_file, num_samples)
    splitted = []
    image = []

    # generate images from user input
    for i in range(num_samples):
        splitted.append( audio_path + 'splitted{}.wav'.format(i) )

        if choice == 'Chroma':
            generate_spectrograms.gen_Chroma(splitted[i], i)
            image.append( Image.open(img_path + 'chroma{}.png'.format(i)) )

        elif choice == 'Tonnetz':
            generate_spectrograms.gen_Tonnetz(splitted[i], i)
            image.append( Image.open(img_path + 'tonnetz{}.png'.format(i)) )
        
        elif choice == 'Mel Spectrogram':
            generate_spectrograms.gen_melspectrogram(splitted[i], i)
            image.append( Image.open(img_path + 'melspec{}.png'.format(i)) )


    ### show spectrograms to user  
    if choice == 'Chroma':
        st.subheader('Chroma Chart')

    elif choice == 'Tonnetz':
        st.subheader('Tonnetz Chart')
        
    elif choice == 'Mel Spectrogram':
        st.subheader('Mel Spectrogram Chart')

    genres = ['blues','classical','country','disco','hiphop','jazz','metal','pop','reggae','rock']
    for i in range(num_samples):
        st.image(image[i], use_column_width=True)
        st.audio(splitted[i], format = 'audio/wav')
        all_probs2 = []
        all_probs2.append(song_predict.predict_song_genre(img_path + 'melspec{}.png'.format(i)))

        genre_probabilities2 = pd.DataFrame(all_probs2)
        avg_probs2 = genre_probabilities2.sum() 

        genre_probabilities2 = pd.DataFrame({
            'genre': genres,
            'probability': avg_probs
        })
        
        best_genre = genre_probabilities['probability'].idxmax()
        st.write("The genre of this clip is ...", best_genre, "!")


    # determine the song genre
    all_probs = []
    for i in range(num_samples):
        all_probs.append(song_predict.predict_song_genre(img_path + 'melspec{}.png'.format(i)))

    genre_probabilities = pd.DataFrame(all_probs)
    avg_probs = genre_probabilities.sum() / num_samples

    genre_probabilities = pd.DataFrame({
        'genre': genres,
        'probability': avg_probs
    })
    
    best_genre = genre_probabilities['probability'].idxmax()
    st.write("The genre of this song is ...", best_genre, "!")

    # show probabilities
    c = alt.Chart(genre_probabilities).mark_bar().encode(x = 'genre', y = 'probability')
    st.altair_chart(c, use_container_width=True)

else:
    st.write('Awaiting Wave file to be uploaded...') 
