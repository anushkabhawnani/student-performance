import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import smtplib
from email.message import EmailMessage
from Dashboard import student_row
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

email = os.getenv('sender_email')
pass_word = os.getenv('password')

st.set_page_config(page_title="Grade Predictor", layout="wide")

st.title("📈 Grade Predictor")

df = st.session_state.file

st.header('Raw Data')
st.dataframe(df.head())

y = df['Final_Score']

features = [
    'Midterm_Score', 'Assignments_Avg', 'Quizzes_Avg',
    'Project_Score', 'Attendance', 'Study_Hours_per_Week', 'Sleep_Hours'
]
X = df[features]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Calculate metrics
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# Display metrics
st.subheader("Model Evaluation Metrics")
st.write(f"**R² Score:** {r2:.4f}")
st.write(f"**RMSE:** {rmse:.4f}")
st.text('The low RMSE score shows the accuracy of the findings.')

results_df = pd.DataFrame({
    'Actual Final Score': y_test,
    'Predicted Final Score': y_pred
})

# Plotly scatter plot
st.subheader('Actual vs Final Predicted Score')
sorted_idx = np.argsort(y_test)
y_test_sorted = y_test.values[sorted_idx]
y_pred_sorted = y_pred[sorted_idx]

# Create figure
fig = go.Figure()

# Scatter plot (actual vs predicted)
fig.add_trace(go.Scatter(
    x=y_test,
    y=y_pred,
    mode='markers',
    name='Predictions',
    marker=dict(color='yellow', size=8, opacity=0.6)
))

# Regression line
fig.add_trace(go.Scatter(
    x=y_test_sorted,
    y=y_test_sorted,  # y = x line
    mode='lines',
    name='Ideal Line',
    line=dict(color='orange')
))

# Layout styling
fig.update_layout(
    title='Actual vs Predicted Final Score',
    xaxis_title='Actual Final Score',
    yaxis_title='Predicted Final Score',
    legend=dict(x=0.01, y=0.99),
    height=500
)

# Show in Streamlit
st.plotly_chart(fig)

thresholds = {
    "Midterm_Score": 65,              # <65 suggests weak base
    "Assignments_Avg": 70,             # <70 suggests missing or poor assignments
    "Quizzes_Avg": 70,                # <70 is weak quiz performance
    "Project_Score": 70,              # <70 suggests poor practical work
    "Study_Hours_per_Week": 10,       # <10 hours/week is insufficient
    "Sleep_Hours": 6,                 # <6 hours may impact focus
    "Attendance": 75                  # <75% attendance is usually poor
}

if student_row['Final_Score'] < 70:
    reasons = []

    for column, threshold in thresholds.items():
        if column in student_row and student_row[column] < threshold:
            reasons.append(f"{column.replace('_', ' ')} is {student_row[column]}, which is below the threshold of {threshold}")

    # Prepare and send email
    if reasons:
        student_email = 'anushkab1411@gmail.com'  # Adjust if your column is named differently

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
        sender_email = email
        password = pass_word # ⚠️ Best to use environment variable or secrets manager

        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = student_email

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, password)
            smtp.send_message(msg)

        st.success(f"Email sent to {student_email} with the reasons for low score.")
    else:
        st.info("Final score is low, but no major issues found in contributing factors.")
else:
    st.success("Final score is satisfactory. No email sent.")

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