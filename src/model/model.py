import pickle
import warnings

from src.utils.short_form import SHORT_FORM
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

warnings.filterwarnings("ignore")

# import nltk
# nltk.download()  # uncomment these two lines to download nltk data


def preprocess(content):
    content = content.lower()

    # convert short form to word
    content = " ".join([t if t not in SHORT_FORM else SHORT_FORM[t].lower() for t in content.split()])

    tokenizer = RegexpTokenizer(r'[a-z]+')
    tokens = tokenizer.tokenize(content)

    # lemmatization
    lemmatiser = WordNetLemmatizer()
    tokens = [lemmatiser.lemmatize(t.lower(), pos='v') for t in tokens]

    return " ".join(tokens)


def predict(text):
    with open('src/model/model.pkl', 'rb') as myfile:
        model = pickle.load(myfile)
    predicted = model.predict_proba([text])
    return predicted[0][1]


def predict_from_text (name):
    replies_dir = "src/replies/" + name + ".txt"
    file = open(replies_dir, "r")
    compiled_messages = file.read().replace("\n", " ")
    file.close()

    return predict(compiled_messages), compiled_messages
