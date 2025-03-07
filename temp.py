from gnews import GNews

google_news = GNews()
news = google_news.get_news_by_topic('WORLD')
headline = news[0]
publisher_name = headline.get('publisher', {}).get('title', 'Unknown Publisher')
print(publisher_name)
