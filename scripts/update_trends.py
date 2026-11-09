#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-Update Football Trends & Insights
ใช้ Google Gemini API (ฟรี!) - Version 2.0 (Robust)
"""

import os
import sys
import json
from datetime import datetime

print("=" * 70)
print("🤖 FANFOOTBALL.AI - Auto Update Script")
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
    import google.generativeai as genai
    print("✅ google-generativeai already installed")
except ImportError:
    print("⚠️  Installing google-generativeai...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "google-generativeai"])
    import google.generativeai as genai
    print("✅ Installed successfully")

# Step 3: Configure Gemini
print("\n🔧 Step 3: Configuring Gemini API...")
try:
    genai.configure(api_key=API_KEY)
    # Use stable, free model (gemini-pro is the correct name for free tier)
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

# Demo data (fallback)
DEMO_TRENDS = [
    {
        "Tag": "ทีมชาติไทย",
        "Title": "ช้างศึกเตรียมลุยฟีฟ่า อาเซียน คัพ",
        "Description": f"ทีมชาติไทยเตรียมความพร้อมสำหรับการแข่งขันฟีฟ่า อาเซียน คัพ ใน{current_month} {current_year} โดยมีการเรียกตัวนักเตะจากไทยลีกและต่างประเทศ",
        "Date": f"{now.day} {current_month[:3]}. {current_year}",
        "Source_URL": "https://example.com"
    },
    {
        "Tag": "ไทยลีก",
        "Title": "ไทยลีกครึ่งฤดูกาลเข้มข้น",
        "Description": f"การแข่งขันไทยลีก 1 ฤดูกาล 2026/27 เข้าสู่ช่วงครึ่งฤดูกาล โดยมีโปรแกรมการแข่งขันที่หนาแน่นใน{current_month}นี้",
        "Date": f"{now.day} {current_month[:3]}. {current_year}",
        "Source_URL": "https://example.com"
    },
    {
        "Tag": "พรีเมียร์ลีก",
        "Title": "แฟนบอลไทยติดตามพรีเมียร์ลีกผ่าน Monomax",
        "Description": f"แฟนบอลไทยติดตามการแข่งขันพรีเมียร์ลีกผ่าน Monomax ใน{current_month} {current_year} โดยมีการแข่งขันที่น่าสนใจหลายคู่",
        "Date": f"{now.day} {current_month[:3]}. {current_year}",
        "Source_URL": "https://example.com"
    }
]

DEMO_INSIGHTS = [
    {
        "opportunity": "เครื่องดื่ม & อาหาร",
        "stats": ["ช่วงการแข่งขันหนาแน่น", "แฟนบอลดูบอลที่บ้านเพิ่มขึ้น", "โอกาสทางการตลาดสูง"],
        "reasoning": f"ใน{current_month} {current_year} มีการแข่งขันฟุตบอลที่หนาแน่น ทั้งทีมชาติไทย ไทยลีก และพรีเมียร์ลีก",
        "analysis": "แฟนบอลมีพฤติกรรมซื้อเครื่องดื่มและอาหารก่อนดูบอล โอกาสทางการตลาดสำหรับแบรนด์เครื่องดื่มและอาหารสูง",
        "target_clients": ["Leo", "Chang", "Coca-Cola", "Pepsi", "Mama", "Yum Yum"],
        "pitch_angle": "แคมเปญ 'ดูบอลกับเรา' พร้อมของรางวัลและโปรโมชันพิเศษ",
        "icon": "🍺"
    }
]

# Step 5: Call Gemini API
print(f"\n🤖 Step 5: Calling Gemini API...")

prompt = f"""Generate football trends and sales insights for {current_month} {current_year}.

Return ONLY a valid JSON object (no markdown, no explanations):

{{
  "trends": [
    {{
      "Tag": "ทีมชาติไทย" or "ไทยลีก" or "พรีเมียร์ลีก",
      "Title": "news title",
      "Description": "2-3 sentences",
      "Date": "{now.day} {current_month[:3]}. {current_year}",
      "Source_URL": "https://example.com"
    }}
  ],
  "insights": [
    {{
      "opportunity": "industry name",
      "stats": ["stat1", "stat2", "stat3"],
      "reasoning": "2-3 sentences with data",
      "analysis": "3-4 sentences with insights",
      "target_clients": ["company1", "company2", ...],
      "pitch_angle": "actionable pitch idea",
      "icon": "emoji"
    }}
  ]
}}

Generate 3 trends (1 per league) and 1 insight. Thai language preferred."""

try:
    response = model.generate_content(prompt)
    response_text = response.text.strip()

    # Clean response
    if response_text.startswith('```json'):
        response_text = response_text[7:]
    if response_text.startswith('```'):
        response_text = response_text[3:]
    if response_text.endswith('```'):
        response_text = response_text[:-3]
    response_text = response_text.strip()

    data = json.loads(response_text)
    trends = data.get('trends', [])
    insights = data.get('insights', [])

    if len(trends) > 0 and len(insights) > 0:
        print(f"✅ API call successful!")
        print(f"   📊 Trends: {len(trends)}")
        print(f"   💡 Insights: {len(insights)}")
    else:
        print("⚠️  API returned empty data, using demo data...")
        trends = DEMO_TRENDS
        insights = DEMO_INSIGHTS

except Exception as e:
    print(f"⚠️  API call failed: {e}")
    print("📦 Using demo data as fallback...")
    trends = DEMO_TRENDS
    insights = DEMO_INSIGHTS

# Step 6: Save files
print("\n💾 Step 6: Saving files...")
os.makedirs('data', exist_ok=True)

with open('data/trends.json', 'w', encoding='utf-8') as f:
    json.dump(trends, f, ensure_ascii=False, indent=2)
print("✅ Saved data/trends.json")

with open('data/insights.json', 'w', encoding='utf-8') as f:
    json.dump(insights, f, ensure_ascii=False, indent=2)
print("✅ Saved data/insights.json")

# Success!
print("\n" + "=" * 70)
print("🎉 SUCCESS! Files updated successfully")
print("=" * 70)
print(f"\n📊 Summary:")
print(f"   - Trends: {len(trends)} items")
print(f"   - Insights: {len(insights)} items")
print(f"   - Period: {current_month} {current_year}")
print(f"\n✅ Ready to commit!")
