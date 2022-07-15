from django.shortcuts import render
from NLP.models import Contact
import string
from collections import Counter
from datetime import datetime
 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import sys, re
from textblob import TextBlob
import tweepy


# Creating your views here.
def home(request):
    return render(request, 'home.html')

def text(request):
    
    return render(request, 'text.html')

def tweet(request):
    return render(request, 'tweet.html')

def contact(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        name = request.POST.get("name1")
        query = request.POST.get("query")
        contact = Contact(name=name, email=email, query=query, date = datetime.today())
        contact.save()
    return render(request, 'contact.html')

def result(request):
    if request.method == 'GET':
        text = request.GET.get("text")
        lower_case = text.lower()
        cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

        
        tokenized_words = word_tokenize(cleaned_text, "english")

        
        final_words = []
        for word in tokenized_words:
            if word not in stopwords.words("english"):
                final_words.append(word)
        
        
        lemma_words = []
        for word in final_words:
            word = WordNetLemmatizer().lemmatize(word)
            lemma_words.append(word)
        
        emotion_list = []
        with open('emotions.txt', 'r') as file:
            for line in file:
                clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
                word, emotion = clear_line.split(':')
        
                if word in lemma_words:
                    emotion_list.append(emotion)
        
        
        w = Counter(emotion_list)        
        
        
        
        fig, ax1 = plt.subplots()
        ax1.bar(w.keys(), w.values())
        fig.autofmt_xdate()
        plt.title('Feelings From the text you entered')
        plt.savefig('D:/Study Material/SEM 2 SD project/Web- Sntimental Analysis/analysis/statics/Text1Analysis')
        plt.close()
    return render(request, 'result.html')

def result2(request):
    if request.method == 'GET':  
        def DownloadData():
           
            consumerKey = 'z9OQ8uZHDGce5AEsZahKSarMH'
            consumerSecret = 'IvwzR3sLsg04wfFfYjPENWNHv5hYjeLiyrUl5SXn60ALz62zww'
            accessToken = '1214740888678584320-C5qOOcZacPsnVjNygkI3x6VKzgCCbq'
            accessTokenSecret = 'WoNHIvQpXv0IBvXx8H6KQOlWMmTaaEuMuB8HI9xnGfkjU'
            auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
            auth.set_access_token(accessToken, accessTokenSecret)
            api = tweepy.API(auth)
        
            
            searchTerm = request.GET.get("tweettext")
            NoOfTerms = int(request.GET.get("tweetnumber"))
        
            
            tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)
            for tweet in tweets:
                tweetText.append((tweet.text).encode('utf-8'))
            return(tweetText)
    
        def TweetAnalysis():
            
            lower_case = text.lower()
        
           
            cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

        
            tokenized_words = word_tokenize(cleaned_text, "english")

        
            final_words = []
            for word in tokenized_words:
                if word not in stopwords.words("english"):
                    final_words.append(word)
        
        
            lemma_words = []
            for word in final_words:
                word = WordNetLemmatizer().lemmatize(word)
                lemma_words.append(word)
    
            
            emotion_list = []
            with open('emotions.txt', 'r') as file:
                for line in file:
                    clear_line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
                    word, emotion = clear_line.split(':')
                    if word in lemma_words:
                        emotion_list.append(emotion)
        
        
            w = Counter(emotion_list)
        
            fig, ax1 = plt.subplots()
            ax1.bar(w.keys(), w.values())
            fig.autofmt_xdate()
            plt.title('How people are Feeling..')
            plt.savefig('D:/Study Material/SEM 2 SD project/Web- Sntimental Analysis/analysis/statics/graph.png')
            plt.close()

        tweets = []
        tweetText = []
        DownloadData()
        text_1 = b" ".join(tweetText)
        text = text_1.decode()
        TweetAnalysis()

        
        def Tweetpie():
            class SentimentAnalysis:
                def DownloadTweet(self):
                    self.tweets = []
                    self.tweetText = []

                    
                    consumerKey = 'z9OQ8uZHDGce5AEsZahKSarMH'
                    consumerSecret = 'IvwzR3sLsg04wfFfYjPENWNHv5hYjeLiyrUl5SXn60ALz62zww'
                    accessToken = '1214740888678584320-C5qOOcZacPsnVjNygkI3x6VKzgCCbq'
                    accessTokenSecret = 'WoNHIvQpXv0IBvXx8H6KQOlWMmTaaEuMuB8HI9xnGfkjU'
                    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
                    auth.set_access_token(accessToken, accessTokenSecret)
                    api = tweepy.API(auth)

                   
                    searchTerm = request.GET.get("tweettext")
                    NoOfTerms = int(request.GET.get("tweetnumber"))

                    
                    self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)



                    
                    polarity = 0
                    positive = 0
                    wpositive = 0
                    spositive = 0
                    negative = 0
                    wnegative = 0
                    snegative = 0
                    neutral = 0


                   
                    for tweet in self.tweets:
                       
                        self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
                     
                        analysis = TextBlob(tweet.text)
                      
                        polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

                        if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                            neutral += 1
                        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                            wpositive += 1
                        elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                            positive += 1
                        elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                            spositive += 1
                        elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                            wnegative += 1
                        elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                            negative += 1
                        elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                            snegative += 1



                    # finding average of how people are reacting
                    positive = self.percentage(positive, NoOfTerms)
                    wpositive = self.percentage(wpositive, NoOfTerms)
                    spositive = self.percentage(spositive, NoOfTerms)
                    negative = self.percentage(negative, NoOfTerms)
                    wnegative = self.percentage(wnegative, NoOfTerms)
                    snegative = self.percentage(snegative, NoOfTerms)
                    neutral = self.percentage(neutral, NoOfTerms)

                    # finding average reaction
                    polarity = polarity / NoOfTerms

                    self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)


                def cleanTweet(self, tweet):
                    # Remove Links, Special Characters etc from tweet
                    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

                
                def percentage(self, part, whole):
                    temp = 100 * float(part) / float(whole)
                    return format(temp, '.2f')

                def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
                    labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                              'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
                    sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
                    colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
                    explode = [0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07]
                    patches, texts = plt.pie(sizes, colors=colors, explode=explode, shadow=True, wedgeprops={'edgecolor':'black'})
                    plt.legend(patches, labels, loc="best")
                    plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
                    plt.axis('equal')
                    plt.tight_layout()
                    plt.savefig('/Study Material/SEM 2 SD project/Web- Sntimental Analysis/analysis/statics/Tweet2Pie.png')
                    plt.close()

            sa = SentimentAnalysis()
            sa.DownloadTweet()
        Tweetpie()
    return render(request, 'result2.html')
