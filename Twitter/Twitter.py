"""
Twitter
assignment 4
"""

from selenium import webdriver
import time
import re


def getTweetsFromComments(url, scrollNum=1000):
    cnter = 0
    # open the browser and visit the url
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    time.sleep(2)

    already_seen = set()  # keeps track of tweets we have already seen.

    popular_tweet = 'N/A'
    tweet_num = 0
    for i in range(scrollNum):

        # find all elements that have the value "tweet" for the data-testid attribute
        tweets = driver.find_elements_by_css_selector('div[data-testid="tweet"]')

        for tweet in tweets:
            if tweet in already_seen: continue  # we have seen this tweet before while scrolling down, ignore
            already_seen.add(tweet)  # first time we see this tweet. Mark as seen and process.

            txt = 'NA'

            try:
                txt = tweet.find_element_by_css_selector(
                    "div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0").text
                txt = txt.replace('\n', ' ')
            except:
                print('no text')

            try:
                comment_num = tweet.find_element_by_css_selector('div[data-testid="reply"]').text
                if comment_num == '':
                    continue
                if comment_num[-1] == 'K':
                    num = float(comment_num[:-1]) * 1000
                else:
                    num = float(comment_num)

                if num > tweet_num:
                    tweet_num = num
                    popular_tweet = txt
            except:
                print('no comment_num')

            cnter += 1
            if cnter == 30:
                return popular_tweet

        # scroll down twice to load more tweets
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)


def getTweetsFromLikes(url, scrollNum=1000):
    cnter = 0
    # open the browser and visit the url
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    time.sleep(2)

    already_seen = set()  # keeps track of tweets we have already seen.

    popular_tweet = 'N/A'
    tweet_num = 0
    for i in range(scrollNum):

        # find all elements that have the value "tweet" for the data-testid attribute
        tweets = driver.find_elements_by_css_selector('div[data-testid="tweet"]')

        for tweet in tweets:
            if tweet in already_seen: continue  # we have seen this tweet before while scrolling down, ignore
            already_seen.add(tweet)  # first time we see this tweet. Mark as seen and process.

            txt = 'NA'
            like_num = 'NA'

            try:
                txt = tweet.find_element_by_css_selector(
                    "div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0").text
                txt = txt.replace('\n', ' ')
            except:
                print('no text')

            try:
                like_num = tweet.find_element_by_css_selector('div[data-testid="like"]').text
                if like_num == '':
                    continue
                if like_num[-1] == 'K':
                    num = float(like_num[:-1]) * 1000
                else:
                    num = float(like_num)

                if num > tweet_num:
                    tweet_num = num
                    popular_tweet = txt
            except:
                print('no like_num')

            cnter += 1
            if cnter == 30:
                return popular_tweet

        # scroll down twice to load more tweets
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)


def run(url1, url2):
    tweet1 = re.findall(r"[\w']+", getTweetsFromComments(url1))
    tweet2 = re.findall(r"[\w']+", getTweetsFromLikes(url2))

    ans = set(tweet1) & set(tweet2)
    # ans = set(tweet1) | set(tweet2)

    print(tweet1)
    print('------------------')
    print(tweet2)

    return ans


if __name__ == '__main__':
    start = time.time()

    url1 = 'https://twitter.com/realdonaldtrump'
    url2 = 'https://twitter.com/shaq'
    print(run(url1, url2))

    print(f"run time: {time.time() - start}")
