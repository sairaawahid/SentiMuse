# SentiMuse: Prompt Co-Creation with Soul
SentiMuse is a human-first, emotionally intelligent writing companion that helps you generate creative, emotionally aware prompts for AI tools like ChatGPT, Claude, or Gemini.

It doesn't just generate prompts, it co-creates them with you based on your mood, topic, and journaling reflections. Think of it as a therapeutic journaling buddy that speaks your emotional language.

---

## Live Demo

---

## Description
AI-generated content often feels robotic, generic, and lacks emotional nuance, especially for people going through emotional distress, cultural marginalization, or neurodivergent thought patterns. SentiMuse solves this by acting as an emotionally aware prompt co-creator that helps users (especially writers, creators, students, and mental health practitioners) craft deeply human, emotionally resonant prompts for generative AI tools like ChatGPT, Claude, or Gemini.
Whether you're a writer, student, creator, or mental health practitioner, SentiMuse helps you feel seen, heard, and inspired.

## Objectives
- Help users generate emotionally aware, simple prompts for AI writing tools.
- Support emotional well-being through creative self-expression.
- Bridge affective computing with real-world journaling and writing needs.
- Make prompt engineering more inclusive for neurodivergent or emotionally sensitive users.

---

## Features
- Emotion-Driven Prompting: Select your mood to guide the prompt tone.
- Topic + Journal Input: Tailor prompts based on your input and reflection.
- VADER Sentiment Analysis: Get real-time sentiment from your journal notes.
- Tears Meter: Reflect on how emotionally resonant the prompt was.
- Prompt Moodboard: Save, filter, and export your favorite prompts as a PDF.
- Reset Button: Clear inputs while keeping your saved prompt history.

---

## Usage
1. Select Your Mood from the sidebar (e.g., Anxious, Joyful).
2. Enter a Topic you want to write or think about.
3. Add a journal note — how you're currently feeling.
4. Click "Generate Prompt" to receive a custom, emotionally nuanced writing prompt.
5. Save to Moodboard, reflect with the Tears Meter, or export your prompt collection as a beautiful PDF.

---

## Tech Stack
- Streamlit for UI
- OpenAI GPT-3.5-turbo or GPT-4o for language generation
- VADER Sentiment Analyzer for emotion detection
- ReportLab for PDF export
- Python 3.10+

--- 

## Getting Started
Clone this repo and run the app locally:
```bash
# 1. Clone the repo
$ git clone https://github.com/yourusername/sentimuse.git
$ cd sentimuse

# 2. Create virtual environment (optional)
$ python -m venv venv
$ source venv/bin/activate   # on Windows: venv\Scripts\activate

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Add OpenAI key
Create a `.streamlit/secrets.toml` file with:
[general]
OPENAI_API_KEY = "your-api-key-here"

# 5. Run the app
$ streamlit run app.py
```

---

## Outcome
- Successfully deployed as an interactive, responsive Streamlit web app.
- Used in CS Girlies Hackathon under the theme "AI vs H.I." to demonstrate human-centered AI.
- Accessible to creators, writers, and wellness professionals seeking emotionally resonant tools.

--- 

## Attribution
SentiMuse was collaboratively developed by:

- [Sairaaw](https://www.linkedin.com/in/sairaabdulwahid/) (Product Design, Prompt Engineering, Frontend Logic)
- [Samiya-AW](https://www.linkedin.com/in/samiyaaw/) (Backend Support, Logic Integration, UI Feedback)

We built this together with care, empathy, and love for emotionally intelligent technology ✨
If you use or adapt this app, please credit the author by linking to the original GitHub repository:
🔗 https://github.com/sairaawahid/SentiMuse

---

## License
This project is licensed under the MIT License.
See the `LICENSE` file for more details.

If you liked this project or want to collaborate on emotion-first AI tools, reach out via LinkedIn or GitHub:
Sairaaw: [LinkedIn](https://www.linkedin.com/in/sairaabdulwahid/) or [GitHub](https://github.com/sairaawahid)
Samiya-AW: [LinkedIn](https://www.linkedin.com/in/samiyaaw/) or [GitHub](https://github.com/Samiya-AW)

*Made with ❤️ at the CS Girlies Hackathon 2025*
