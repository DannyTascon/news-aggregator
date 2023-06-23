import feedparser
from datetime import datetime
from dateutil.parser import parse
from . import db, create_app  # import your db instance and your application factory function
from myflaskapp.models import Article, Source  # import your models

def fetch_news(rss_url):
    rss_feed = feedparser.parse(rss_url)
    print(f"\nParsing RSS feed: {rss_url}")

    print(f"Number of entries found: {len(rss_feed.entries)}")
    
    if rss_feed.entries:
        print(f"First entry title: {rss_feed.entries[0].title}")
        published = rss_feed.entries[0].get('published')
        
        if published is None:
            published = datetime.now()
        else:
            published = parse(published)

        return {
            "title": rss_feed.entries[0].title,
            "link": rss_feed.entries[0].link,
            "published": published
        }

rss_urls = [
    "https://news.google.com/news/rss",
    "https://www.huffingtonpost.com/section/front-page/feed",
    "http://rss.cnn.com/rss/edition.rss",
]

# Run this script only when this file is directly run, not when it is imported
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        for url in rss_urls:
            article_data = fetch_news(url)
            if article_data:
                # Check if the source is already in the database
                source = Source.query.filter_by(rss_feed_url=url).first()
                if not source:
                    source = Source(name=url.split('//')[1].split('/')[0], rss_feed_url=url)
                    db.session.add(source)
                    
                # Check if the article already exists in the database
                existing_article = Article.query.filter_by(title=article_data['title']).first()
                if not existing_article:
                    # Add the new article
                    article = Article(
                        title=article_data['title'],
                        link=article_data['link'],
                        posted_timestamp=article_data['published'],
                        source=source
                    )
                    db.session.add(article)
        db.session.commit()  # commit the changes to the database

        # Print all articles
        for i, article in enumerate(Article.query.all(), 1):
            print(f"\nNews {i}:")
            print(f"Title: {article.title}")
            print(f"Link: {article.link}")
            print(f"Published: {article.posted_timestamp}")





