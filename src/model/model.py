import pickle
import warnings
import os


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


with open('model.pkl', 'rb') as myfile:
    model = pickle.load(myfile)


def predict(text):
    predicted = model.predict_proba([text])
    return predicted[0][1]


def main():
    ospath = os.getcwd().replace("\\", "/").split("model")[0] + "replies"
    for txtfile in os.listdir(ospath):
        if not txtfile.startswith("SAMPLE"):  # if want to see prediction on sample txt file, remove the negation "not"
            directory = os.path.join(ospath, txtfile)
            file = open(directory, "r")
            compiledmessages = file.read().replace("\n", " ")
            print(compiledmessages)
            file.close()
            print(predict(compiledmessages))
    # print(predict("can we have a meeting later?"))


if __name__ == "__main__":
    main()