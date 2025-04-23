import json
from datetime import datetime, timedelta
from pathlib import Path

# === إعداد ملف الاهتمامات ===
with open("interests.json", "r", encoding="utf-8") as f:
    interests = json.load(f)["categories"]

# === إعداد ملف .ics ===
ics_content = (
    "BEGIN:VCALENDAR\n"
    "VERSION:2.0\n"
    "CALSCALE:GREGORIAN\n"
    "PRODID:-//Taamoul Calendar//EN\n"
)

# === توليد أحداث تجريبية بناءً على الاهتمامات ===
start_date = datetime.now()
for i, category in enumerate(interests):
    event_date = start_date + timedelta(days=i)
    ics_content += (
        "BEGIN:VEVENT\n"
        f"UID:event-{i+1}@taamoul.com\n"
        f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}\n"
        f"DTSTART:{event_date.strftime('%Y%m%dT100000Z')}\n"
        f"DTEND:{event_date.strftime('%Y%m%dT110000Z')}\n"
        f"SUMMARY:📌 حدث {category}\n"
        f"DESCRIPTION:تم إنشاء هذا الحدث لاختبار عرض التقويم للفئة: {category}\n"
        "LOCATION:Dubai, UAE\n"
        "STATUS:CONFIRMED\n"
        "END:VEVENT\n"
    )

# === إغلاق ملف التقويم ===
ics_content += "END:VCALENDAR\n"

# Python script to generate .ics file with OpenAI integration
print("✅ تم إنشاء ملف التقويم بنجاح.")

# === حفظ الملف ===
Path("live_calendar.ics").write_text(ics_content, encoding="utf-8")
