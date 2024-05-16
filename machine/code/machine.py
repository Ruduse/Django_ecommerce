import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import style

style.use("ggplot")
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

df = pd.read_csv("amazon_alexa.tsv", sep="\t")
print(df.head())
print(df.info())

sns.countplot(x="rating", data=df)
plt.show()

fig = plt.figure(figsize=(7, 7))
colors = ("red", "gold", "yellowgreen", "cyan", "orange")
wp = {"linewidth": 2, "edgecolor": "black"}
tags = df["rating"].value_counts()
explode = (0.1, 0.1, 0.2, 0.3, 0.2)
tags.plot(
    kind="pie",
    autopct="%1.1f",
    colors=colors,
    shadow=True,
    startangle=0,
    wedgeprops=wp,
    explode=explode,
    label="",
)
plt.title("Distribution of the different ratings")
plt.show()

fig = plt.figure(figsize=(30, 7))
sns.countplot(x="variation", data=df)
plt.show()

fig = plt.figure(figsize=(20, 10))
sns.countplot(y="variation", data=df)
plt.show()

print(df["variation"].value_counts())

sns.countplot(x="feedback", data=df)
plt.show()

fig = plt.figure(figsize=(7, 7))
tags = df["feedback"].value_counts()
tags.plot(kind="pie", autopct="%1.1f%%", label="")
plt.title("Distribution of the different sentiments")
plt.show()

for i in range(5):
    print(df["verified_reviews"].iloc[i], "\n")


def data_processing(text):
    text = text.lower()
    text = re.sub(r"http\S+www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[^\w\s]", "", text)
    text_tokens = word_tokenize(text)
    filtered_text = [w for w in text_tokens if not w in stop_words]
    return " ".join(filtered_text)


df.verified_reviews = df["verified_reviews"].apply(data_processing)

stemmer = PorterStemmer()


def stemming(data):
    text = [stemmer.stem(word) for word in data]
    return data


df["verified_reviews"] = df["verified_reviews"].apply(lambda x: stemming(x))

for i in range(5):
    print(df["verified_reviews"].iloc[i], "\n")

pos_reviews = df[df.feedback == 1]
print(pos_reviews.head())

text = " ".join([word for word in pos_reviews["verified_reviews"]])
plt.figure(figsize=(20, 15), facecolor="None")
wordcloud = WordCloud(max_words=500, width=1600, height=800).generate(text)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Most frequent words in positive reviews", fontsize=19)
plt.show()

neg_reviews = df[df.feedback == 0]
print(neg_reviews.head())

text = " ".join([word for word in neg_reviews["verified_reviews"]])
plt.figure(figsize=(20, 15), facecolor="None")
wordcloud = WordCloud(max_words=500, width=1600, height=800).generate(text)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Most frequent words in negative reviews", fontsize=19)
plt.show()

X = df["verified_reviews"]
Y = df["feedback"]

cv = CountVectorizer()
X = cv.fit_transform(df["verified_reviews"])

x_train, x_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

print("Size of x_train: ", (x_train.shape))
print("Size of y_train: ", (y_train.shape))
print("Size of x_test: ", (x_test.shape))
print("Size of y_test: ", (y_test.shape))

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

logreg = LogisticRegression()
logreg.fit(x_train, y_train)
logreg_pred = logreg.predict(x_test)
logreg_acc = accuracy_score(logreg_pred, y_test)
print("Test accuracy: {:.2f}%".format(logreg_acc * 100))

print(confusion_matrix(y_test, logreg_pred))
print("\n")
print(classification_report(y_test, logreg_pred))
