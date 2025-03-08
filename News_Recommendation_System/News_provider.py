from gnews import GNews
import requests
import tldextract
import json
from newspaper import Article
from newspaper.article import ArticleException
import google.generativeai as genai
from googlenewsdecoder import gnewsdecoder
from newsapi import NewsApiClient
from textblob import TextBlob
from textblob.en import polarity, subjectivity


# Initialize Gemini API
GEMINI_API_KEY = "AIzaSyC_hvafYx0Jdmilr3l1wwPPbHFdULViqbc"
# NEWS_API_KEY = "f5f346835b0d424ebbfa7005c72ce0b8"
newsapi = NewsApiClient(api_key='b128924ffe9e45db93e9cc73284b34c3')
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


def get_domain(url):
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"
    return domain

def resolve_final_url(url):
    interval_time = 1  # interval is optional, default is None

    decoded_url = gnewsdecoder(url, interval=interval_time)

    return decoded_url["decoded_url"]
    
def check_news_source(url):
    """
    Check the bias, factual reporting, and credibility of a given URL based on the provided JSON file.

    :param url: The URL of the news source to check.
    :param json_file: The path to the JSON file containing the news source data.
    :return: A dictionary containing the bias, factual reporting, and credibility of the URL.
             Returns None if the URL is not found in the JSON file.
    """
    domain = get_domain(url)
    json_file = 'News_Recommendation_System/bias-check.json'  # Replace with the actual path to your JSON file
    # Load the JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    if domain in data:
        return data[domain]
    else:
        return data["default"]


def scrape_article(url):
    """Scrape article content using newspaper3k."""
    # Set a User-Agent header to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        # Fetch the HTML content using requests
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 403, 404)

        # Create an Article object
        article = Article(url)

        # Download and parse the article using the fetched HTML
        article.download(input_html=response.text)
        article.parse()

        # Extract the image and text
        image = article.top_image
        text = article.text

        return text, image

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the article: {e}")
        return "","" 
    except ArticleException as e:
        print(f"Failed to parse the article: {e}")
        return "","" 



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
        domain = get_domain(url)
        content, image = scrape_article(url)
        summary = summarize_with_gemini(content)
        blob = TextBlob(content)
        sentiment = blob.sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity
        new_dict = {
            'url': url,
            'title': title,
            'content' : content,
            'image' : image,
            'domain' : domain,
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
        domain = get_domain(url)
        title = article.get('title')
        summary = summarize_with_gemini(content)
        blob = TextBlob(content)
        sentiment = blob.sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity
        bias = check_news_source(url)
    
        filtered_article = {
            'url' : url,
            'title' : title,
            'content' : content,
            'image' : image,
            'domain' : domain,
            'publisher' : publisher,
            'summary' : summary,
            'polarity' : polarity,
            'subjectivity' : subjectivity,
        }
        for key, value in bias.items():
            filtered_article[key] = value
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
        return Fetch_top_news()
    
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
