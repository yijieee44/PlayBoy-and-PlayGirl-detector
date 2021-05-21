import pickle
from src.utils.short_form import SHORT_FORM
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import warnings
warnings.filterwarnings("ignore")


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


with open('model.pkl', 'rb') as myfile:
    model = pickle.load(myfile)


def predict(text):
    predicted = model.predict_proba([text])
    return predicted[0][1]


def main():
    print(predict("can we have a meeting later?"))


if __name__ == "__main__":
    main()