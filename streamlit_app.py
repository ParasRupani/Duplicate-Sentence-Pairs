# Importing necessary libraries
import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from helper import preprocess  # Importing custom preprocessing function
import pickle

# Loading pre-trained machine learning model
model = pickle.load(open('./models/sgdc_con_calib.pkl','rb'))

# Loading SentenceTransformer model
helper_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Streamlit interface
st.header('Duplicate Question Pairs')

# Input fields for questions
q1 = st.text_input('Enter Question 1')
q2 = st.text_input('Enter Question 2')

# Button to trigger duplicate detection
if st.button('Find'):
    # Preprocessing input questions
    q1 = preprocess(q1)
    q2 = preprocess(q2)

    # Encoding questions using SentenceTransformer
    sentences = [q1, q2]
    embeddings = helper_model.encode(sentences)

    
    # Concatenating the embeddings before predicting
    embeddings_list = [embeddings.flatten()]
    embeddings_array = np.array(embeddings_list)

    # Predicting duplicate or not using the pre-trained model
    result = model.predict_proba([embeddings[0]*embeddings[1]])[0]

    if result[1] > 0.5:
        st.success('Duplicate, Score: {}'.format(round(result[1], 2)))
    else:
        st.success('Not Duplicate, Score: {}'.format(round(result[1], 2)))