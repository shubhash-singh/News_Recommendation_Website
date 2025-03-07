from gnews import GNews
import newspaper
import google.generativeai as genai
from collections import defaultdict
from googlenewsdecoder import gnewsdecoder
from newsapi import NewsApiClient
from textblob import TextBlob
from textblob.en import polarity, subjectivity


# Initialize Gemini API
GEMINI_API_KEY = "AIzaSyCsc_ClsvSjLymAZFwZIHITfiaNzA4lvh4"
NEWS_API_KEY = "f5f346835b0d424ebbfa7005c72ce0b8"
newsapi = NewsApiClient(api_key='f5f346835b0d424ebbfa7005c72ce0b8')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Initialize GNews
google_news = GNews()
google_news = GNews(
    language='en',
    country='IN',
    period='7d',
    start_date=None,
    end_date=None,
    max_results=10,
)


# Mapping of user topics to valid GNews topic
VALID_TOPIC = [
    "WORLD", "NATION", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT", "SPORTS", "SCIENCE", "HEALTH", 
    "POLITICS", "CELEBRITIES", "TV", "MUSIC", "MOVIES", "THEATER", "SOCCER", "CYCLING", "MOTOR SPORTS", 
    "TENNIS", "COMBAT SPORTS", "BASKETBALL", "BASEBALL", "FOOTBALL", "SPORTS BETTING", "WATER SPORTS", 
    "HOCKEY", "GOLF", "CRICKET", "RUGBY", "ECONOMY", "PERSONAL FINANCE", "FINANCE", "DIGITAL CURRENCIES", 
    "MOBILE", "ENERGY", "GAMING", "INTERNET SECURITY", "GADGETS", "VIRTUAL REALITY", "ROBOTICS", 
    "NUTRITION", "PUBLIC HEALTH", "MENTAL HEALTH", "MEDICINE", "SPACE", "WILDLIFE", "ENVIRONMENT", 
    "NEUROSCIENCE", "PHYSICS", "GEOLOGY", "PALEONTOLOGY", "SOCIAL SCIENCES", "EDUCATION", "JOBS", 
    "ONLINE EDUCATION", "HIGHER EDUCATION", "VEHICLES", "ARTS-DESIGN", "BEAUTY", "FOOD", "TRAVEL", 
    "SHOPPING", "HOME", "OUTDOORS", "FASHION"
]



def resolve_final_url(url):
    interval_time = 1  # interval is optional, default is None

    decoded_url = gnewsdecoder(url, interval=interval_time)

    return decoded_url["decoded_url"]
    

def scrape_article(url):
    """Scrape article content using newspaper3k."""
    try:
        # Resolve the final URL
        final_url = resolve_final_url(url)
        print(f"Final URL: {final_url}")

        # Use newspaper3k to scrape the article
        article = newspaper.Article(final_url)
        article.download()
        article.parse()

        return article.text, article.images  # Use the .text attribute to get the article content
    except Exception as e:
        print(f"Error scraping article: {e}")
        return ""

def summarize_with_gemini(text):
    """Summarize article content using Gemini."""
    if not text:
        return "Summary unavailable: Article text is empty or could not be scraped."
    
    try:
        response = model.generate_content(f"Summarize the following article in 3 sentences: {text}.")
        return response.text
    except Exception as e:
        print(f"Error summarizing with Gemini: {e}")
        return "Summary unavailable due to an error."

def add_like(topic_list, add, user_preferences):
    for topic in topic_list:
        user_preferences[topic] += add

def get_news(topic, liked_factor):
    google_news.max_results = int(20*liked_factor)
    headlines = google_news.get_news_by_topic(topic)
    articles= []
    for data in headlines:
        title = data['title']
        publisher = data.get('publisher', {}).get('title', 'unknown publisher')
        url = resolve_final_url(data['url']) 
        content, image = scrape_article(url)
        summary = summarize_with_gemini(content)
        blob = textblob(content)
        sentiment = blob.sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity
        new_dict = {
            'url': url,
            'title': title,
            'content' : content,
            'image' : image,
            'publisher': publisher,
            'summary' : summary,
            'polarity' : polarity,
            'subjectivity' : subjectivity,
        }
        articles.append(new_dict)
    return articles 

"""
reccomended_news(user_preferences) -> list of map
map{
title:
published_date:
url:
}


top_news() -> list of map
map{
title:
published_date:
url:
}

get_news_on()

"""


def Fetch_top_news():
    top_headlines = newsapi.get_top_headlines(
        language='en',
    )
    articles = top_headlines.get('articles', [])
    
    filtered_articles = []
    
    for article in articles[:11]:

        url = article.get('url')
        content, image = scrape_article(url)
        publisher = article.get('author')
        title = article.get('title')
        summary = summarize_with_gemini(content)
        blob = textblob(content)
        sentiment = blob.sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity
    
        filtered_article = {
            'url' : url,
            'title' : title,
            'content' : content,
            'image' : image,
            'publisher' : publisher,
            'summary' : summary,
            'polarity' : polarity,
            'subjectivity' : subjectivity,
        }
        filtered_articles.append(filtered_article)
    
    return filtered_articles


def Recommend_news(user_preferences):
    """
reccomended_news(user_preferences) -> list of map
map{
title:
published_date:
url:
}
    """
    if not user_preferences:
        print("no preferences recorded yet. showing top headlines instead.")
        return fetch_top_news()
    
    # calculate the total frequency of all topics
    total_frequency = sum(user_preferences.values())
    
    # normalize frequencies to calculate liked_factor (between 0 and 1)
    topics_with_liked_factor = [
        (topic, freq / total_frequency)  # liked_factor = freq / total_frequency
        for topic, freq in user_preferences.items()
    ]
    
    # fetch news for each topic and combine the results
    recommended_articles = []
    for topic, liked_factor in topics_with_liked_factor:
        # fetch news for the topic with the given liked_factor
        articles = get_news(topic, liked_factor)
        print("Article fetched")
        for article in articles:
            recommended_articles.append(article)
        
    unique_articles = list({article['url']: article for article in recommended_articles}.values())
    print(unique_articles)
    return unique_articles

def Get_topic(url):
    article_text = scrape_article(url)
    if not article_text:
        return []  # return an empty list if the article text is empty

    # prompt gemini to extract topics
    prompt = (
        "categorize the following article into one or more of the follwing topics. seperate the values by space and do not add anyother information. only the topics [world, nation, business, technology, entertainment, sports, science, health, politics, celebrities, tv, music, movies, theater, soccer, cycling, motor sports, tennis, combat sports, basketball, baseball, football, sports betting, water sports, hockey, golf,  cricket, rugby, economy, personal finance, finance, digital currencies, mobile, energy, gaming, internet security, gadgets, virtual reality, robotics, nutrition, public health, mental health, medicine, space, wildlife, environment, neuroscience, physics, geology, paleontology, social sciences, education, jobs, online education, higher education, vehicles, arts-design, beauty, food, travel, shopping, home, outdoors, fashion]. here is the article :"
            f"{article_text}"
    )
    response = model.generate_content(prompt)

    # parse the response into a list of topics
    topics = response.text.strip().split(" ")
    topics = [topic.strip() for topic in topics if topic.strip()]  # clean up the topics
    for topic in topics:
        print(topic)
    cleaned_topic = []
    for topic in topics:
        if topic in VALID_TOPIC:
            cleaned_topic.append(topic)
    return cleaned_topic
