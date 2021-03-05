"""
Classifier
assignment 5
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
from sklearn import svm
from time import time
import nltk
import re
from nltk.stem import WordNetLemmatizer


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
        reviews.append(review.lower()) #convert to lower case
        labels.append(int(rating))
    f.close()
    return reviews, labels







def Filter(reviews):
    """
    decrease the dimension of dataset
    :param reviews: reviews from dataset
    :return: reviews without stop words
    """
    stopLex = set(stopwords.words('english'))  # build a set of english stopwords

    ans = []
    for review in reviews:
        temp = []
        review = re.sub(r'[^\w\s]', '', review) #remove puctuations
        #review = re.sub('[^a-z]', ' ', review)  # replace all non-letter characters
        review = re.sub(r'\d+', '', review) #remove numbers
        
        

        ps = nltk.stem.porter.PorterStemmer()
        lem = nltk.stem.WordNetLemmatizer()

        new_review = []
        for word in review.split():
            word = ps.stem(word)
            word = lem.lemmatize(word)
            if word == '' or word in stopLex:
                continue  # ignore empty words and stopwords
            else:
                new_review.append(word)
        temp.append(' '.join(new_review))
        ans += temp
    return ans











def Rdf(counts_train, lab_train, counts_test, lab_test):
    """
    Random Forest Classifier
    :param counts_train: counts_train
    :param lab_train: lab_train
    :param counts_test: counts_test
    :param lab_test: lab_test
    :return: accuracy
    """
    # train classifier
    clf = RandomForestClassifier(n_estimators=2100, criterion="entropy",max_features='log2',random_state=150,max_depth=600,min_samples_split=160)

    # train all classifier on the same dataset
    clf.fit(counts_train, lab_train)

    # use hard voting to predict (majority voting)
    pred = clf.predict(counts_test)

    # return accuracy
    score = accuracy_score(pred, lab_test)
    return score


def Bys(counts_train, lab_train, counts_test, lab_test):
    """
    Naive Bayes Classifier
    :param counts_train: counts_train
    :param lab_train: lab_train
    :param counts_test: counts_test
    :param lab_test: lab_test
    :return: accuracy
    """
    # train classifier
    clf = MultinomialNB()

    # train all classifier on the same dataset
    clf.fit(counts_train, lab_train)

    # use hard voting to predict (majority voting)
    pred = clf.predict(counts_test)

    # return accuracy
    score = accuracy_score(pred, lab_test)
    return score


def Svm(counts_train, lab_train, counts_test, lab_test):
    """
    Naive Bayes Classifier
    :param counts_train: counts_train
    :param lab_train: lab_train
    :param counts_test: counts_test
    :param lab_test: lab_test
    :return: accuracy
    """
    # train classifier
    clf = svm.SVC(C=0.85)

    # train all classifier on the same datasets
    clf.fit(counts_train, lab_train)

    # use hard voting to predict (majority voting)
    pred = clf.predict(counts_test)

    # return accuracy
    score = accuracy_score(pred, lab_test)
    return score


if __name__ == '__main__':
    start = time()
    print('start training...')

    rev_train, lab_train = loadData('/Users/mosaic/Desktop/今/BIA 660 WS/HW/6. classifier/reviews_train.txt')
    rev_test, lab_test = loadData('/Users/mosaic/Desktop/今/BIA 660 WS/HW/6. classifier/reviews_test.txt')

    rev_train = Filter(rev_train)
    rev_test = Filter(rev_test)

    # Build a counter based on the training dataset
    count_vect = CountVectorizer()
    # count_vect = TfidfVectorizer()
    count_vect.fit(rev_train)
    counts_train = count_vect.transform(rev_train)  # transform the training data
    counts_test = count_vect.transform(rev_test)  # transform the testing data
    print(f"dimension: {counts_train.getnnz()} X {counts_train[0].getnnz()}\naccuracy:")


    SVM_score = Svm(counts_train, lab_train, counts_test, lab_test)
    RDF_score = Rdf(counts_train, lab_train, counts_test, lab_test)
    #BYS_score = Bys(counts_train, lab_train, counts_test, lab_test)
    
    print(f"\t{SVM_score*100}")
    print(f"\t{RDF_score*100}")
    #print(f"\t{BYS_score*100}")

    print(f"finished, run time: {time() - start}")
