import json
from datetime import datetime, timedelta
from pathlib import Path

# === إعداد الاهتمامات من ملف JSON ===
with open("interests.json", "r", encoding="utf-8") as f:
    interests = json.load(f)["categories"]

# === بناء محتوى التقويم ===
ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\nPRODID:-//Taamoul Calendar//EN\n"

# === إعداد أحداث حسب الاهتمامات (نموذجياً فقط) ===
start_date = datetime.now()
event_count = 0

for interest in interests:
    if event_count >= 10:
        break  # الحد الأقصى لعدد الأحداث المولدة

    event_date = start_date + timedelta(days=event_count)
    ics_content += f"""BEGIN:VEVENT
UID:{interest}-{event_count}@taamoul.com
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{event_date.strftime('%Y%m%dT100000Z')}
DTEND:{event_date.strftime('%Y%m%dT110000Z')}
SUMMARY:✨ {interest.capitalize()} Experience
DESCRIPTION:Automatic event generated for category: {interest}
LOCATION:Dubai, UAE
STATUS:CONFIRMED
END:VEVENT
"""
    event_count += 1

# === إنهاء ملف التقويم ===
ics_content += "END:VCALENDAR\n"

# === حفظ الملف ===
Path("live_calendar.ics").write_text(ics_content, encoding="utf-8")
print("✅ Calendar updated with", event_count, "events.")
