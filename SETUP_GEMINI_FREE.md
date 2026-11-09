# 🎁 Setup Guide: 100% Automated + ฟรี! (Google Gemini API)

## ✅ สิ่งที่ได้รับ:

**100% Fully Automated + ไม่ต้องจ่ายเงิน:**
```
GitHub Actions รันทุกวันที่ 1 (07:00 Bangkok)
→ เรียก Google Gemini API (ฟรี!)
→ ค้นหาข่าวฟุตบอล + วิเคราะห์ Sales Insights
→ สร้าง JSON files
→ Auto commit & push
→ Website อัพเดทอัตโนมัติ
```

**💰 ค่าใช้จ่าย: ฟรี 100%!**

---

## 📋 ขั้นตอน Setup (ครั้งเดียว - 10 นาที):

### **Step 1: สร้าง Google Gemini API Key (ฟรี!)**

1. **ไปที่:** https://aistudio.google.com/apikey

2. **Login ด้วย Google Account** (account ธรรมดาก็ได้)

3. คลิก **"Create API Key"** (ปุ่มสีน้ำเงิน)

4. เลือก:
   - **Create API key in new project** (ถ้ายังไม่มี project)
   - หรือเลือก existing project

5. **Copy API Key** (จะขึ้นทันที):
   ```
   AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

6. **เก็บไว้** (จะใช้ในขั้นตอนถัดไป)

**หมายเหตุ:**
- ✅ **ไม่ต้องใส่บัตรเครดิต**
- ✅ Free tier: 15 requests/minute, 1,500 requests/day
- ✅ เพียงพอสำหรับรันเดือนละครั้ง

---

### **Step 2: เพิ่ม API Key ใน GitHub Secrets**

1. ไปที่: https://github.com/tarakornsr/FANFOOTBALL.AI/settings/secrets/actions

2. คลิก **"New repository secret"**

3. กรอก:
   - **Name**: `GOOGLE_GEMINI_API_KEY`
   - **Secret**: paste API Key ที่ copy มา

4. คลิก **"Add secret"**

5. ✅ เสร็จ!

---

### **Step 3: เปิด Workflow Permissions (สำคัญ!)**

1. ไปที่: https://github.com/tarakornsr/FANFOOTBALL.AI/settings/actions

2. เลื่อนลงไปหา **"Workflow permissions"**

3. เลือก:
   - ☑️ **"Read and write permissions"**

4. คลิก **"Save"**

---

### **Step 4: อัพโหลดไฟล์ขึ้น GitHub**

อัพโหลดไฟล์เหล่านี้:

```
.github/workflows/update-trends.yml  ← (แก้ไขแล้ว - ใช้ Gemini)
scripts/update_trends.py             ← (แก้ไขแล้ว - ใช้ Gemini)
data/.gitkeep
index.html
SETUP_GEMINI_FREE.md (ไฟล์นี้)
```

**วิธีอัพโหลด:**

1. ไปที่ https://github.com/tarakornsr/FANFOOTBALL.AI
2. กด **"Add file"** → **"Upload files"**
3. ลากไฟล์ทั้งหมดจาก Desktop/Project AI/ มาวาง
4. Commit message: `Setup Gemini API - 100% Free Automation`
5. กด **"Commit changes"**

---

### **Step 5: ทดสอบรัน!**

1. ไปที่: https://github.com/tarakornsr/FANFOOTBALL.AI/actions

2. เลือก workflow: **"🤖 Auto-Update Football Trends & Insights"**

3. คลิก **"Run workflow"** → **"Run workflow"**

4. **รอ 2-3 นาที**

5. **เช็คผลลัพธ์:**
   - ✅ Status = Success (✓ สีเขียว)
   - ✅ มี commit ใหม่: "🤖 Auto-update..."
   - ✅ ใน folder `data/` มี:
     - `trends.json`
     - `insights.json`

6. **เปิดเว็บไซต์:** https://tarakornsr.github.io/FANFOOTBALL.AI/
   - รอ 1-2 นาที (GitHub Pages deploy)
   - กด **Ctrl+Shift+R** (Hard refresh)
   - ✅ **ควรเห็นข้อมูลใหม่!**

---

## 🎉 เสร็จแล้ว!

**หลังจากนี้:**
- ✅ GitHub Actions รันอัตโนมัติทุกวันที่ 1 ของเดือน
- ✅ **ฟรี 100% - ไม่ต้องจ่ายเงินเลย!**
- ✅ ไม่ต้องทำอะไรเพิ่ม

---

## 🐛 Troubleshooting:

### **ถ้า Workflow ล้มเหลว:**

**Error: "GOOGLE_GEMINI_API_KEY not found"**
- → เช็คว่าใส่ Secret ใน GitHub ถูกต้อง
- → ชื่อต้องเป็น `GOOGLE_GEMINI_API_KEY`

**Error: "API key not valid"**
- → เช็คว่า API Key ที่ copy ถูกต้อง
- → ลองสร้าง API Key ใหม่

**Error: "Permission denied (push)"**
- → ไปที่ Settings → Actions → General
- → เลือก "Read and write permissions"
- → Save

**Error: "Rate limit exceeded"**
- → ไม่น่าจะเกิด (free tier = 1,500 requests/day)
- → รอ 1 ชั่วโมงแล้วลองใหม่

---

## 💰 ค่าใช้จ่าย:

### **Google Gemini API:**
- ✅ **ฟรี 100%!**
- ✅ ไม่ต้องใส่บัตรเครดิต
- ✅ Free quota: 1,500 requests/day
- ✅ รันเดือนละครั้ง = ใช้ free tier ได้ตลอด!

### **GitHub Actions:**
- ✅ **ฟรี!** (Public repository)
- ✅ 2,000 minutes/month

**สรุป: ไม่มีค่าใช้จ่ายเลย!** 🎁

---

## 📊 Monitoring:

**ดู Workflow History:**
- https://github.com/tarakornsr/FANFOOTBALL.AI/actions

**ดู Latest Data:**
- https://github.com/tarakornsr/FANFOOTBALL.AI/tree/master/data

**ดูเว็บไซต์:**
- https://tarakornsr.github.io/FANFOOTBALL.AI/

---

## 🎯 Quick Start Checklist:

- [ ] สร้าง Gemini API Key (ฟรี)
- [ ] เพิ่ม Secret ใน GitHub
- [ ] เปิด Workflow Permissions
- [ ] อัพโหลดไฟล์ทั้งหมด
- [ ] ทดสอบรัน manual 1 ครั้ง
- [ ] ✅ เสร็จ - ปล่อยให้รันอัตโนมัติ!

---

**🎉 Happy Free Automating!** 🚀

**ไม่ต้องจ่ายเงินสักบาท!**
