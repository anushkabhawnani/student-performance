import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime
import plotly.express as px

st.set_page_config(layout="wide", page_title="Student Dashboard")

file = 'Student Performance Sample.csv'
df = pd.read_csv(file)
st.session_state['file'] = df

# Set up a key for session state
if 'student_id' not in st.session_state:
    st.session_state.student_id = ""

# Show input only if student_id is not already set
if not st.session_state.student_id:
    user = st.selectbox('Are you a Student or Teacher?', ('Student', 'Teacher'))

    if user == 'Student':
        student_id = st.text_input('Please enter your Student ID to continue')

        if student_id:
            st.session_state.student_id = student_id
            student_row = df[df.Student_ID == student_id].iloc[0]
            st.session_state['student_row'] = student_row
            st.rerun()
else:
    # Top Header
    student_name = df.First_Name[df.Student_ID == st.session_state.student_id].values[0]
    st.markdown(f"## 👋 Hello {student_name}")
    st.markdown("Let’s See What’s Scheduled Up For You Today!")

    # Columns
    col1, col2, col3 = st.columns([1.2, 1.5, 1])

    # Recent Hackathons
    with col1:
        st.subheader("Recent Assignments")
        st.progress(25/30)
        st.text("100x Engineers Buildathon")

    # Your Resources
    with col2:
        st.subheader("Study Materials")
        st.write("📘 Guides and Regulations - 6.5 MB")
        st.write("📕 AI in Data Science - 5.1 MB")
        st.write("📗 Intro to Linear Algebra - 2.3 MB")

    # Calendar (Static placeholder for now)
    with col3:
        st.subheader(f"Calendar")
        st.markdown(
            f"""
            <style>
            .calendar-container {{
                font-size: 12px;
                width: 250px;
                padding: 5px;
                margin: auto;
                background-color: #1e1e2f;
                color: white;
                border-radius: 10px;
            }}
    
            .calendar-container table {{
                width: 100%;
                border-collapse: collapse;
            }}
    
            .calendar-container td, .calendar-container th {{
                padding: 2px;
                text-align: center;
                border: 1px solid #444;
            }}
    
            .calendar-container .month-title {{
                font-size: 14px;
                margin-bottom: 5px;
            }}
    
            .calendar-container .nav-buttons {{
                font-size: 12px;
                padding: 2px 6px;
            }}
            </style>
    
            <div class="calendar-container">
                <div class="month-title">{datetime.now().strftime('%B')} - {datetime.now().year}</div>
                <table>
                    <tr>
                        <th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th>
                        <th>Thu</th><th>Fri</th><th>Sat</th>
                    </tr>
                    <tr><td>29</td><td>30</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr>
                    <tr><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td><td>11</td><td>12</td></tr>
                    <tr><td>13</td><td>14</td><td>15</td><td>16</td><td>17</td><td>18</td><td>19</td></tr>
                    <tr><td>20</td><td>21</td><td>22</td><td>23</td><td>24</td><td>25</td><td>26</td></tr>
                    <tr><td>27</td><td>28</td><td>29</td><td>30</td><td>31</td><td>1</td><td>2</td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Achievements
    st.markdown("---")
    st.subheader("Recent Achievements")
    st.success("🏆 Top 10 On The Leaderboard - Grinded 6 hrs | 05 Checkpoints")
    st.info("🎖️ Early Bird Badge - 4 hrs | 03 Logins | 4 Tasks")

    # Charts and Graphs
    col4, col5, col6 = st.columns(3)

    with col4:
        st.subheader("Hours Spent")
        # data = {"Month": ["Jan", "Feb", "Mar", "Apr", "May"],
        #         "Grind": [40, 60, 70, 45, 20],
        #         "Assignments": [20, 30, 35, 25, 10]}
        if 'student_row' in st.session_state:
            student_data = st.session_state['student_row']

            # Extract required values
            hours_data = {
                'Category': ['Study Hours per Week', 'Sleep Hours'],
                'Hours': [student_data['Study_Hours_per_Week'], student_data['Sleep_Hours']]
            }

            hours_df = pd.DataFrame(hours_data)

            # Plot horizontal bar chart
            fig = px.bar(
                hours_df,
                x='Category',
                y='Hours',
                text='Hours',
                height=400,
                title=f"Study vs Sleep Hours for {student_data['Student_ID']}"
            )

            fig.update_traces(textposition='inside')
            fig.update_layout(yaxis_title='Hours', xaxis_title='Category', showlegend=False)

            # Show in Streamlit
            st.plotly_chart(fig)

        else:
            st.warning("No student data found. Please select a student first.")

    student_row = st.session_state.student_row
    gpa = (student_row['Final_Score'] / 100) * 10

    with col5:
        st.subheader("Grade Overview")
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=gpa,
            title={'text': "Your Grade"},
            gauge={'axis': {'range': [0, 10]}}
        ))
        st.plotly_chart(gauge)

    with col6:
        st.subheader("To Do List")
        st.checkbox("Complete Math Homework")
        st.checkbox("Prepare for physics quiz")
        st.checkbox("Submit essay draft")
        # st.checkbox("Subscription")

    st.markdown("""
        <style>
        .floating-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background-color: #2e004d;
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 10px;
            font-size: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            cursor: pointer;
            z-index: 9999;
            text-decoration: none; !important
            font-family: inherit;
            outline: none;
            -webkit-font-smoothing: antialiased;
            text-align: center;
            display: inline-block;
        }
    
        .floating-btn:hover {
            background-color: #130316;
            text-decoration: none;
        }
    
        .floating-btn:focus {
            outline: none;
            box-shadow: none;
            text-decoration: none;
        }
    
        a.floating-btn:visited,
        a.floating-btn:active {
            color: white;
            text-decoration: none;
        }
        </style>
    
        <a href="/Ask_AI" class="floating-btn" target="_self" style="text-decoration: none; color: white;">💬 Ask AI</a>
    """, unsafe_allow_html=True)



# ---

## 🎨 Styling Like the Image
#
# - Streamlit uses a dark theme by default if system settings are dark.
# - For advanced theming:
# ```toml
# # .streamlit/config.toml
# [theme]
# primaryColor = "#f97316"
# backgroundColor = "#0d0d0d"
# secondaryBackgroundColor = "#1a1a1a"
# textColor = "#ffffff"
