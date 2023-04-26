# Import dependencies
from collections import defaultdict
from heapq import nlargest
# from io import StringIO
from string import punctuation

# If you have problems in install nltk, try the options:
import nltk
nltk.download('stopwords')
nltk.download('punkt')
import streamlit as st
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize

import PyPDF2


# Functions for resume in Spanish
stopwords_es = set(stopwords.words('spanish') + list(punctuation))


def remove_stopwords_and_punct_in_spanish(text):
    words = word_tokenize(text.lower())
    return [word for word in words if word not in stopwords_es]


def summarize_text_spanish(text, n_sent=2):
    words_not_stopwords = remove_stopwords_and_punct_in_spanish(text)
    sentences = sent_tokenize(text)
    frequency = FreqDist(words_not_stopwords)
    important_sentences = defaultdict(int)

    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in frequency:
                important_sentences[i] += frequency[word]

    numb_sent = n_sent
    idx_important_sentences = nlargest(numb_sent,
                                       important_sentences,
                                       important_sentences.get)

    for i in sorted(idx_important_sentences):
        st.write(sentences[i])


def main():
    st.title('Resumen de textos con NLP :hugging_face:')
    st.markdown("<h4 '>¡Sube un archivo en formato PDF y elige el número de frases que consideras importantes para\
        tu resumen! ¡El procesamiento de lenguaje natural y las estadísticas harán el resto!</h4>", unsafe_allow_html=True)
    st.write('')

    # Upload file
    file_uploaded = st.file_uploader("Upload a PDF file", type=["pdf"])

    if file_uploaded is not None:
        pdf_reader = PyPDF2.PdfReader(file_uploaded)
        full_text = ""
        for page in range(len(reader.pages)):
            full_text += pdf_reader.getPage(page).extractText()

        # Sidebar Menu
        options = ["Español"]
        menu = st.sidebar.selectbox("Elige el idioma:", options)

        # Choices
        if menu == "Español":
            st.title("Este es el resumen de tu texto :unlock:")
            n_sent = st.sidebar.slider('Elige el número de frases importantes:', value=1)
            summarize_text_spanish(full_text, n_sent)

        st.sidebar.info('Revisa el proyecto en [Github](https://github.com/marinaramalhete/NLP-Text-Summary-App)')


if __name__ == '__main__':
    main()
