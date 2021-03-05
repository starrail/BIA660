"""
Classifier2
assignment 5
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
from sklearn import svm
from time import time
import nltk
import re


def loadData(file):
    """
    read the reviews and their polarities from a given file
    :param file: the path of review file
    :return: reviews and labels
    """
    reviews, labels = [], []
    f = open(file)
    for line in f:
        review, rating = line.strip().split('\t')
        reviews.append(review.lower())
        labels.append(int(rating))
    f.close()
    return reviews, labels


def Filter(reviews):
    """
    decrease the dimension of dataset
    :param reviews: reviews from dataset
    :return: reviews without stop words
    """
    ans = []
    for review in reviews:
        temp = []
        review = re.sub(r'[^\w\s]', ' ', review)
        review = re.sub('[^a-z]', ' ', review)  # replace all non-letter characters

        ps = nltk.stem.porter.PorterStemmer()

        new_review = []
        for word in review.split():
            word = ps.stem(word)
            if word == '':
                continue  # ignore empty words and stopwords
            else:
                new_review.append(word)
        temp.append(' '.join(new_review))
        ans += temp
    return ans


def vt(predictors, counts_test, counts_train, lab_train):
    """
    Voting Classifier with different classification algorithms
    :param predictors: different classification algorithms
    :param counts_test: the transformed testing data
    :return: the accuracy score
    """
    VT = VotingClassifier(predictors)
    VT.fit(counts_train, lab_train)
    predicted = VT.predict(counts_test)
    return accuracy_score(predicted, lab_test)


def lgr_classifier(counts_train, lab_train):
    clf = LogisticRegression(solver='liblinear')
    LGR_grid = [{'penalty': ['l1', 'l2'], 'C': [0.5, 1, 1.5, 2, 3, 5, 10]}]
    gridsearchLGR = GridSearchCV(clf, LGR_grid, cv=5)
    return gridsearchLGR.fit(counts_train, lab_train)


def rf_classifier(counts_train, lab_train):
    clf = RandomForestClassifier(random_state=150, max_depth=600, min_samples_split=160)
    RF_grid = [{'n_estimators': [50, 100, 150, 200, 300, 500, 800, 1200, 1600, 2100],
                'criterion': ['gini', 'entropy'], 'max_features': ['auto', 'sqrt', 'log2']}]
    gridsearchRF = GridSearchCV(clf, RF_grid, cv=5)
    return gridsearchRF.fit(counts_train, lab_train)


def knn_classifier(counts_train, lab_train):
    clf = KNeighborsClassifier()
    KNN_grid = [{'n_neighbors': [1, 3, 5, 7, 9, 11, 13, 15, 17],
                 'weights': ['uniform', 'distance'], 'algorithm': ['auto', 'brute']}]
    gridsearchKNN = GridSearchCV(clf, KNN_grid, cv=5)
    return gridsearchKNN.fit(counts_train, lab_train)


def dt_classifier(counts_train, lab_train):
    clf = DecisionTreeClassifier()
    DT_grid = [{'max_depth': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'criterion': ['gini', 'entropy'],
                'splitter': ['best', 'random']}]
    gridsearchDT = GridSearchCV(clf, DT_grid, cv=5)
    return gridsearchDT.fit(counts_train, lab_train)


def nb_classifier(counts_train, lab_train):
    clf = MultinomialNB()
    NB_grid = [{'alpha': [0.0001, 0.001, 0.01, 0.1, 0.8, 1, 10], 'fit_prior': [True, False]}]
    gridsearchNB = GridSearchCV(clf, NB_grid, cv=5)
    return gridsearchNB.fit(counts_train, lab_train)


def svm_classifier(counts_train, lab_train):
    clf = svm.SVC()
    SVM_grid = [{'C': [0.0001, 0.001, 0.01, 0.1, 0.8, 1, 10], 'kernel': ['linear', 'poly', 'rbf', 'sigmoid']}]
    gridsearchSVM = GridSearchCV(clf, SVM_grid, cv=5)
    return gridsearchSVM.fit(counts_train, lab_train)


if __name__ == '__main__':
    start = time()
    print('start training...')

    rev_train, lab_train = loadData('/Users/yaoyuchen/Desktop/BIA660/week9/reviews_train.txt')
    rev_test, lab_test = loadData('/Users/yaoyuchen/Desktop/BIA660/week9/reviews_test.txt')

    # remove the noise
    rev_train = Filter(rev_train)
    rev_test = Filter(rev_test)

    # Build a counter based on the training dataset
    counter = CountVectorizer(stop_words=stopwords.words('english'))
    counter.fit(rev_train)

    # count the number of times each term appears in a document and transform each doc into a count vector
    counts_train = counter.transform(rev_train)  # transform the training data
    counts_test = counter.transform(rev_test)  # transform the testing data

    # fit the models
    lgr_classifier(counts_train, lab_train)
    print("Logistic regression finished")
    rf_classifier(counts_train, lab_train)
    print("Random Forest finished")
    knn_classifier(counts_train, lab_train)
    print("KNN finished")
    dt_classifier(counts_train, lab_train)
    print("Decision tree finished")
    nb_classifier(counts_train, lab_train)
    print("Naive Bayes finished")
    svm_classifier(counts_train, lab_train)
    print("SVM finished")

    predictors = [('lreg', LogisticRegression()), ('rf', RandomForestClassifier()), ('knn', KNeighborsClassifier()), ('dt', DecisionTreeClassifier()), ('nb', MultinomialNB()), ('svm', svm.SVC())]

    score = vt(predictors, counts_test, counts_train, lab_train)

    print(f"all finished, run time: {time() - start}")
    print(f"accuracy: {score}")
