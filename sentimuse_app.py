import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import openai
import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from io import BytesIO

# --- Set OpenAI API key from Streamlit secrets ---
openai.api_key = st.secrets["OPENAI_API_KEY"]
OPENAI_MODEL = "gpt-3.5-turbo"  # or "gpt-4o"

# ---- Mood + Color Definitions ----
EMOJI_MOODS = {
    "Select---": "",
    # Positive
    "😄 Joyful": "Joyful",
    "😊 Grateful": "Grateful",
    "😍 Loved": "Loved",
    "🤩 Excited": "Excited",
    "😌 Calm": "Calm",
    "😃 Optimistic": "Optimistic",
    "😎 Confident": "Confident",
    "😇 Peaceful": "Peaceful",
    "😋 Content": "Content",
    "🫡 Proud": "Proud",
    "😇 Inspired": "Inspired",
    "🕊️ Hopeful": "Hopeful",
    "🥰 Affectionate": "Affectionate",
    "🫶 Appreciative": "Appreciative",
    "🦸 Empowered": "Empowered",
    # Mixed/Reflective
    "🤔 Reflective": "Reflective",
    "😶‍🌫️ Numb": "Numb",
    "😐 Neutral": "Neutral",
    "🥲 Bittersweet": "Bittersweet",
    "😅 Relieved": "Relieved",
    "😯 Surprised": "Surprised",
    "😕 Confused": "Confused",
    "🧐 Curious": "Curious",
    "😬 Awkward": "Awkward",
    "😳 Embarrassed": "Embarrassed",
    "😶 Speechless": "Speechless",
    # Negative
    "😔 Sad": "Sad",
    "😤 Angry": "Angry",
    "😰 Anxious": "Anxious",
    "😭 Heartbroken": "Heartbroken",
    "😢 Lonely": "Lonely",
    "😨 Fearful": "Fearful",
    "😩 Overwhelmed": "Overwhelmed",
    "😔 Guilty": "Guilty",
    "🫠 Burnt Out": "Burnt Out",
    "😒 Disappointed": "Disappointed",
    "😠 Frustrated": "Frustrated",
    "🥺 Vulnerable": "Vulnerable",
    "😞 Discouraged": "Discouraged",
    "😓 Ashamed": "Ashamed",
    "🥱 Bored": "Bored",
    "😟 Worried": "Worried",
    "🫥 Invisible": "Invisible",
    "🙁 Hopeless": "Hopeless",
    "🤒 Sick": "Sick",
    "🥶 Shocked": "Shocked",
    "🥵 Drained": "Drained",
    "😿 Regretful": "Regretful",
    "🥵 Stressed": "Stressed"
}

MOOD_DISPLAY = {
    # Positive
    "Joyful": {"emoji": "😄", "color": "#FFD700"},
    "Grateful": {"emoji": "😊", "color": "#D4FC79"},
    "Loved": {"emoji": "😍", "color": "#FFB6B9"},
    "Excited": {"emoji": "🤩", "color": "#FFB347"},
    "Calm": {"emoji": "😌", "color": "#A7E9AF"},
    "Optimistic": {"emoji": "😃", "color": "#A1C6EA"},
    "Confident": {"emoji": "😎", "color": "#C2F5FF"},
    "Peaceful": {"emoji": "😇", "color": "#C3F8FF"},
    "Content": {"emoji": "😋", "color": "#FFE066"},
    "Proud": {"emoji": "🫡", "color": "#D6FFD7"},
    "Inspired": {"emoji": "😇", "color": "#B1E1FF"},
    "Hopeful": {"emoji": "🕊️", "color": "#B7E5D1"},
    "Affectionate": {"emoji": "🥰", "color": "#FFCFDF"},
    "Appreciative": {"emoji": "🫶", "color": "#FFE5B4"},
    "Empowered": {"emoji": "🦸", "color": "#A3F7BF"},
    # Mixed/Reflective
    "Reflective": {"emoji": "🤔", "color": "#D1A3FF"},
    "Numb": {"emoji": "😶‍🌫️", "color": "#B0B0B0"},
    "Neutral": {"emoji": "😐", "color": "#CCCCCC"},
    "Bittersweet": {"emoji": "🥲", "color": "#F7C59F"},
    "Relieved": {"emoji": "😅", "color": "#C9F9FF"},
    "Surprised": {"emoji": "😯", "color": "#FFD3E0"},
    "Confused": {"emoji": "😕", "color": "#BDBDBD"},
    "Curious": {"emoji": "🧐", "color": "#C5DFFF"},
    "Awkward": {"emoji": "😬", "color": "#F7F6CF"},
    "Embarrassed": {"emoji": "😳", "color": "#FFD6C0"},
    "Speechless": {"emoji": "😶", "color": "#E0E0E0"},
    # Negative
    "Sad": {"emoji": "😔", "color": "#A2C5E0"},
    "Angry": {"emoji": "😤", "color": "#FF7F7F"},
    "Anxious": {"emoji": "😰", "color": "#B7D4FF"},
    "Heartbroken": {"emoji": "😭", "color": "#D291BC"},
    "Lonely": {"emoji": "😢", "color": "#86A8E7"},
    "Fearful": {"emoji": "😨", "color": "#FFA07A"},
    "Overwhelmed": {"emoji": "😩", "color": "#F67280"},
    "Guilty": {"emoji": "😔", "color": "#FFD6E0"},
    "Burnt Out": {"emoji": "🫠", "color": "#EAD7B7"},
    "Disappointed": {"emoji": "😒", "color": "#BDBDBD"},
    "Frustrated": {"emoji": "😠", "color": "#FFC3A0"},
    "Vulnerable": {"emoji": "🥺", "color": "#D6E0F0"},
    "Discouraged": {"emoji": "😞", "color": "#C2B9B0"},
    "Ashamed": {"emoji": "😓", "color": "#A9C9FF"},
    "Bored": {"emoji": "🥱", "color": "#F0EAD6"},
    "Worried": {"emoji": "😟", "color": "#ADD8E6"},
    "Invisible": {"emoji": "🫥", "color": "#CFCFCF"},
    "Hopeless": {"emoji": "🙁", "color": "#9E9E9E"},
    "Sick": {"emoji": "🤒", "color": "#E2CFC3"},
    "Shocked": {"emoji": "🥶", "color": "#AFE9FF"},
    "Drained": {"emoji": "🥵", "color": "#FFBCB3"},
    "Regretful": {"emoji": "😿", "color": "#B5C6E0"},
    "Stressed": {"emoji": "🥵", "color": "#FFC1B6"}
}

# ---- Sentiment Analyzer ----
analyzer = SentimentIntensityAnalyzer()
def detect_sentiment(text):
    if not text:
        return "neutral"
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.5:
        return "positive"
    elif score <= -0.5:
        return "negative"
    else:
        return "neutral"

# ---- OpenAI Prompt Generator ----
def generate_prompt_openai(emotion, topic, journal=None):
    base_prompt = f"""
You are SentiMuse: a creative prompt starter designer for emotionally intelligent AI tools.

Your job is to co-create a human-centered, emotionally-aware writing prompt in simple, natural language (not a question, not poetic/metaphorical, not advice-giving).

Rules:
- Reflect the emotion (“{emotion}”) clearly in the tone.
- Use simple, clear, direct language that feels natural in daily life.
- The prompt should be something the user can copy and paste into ChatGPT, Claude, or Gemini to get emotionally resonant content.
- Do NOT ask a question. Do NOT give advice. Do NOT use metaphors or poetic language.
- If journal notes are present, use the user’s words or themes naturally.
- Make sure the prompt is actionable, relatable, and safe for anyone.
- Keep the prompt under 20 words if possible.
- Use everyday words that anyone could understand.
- No need for details unless the journal includes them.

Examples:

Good:
- "Write a short story about a time you overcame fear and felt proud."
- "Describe a place that feels like home when you’re feeling anxious."
- "Imagine your future self sending you a message of encouragement after a hard day."
- "Write about a time you felt nervous before speaking but went for it."
- "Describe how you handled anxiety before an important event."
- "Share a moment you surprised yourself by being brave."

Bad:
- "How do you feel when you’re anxious?"
- "Fear is a gentle visitor in your life."
- "Describe your feelings in detail."
- "Imagine anxiety as a gentle visitor…"
- "Describe your feelings in detail."

Input:
- Emotion: {emotion}
- Topic: {topic}
- Journal: {journal if journal else "None"}

Output:
Return ONLY a single, original, emotionally-aware writing prompt (not a question, not advice, not poetic).
"""
    try:
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a creative and emotionally intelligent prompt generator."},
                {"role": "user", "content": base_prompt}
            ],
            temperature=0.7,   # Lowered for clarity/simplicity
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ---- Save/Load Prompts ----
if "favorites" not in st.session_state:
    st.session_state.favorites = []

def save_prompt(prompt_text, emotion=None):
    entry = {
        "prompt": prompt_text,
        "emotion": emotion or "Reflective"
    }
    if entry not in st.session_state.favorites:
        st.session_state.favorites.append(entry)

def load_saved_prompts():
    return st.session_state.favorites

# ---- Streamlit State Initialization ----
if "generated_prompt" not in st.session_state:
    st.session_state.generated_prompt = ""
if "tears_rating" not in st.session_state:
    st.session_state.tears_rating = None
if "tears_reason" not in st.session_state:
    st.session_state.tears_reason = ""
if "show_save_success" not in st.session_state:
    st.session_state.show_save_success = False

# ---- UI Layout ----
st.set_page_config(page_title="SentiMuse", layout="wide")
st.title("🎭 SentiMuse: Prompt Co-Creation with Soul")

with st.sidebar:
    st.header("🧠 Select Your Mood")
    st.markdown("📝 *Set your emotional tone to guide your creative prompt journey.*")
    mood_emoji = st.selectbox("How are you feeling?", list(EMOJI_MOODS.keys()))
    selected_emotion = EMOJI_MOODS[mood_emoji]
    st.markdown("---")

topic_input = st.text_input("What do you want to write/talk about?", "")
journal_entry = st.text_area("Optional: Write how you feel in your own words", "")

if journal_entry:
    detected = detect_sentiment(journal_entry)
    st.info(f"🧠 Sentiment Detected from Journal: **{detected.capitalize()}**")

if st.button("✨ Generate Prompt"):
    if topic_input:
        with st.spinner("Generating with emotional nuance..."):
            st.session_state.generated_prompt = generate_prompt_openai(selected_emotion, topic_input, journal_entry)
            st.session_state.tears_rating = None
            st.session_state.tears_reason = ""
    else:
        st.warning("Please enter a topic first.")

if st.session_state.generated_prompt:
    st.markdown("### ✨ Your Personalized Prompt:")
    st.markdown(
        f"""
        <div style="
            background-color: #f9fafc;
            border-left: 6px solid #6366f1;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            font-size: 1.15rem;
            color: #222;
            font-weight: 500;
            box-shadow: 0 2px 12px 0 rgba(99,102,241,0.10);
        ">
            {st.session_state.generated_prompt}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("💾 Save to Favorites"):
        save_prompt(st.session_state.generated_prompt, selected_emotion)
        st.session_state.show_save_success = True
        st.rerun()

    if st.session_state.show_save_success:
        st.success("Saved to favorites!")
        time.sleep(2)
        st.session_state.show_save_success = False
        st.rerun()

    st.markdown("### 😭 Tears Meter — How much did this move you?")
    tears_options = {
        "😐 Meh, not really": 1,
        "🥲 A little emotional": 2,
        "😭 This HIT me hard!": 3
    }
    rating_label = st.radio("Emotional Impact:", list(tears_options.keys()))
    st.session_state.tears_rating = tears_options[rating_label]
    st.session_state.tears_reason = st.text_area("Optional: Why did this move you?", "")
    if st.button("📝 Submit Rating"):
        st.success("Thanks for your emotional feedback!")
        with st.expander("🔍 View Your Tears Feedback"):
            st.markdown(f"**Rating Level:** {st.session_state.tears_rating}")
            if st.session_state.tears_reason:
                st.markdown(f"**Reflection:** {st.session_state.tears_reason}")
            else:
                st.markdown("_No reflection provided._")

with st.expander("🖼️ Prompt Moodboard"):
    favorites = load_saved_prompts()
    if favorites:
        all_emotions = sorted(set([f["emotion"] for f in favorites]))
        filter_emotion = st.selectbox("🎯 Filter by Emotion", options=["All"] + all_emotions)
        filtered_prompts = [f for f in favorites if filter_emotion == "All" or f["emotion"] == filter_emotion]
        for i, item in enumerate(filtered_prompts[::-1]):
            prompt = item["prompt"]
            emotion = item["emotion"]
            mood_data = MOOD_DISPLAY.get(emotion, {"emoji": "📝", "color": "#DDD"})
            col1, col2 = st.columns([10, 1])
            with col1:
                st.markdown(
                    f"""
                    <div style='
                        background-color: {mood_data['color']};
                        padding: 1rem;
                        border-radius: 10px;
                        margin-bottom: 1rem;
                    '>
                        <strong>{mood_data['emoji']} {emotion.capitalize()}</strong><br>
                        <span>{prompt}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col2:
                if st.button("🗑", key=f"delete_{i}"):
                    st.session_state.favorites.remove(item)
                    st.success("Prompt deleted!")
                    st.rerun()

        # Export Moodboard PDF
        if filtered_prompts:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter,
                                    rightMargin=40, leftMargin=40,
                                    topMargin=60, bottomMargin=40)
            heading_style = ParagraphStyle(name="Heading", fontSize=16, leading=20, spaceAfter=10, alignment=TA_LEFT, fontName="Helvetica-Bold")
            subheading_style = ParagraphStyle(name="Subheading", fontSize=12, leading=16, spaceAfter=6, fontName="Helvetica-Bold")
            body_style = ParagraphStyle(name="Body", fontSize=11, leading=14, spaceAfter=12, fontName="Helvetica")
            story = []
            story.append(Paragraph("SentiMuse Prompt Moodboard", heading_style))
            story.append(Spacer(1, 12))
            for item in filtered_prompts:
                emotion = item["emotion"].capitalize()
                emoji = MOOD_DISPLAY.get(item["emotion"], {}).get("emoji", "📝")
                prompt_text = item["prompt"]
                story.append(Paragraph(f"{emoji} {emotion}", subheading_style))
                story.append(Paragraph(prompt_text, body_style))
                story.append(Spacer(1, 6))
            doc.build(story)
            buffer.seek(0)
            st.download_button(
                label="📥 Export Moodboard as PDF",
                data=buffer,
                file_name="senti_muse_moodboard.pdf",
                mime="application/pdf"
            )
    else:
        st.markdown("_No prompts saved yet._")
