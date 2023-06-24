from myflaskapp.news_fetcher import fetch_news, rss_urls
from myflaskapp import create_app, db
from myflaskapp.models import Article, Source

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
