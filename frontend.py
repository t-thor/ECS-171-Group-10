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
# Music Genre Classification
## ECS171 Group 8 Final Project
### University of California, Davis
This app analyzes a song and classifies it into one of the 10 genres
""")

col1 = st.sidebar
col2, col3 = st.columns((2,1))

col1.header('User Input Features')

# Collects user input 
uploaded_file = col1.file_uploader("Upload your wave file", type=["wav"])

choice = col1.selectbox('Chart',('Mel Spectrogram', 'Chroma', 'Tonnetz'))
choice2 = col1.selectbox('Sampling Method (for full length songs only)', 
    ('Beg/Mid/End',
    'Quartiles',
    'Sample x3 (nondeterministic)',
    'Sample x7 (nondeterministic)',
    'Sample x15 (nondeterministic)'))

if uploaded_file is not None:
    num_samples = 1
    audio_ms = len(AudioSegment.from_wav(uploaded_file))
    if 1:
        if choice2 == 'Sample x3(nondeterministic)':
            num_samples = 3
        elif choice2 == 'Sample x7(nondeterministic)':
            num_samples = 7
        elif choice2 == 'Sample x15(nondeterministic)':
            num_samples = 15

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


    ### show clip images and classifications to user  
    if choice == 'Chroma':
        st.subheader('Chroma Chart')

    elif choice == 'Tonnetz':
        st.subheader('Tonnetz Chart')
        
    elif choice == 'Mel Spectrogram':
        st.subheader('Mel Spectrogram Chart')

    genres = ['blues','classical','country','disco','hiphop','jazz','metal','pop','reggae','rock']
    all_probs = []
    for i in range(num_samples):
        st.image(image[i], use_column_width=True)
        st.audio(splitted[i], format = 'audio/wav')
        probs = song_predict.predict_song_genre(img_path + 'melspec{}.png'.format(i))
        all_probs.append(probs)
        samp_genre = max(probs, key=probs.get)
        st.write( samp_genre, "!")
        st.write( samp_genre, " has been to determined to be the most likely genre of this sample clip.")
        st.markdown('---')

    # determine the song genre
    genre_probabilities = pd.DataFrame(all_probs)
    avg_probs = genre_probabilities.sum() / num_samples

    genre_probabilities = pd.DataFrame({
        'genre': genres,
        'probability': avg_probs
    })
    
    # show final results
    best_genre = genre_probabilities['probability'].idxmax()
    st.write("""
        ## Final analysis:
        The genre of this song is ...
        """, best_genre, "!" )
        
   
    c = alt.Chart(genre_probabilities).mark_bar().encode(x = 'genre', y = 'probability')
    st.altair_chart(c, use_container_width=True)

else:
    st.write('Awaiting Wave file to be uploaded...') 
