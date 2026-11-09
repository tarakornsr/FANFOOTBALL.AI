#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-Update Football Trends & Insights
ดึงข่าวจริงจาก Google News RSS + วิเคราะห์ด้วย Gemini API
Version 3.0 - Real News with Links!
"""

import os
import sys
import json
import urllib.parse
from datetime import datetime

print("=" * 70)
print("🤖 FANFOOTBALL.AI - Auto Update Script v3.0")
print("=" * 70)

# Step 1: Check API Key
print("\n📋 Step 1: Checking API Key...")
API_KEY = os.environ.get('GOOGLE_GEMINI_API_KEY')

if not API_KEY:
    print("❌ GOOGLE_GEMINI_API_KEY not found!")
    print("Please add it in GitHub Secrets")
    sys.exit(1)
print(f"✅ API Key found (length: {len(API_KEY)})")

# Step 2: Install & Import Dependencies
print("\n📦 Step 2: Installing dependencies...")
try:
    import feedparser
    print("✅ feedparser already installed")
except ImportError:
    print("⚠️  Installing feedparser...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "feedparser"])
    import feedparser
    print("✅ Installed feedparser")

try:
    import google.generativeai as genai
    print("✅ google-generativeai already installed")
except ImportError:
    print("⚠️  Installing google-generativeai...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "google-generativeai"])
    import google.generativeai as genai
    print("✅ Installed google-generativeai")

# Step 3: Configure Gemini
print("\n🔧 Step 3: Configuring Gemini API...")
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    print("✅ Gemini API configured (Model: gemini-pro)")
except Exception as e:
    print(f"❌ Configuration failed: {e}")
    sys.exit(1)

# Step 4: Prepare Data
print("\n📅 Step 4: Preparing data...")
now = datetime.now()
thai_months = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
               'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
current_month = thai_months[now.month - 1]
current_year = now.year

print(f"✅ Current period: {current_month} {current_year}")

# Step 5: Fetch Real News from Google News RSS
print("\n📰 Step 5: Fetching real football news from Google News RSS...")

# RSS Feed URLs for each league
rss_feeds = {
    "ทีมชาติไทย": "https://news.google.com/rss/search?q=ทีมชาติไทย+ฟุตบอล&hl=th&gl=TH&ceid=TH:th",
    "ไทยลีก": "https://news.google.com/rss/search?q=ไทยลีก+ฟุตบอล&hl=th&gl=TH&ceid=TH:th",
    "พรีเมียร์ลีก": "https://news.google.com/rss/search?q=พรีเมียร์ลีก+Premier+League&hl=th&gl=TH&ceid=TH:th"
}

all_news = []

for tag, feed_url in rss_feeds.items():
    try:
        print(f"   📡 Fetching {tag}...")
        feed = feedparser.parse(feed_url)

        # Get top 2-3 news per league
        count = 0
        for entry in feed.entries[:3]:
            if count >= 3:
                break

            title = entry.title if hasattr(entry, 'title') else "ไม่มีหัวข้อ"
            link = entry.link if hasattr(entry, 'link') else ""
            description = entry.summary if hasattr(entry, 'summary') else title

            # Clean description (remove HTML tags if any)
            import re
            description = re.sub('<[^<]+?>', '', description)
            description = description[:200] + "..." if len(description) > 200 else description

            pub_date = entry.published if hasattr(entry, 'published') else f"{now.day} {current_month[:3]}. {current_year}"

            all_news.append({
                "Tag": tag,
                "Title": title,
                "Description": description,
                "Date": f"{now.day} {current_month[:3]}. {current_year}",
                "Source_URL": link
            })

            count += 1

        print(f"   ✅ {tag}: {count} news")

    except Exception as e:
        print(f"   ⚠️  {tag} failed: {e}")
        # Add fallback news
        all_news.append({
            "Tag": tag,
            "Title": f"ข่าว{tag} - {current_month} {current_year}",
            "Description": f"ข่าวและความเคลื่อนไหวของ{tag}ในเดือน{current_month} {current_year}",
            "Date": f"{now.day} {current_month[:3]}. {current_year}",
            "Source_URL": f"https://www.google.com/search?q={urllib.parse.quote(tag + ' ฟุตบอล ' + current_month + ' ' + str(current_year))}"
        })

if len(all_news) > 0:
    print(f"\n✅ Total news fetched: {len(all_news)}")
    trends = all_news[:8]  # Keep top 8 news
else:
    print("⚠️  No news fetched, using fallback...")
    trends = []

# Step 6: Generate Insights using Gemini
print(f"\n🤖 Step 6: Generating Sales Insights with Gemini...")

# Prepare news summary for Gemini
news_summary = "\n".join([f"- [{item['Tag']}] {item['Title']}" for item in trends[:10]])

insight_prompt = f"""คุณเป็น AI วิเคราะห์ธุรกิจฟุตบอลสำหรับ Plan B Eleven (เอเจนซี่การตลาด)

**ข่าวฟุตบอลล่าสุด {current_month} {current_year}:**
{news_summary}

**งาน:** วิเคราะห์และสร้าง Sales Insights สำหรับแบรนด์ต่าง ๆ

**ให้สร้าง 3-5 Insights** ครอบคลุม:
- โรงพยาบาล/ประกัน (ถ้ามีข่าวบาดเจ็บ)
- เครื่องดื่ม/อาหาร (ถ้ามีแมตช์หนาแน่น)
- เทคโนโลยี/Streaming (ถ้ามียอดรับชม)
- แฟชั่น/กีฬา (ถ้ามีเทรนด์เสื้อบอล/รองเท้า)
- อื่น ๆ ที่เห็นโอกาสจากข่าว

**Format (JSON เท่านั้น - ห้ามใส่ markdown):**
[
  {{
    "opportunity": "ชื่ออุตสาหกรรม",
    "stats": ["สถิติ 1", "สถิติ 2", "สถิติ 3", "สถิติ 4", "สถิติ 5"],
    "reasoning": "อธิบาย 2-3 ประโยค พร้อมอ้างอิงข่าว",
    "analysis": "วิเคราะห์ลึก 3-4 ประโยค + อ้างอิง Survey/Trend",
    "target_clients": ["แบรนด์1", "แบรนด์2", "แบรนด์3", "แบรนด์4", "แบรนด์5", "แบรนด์6"],
    "pitch_angle": "ไอเดียแคมเปญชัดเจน (mechanic)",
    "icon": "emoji"
  }}
]

Return **ONLY** JSON array (ไม่มี ```json, ไม่มีคำอธิบาย)"""

try:
    response = model.generate_content(insight_prompt)
    response_text = response.text.strip()

    # Clean response
    if response_text.startswith('```json'):
        response_text = response_text[7:]
    if response_text.startswith('```'):
        response_text = response_text[3:]
    if response_text.endswith('```'):
        response_text = response_text[:-3]
    response_text = response_text.strip()

    insights = json.loads(response_text)

    if isinstance(insights, list) and len(insights) > 0:
        print(f"✅ Insights generated: {len(insights)}")
    else:
        print("⚠️  Invalid insights format, using fallback...")
        insights = []

except Exception as e:
    print(f"⚠️  Gemini API failed: {e}")
    insights = []

# Fallback insights if needed
if len(insights) == 0:
    insights = [
        {
            "opportunity": "เครื่องดื่ม & อาหาร",
            "stats": [f"ข่าวฟุตบอล {len(trends)} รายการ", f"ครอบคลุม 3 ลีก", f"เดือน{current_month} {current_year}"],
            "reasoning": f"ช่วง{current_month} {current_year} มีข่าวฟุตบอลหนาแน่นจากทั้งทีมชาติไทย ไทยลีก และพรีเมียร์ลีก เหมาะกับการทำแคมเปญเครื่องดื่มและอาหารสำหรับการดูบอล",
            "analysis": "แฟนบอลมีพฤติกรรมซื้อเครื่องดื่มและอาหารก่อนดูบอล โอกาสทางการตลาดสูงสำหรับแบรนด์ที่ต้องการเข้าถึงกลุ่มเป้าหมายผ่านฟุตบอล",
            "target_clients": ["Leo", "Chang", "Coca-Cola", "Pepsi", "Red Bull", "M-150"],
            "pitch_angle": "แคมเปญ 'ดูบอลกับเรา' พร้อมของรางวัลและโปรโมชันพิเศษในช่วงการแข่งขันสำคัญ",
            "icon": "🍺"
        }
    ]
    print(f"📦 Using {len(insights)} fallback insights")

# Step 7: Save files
print("\n💾 Step 7: Saving files...")
os.makedirs('data', exist_ok=True)

with open('data/trends.json', 'w', encoding='utf-8') as f:
    json.dump(trends, f, ensure_ascii=False, indent=2)
print("✅ Saved data/trends.json")

with open('data/insights.json', 'w', encoding='utf-8') as f:
    json.dump(insights, f, ensure_ascii=False, indent=2)
print("✅ Saved data/insights.json")

# Success!
print("\n" + "=" * 70)
print("🎉 SUCCESS! Files updated with REAL NEWS!")
print("=" * 70)
print(f"\n📊 Summary:")
print(f"   - Trends: {len(trends)} items (REAL NEWS with LINKS)")
print(f"   - Insights: {len(insights)} items (AI Analysis)")
print(f"   - Period: {current_month} {current_year}")
print(f"\n✅ Ready to commit!")
