import openai
import os
from datetime import datetime, timedelta
import random

# تحميل مفتاح OpenAI من متغير البيئة
openai.api_key = os.getenv("OPENAI_API_KEY")

# تصنيفات الفعاليات ونبرة الكتابة المخصصة لكل فئة
categories = {
    "Aviation": {"emoji": "✈️", "tone": "technical and professional"},
    "Lifestyle": {"emoji": "💫", "tone": "elegant and refined"},
    "Exhibition": {"emoji": "🖼️", "tone": "informative and descriptive"},
    "Seasonal": {"emoji": "🌿", "tone": "inspiring and uplifting"},
}

def generate_event_prompt(category, tone):
    return f"Write a {tone} short event description for a public calendar. Include a title, short paragraph, location in Dubai, a public email, and a public website link. The event category is {category.lower()}."

def get_openai_event(category):
    prompt = generate_event_prompt(category, categories[category]["tone"])
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional event planner."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.8
    )
    text = response.choices[0].message.content.strip()

    # استخراج معلومات الحدث من النص
    title = text.splitlines()[0].strip()
    description = "\\n".join(text.splitlines()[1:]).strip()
    location = "Dubai"
    url = "https://example.com"
    email = "contact@example.com"

    return {
        "title": title,
        "description": description,
        "location": location,
        "url": url,
        "contact_email": email,
        "emoji": categories[category]["emoji"]
    }

def format_event_ics(event, start_time, end_time):
    return f"""BEGIN:VEVENT
SUMMARY:{event['emoji']} {event['title']}
DTSTART;TZID=Asia/Dubai:{start_time.strftime('%Y%m%dT%H%M%S')}
DTEND;TZID=Asia/Dubai:{end_time.strftime('%Y%m%dT%H%M%S')}
DESCRIPTION:{event['description']}\\nURL: {event['url']}\\nContact: {event['contact_email']}
LOCATION:{event['location']}
URL:{event['url']}
STATUS:CONFIRMED
END:VEVENT"""

def generate_calendar():
    now = datetime.now()
    events = []

    for day_offset in range(0, 2):  # اليوم واليوم التالي
        date = now + timedelta(days=day_offset)
        for _ in range(25):  # توليد حتى 50 فعالية إجمالية
            category = random.choice(list(categories.keys()))
            try:
                event_data = get_openai_event(category)
                start_time = date.replace(hour=random.choice([10, 14, 18]), minute=0, second=0, microsecond=0)
                end_time = start_time + timedelta(hours=2)
                events.append(format_event_ics(event_data, start_time, end_time))
            except Exception as e:
                print(f"OpenAI error: {e}")

    ics = "BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\nPRODID:-//Taamoul Calendar//EN\n" + "\n".join(events) + "\nEND:VCALENDAR"
    with open("live_calendar.ics", "w", encoding="utf-8") as f:
        f.write(ics)

if __name__ == "__main__":
    generate_calendar()
