import json
from datetime import datetime, timedelta
from pathlib import Path

# === إعداد ملف الاهتمامات ===
with open("interests.json", "r", encoding="utf-8") as f:
    interests = json.load(f)["categories"]

# === إعداد ملف .ics ===
ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\nPRODID:-//Taamoul Calendar//EN\n"

# === توليد أحداث تجريبية بناءً على الاهتمامات ===
start_date = datetime.now()
for i, category in enumerate(interests):
    event_date = start_date + timedelta(days=i)
    ics_content += f"""BEGIN:VEVENT
UID:event-{i+1}@taamoul.com
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{event_date.strftime('%Y%m%dT100000Z')}
DTEND:{event_date.strftime('%Y%m%dT110000Z')}
SUMMARY:📌 حدث {category}
DESCRIPTION:تم إنشاء هذا الحدث لاختبار عرض التقويم للفئة: {category}
LOCATION:Dubai, UAE
STATUS:CONFIRMED
END:VEVENT
"""

# === إغلاق ملف التقويم ===
ics_content += "END:VCALENDAR\n"

# === حفظ الملف ===
Path("live_calendar.ics").write_text(ics_content, encoding="utf-8")
print("✅ تم إنشاء ملف التقويم بنجاح.")# Python script to generate .ics file with OpenAI integration
