import feedparser
import google.generativeai as genai
import requests
import os

# ตั้งค่า API (ดึงจาก Environment Variables เพื่อความปลอดภัย)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")

def get_trending_news():
    # ใช้ RSS Feed จาก Google News ประเทศไทย
    rss_url = "https://news.google.com/rss?hl=th&gl=TH&ceid=TH:th"
    feed = feedparser.parse(rss_url)
    return feed.entries[0] # เอาข่าวล่าสุด 1 ข่าวมาทดสอบ

def summarize_news(title, link):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"สรุปข่าวหัวข้อ '{title}' จากลิงก์ {link} ให้เป็นโพสต์ Facebook สั้นๆ น่าสนใจ พร้อมใส่ Hashtag"
    response = model.generate_content(prompt)
    return response.text

def post_to_facebook(message):
    url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    payload = {'message': message, 'access_token': FB_ACCESS_TOKEN}
    requests.post(url, data=payload)

# รันขั้นตอนทั้งหมด
news = get_trending_news()
summary = summarize_news(news.title, news.link)
post_to_facebook(summary)
print("Post Success!")
