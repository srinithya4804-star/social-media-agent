import json
import os

import pandas as pd
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field


# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")


# Create Gemini client
client = genai.Client(api_key=api_key)


# Load the brand brief
with open("data/sample_brand.json", "r", encoding="utf-8") as file:
    brand = json.load(file)


class ContentDay(BaseModel):
    day: str
    platform: str
    content_type: str
    topic: str
    caption: str
    hashtags: list[str] = Field(min_length=1, max_length=5)
    suggested_time: str
    reason: str


class ContentCalendar(BaseModel):
    calendar: list[ContentDay] = Field(min_length=7, max_length=7)


system_prompt = """
You are an expert social media content strategist.

Your job is to create a 7-day social media content calendar
for the brand information provided by the user.

Follow these rules carefully:

1. Create exactly 7 days of content.
2. Keep every idea relevant to the brand and target audience.
3. Follow the specified brand voice.
4. Use the specified content themes.
5. Every day must have a completely unique topic.
6. Before returning the final calendar, compare all 7 topics and make sure no two topics are identical or substantially similar.
7. Do not reuse the same subject with only minor wording changes.
8. Create engaging but realistic captions.
9. Generate a maximum of 5 relevant hashtags per post.
10. Hashtags must contain only normal words and must never contain long sequences of numbers, binary patterns, or repeated characters.
11. Suggest a reasonable posting time for each day.
12. Explain briefly why each piece of content is useful.
13. Keep the content practical and suitable for the specified platform.
14. Never invent customer testimonials, customer names, reviews,
   statistics, clinical results, before-and-after results, or performance claims.
15. Never claim that a product produces a specific result unless that
   information is explicitly provided in the brand information.
16. Do not invent facts about the company or its products.
17. If a promotional post is needed but no verified product information
   is provided, keep the language general and avoid unsupported claims.
18. Keep each day's content meaningfully different from the other days.
"""


brand_information = json.dumps(brand, indent=2)

user_prompt = f"""
Create a 7-day social media content calendar for this brand.

Brand information:
{brand_information}
"""


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=[
        system_prompt,
        user_prompt
    ],
    config={
        "response_mime_type": "application/json",
        "response_schema": ContentCalendar
    }
)


calendar = ContentCalendar.model_validate_json(response.text)

def validate_calendar(calendar):
    # Check that exactly 7 posts were generated
    if len(calendar.calendar) != 7:
        raise ValueError(
            f"Expected 7 posts, but received {len(calendar.calendar)}"
        )

    # Check for duplicate topics
    topics = [
        item.topic.strip().lower()
        for item in calendar.calendar
    ]

    if len(topics) != len(set(topics)):
        raise ValueError("Duplicate topics detected in the calendar.")

    # Check hashtag quality
    for item in calendar.calendar:
        if not 1 <= len(item.hashtags) <= 5:
            raise ValueError(
                f"Invalid hashtag count for {item.day}"
            )

        for hashtag in item.hashtags:
            if len(hashtag) > 40:
                raise ValueError(
                    f"Suspiciously long hashtag detected for {item.day}"
                )

            if "010101" in hashtag or "101010" in hashtag:
                raise ValueError(
                    f"Suspicious repetitive hashtag detected for {item.day}"
                )

    return True
validate_calendar(calendar)

print("\nValidation passed successfully.")

print("\nGenerated Content Calendar:\n")

for item in calendar.calendar:
    print(f"{item.day} - {item.platform}")
    print(f"Type: {item.content_type}")
    print(f"Topic: {item.topic}")
    print(f"Caption: {item.caption}")
    print(f"Hashtags: {' '.join(item.hashtags)}")
    print(f"Suggested time: {item.suggested_time}")
    print(f"Reason: {item.reason}")
    print("-" * 60)

# Save the generated calendar as JSON
os.makedirs("outputs", exist_ok=True)

with open(
    "outputs/content_calendar.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        calendar.model_dump(),
        file,
        indent=2,
        ensure_ascii=False
    )

print("\nCalendar saved to outputs/content_calendar.json")    

# Save the calendar as CSV
calendar_df = pd.DataFrame(
    [item.model_dump() for item in calendar.calendar]
)

calendar_df["hashtags"] = calendar_df["hashtags"].apply(
    lambda tags: " ".join(tags)
)

calendar_df.to_csv(
    "outputs/content_calendar.csv",
    index=False,
    encoding="utf-8"
)

print("Calendar saved to outputs/content_calendar.csv")