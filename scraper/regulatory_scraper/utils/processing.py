import spacy
from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer
import warnings
import fitz
import re 
from langchain_community.llms import Ollama

# Filter out the specific sklearn warning about token patterns
warnings.filterwarnings("ignore", message="The parameter 'token_pattern' will not be used since 'tokenizer' is not None")


# Load spaCy English model
nlp = spacy.load('en_core_web_sm')

# Explicitly specify the model for summarization
kw_model = KeyBERT()
vectorizer = KeyphraseCountVectorizer(spacy_pipeline=nlp, pos_pattern='<J.*>*<N.*>+')

llm = Ollama(
    model="llama3"
)

def get_keywords(file_text):
    """
    This function extracts keywords from the provided text using KeyBERT and KeyphraseVectorizers.
    It focuses on noun phrases that are contextually relevant to the document's content.
    """
    # Extract keyphrases
    keyphrases = vectorizer.fit_transform([file_text])
    keywords = kw_model.extract_keywords(docs=[file_text], vectorizer=vectorizer, top_n=8)
    
    # Return only the keywords, stripping out the scores for simplicity in this example
    return [keyword for keyword, _ in keywords]

def clean_hyphenated_words(text):
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
    return text

def extract_text_with_pymupdf(pdf_body):
    doc = fitz.open("pdf", pdf_body)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    doc.close()
    return clean_hyphenated_words(text)

def get_summary(file_text):
    summary = llm.invoke("Tell me a joke")

    print(summary)