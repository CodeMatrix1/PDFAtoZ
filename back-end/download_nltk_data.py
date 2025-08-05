import nltk
import spacy

nltk_data_dir = r'C:\Users\capra\nltk_data'
nltk.data.path.append(nltk_data_dir)

nltk.download('wordnet', download_dir=nltk_data_dir)
nltk.download('averaged_perceptron_tagger', download_dir=nltk_data_dir)
nltk.download('punkt', download_dir=nltk_data_dir)
nltk.download('stopwords', download_dir=nltk_data_dir)
nltk.download('omw-1.4', download_dir=nltk_data_dir)  # <-- Add this line

# Check if spaCy English model is installed
try:
    nlp = spacy.load("en_core_web_sm")
    print("spaCy English model loaded successfully!")
except OSError:
    print("spaCy English model not found. Please run: python -m spacy download en_core_web_sm")