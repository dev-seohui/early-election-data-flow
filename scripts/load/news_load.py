import psycopg2
import pandas as pd
from config.settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from scripts.extract.news_extract import NaverBlogExtractor

class PostgresLoader:
    """네이버 블로그 데이터를 PostgreSQL에 저장하는 클래스"""

    def __init__(self):
        self.conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        self.cur = self.conn.cursor()
        self.create_table()

    def insert_data(self, blog_data):
        """데이터를 중복 방지하며 삽입"""
        if not blog_data:
            print("No new data to insert.")
            return

        df = pd.DataFrame(blog_data)
        insert_query = """
        INSERT INTO naver_blog (candidate, title, link, description, blogger_name, blogger_link, post_date, scraped_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (link) DO NOTHING;
        """
        for _, row in df.iterrows():
            self.cur.execute(insert_query, (
                row["candidate"], row["title"], row["link"], row["description"],
                row["blogger_name"], row["blogger_link"], row["post_date"], row["scraped_date"]
            ))

        self.conn.commit()
        print(f"Inserted {len(df)} records successfully.")

    def close_connection(self):
        self.cur.close()
        self.conn.close()
