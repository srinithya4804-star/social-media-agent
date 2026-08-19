import json
from pathlib import Path


def test_calendar_output_exists():
    output_file = Path("outputs/content_calendar.json")

    assert output_file.exists(), "Calendar output file does not exist."


def test_calendar_has_seven_days():
    output_file = Path("outputs/content_calendar.json")

    with open(output_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    calendar = data["calendar"]

    assert len(calendar) == 7, "Calendar should contain exactly 7 days."


def test_each_day_has_required_fields():
    output_file = Path("outputs/content_calendar.json")

    with open(output_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    required_fields = {
        "day",
        "platform",
        "content_type",
        "topic",
        "caption",
        "hashtags",
        "suggested_time",
        "reason"
    }

    for item in data["calendar"]:
        assert required_fields.issubset(item.keys())


def test_no_duplicate_topics():
    output_file = Path("outputs/content_calendar.json")

    with open(output_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    topics = [
        item["topic"].strip().lower()
        for item in data["calendar"]
    ]

    assert len(topics) == len(set(topics)), "Duplicate topics found."