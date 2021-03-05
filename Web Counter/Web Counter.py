import re
from nltk.corpus import stopwords
import requests
from collections import Counter

def run(url1, url2, url3):
    #buid three dictionaries to store words and frequencies for three websites
    word_freq1={}
    word_freq2={}
    word_freq3={}
    
    stopLex=set(stopwords.words('english')) # build a set of english stopwrods 
    
    #check if the urls work
    def scrape(url):
        word_freq={}
        for i in range(5):
            response = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/6.1.6 Safari/537.78.2'})
            if response:
                break
            else: print('failed attempt',i)
        if not response: return None #all five attempts fail
        
        #get text from response
        text = response.text
        text = re.sub('[^a-z]', ' ', text.lower()) #replace no characters with whitespace
        words = text.split(' ') #split text to get words
        
        for word in words:
            if word=='' or word in stopLex: continue
            else: word_freq[word] = word_freq.get(word,0)+1
        
        return word_freq
    
    word_freq1 = Counter(scrape(url1))
    word_freq2 = Counter(scrape(url2))
    word_freq3 = Counter(scrape(url3))
    
    #select words
    ans = set()
    for word, freq in word_freq2.items():
        if word_freq1[word] < word_freq2[word] < word_freq3[word]:
            ans.add(word)
    return ans
 

url1 = 'https://raw.githubusercontent.com/starrail/BIA660/master/Web%20Counter/1.txt'
url2 = 'https://raw.githubusercontent.com/starrail/BIA660/master/Web%20Counter/2.txt'
url3 = 'https://raw.githubusercontent.com/starrail/BIA660/master/Web%20Counter/3.txt'

print(run(url1, url2, url3))







