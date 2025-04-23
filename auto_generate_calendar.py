import openai
import pytz
import os
import datetime
from ics import Calendar, Event

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Settings
NUM_DAYS_AHEAD = 60  # Rolling window
MAX_EVENTS_PER_DAY = 50
TIMEZONE = pytz.timezone("Asia/Dubai")

# Event categories to use
CATEGORIES = ["Aviation", "Lifestyle", "Exhibitions", "Seasonal"]

# Prompt Template
PROMPT_TEMPLATE = """
Generate {num_events} unique {category} events happening in Dubai, UAE between {start_date} and {end_date}.
For each event include:
1. Title (max 10 words)
2. 1-paragraph description in English
3. Realistic time (HH:MM) and date
4. Location (real or logical, e.g., Dubai World Trade Centre)
5. Contact email (if available or realistic placeholder)
6. Ticket or registration link (realistic or dummy)

Format it in JSON with keys: title, description, date, time, location, contact_email, ticket_link.
"""

def fetch_events(category, start_date, end_date, num_events):
    prompt = PROMPT_TEMPLATE.format(
        category=category,
        num_events=num_events,
        start_date=start_date.strftime("%B %d, %Y"),
        end_date=end_date.strftime("%B %d, %Y"),
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    content = response["choices"][0]["message"]["content"]
    return content

def parse_events(json_text):
    import json
    try:
        events = json.loads(json_text)
        return events if isinstance(events, list) else []
    except Exception:
        return []

def generate_calendar():
    cal = Calendar()
    today = datetime.datetime.now(TIMEZONE).date()
    end_date = today + datetime.timedelta(days=NUM_DAYS_AHEAD)

    for day_offset in range(NUM_DAYS_AHEAD):
        day = today + datetime.timedelta(days=day_offset)
        for category in CATEGORIES:
            response_text = fetch_events(category, day, day, min(5, MAX_EVENTS_PER_DAY))
            parsed = parse_events(response_text)
            for item in parsed[:MAX_EVENTS_PER_DAY]:
                try:
                    event = Event()
                    event.name = item["title"]
                    dt_str = f"{item['date']} {item['time']}"
                    event.begin = TIMEZONE.localize(datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M"))
                    event.duration = datetime.timedelta(hours=2)
                    event.description = f"{item['description']}\n\nContact: {item.get('contact_email', 'N/A')}\nTickets: {item.get('ticket_link', '')}"
                    event.location = item.get("location", "")
                    cal.events.add(event)
                except Exception:
                    continue  # Skip malformed entries

    with open("live_calendar.ics", "w") as f:
        f.writelines(cal.serialize_iter())

if __name__ == "__main__":
    generate_calendar()
