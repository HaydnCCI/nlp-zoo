import click
from PIL import Image
import tensorflow as tf
import streamlit as st
from languageModels.GPT2 import sequenceExtend, sequenceExtend_aitextgen, demoGPT2
from languageModels.QA import answerQuery
from utils.database import load_database

@st.cache
def textGen(input_text, model_selected, max_length):
    """ Generate text based on given words
    """
    with st.spinner("This is AI and I am thinking about how to extend your words, hmmm..."):
        
        tf.random.set_seed(0) 

        if model_selected == "GPT2":
            gpt_text = sequenceExtend(input_text, max_length=max_length)

        elif model_selected == "GPT2-Aigentext":
            gpt_text = sequenceExtend_aitextgen(input_text, max_length=max_length)

        elif model_selected == "GPT3":
            pass

    return gpt_text


@st.cache
def questionAnswer(query):
    """ Question Answering with BERT
    """
    with st.spinner("This is AI and I am thinking about how to extend your words, hmmm..."):
        bert_text = answerQuery(query)

    return bert_text


def st_big_title():    
    st.markdown("""
    <style>
    .big-font {
        font-size:40px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">Natural Language Processing Zoo</p>', unsafe_allow_html=True)
    st.write("Author: Haydn Cheong")

def main():
    icon = Image.open('img/icon.png')
    # Ref: https://github.com/streamlit/streamlit/issues/1770
    st.set_page_config(layout="centered", initial_sidebar_state="auto", page_title="NLP Zoo", page_icon=icon)

    st_big_title()

    # image = Image.open('img/cover.png')
    # st.image(image, caption='Image by K.Johnson via https://venturebeat.com/', use_column_width=True)

    st.title("AI text generator")
    st.write("Currently only support model GPT2")

    image = Image.open('img/gpt2_cover.png')
    st.image(image, caption='Image by K.Johnson via https://venturebeat.com/', use_column_width=True)
    

    """
    Text generation
    """
    model_selected = st.selectbox("Which language model do you prefer?", 
                ("GPT2", "GPT2-Aigentext", "GPT3"))
    st.text(f"You selected: {model_selected}")
    max_length = st.number_input("Put the maximum number of words here."
                                , value = 100
                                , step = 5
                                , min_value = 20
                                , max_value = 2000)
    input_text = st.text_input(label= "Enter your text here.", value="Food is happiness.")
    gpt_text = textGen(input_text, model_selected, max_length)
    # Display results
    if len(gpt_text) > 0:
        st.success("AI generated text for you!")
        st.write(gpt_text)
    else:
        st.success("Hmm... Please rephrase your words.")


    st.title("AI question answering")
    st.write("Using model BERT. Flexibility in database in progress")

    image = Image.open('img/bert_cover.png')
    st.image(image, caption='Image by A.Singh via https://medium.com/', use_column_width=True)

    query_text = st.text_input("Enter your text here", value="What is excellence?")
    bert_text = questionAnswer(query_text)
    # Display results
    if len(bert_text) > 0:
        st.success("AI answered your query!")
        st.write(f"Hey, I believe: {bert_text['answer']}")
        st.write(f"I got my idea from the {bert_text['title']}")
        st.write(f"Let me show you an example.")
        st.write(f"{bert_text['paragraph']}")
    else:
        st.success("Hmm, please clarify a little bit...")



if __name__ == "__main__":
    main()