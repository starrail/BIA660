import pandas as pd
import re

#from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
#import nltk
from nltk.corpus import stopwords

from sklearn.svm import LinearSVC

jobs = pd.read_csv('/Users/mosaic/Desktop/660 Project/import dataset/Jobs.csv')

text = jobs['text'].to_frame()

#clean text
def clean(text):

    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text=re.sub(r'@[A-Za-z0-9]+','',text)
    text=re.sub(r'#','',text)
    text=re.sub(r'RT[\s]+','',text)
    text=re.sub(r'[^\w]', ' ', text)
    
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub('[^a-z]', ' ', text)
    
    text = re.sub('data sci[a-z]+', ' ', text, re.I)
    text = re.sub('data eng[a-z]+', ' ', text, re.I)
    text = re.sub('software eng[a-z]+', ' ', text, re.I)
    return text

jobs['clear_text'] = jobs['text'].apply(clean)

X = jobs['clear_text']
y = jobs['title']

counter = CountVectorizer(stop_words=stopwords.words('english'))
counter_fit = counter.fit(X)
X_train = counter_fit.transform(X)
#X_test = counter.transform(X_test)

text_trans_tf = TfidfTransformer().fit(X_train)
X_train = text_trans_tf.transform(X_train)
#X_test = text_trans_tf.transform(X_test)

LSVC_model = LinearSVC().fit(X_train, y)
LSVC_pre = LSVC_model.predict(X_train)
#target_names=["DS","SE","DE"]
#print("classification report：", classification_report(y_test, LSVC_pre, target_names=target_names))

def label(target):
    if target==1:
        return "Data Scientist"
    elif target==2:
        return "Software Engineer"
    else:
        return "Data Engineer"
    
LSVC_df = pd.DataFrame(LSVC_pre)
predict = LSVC_df[0].apply(label) #label y vairable
predict = predict.to_frame()
predict["text"] = jobs['text']
predict = predict.rename(columns={0: "job title"})
predict.to_csv("prediction.csv", index=False)




