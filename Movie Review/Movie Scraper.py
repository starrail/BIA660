from bs4 import BeautifulSoup
import re
import time
import requests
import csv

def run(url):
    
    fw = open('review.text', 'w', encoding='utf8') #output file
    
    writer = csv.writer(fw, lineterminator='\n') #create a csv writer for the file
    
    #run first two web pages
    for p in range(1,3):
        
        print("page", p)
        html = None
        
        if p==1: pageLink=url
        else: pageLink = url + '?type=&sort=&page=' + str(p)
        
        #check url response
        for i in range(5): #try 5 times
            response = requests.get(pageLink, headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/6.1.6 Safari/537.78.2'})
            if response:
                break
            else: time.sleep(2) #wait two seconds for response  
        if not response: return None
        
        #load web html
        html = response.text #read in the text from the file 
        
        soup = BeautifulSoup(html, 'html') #parse the html
        
        reviews = soup.findAll('div', {'class':'row review_table_row'}) #get all review divs
        
        # write file
        for review in reviews:
            
            #initialize
            critic,rating,source,text,date = 'NA', 'NA', 'NA', 'NA', 'NA' 
            
            #critic
            criticChunk = review.find('a', {'href':re.compile('/critic/')})
            if criticChunk: critic = criticChunk.text.strip()
            
            #rating
            if review.find('div', {'class': 'review_icon icon small rotten'}): rating = "rotten"
            elif review.find('div', {'class': 'review_icon icon small fresh'}): rating = "fresh"
            
            #source
            sourceChunk = review.find('em', {'class': 'subtle'})
            if sourceChunk: source = sourceChunk.text.strip()
            
            #text
            textChunk = review.find('div', {'class': "the_review"})
            if textChunk: text = textChunk.text.strip()
            
            #date
            dateChunk = review.find('div', {'class': 'review-date'})
            if dateChunk: date = dateChunk.text.strip()
                      
            
            writer.writerow([critic,rating,source,text,date]) # write to file 
    
    fw.close()
    
if __name__ == '__main__':   
    url='https://www.rottentomatoes.com/m/django_unchained_2012/reviews'
    run(url)
    
    
    
    
    
    
    
    
    
    
    
