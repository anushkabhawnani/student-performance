import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import plotly.graph_objects as go
import os
from dotenv import find_dotenv, load_dotenv
import smtplib
from email.message import EmailMessage
import textwrap
from tabulate import tabulate

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

senderemail = os.getenv("senderemail")
senderpass = os.getenv("senderpass")


def predict(df):
    y = df['Final_Score']
    features = [
        'Midterm_Score', 'Assignments_Avg', 'Quizzes_Avg', 'Project_Score',
        'Attendance', 'Study_Hours_per_Week', 'Sleep_Hours'
    ]
    X = df[features]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    test_students = df.loc[X_test.index].copy()
    test_students['Predicted_Final_Score'] = y_pred
    results_df = test_students[['First_Name', 'Final_Score', 'Predicted_Final_Score']]
    return r2, rmse, results_df, test_students, features, model

# Safe session state initialization
if "model" not in st.session_state:
    raw_data = pd.read_csv("Student Performance Sample.csv")
    r2, rmse, results_df, test_students, features, model = predict(raw_data)
    st.session_state.model = model
    st.session_state.full_df = raw_data

st.title("📊 Grade Predictor")

if st.session_state.user_role == "Student":
    if "student_row" not in st.session_state:
        st.session_state.student_row = None

    student_row = st.session_state.get("student_row")

    if not student_row:
        st.write("Please log in / enter your details.")
        with st.form("Student Login"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            attendance = st.number_input("Attendance", min_value=0.0, max_value=100.0)
            assignments_avg = st.number_input("Assignments Avg", min_value=0.0, max_value=100.0)
            midterm = st.number_input("Midterm Score", min_value=0.0, max_value=100.0)
            quizzes_avg = st.number_input("Quizzes Avg", min_value=0.0, max_value=100.0)
            project_score = st.number_input("Project Score", min_value=0.0, max_value=100.0)
            study_hours = st.number_input("Study Hours/Week", min_value=0.0)
            sleep_hours = st.number_input("Sleep Hours", min_value=0.0)
            submit = st.form_submit_button("Predict My Grade")
            if submit:
                student_row = {
                    "First_Name": name,
                    "Email_ID": email,
                    "Attendance": attendance,
                    "Assignments_Avg": assignments_avg,
                    "Midterm_Score": midterm,
                    "Quizzes_Avg": quizzes_avg,
                    "Project_Score": project_score,
                    "Study_Hours_per_Week": study_hours,
                    "Sleep_Hours": sleep_hours
                }
                st.session_state.student_row = student_row
                st.rerun()
    else:
        st.subheader(f"Welcome, {student_row['First_Name']}!")
        st.markdown("### Your Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Midterm Score", student_row["Midterm_Score"])
            st.metric("Assignments", student_row["Assignments_Avg"])
            st.metric("Quiz Score", student_row["Quizzes_Avg"])
        with col2:
            st.metric("Attendance", f"{student_row['Attendance']}%")
            st.metric("Hours Studied", student_row["Study_Hours_per_Week"])

        #Prediction
        model = st.session_state.model
        features = [
            'Midterm_Score', 'Assignments_Avg', 'Quizzes_Avg', 'Project_Score',
            'Attendance', 'Study_Hours_per_Week', 'Sleep_Hours'
        ]
        student_data = pd.DataFrame([[student_row[x] for x in features]], columns=features)
        predicted_score = model.predict(student_data)[0]
        st.markdown("### 🎯 Predicted Final Score")
        st.success(f"Your predicted final score is **{predicted_score:.2f}**")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=predicted_score,
            title={'text': "Predicted Final Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [0, 50], 'color': "red"},
                    {'range': [50, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "lightgreen"},
                ],
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

    thresholds = {
        "Midterm_Score": 65,  # <65 suggests weak base
        "Assignments_Avg": 70,  # <70 suggests missing or poor assignments
        "Quizzes_Avg": 70,  # <70 is weak quiz performance
        "Project_Score": 70,  # <70 suggests poor practical work
        "Study_Hours_per_Week": 10,  # <10 hours/week is insufficient
        "Sleep_Hours": 6,  # <6 hours may impact focus
        "Attendance": 75  # <75% attendance is usually poor
    }

    if predicted_score < 70:
        reasons = []

        for column, threshold in thresholds.items():
            if column in student_row and student_row[column] < threshold:
                reasons.append(
                    f"{column.replace('_', ' ')} is {student_row[column]}, which is below the threshold of {threshold}")

        # Prepare and send email
        if reasons:
            student_email = st.session_state.student_row['Email_ID']  # Adjust if your column is named differently

            subject = "Academic Performance Alert"
            body = f"""
    Hi {student_row['First_Name']},

    We noticed that your predicted final score is below 70. Based on our analysis, the following factors may be contributing to this:

    - {chr(10).join(reasons)}

    We recommend addressing these areas to improve your performance.

    Best,
    Model Minds Team
    """

            # Sending the email (fill in your email credentials)
            sender_email = senderemail
            password = senderpass # ⚠️ Best to use environment variable or secrets manager

            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = email

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(sender_email, password)
                smtp.send_message(msg)

            st.success(f"Email sent to {st.session_state.student_row['Email_ID']} with the reasons for low score.")
        else:
            st.info("Final score is low, but no major issues found in contributing factors.")
    else:
        st.success("Final score is satisfactory. No email sent.")

if st.session_state.user_role == "Teacher":
    raw_data = pd.read_csv("Student Performance Sample.csv")
    r2, rmse, results_df, test_students, features, model = predict(raw_data)
    df = st.session_state.full_df

    st.header('Raw Data')
    cols = [
        'Student_ID', 'First_Name', 'Gender', 'Department', 'Midterm_Score', 'Assignments_Avg',
        'Quizzes_Avg', 'Project_Score', 'Attendance',
        'Study_Hours_per_Week', 'Sleep_Hours'
    ]
    st.dataframe(df[cols].head())

    # Display metrics
    st.subheader("Model Evaluation Metrics")
    st.write(f"**R² Score:** {r2:.4f}")
    st.write(f"**RMSE:** {rmse:.4f}")
    st.text('The low RMSE score shows the accuracy of the findings.')

    st.subheader("Top 10 individual predictions")
    final_students = test_students.sort_values('Predicted_Final_Score', ascending=False)
    st.dataframe(final_students.head(10))

    st.session_state.final_students = final_students
    risk_alert = st.checkbox(
        "Would you like to receive a mail about the students predicted to score less than the threshold?")
    if risk_alert:
        threshold = st.select_slider(label="Select the threshold",
                                     options=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        button = st.button("Send Email")
        if button:
            risk_students = []
            for _, row in st.session_state.file.iterrows():
                if row['Final_Score'] < int(threshold):
                    risk_students.append({
                        "Student_Name": row["First_Name"],
                        "Student_ID": row['Student_ID'],
                        "Final_Score": row['Predicted_Final_Score']
                    })

            teacher_email = st.session_state.teacher_email

            table = tabulate(risk_students, headers="keys", tablefmt="github")

            subject = "Academic Performance Alert"
            body = textwrap.dedent(f"""
    Hello Teacher,

    This is in regards to the students who are estimated to perform lower than {threshold} this semester according to our Grade Prediction system:

    {table}

    We recommend reaching out to these students asking them to improve.

    Best,
    Model Minds Team
    """)

            sender_email = senderemail
            password = senderpass

            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = senderemail
            msg['To'] = st.session_state.teacher_email

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(senderemail, senderpass)
                smtp.send_message(msg)

            st.success(f"Email sent!")

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
