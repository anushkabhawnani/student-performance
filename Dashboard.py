import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# ------------------- PREDICTION FUNCTION -------------------
def predict(df):
    y = df['Final_Score']
    features = [
        'Midterm_Score', 'Assignments_Avg', 'Quizzes_Avg',
        'Project_Score', 'Attendance', 'Study_Hours_per_Week', 'Sleep_Hours'
    ]
    X = df[features]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    test_students = df.loc[y_test.index].copy()
    test_students['Predicted_Final_Score'] = y_pred
    test_students = test_students.round(2)

    cols_to_show = [
        'Student_ID', 'First_Name', 'Gender', 'Department', 'Midterm_Score', 'Assignments_Avg',
        'Quizzes_Avg', 'Project_Score', 'Attendance',
        'Study_Hours_per_Week', 'Sleep_Hours', 'Predicted_Final_Score'
    ]

    results_df = pd.DataFrame({
        'Actual Final Score': y_test,
        'Predicted Final Score': y_pred
    })

    return r2, rmse, results_df, test_students, cols_to_show, model

# ------------------- INITIALIZE SESSION + DATA -------------------
if "model" not in st.session_state:
    raw_data = pd.read_csv("Student Performance Sample.csv")
    r2, rmse, results_df, test_students, cols_to_show, model = predict(raw_data)
    st.session_state.file = test_students[cols_to_show]
    st.session_state.model = model
    st.session_state.full_df = raw_data

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "student_row" not in st.session_state:
    st.session_state.student_row = None
if "teacher_email" not in st.session_state:
    st.session_state.teacher_email = ""

# ------------------- LOGIN PAGE -------------------
if not st.session_state.logged_in:
    st.set_page_config(page_title="Login Page", layout="centered", initial_sidebar_state="collapsed")
    st.title("Login Portal")

    role = st.selectbox("Are you a Student or a Teacher?", ["", "Student", "Teacher"])
    if role:
        st.session_state.user_role = role

    df = st.session_state.file

    if role == "Student":
        name = st.text_input("Enter your Name")
        email = st.text_input("Enter your Email ID")
        mid_term_score = st.number_input("Enter your Mid Term Score", min_value=0.0, max_value=100.0)
        assignment_avg_score = st.number_input("Enter your Assignment Average Score", min_value=0.0, max_value=100.0)
        quiz_avg_score = st.number_input("Enter your Quiz Average Score", min_value=0.0, max_value=100.0)
        project_avg_score = st.number_input("Enter your Project Average Score", min_value=0.0, max_value=100.0)
        attendance = st.slider("Attendance (%)", 0, 100, 75)
        study_hrs_week = st.number_input("Enter your Study Hours Per Week", min_value=0.0)
        sleep_hrs_week = st.number_input("Enter your Sleep Hours", min_value=0.0)

        if st.button("Login"):
            model = st.session_state.model
            input_df = pd.DataFrame([{
                'Midterm_Score': mid_term_score,
                'Assignments_Avg': assignment_avg_score,
                'Quizzes_Avg': quiz_avg_score,
                'Project_Score': project_avg_score,
                'Attendance': attendance,
                'Study_Hours_per_Week': study_hrs_week,
                'Sleep_Hours': sleep_hrs_week
            }])
            predicted_score = model.predict(input_df)[0]

            new_row = {
                'Student_ID': f"ST{np.random.randint(1000, 9999)}",
                'Email_ID': email,
                'First_Name': name,
                'Gender': np.random.choice(['Male', 'Female']),
                'Department': np.random.choice(['Data Science', 'AI', 'ML']),
                'Midterm_Score': mid_term_score,
                'Assignments_Avg': assignment_avg_score,
                'Quizzes_Avg': quiz_avg_score,
                'Project_Score': project_avg_score,
                'Attendance': attendance,
                'Study_Hours_per_Week': study_hrs_week,
                'Sleep_Hours': sleep_hrs_week,
                'Final_Score': predicted_score
            }

            st.session_state.student_row = new_row
            st.session_state.logged_in = True
            st.rerun()

    elif role == "Teacher":
        email = st.text_input("Enter your Email ID")
        if st.button("Login"):
            if email:
                st.session_state.teacher_email = email
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.warning("Please enter your email.")

    st.stop()

# ------------------- STUDENT DASHBOARD -------------------
if st.session_state.logged_in and st.session_state.user_role == "Student":
    st.set_page_config(page_title="Student Dashboard", layout="wide", initial_sidebar_state="expanded")

    student_row = st.session_state.student_row
    st.markdown(f"## 👋 Hello {student_row['First_Name']}")
    st.markdown("Let’s See What’s Scheduled Up For You Today!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Recent Assignments")
        st.progress(25 / 30)
        st.text("100x Engineers Buildathon")

    with col2:
        st.subheader("Study Materials")
        st.write("📘 Guides and Regulations - 6.5 MB")
        st.write("📕 AI in Data Science - 5.1 MB")
        st.write("📗 Intro to Linear Algebra - 2.3 MB")

    with col3:
        st.subheader("Calendar")
        calendar_html = f"""
            <style>
                .calendar-container {{
                    font-size: 12px;
                    width: 250px;
                    padding: 5px;
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
            </style>
            <div class="calendar-container">
                <div class="month-title">{datetime.now().strftime('%B')} - {datetime.now().year}</div>
                <table>
                    <tr><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr>
                    <tr><td>28</td><td>29</td><td>30</td><td>31</td><td>1</td><td>2</td><td>3</td></tr>
                    <tr><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td></tr>
                    <tr><td>11</td><td>12</td><td>13</td><td>14</td><td>15</td><td>16</td><td>17</td></tr>
                    <tr><td>18</td><td>19</td><td>20</td><td>21</td><td>22</td><td>23</td><td>24</td></tr>
                    <tr><td>25</td><td>26</td><td>27</td><td>28</td><td>29</td><td>30</td><td>31</td></tr>
                </table>
            </div>
        """

        st.markdown(calendar_html, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Recent Achievements")
    st.success("🏆 Top 10 On The Leaderboard - Grinded 6 hrs | 05 Checkpoints")
    st.info("🎖️ Early Bird Badge - 4 hrs | 03 Logins | 4 Tasks")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.subheader("Hours Spent")
        hours_df = pd.DataFrame({
            'Category': ['Study Hours per Week', 'Sleep Hours'],
            'Hours': [student_row['Study_Hours_per_Week'], student_row['Sleep_Hours']]
        })
        fig = px.bar(hours_df, x='Category', y='Hours', text='Hours', height=400,
                     title=f"Study vs Sleep Hours for {student_row['Student_ID']}")
        fig.update_traces(textposition='inside')
        fig.update_layout(yaxis_title='Hours', xaxis_title='Category', showlegend=False)
        st.plotly_chart(fig)

    with col5:
        st.subheader("Grade Overview")
        gpa = (student_row['Final_Score'] / 100) * 10
        gauge = go.Figure(go.Indicator(mode="gauge+number", value=gpa, title={'text': "Your Grade"},
                                       gauge={'axis': {'range': [0, 10]}}))
        st.plotly_chart(gauge)

    with col6:
        st.subheader("To Do List")
        st.checkbox("Complete Math Homework")
        st.checkbox("Prepare for physics quiz")
        st.checkbox("Submit essay draft")

# ------------------- TEACHER DASHBOARD -------------------
if st.session_state.logged_in and st.session_state.user_role == "Teacher":
    st.set_page_config(page_title="Teacher Dashboard", layout="wide")
    df = st.session_state.file

    st.markdown("## 🧑‍🏫 Welcome Back, Teacher!")
    st.write("Here's your classroom overview and student performance insights.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Resources & Actions")
        st.file_uploader("Upload new study material or student report", type=["pdf", "csv", "xlsx"])

    with col2:
        st.subheader("Upcoming Deadlines")
        st.markdown("- **Midterm Report** — Aug 20")
        st.markdown("- **Assignment Review** — Sep 5")
        st.markdown("- **Final Exams** — Oct 10")

    with col3:
        st.subheader("Top 3 Students")
        top_students = df.sort_values("Predicted_Final_Score", ascending=False).head(3)
        st.table(top_students[["Student_ID", "First_Name", "Predicted_Final_Score"]].reset_index(drop=True))

    st.markdown("---")

    st.subheader("Recent Achievements")
    st.success("🏆 Completed New Curriculum Training - AI in Data Science - July 2025")
    st.info("🎖️ Proactive Planner Badge - 5 Early Submissions | 3 Lesson Plans Ahead")

    col5, col6, col7 = st.columns(3)

    with col5:
        st.subheader("Grade Distribution")
        fig = px.histogram(df, x="Predicted_Final_Score", nbins=10, labels={"x": "Predicted Score"}, height=300)
        fig.update_layout(xaxis_title="Score", yaxis_title="No. of Students")
        st.plotly_chart(fig)

    with col6:
        st.subheader("Grade Overview")
        avg_gpa = df["Predicted_Final_Score"].mean()
        gauge = go.Figure(go.Indicator(mode="gauge+number", value=(avg_gpa / 100) * 10,
                                       title={'text': "Average"}, gauge={'axis': {'range': [0, 10]}}))
        st.plotly_chart(gauge)

    with col7:
        st.subheader("To Do List")
        st.checkbox("Send Announcement")
        st.checkbox("Update Grade Sheet")
        st.checkbox("Review Absentees")

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

    <a href="Ask_AI" class="floating-btn" target="_self" style="text-decoration: none; color: white;">💬 Ask AI</a>
""", unsafe_allow_html=True)
