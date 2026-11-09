#!/usr/bin/env python3
"""
Auto-Update Football Trends & Insights
ใช้ Google Gemini API (ฟรี!) ค้นหาข่าวและวิเคราะห์โอกาสทางการขาย
"""

import os
import json
import google.generativeai as genai
from datetime import datetime

# Google Gemini API Key (from environment variable)
API_KEY = os.environ.get('GOOGLE_GEMINI_API_KEY')

if not API_KEY:
    print("❌ Error: GOOGLE_GEMINI_API_KEY not found in environment variables")
    exit(1)

# Configure Gemini
try:
    genai.configure(api_key=API_KEY)
    # Use stable model (gemini-1.5-flash) instead of experimental
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("✅ Gemini API configured successfully")
except Exception as e:
    print(f"❌ Error configuring Gemini: {e}")
    exit(1)

# Get current month/year
now = datetime.now()
thai_months = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
               'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
current_month = thai_months[now.month - 1]
current_year = now.year

print(f"🗓️  กำลังอัพเดทข้อมูลประจำ {current_month} {current_year}")
print("=" * 60)

# Prompt for Claude
prompt = f"""## 🎯 Mission: ค้นหาข่าวฟุตบอลและวิเคราะห์โอกาสทางการขาย

**เดือนปัจจุบัน:** {current_month} {current_year}

---

## ขั้นตอนที่ 1: ค้นหาข่าวฟุตบอล (8-10 ข่าว)

ค้นหาข่าวล่าสุดจาก 3 ลีก:
- **ทีมชาติไทย**: 2-3 ข่าว
- **ไทยลีก**: 2-3 ข่าว
- **พรีเมียร์ลีก**: 2-3 ข่าว

Search keywords:
- "ทีมชาติไทย {current_month} {current_year}"
- "ไทยลีก {current_month} {current_year}"
- "พรีเมียร์ลีก ไทย {current_month} {current_year}"

**Format:**
```json
[
  {{
    "Tag": "ทีมชาติไทย",
    "Title": "หัวข้อข่าว",
    "Description": "รายละเอียดข่าว 2-3 ประโยค",
    "Date": "9 พ.ย. 2026",
    "Source_URL": "https://..."
  }}
]
```

---

## ขั้นตอนที่ 2: วิเคราะห์ Sales Insights (3-5 insights)

วิเคราะห์โอกาสทางธุรกิจจากข่าวที่พบ

แต่ละ insight ต้องมี:
- **opportunity**: ชื่ออุตสาหกรรม/กลุ่มลูกค้า
- **stats**: ["stat1", "stat2", "stat3"] - ตัวเลขเฉพาะเจาะจง
- **reasoning**: 2-3 ประโยค อธิบายข้อมูลและแนวโน้ม
- **analysis**: 3-4 ประโยค วิเคราะห์เชิงลึก + อ้างอิง Survey data
- **target_clients**: 6-8 บริษัทจริงในไทย
- **pitch_angle**: แนวทางการเสนอขายที่มี mechanic ชัดเจน
- **icon**: emoji ที่เหมาะสม

**Format:**
```json
[
  {{
    "opportunity": "โรงพยาบาล & ประกันสุขภาพ",
    "stats": ["พบข่าวบาดเจ็บ 8 รายการ", "นักเตะหลักบาดเจ็บ 5 ราย"],
    "reasoning": "...",
    "analysis": "...",
    "target_clients": ["AIA", "Cigna", ...],
    "pitch_angle": "...",
    "icon": "🏥"
  }}
]
```

---

## Output Format:

ส่งผลลัพธ์เป็น JSON object:

```json
{{
  "trends": [...],
  "insights": [...]
}}
```

**ห้าม:**
- ใส่ markdown code block (```json)
- ใส่คำอธิบายเพิ่มเติม
- แค่ JSON object เท่านั้น

**เริ่มได้เลย!**
"""

print("🤖 กำลังเรียก Google Gemini API (ฟรี!)...")
print("")

try:
    # Call Gemini API
    response = model.generate_content(prompt)

    # Extract response
    response_text = response.text

    # Parse JSON (remove markdown code blocks if present)
    response_text = response_text.strip()
    if response_text.startswith('```json'):
        response_text = response_text[7:]
    if response_text.startswith('```'):
        response_text = response_text[3:]
    if response_text.endswith('```'):
        response_text = response_text[:-3]
    response_text = response_text.strip()

    # Parse JSON
    data = json.loads(response_text)

    trends = data.get('trends', [])
    insights = data.get('insights', [])

    print(f"✅ ได้ข้อมูลจาก Claude API:")
    print(f"   📊 Trends: {len(trends)} ข่าว")
    print(f"   💡 Insights: {len(insights)} insights")
    print("")

    # Save to files
    os.makedirs('data', exist_ok=True)

    # Save trends.json
    with open('data/trends.json', 'w', encoding='utf-8') as f:
        json.dump(trends, f, ensure_ascii=False, indent=2)
    print("✅ บันทึก data/trends.json")

    # Save insights.json
    with open('data/insights.json', 'w', encoding='utf-8') as f:
        json.dump(insights, f, ensure_ascii=False, indent=2)
    print("✅ บันทึก data/insights.json")

    print("")
    print("=" * 60)
    print("🎉 อัพเดทสำเร็จ!")
    print("=" * 60)

except json.JSONDecodeError as e:
    print(f"❌ JSON Parse Error: {e}")
    print(f"Response: {response_text[:500]}")
    exit(1)

except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
