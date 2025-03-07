from gnews import GNews
import newspaper
import google.generativeai as genai
from collections import defaultdict
from googlenewsdecoder import gnewsdecoder
from newsapi import NewsApiClient

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

# Dictionary to store user preferences
user_preferences = defaultdict(int)

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


def get_news(topic, liked_factor):
    google_news.max_results = int(20*liked_factor)
    headlines = google_news.get_news_by_topic(topic)
    article = []
    for data in headlines:
        new_dict = {'title': data['title'],
                    'published_date': data['published date'],
                    'url': resolve_final_url(data['url']) 
                    }
        article.append(new_dict)
    return article

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

def get_topic(article_text):
    """
    Extract topics from the article using Gemini.

    Args:
        article_text (str): The text of the article.

    Returns:
        list: A list of topics (strings) extracted from the article.
    """
    if not article_text:
        return []  # Return an empty list if the article text is empty

    try:
        # Prompt Gemini to extract topics
        prompt = (
            "Categorize the following article into one or more of the follwing topics. Seperate the values by space and do not add anyother information. Only the topics [WORLD, NATION, BUSINESS, TECHNOLOGY, ENTERTAINMENT, SPORTS, SCIENCE, HEALTH, POLITICS, CELEBRITIES, TV, MUSIC, MOVIES, THEATER, SOCCER, CYCLING, MOTOR SPORTS, TENNIS, COMBAT SPORTS, BASKETBALL, BASEBALL, FOOTBALL, SPORTS BETTING, WATER SPORTS, HOCKEY, GOLF,  CRICKET, RUGBY, ECONOMY, PERSONAL FINANCE, FINANCE, DIGITAL CURRENCIES, MOBILE, ENERGY, GAMING, INTERNET SECURITY, GADGETS, VIRTUAL REALITY, ROBOTICS, NUTRITION, PUBLIC HEALTH, MENTAL HEALTH, MEDICINE, SPACE, WILDLIFE, ENVIRONMENT, NEUROSCIENCE, PHYSICS, GEOLOGY, PALEONTOLOGY, SOCIAL SCIENCES, EDUCATION, JOBS, ONLINE EDUCATION, HIGHER EDUCATION, VEHICLES, ARTS-DESIGN, BEAUTY, FOOD, TRAVEL, SHOPPING, HOME, OUTDOORS, FASHION]. Here is the article :"
            f"{article_text}"
        )
        response = model.generate_content(prompt)

        # Parse the response into a list of topics
        topics = response.text.strip().split(" ")
        topics = [topic.strip() for topic in topics if topic.strip()]  # Clean up the topics
        for topic in topics:
            print(topic)
        cleaned_topic = []
        for topic in topics:
            if topic in VALID_TOPIC:
                cleaned_topic.append(topic)
        return cleaned_topic
    except Exception as e:
        print(f"Error extracting topics with Gemini: {e}")
        return []  # Return an empty list if there's an error

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
        print("No preferences recorded yet. Showing top headlines instead.")
        return
    
    # Calculate the total frequency of all topics
    total_frequency = sum(user_preferences.values())
    
    # Normalize frequencies to calculate liked_factor (between 0 and 1)
    topics_with_liked_factor = [
        (topic, freq / total_frequency)  # liked_factor = freq / total_frequency
        for topic, freq in user_preferences.items()
    ]
    
    # Fetch news for each topic and combine the results
    recommended_articles = []
    for topic, liked_factor in topics_with_liked_factor:
        # Fetch news for the topic with the given liked_factor
        articles = get_news(topic, liked_factor)
        for article in articles:
            recommended_articles.append(article)
        
    unique_articles = list({article['url']: article for article in recommended_articles}.values())
    print(unique_articles)
    return unique_articles

def Summarise_with_image (url):
    """
summary(url) -> summarised article
    """
    text, image= scrape_article(url)
    return summarize_with_gemini(text), image

def Fetch_top_headlines():
    """
Fetch_top_headlines() -> list of map
map{
title:
published_date:
url:
}
"""
    headlines = google_news.get_top_news()
    article = []
    for data in headlines:
        new_dict = {'title': data['title'],
                    'published_date': data['published date'],
                    'url': resolve_final_url(data['url']) 
                    }
        article.append(new_dict)

    return article if article else []

def Get_news_on (topic):
    """
get_news_on() -> list of map
map{
title:
published_date:
url:
}
"""
    headlines = google_news.get_news_by_topic(topic)
    article = []
    for data in headlines:
        new_dict = {
            'title': data['title'],
            'published_date': data['published date'],
            'url': resolve_final_url(data['url']),
        }
        article.append(new_dict)
    return article

def Add_like(topic_list, add):
    for topic in topic_list:
        user_preferences[topic] += add


def Fetch_top_news():
    top_headlines = newsapi.get_top_headlines(
        category='business',
        language='en',
    )

    articles = top_headlines.get('articles', [])
    
    filtered_articles = []
    
    for article in articles:
        filtered_article = {
            'website': article.get('author'),
            'title': article.get('title'),
            'publishedAt': article.get('publishedAt'),
            'url': article.get('url'),
            'urlToImage': article.get('urlToImage'),
        }
        
        filtered_articles.append(filtered_article)
    
    return filtered_articles

