import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import random

# ------------------------
# Page config
# ------------------------
st.set_page_config(page_title="IELTS Momentum Path", layout="wide", initial_sidebar_state="expanded")

# ------------------------
# Dark theme styling
# ------------------------
st.markdown("""
<style>
body {background: linear-gradient(135deg,#1f1f2e,#3a3a5e); color:white;}
.stButton>button {background: linear-gradient(45deg,#ff6a00,#ee0979); color:white; border-radius:25px; margin:5px;}
.stTextInput>div>input, .stTextArea>div>textarea {background:#2b2b3f; color:white;}
.stSelectbox>div>div>div>span {color:white;}
</style>
""", unsafe_allow_html=True)

# ------------------------
# Session state initialization
# ------------------------
if 'video_progress' not in st.session_state:
    st.session_state.video_progress = {"Listening":False, "Reading":False, "Writing":False, "Speaking":False}
if 'doubts' not in st.session_state:
    st.session_state.doubts = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = []
if 'streak' not in st.session_state:
    st.session_state.streak = 3
if 'completed_goals' not in st.session_state:
    st.session_state.completed_goals = 6
if 'momentum' not in st.session_state:
    st.session_state.momentum = 70
if 'exam_date' not in st.session_state:
    st.session_state.exam_date = datetime.date.today() + datetime.timedelta(days=30)
if 'prep_mode' not in st.session_state:
    st.session_state.prep_mode = "Regular (1 hr/day)"
if 'daily_time' not in st.session_state:
    st.session_state.daily_time = 60

# ------------------------
# Sidebar navigation
# ------------------------
page = st.sidebar.radio("Navigation", ["Dashboard","Daily Goals","Weekly Summary","Videos","Doubts","Feedback","Comeback Mode","Calendar / Exam Setup"])

# ------------------------
# Sample data
# ------------------------
skills = {"Listening": 70, "Reading": 65, "Writing": 60, "Speaking": 50}
weekly_goals = [5, 6, 4, 7]

# ------------------------
# Pages
# ------------------------
if page == "Dashboard":
    st.title("📊 IELTS Momentum Path Dashboard")
    col1, col2 = st.columns([1,2])
    
    with col1:
        st.metric("Weekly Streak", f"{st.session_state.streak} days")
        st.metric("Completed Goals", f"{st.session_state.completed_goals}/7")
        # Momentum meter
        fig_mom = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = st.session_state.momentum,
            domain = {'x':[0,1],'y':[0,1]},
            title = {'text': "Momentum Meter"},
            gauge = {'axis': {'range':[0,100]},
                     'bar': {'color':'cyan'},
                     'steps':[{'range':[0,50],'color':'red'},
                              {'range':[50,75],'color':'orange'},
                              {'range':[75,100],'color':'green'}]}))
        fig_mom.update_layout(paper_bgcolor='#1f1f2e', font_color='white', height=300)
        st.plotly_chart(fig_mom, use_container_width=True)

    with col2:
        # Radar chart for skills
        df_skills = pd.DataFrame({"Skill": list(skills.keys()), "Score": list(skills.values())})
        fig = px.line_polar(df_skills, r='Score', theta='Skill', line_close=True)
        fig.update_traces(fill='toself', line_color='cyan')
        fig.update_layout(polar_bgcolor='#1f1f2e', paper_bgcolor='#1f1f2e', font_color='white', height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("4-Week Engagement Trend")
    df_trend = pd.DataFrame({"Week":["Week 1","Week 2","Week 3","Week 4"], "Goals Completed": weekly_goals})
    fig2 = px.bar(df_trend, x="Week", y="Goals Completed", color="Goals Completed", color_continuous_scale='viridis')
    fig2.update_layout(paper_bgcolor='#1f1f2e', plot_bgcolor='#1f1f2e', font_color='white', height=350)
    st.plotly_chart(fig2, use_container_width=True)

# ------------------------
elif page == "Daily Goals":
    st.title("📅 Today's Micro Goals")
    goals = {"Listening":10,"Reading":10,"Writing":10,"Speaking":10}
    for skill, minutes in goals.items():
        st.write(f"{skill}: {minutes} minutes")
        st.progress(minutes/15)
    st.info("Keep up the momentum!")
    if st.button("Complete Daily Goal", key="daily_goal"):
        st.session_state.completed_goals += 1
        st.session_state.streak += 1
        st.session_state.momentum = min(100, st.session_state.momentum + 5)
        st.success("Daily goal completed! Momentum increased 🎉")
        st.balloons()

# ------------------------
elif page == "Weekly Summary":
    st.title("🗓 Weekly Summary")
    st.write(f"Completed {st.session_state.completed_goals} out of 7 daily goals this week")
    cal = pd.DataFrame(np.random.choice([0,1], size=(1,7)), columns=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
    st.dataframe(cal.style.applymap(lambda x: 'background-color: #28a745; color:#fff' if x==1 else 'background-color:#2b2b3f; color:#fff'))
    st.subheader("Badges Earned")
    if st.session_state.streak >=3:
        st.markdown("🏆 <span style='color:#ffc107;'>3-Day Streak Badge</span>", unsafe_allow_html=True)
        st.balloons()

# ------------------------
elif page == "Videos":
    st.title("🎥 Video Lectures")
    skill_filter = st.selectbox("Filter by Skill", ["All","Listening","Reading","Writing","Speaking"])
    videos = {
        "Listening":"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "Reading":"https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
        "Writing":"https://www.youtube.com/watch?v=V-_O7nl0Ii0",
        "Speaking":"https://www.youtube.com/watch?v=2Z4m4lnjxkY"
    }
    for skill, url in videos.items():
        if skill_filter=="All" or skill_filter==skill:
            st.subheader(skill)
            st.video(url)
            btn_key = f"watch_{skill}"
            if not st.session_state.video_progress[skill]:
                if st.button(f"Mark {skill} video as watched", key=btn_key):
                    st.session_state.video_progress[skill] = True
                    st.success(f"{skill} video completed! ⭐")
                    st.session_state.momentum = min(100, st.session_state.momentum + 3)

# ------------------------
elif page == "Doubts":
    st.title("❓ Raise Your Doubts")
    skill = st.selectbox("Select Skill/Topic", ["Listening","Reading","Writing","Speaking"])
    question = st.text_area("Type your doubt/question here")
    submit_key = f"doubt_submit_{skill}"
    submit = st.button("Submit Doubt", key=submit_key)
    if submit and question:
        st.session_state.doubts.append({"skill":skill,"question":question})
        st.success(f"Doubt submitted for {skill}! 💡")
        st.session_state.momentum = min(100, st.session_state.momentum + 2)
    st.subheader("Doubt Feed")
    for idx,d in enumerate(st.session_state.doubts[::-1],1):
        st.write(f"{idx}. [{d['skill']}] {d['question']}")

# ------------------------
elif page == "Feedback":
    st.title("✍ Feedback")
    rating = st.slider("Rate your experience",1,5)
    comments = st.text_area("Comments")
    submit_fb = st.button("Submit Feedback", key="submit_feedback")
    if submit_fb:
        st.session_state.feedback.append({"rating":rating,"comments":comments})
        st.success(f"Feedback submitted! Total entries: {len(st.session_state.feedback)} 🎉")
        st.session_state.momentum = min(100, st.session_state.momentum + rating)

    st.subheader("Feedback Summary")
    for idx, f in enumerate(st.session_state.feedback[::-1],1):
        st.write(f"{idx}. Rating: {f['rating']} stars, Comment: {f['comments']}")

# ------------------------
elif page == "Comeback Mode":
    st.title("👋 Welcome Back!")
    st.info("Let's restart gently with today's micro-goal")
    if st.button("Start Today's Goal", key="comeback_goal"):
        st.session_state.completed_goals += 1
        st.session_state.streak += 1
        st.session_state.momentum = min(100, st.session_state.momentum + 5)
        st.success("Micro-goal restarted! Keep going!")
        st.balloons()

# ------------------------
elif page == "Calendar / Exam Setup":
    st.title("📅 Setup Your IELTS Preparation")
    
    # Exam date selection
    exam_date = st.date_input("Select your exam date", value=st.session_state.exam_date, min_value=datetime.date.today())
    
    # Preparation mode selection
    prep_mode = st.radio(
        "Choose your preparation mode",
        ["Intensive (2+ hrs/day)", "Regular (1 hr/day)", "Light (30 mins/day)"],
        index=["Intensive (2+ hrs/day)", "Regular (1 hr/day)", "Light (30 mins/day)"].index(st.session_state.prep_mode)
    )
    
    # Daily study time input
    daily_time = st.number_input(
        "How many minutes can you dedicate daily?", min_value=10, max_value=300, value=st.session_state.daily_time, step=5
    )
    
    if st.button("Save Settings"):
        st.session_state.exam_date = exam_date
        st.session_state.prep_mode = prep_mode
        st.session_state.daily_time = daily_time
        st.success(f"Settings saved! Exam on {exam_date}, Mode: {prep_mode}, Daily Time: {daily_time} mins")
    
    # Motivational Quote
    quotes = [
        "Consistency is the key to success! 🔑",
        "Small daily progress leads to big results. 💪",
        "Your future self will thank you! 🌟",
        "Focus on progress, not perfection. 🏆",
        "Every minute counts! Keep going. ⏱️"
    ]
    st.info(random.choice(quotes))
    
    # Progress graph based on completed goals
    st.subheader("Progress Tracker")
    weeks_passed = min(4, (datetime.date.today() - datetime.date.today().replace(day=1)).days // 7 + 1)
    completed_goals = [st.session_state.completed_goals if 'completed_goals' in st.session_state else 0] * weeks_passed
    df_progress = pd.DataFrame({
        "Week": [f"Week {i+1}" for i in range(weeks_passed)],
        "Goals Completed": completed_goals
    })
    fig_progress = px.bar(df_progress, x="Week", y="Goals Completed", color="Goals Completed",
                          color_continuous_scale="viridis")
    fig_progress.update_layout(paper_bgcolor='#1f1f2e', plot_bgcolor='#1f1f2e', font_color='white')
    st.plotly_chart(fig_progress, use_container_width=True)
    
    # Leaderboard
    st.subheader("Leaderboard 🌟")
    leaderboard = pd.DataFrame({
        "User": ["Alice", "Bob", "Charlie", "You", "Eve"],
        "Points": [120, 110, 100, st.session_state.momentum if 'momentum' in st.session_state else 70, 90]
    }).sort_values(by="Points", ascending=False)
    st.table(leaderboard.reset_index(drop=True))
