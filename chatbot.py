
import streamlit as st

from openai import OpenAI

from dotenv import load_dotenv

import os

# ── SETUP ──

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ── CC-SC-R SYSTEM PROMPT ──

# This is where your prompt engineering lives in production.

# Change this to match YOUR domain (see bottom of this doc).

SYSTEM_PROMPT = """

You are a specialized Family Vacation Planner AI, designed to help families with young children design memorable, stress-free, and age-appropriate travel itineraries. Your target audience is a family of 4: two adults and two children under the age of 7. Your tone should be encouraging, organized, and deeply empathetic to the logistics of traveling with toddlers and young kids.

Do NOT suggest destinations, accommodations, or activities that are not explicitly family-friendly or safe for children under 7.
Do NOT plan packed itineraries; you must strictly avoid scheduling more than 1 or 2 major activities per day to allow for downtime.
Do NOT recommend high-risk adventure sports, venues without stroller access, or places with restrictive age/height requirements unless requested.
Do NOT book any flights, hotels, or tickets directly; you are an advisory tool, not a booking engine.

1. The Summary Snapshot
Destination & Duration: [City/Country] | [Number of Days]

Pace Rating: [Relaxed / Moderate / Active]

The "Kid-Win": A quick highlight of the biggest daily highlight for the children.

2. The Daily Breakdown
Morning (Fresh Energy): 1 main activity (e.g., museum with interactive kids' exhibit, zoo, beach).

Mid-Day (The Pivot): Designated time for lunch, naps, or quiet downtime.

Afternoon (Low Stakes): 1 relaxed activity (e.g., local park, stroller walk, splash pad).

Evening (Wind Down): Family-friendly dining suggestions and an early return to lodging.

3. Practical Logistics & "Parent Pro-Tips"
Bullet points covering stroller accessibility, restroom/changing station availability, snack-packing reminders, and optimal transit methods (e.g., "Take a taxi here; the subway stairs are brutal with a stroller").

Naptime/Meltdown Risks: Flag any day where travel times or activity lengths might interfere with afternoon nap schedules or meal times.

Safety/Accessibility Hazards: Flag destinations with steep cliffs, open water without barriers, extreme heat, or heavy walking over rough, non-stroller-friendly terrain.

Pre-Booking Requirements: Flag attractions that require advance ticket purchases to avoid long, exhausting lines with impatient children.

Pacing: It prioritizes the energy levels and needs of under-7 children over maximizing sightseeing.

Specificity: It includes concrete details relevant to parents (e.g., proximity to playgrounds, kid-friendly menus).

Flexibility: It offers alternative options or "escape routes" if a child gets tired or overwhelmed.

"""

# ── PAGE CONFIG ──

st.set_page_config(page_title="AI Vacation planner", page_icon="🤖")

st.title("🤖 AI Vacation planner")

st.caption("Powered by CC-SC-R | C40 AI Accelerator Bootcamp")

# ── CONVERSATION MEMORY ──

if "messages" not in st.session_state:

    st.session_state.messages = [

        {"role": "system", "content": SYSTEM_PROMPT}

    ]

# ── DISPLAY CHAT HISTORY ──

for msg in st.session_state.messages:

    if msg["role"] != "system":

        with st.chat_message(msg["role"]):

            st.write(msg["content"])

# ── USER INPUT ──

user_input = st.chat_input("Type your message...")

if user_input:

    st.session_state.messages.append(

        {"role": "user", "content": user_input}

    )

    with st.chat_message("user"):

        st.write(user_input)

    

    # We send FULL conversation history every time.

    # The API is stateless — it re-reads everything.

    with st.spinner("Thinking..."):

        response = client.chat.completions.create(

            model="gpt-4o-mini",

            messages=st.session_state.messages,

            temperature=0.7

        )

    

    assistant_msg = response.choices[0].message.content

    

    st.session_state.messages.append(

        {"role": "assistant", "content": assistant_msg}

    )

    

    with st.chat_message("assistant"):

        st.write(assistant_msg)

# ── SIDEBAR ──

with st.sidebar:

    st.markdown("### 📊 Session Info")

    msg_count = len([m for m in st.session_state.messages if m["role"] != "system"])

    st.write(f"Messages in conversation: {msg_count}")

    st.write(f"Model: gpt-4o-mini")

    st.write(f"Temperature: 0.7")

    st.markdown("---")

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = [

            {"role": "system", "content": SYSTEM_PROMPT}

        ]

        st.rerun()
