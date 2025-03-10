import urllib.request
import json
from datetime import datetime
from config.settings import CLIENT_ID, CLIENT_SECRET
import psycopg2
from config.settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

class NaverBlogExtractor:
    """네이버 API에서 블로그 데이터를 가져오는 클래스"""

    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET

    def get_candidate_names(self):
        """PostgreSQL에서 후보 목록 가져오기"""
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT candidate_name FROM candidate_info;")
        candidates = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return candidates

    def fetch_blog_data(self):
        """네이버 블로그 API 호출하여 데이터 수집"""
        candidates = self.get_candidate_names()
        all_blog_data = []

        for candidate in candidates:
            encText = urllib.parse.quote(candidate)
            url = f"https://openapi.naver.com/v1/search/blog?query={encText}"

            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", self.client_id)
            request.add_header("X-Naver-Client-Secret", self.client_secret)

            try:
                response = urllib.request.urlopen(request)
                rescode = response.getcode()

                if rescode == 200:
                    response_body = response.read().decode("utf-8")
                    response_json = json.loads(response_body)

                    blog_data = [
                        {
                            "candidate": candidate,
                            "title": item["title"].replace("<b>", "").replace("</b>", ""),
                            "link": item["link"],
                            "description": item["description"].replace("<b>", "").replace("</b>", ""),
                            "blogger_name": item["bloggername"],
                            "blogger_link": item["bloggerlink"],
                            "post_date": item["postdate"],
                            "scraped_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                        for item in response_json.get("items", [])
                    ]
                    all_blog_data.extend(blog_data)

            except Exception as e:
                print(f"Error fetching blog data: {e}")

        return all_blog_data
