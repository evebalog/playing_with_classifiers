import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode
# nltk.download('punkt')
from nltk.tokenize import word_tokenize

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

short_pos = open("polaritydata/rt-polarity.pos", "r").read()
short_neg = open("polaritydata/rt-polarity.neg", "r").read()

documents = []

for r in short_pos.split('\n'):
    documents.append( (r, "pos") )

for r in short_neg.split('\n'):
    documents.append( (r, "neg") )

# documents = [(list(movie_reviews.words(fileid)), category)
#             for category in movie_reviews.categories()
#             for fileid in movie_reviews.fileids(category)]

print(documents[10001])

all_words = []

short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)

for w in short_pos_words:
    all_words.append(w.lower())
for w in short_neg_words:
    all_words.append(w.lower())

# all_words = []
#
# for w in movie_reviews.words():
#     all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

common_words = all_words.most_common(20)
common_words_dictionary = dict(common_words)
stop_words = list(common_words_dictionary.keys())

word_features = list(all_words.keys())[:3000]
refined_word_features = [x for x in word_features if x not in stop_words]



# print(refined_word_features)

def find_features(document):
    words = word_tokenize(document)
    # words = set(document)
    features = {}
    for w in refined_word_features:
        features[w] = (w in words)

    return features

# print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))

# random.shuffle(documents)

featuresets = [(find_features(rev), category) for (rev, category) in documents]

# random.shuffle(featuresets)
# movie_reviews data example (1-999:negative data, 1000-1999:positive data)
# training_set = featuresets[:10000]
testing_set =  featuresets[:800]

# classifier = nltk.NaiveBayesClassifier.train(training_set)

classifier_f = open("naivebayes.pickle", "rb")
classifier = pickle.load(classifier_f)
classifier_f.close()

classifier_MNB = open("MNB.pickle", "rb")
MNB_classifier = pickle.load(classifier_MNB)
classifier_MNB.close()

classifier_BernoulliNB = open("BernoulliNB.pickle", "rb")
BernoulliNB_classifier = pickle.load(classifier_BernoulliNB)
classifier_BernoulliNB.close()

classifier_LogisticRegression = open("LogisticRegression.pickle", "rb")
LogisticRegression_classifier = pickle.load(classifier_LogisticRegression)
classifier_LogisticRegression.close()

classifier_SGDClassifier = open("SGDClassifier.pickle", "rb")
SGDClassifier_classifier = pickle.load(classifier_SGDClassifier)
classifier_SGDClassifier.close()

classifier_SVC = open("SVC.pickle", "rb")
SVC_classifier = pickle.load(classifier_SVC)
classifier_SVC.close()

classifier_LinearSVC = open("LinearSVC.pickle", "rb")
LinearSVC_classifier = pickle.load(classifier_LinearSVC)
classifier_LinearSVC.close()

classifier_NuSVC = open("NuSVC.pickle", "rb")
NuSVC_classifier = pickle.load(classifier_NuSVC)
classifier_NuSVC.close()

# print("Accuracy on positive reviews:")
print("Testing accuracy on positive short reviews:")
print("(all classifiers are trained on short reviews)" )
print("Original Naive Bayes accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
# classifier.show_most_informative_features(15)

# MNB_classifier = SklearnClassifier(MultinomialNB())
# MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

# BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
# BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

# LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
# LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

# SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
# SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)

# SVC_classifier = SklearnClassifier(SVC())
# SVC_classifier.train(training_set)
print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

# LinearSVC_classifier = SklearnClassifier(LinearSVC())
# LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

# NuSVC_classifier = SklearnClassifier(NuSVC())
# NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)

voted_classifier = VoteClassifier(classifier, MNB_classifier,  LogisticRegression_classifier, SGDClassifier_classifier, SVC_classifier, LinearSVC_classifier, NuSVC_classifier)

# print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)
# print("Classification:", voted_classifier.classify(testing_set[0][0]), "Confidence %:", voted_classifier.confidence(testing_set[0][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[1][0]), "Confidence %:", voted_classifier.confidence(testing_set[1][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[2][0]), "Confidence %:", voted_classifier.confidence(testing_set[2][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[3][0]), "Confidence %:", voted_classifier.confidence(testing_set[3][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[4][0]), "Confidence %:", voted_classifier.confidence(testing_set[4][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[5][0]), "Confidence %:", voted_classifier.confidence(testing_set[5][0])*100)
# save_NuSVC_classifier = open("NuSVC.pickle", "wb")
# pickle.dump(NuSVC_classifier, save_NuSVC_classifier)
# save_NuSVC_classifier.close()
#
# save_LinearSVC_classifier = open("LinearSVC.pickle", "wb")
# pickle.dump(LinearSVC_classifier, save_LinearSVC_classifier)
# save_LinearSVC_classifier.close()
#
# save_SVCclassifier = open("SVC.pickle", "wb")
# pickle.dump(SVC_classifier, save_SVCclassifier)
# save_SVCclassifier.close()
#
# save_SGDClassifier= open("SGDClassifier.pickle", "wb")
# pickle.dump(SGDClassifier_classifier, save_SGDClassifier)
# save_SGDClassifier.close()
#
# save_LogisticRegression_classifier = open("LogisticRegression.pickle", "wb")
# pickle.dump(LogisticRegression_classifier, save_LogisticRegression_classifier)
# save_LogisticRegression_classifier.close()
#
# save_BernoulliNB_classifier = open("BernoulliNB.pickle", "wb")
# pickle.dump(BernoulliNB_classifier, save_BernoulliNB_classifier)
# save_BernoulliNB_classifier.close()
#
# save_MNBclassifier = open("MNB.pickle", "wb")
# pickle.dump(MNB_classifier, save_MNBclassifier)
# save_MNBclassifier.close()
#
# save_classifier = open("naivebayes.pickle", "wb")
# pickle.dump(classifier, save_classifier)
# save_classifier.close()
