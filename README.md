# Social Media Content Planning AI Agent

-> Overview

This project is an AI-powered social media content planning agent built for the Rooman AI Challenge.

The agent takes a structured brand brief containing information such as the brand, industry, target audience, brand voice, content themes, and preferred platform.

It then uses the Gemini API to generate a structured 7-day social media content calendar containing content ideas, captions, hashtags, suggested posting times, and a short reason for each recommendation.

The generated calendar is validated before being saved as JSON and CSV files.

---

-> Features

* Generates a 7-day social media content calendar
* Creates platform-specific content ideas
* Generates captions
* Generates relevant hashtags
* Suggests posting times
* Provides a reason for each content recommendation
* Keeps content aligned with the brand voice and target audience
* Detects duplicate topics
* Validates the number and structure of generated posts
* Limits hashtags to a maximum of five per post
* Detects suspiciously repetitive hashtag output
* Prevents fabricated testimonials and unsupported product claims
* Exports the final calendar as JSON and CSV

---

-> Tech Stack

* Python
* Google Gemini API
* `google-genai`
* Pydantic
* Pandas
* python-dotenv

---

-> Project Structure


social-media-agent/
│
├── agent.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── sample_brand.json
│
├── outputs/
│   ├── content_calendar.json
│   └── content_calendar.csv
│
└── venv/


The `.env` file and virtual environment are intentionally excluded from version control.

---

-> How It Works

The agent follows this workflow:

Brand Brief
    ↓
Python Application
    ↓
System Prompt + Brand Information
    ↓
Gemini API
    ↓
Structured Calendar
    ↓
Pydantic Validation
    ↓
JSON + CSV Output


The LLM is used as the reasoning and content-generation component, while Python handles orchestration, input loading, validation, and output storage.

---

-> Input

The agent reads the sample brand information from:


data/sample_brand.json


Example:

```json
{
  "brand_name": "GlowNest",
  "industry": "Skincare",
  "target_audience": "Women aged 18-30 who are interested in simple and effective skincare",
  "brand_voice": "Friendly, modern, educational and trustworthy",
  "content_themes": [
    "Skincare education",
    "Product awareness",
    "Self-care",
    "Lifestyle",
    "Skincare tips"
  ],
  "platforms": [
    "Instagram"
  ],
  "posting_frequency": "1 post per day"
}
```

The same agent can generate different calendars when the brand brief is changed. During testing, the agent was also tested with restaurant and fitness brand profiles.

---

-> Output

The generated files are stored in:


outputs/content_calendar.json
outputs/content_calendar.csv


Each calendar entry contains:

* Day
* Platform
* Content type
* Topic
* Caption
* Hashtags
* Suggested posting time
* Reason for recommendation

---

-> Setup

1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd social-media-agent
```

2. Create a virtual environment

```bash
python -m venv venv
```

On Windows: venv\Scripts\activate

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure the API key

Create a `.env` file in the project root: GEMINI_API_KEY=your_api_key_here

The API key should not be committed to GitHub.

5. Run the agent
```bash
python agent.py
```
The generated calendar will be displayed in the terminal and saved to the `outputs` directory.

---

-> Validation

The agent validates the generated output before saving it.

The validation layer checks:

1. Exactly seven posts are generated.
2. Topics are not duplicated.
3. Each post contains between one and five hashtags.
4. Hashtags are not suspiciously long.
5. Known repetitive binary-style hashtag patterns are rejected.

Structured output is also validated using Pydantic.

This prevents malformed or low-quality model output from being silently accepted by the application.

---

-> Design Choices

Q1. Why Python?

Python provides a simple environment for integrating with an LLM API and implementing data processing and validation.

Q2. Why Gemini?

Gemini provides the language-model capabilities required for generating the content calendar while allowing the project to be developed using an available API free tier.

Q3. Why structured output?

The application requires predictable fields for each day. Structured output makes the LLM response easier to validate and process programmatically.

Q4. Why Pydantic?

Pydantic provides schema validation for the generated calendar and ensures that the application receives the expected structure before saving the result.

Q5. Why JSON and CSV?

JSON preserves the structured representation of the generated calendar, while CSV provides a convenient format for viewing and working with the calendar in spreadsheet software.

---

-> Tradeoffs

The project prioritizes a reliable end-to-end workflow over a complex user interface.

A command-line interface was chosen because the challenge evaluates the functionality and reasoning of the agent rather than UI design.

The system also uses an LLM for content generation instead of training a custom machine-learning model. This keeps the implementation lightweight and allows the agent to adapt to different brand briefs.

---

-> Limitations

* Suggested posting times are generated recommendations and are not based on historical engagement analytics.
* The agent does not directly publish content to social media platforms.
* The agent does not have access to real-time social media trends or platform analytics.
* Content quality depends partly on the quality and completeness of the supplied brand brief.
* The agent uses an external LLM API, so API availability and rate limits can affect execution.

---

-> Future Improvements

With additional development time, the agent could be extended with:

* Platform-specific content optimization
* Real social media analytics
* Historical engagement data
* Trend detection
* User editing before export
* A web-based interface
* Direct scheduling or publishing integrations
* More advanced semantic duplicate detection

---

-> Sample Output

A sample generated calendar is included in:

outputs/content_calendar.json
outputs/content_calendar.csv

The agent can be run with different brand briefs to produce different content calendars.

---

->Conclusion

This project demonstrates an end-to-end AI agent workflow:

Input → Reason → Generate → Validate → Store

The focus is on producing a practical, reproducible, and explainable social media content planning agent rather than simply generating individual captions.

---