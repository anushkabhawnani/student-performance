import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

st.set_page_config(page_title="Stats", layout="wide")

st.title("📊 Data Stats Dashboard")

df = st.session_state.file

if st.session_state.user_role == "Teacher":
    # Check if file was uploaded
    st.write("Uploaded dataset preview:")
    st.dataframe(df.head())

    # Show basic info
    st.subheader("Dataset Summary")
    st.write(df.describe())

    st.subheader("View Individual Student")

    student_id = st.selectbox("Select a student ID", df["Student_ID"].unique())
    student_data = df[df["Student_ID"] == student_id].iloc[0]

    st.markdown(f"### 👤 {student_data['First_Name']} (ID: {student_id})")

    col4, col5 = st.columns(2)

    with col4:
        st.metric("Midterm Score", f"{student_data['Midterm_Score']}%")
        st.metric("Final Score", f"{student_data['Predicted_Final_Score']}%")

    with col5:
        st.metric("Study Hours/Week", f"{student_data['Study_Hours_per_Week']} hrs")
        st.metric("Sleep Hours", f"{student_data['Sleep_Hours']} hrs")

    st.markdown("---")

    numeric_df = df.select_dtypes(include=['float64', 'int64'])

    # Select variables to visualize
    st.subheader("Interactive Scatter Plot")
    x_col = st.selectbox("Select X-axis feature", df.columns)
    y_col = st.selectbox("Select Y-axis feature", df.columns)

    if pd.api.types.is_numeric_dtype(df[x_col]) and pd.api.types.is_numeric_dtype(df[y_col]):
        fig = px.scatter(df, x=x_col, y=y_col, color=df.columns[-1], title=f"{y_col} vs {x_col}")
        st.plotly_chart(fig)
    else:
        st.warning("Please select numeric columns for scatter plot.")

    # Bar plot for categorical impact
    st.subheader("Categorical Feature Impact")
    cat_col = st.selectbox("Select a Categorical Feature", df.select_dtypes(include='object').columns)
    num_col = st.selectbox("Select a Numeric Feature", numeric_df.columns)

    fig2 = px.box(df, x=cat_col, y=num_col, points="all", title=f"{num_col} Distribution by {cat_col}")
    st.plotly_chart(fig2)

    # Optional: Pairplot with Seaborn (for full relationship matrix)
    st.subheader("Pairplot of Numeric Features")
    if st.checkbox("Show Pairplot (Warning: Can be slow)"):
        fig3 = sns.pairplot(numeric_df)
        st.pyplot(fig3)

if st.session_state.user_role == "Student":
    email = st.session_state.student_row['Email_ID']
    name = st.session_state.student_row['First_Name']
    attendance = st.session_state.student_row['Attendance']
    midterm = st.session_state.student_row['Midterm_Score']
    assignment = st.session_state.student_row['Assignments_Avg']
    final = st.session_state.student_row['Final_Score']

    st.subheader(f"Welcome, {name} 👋")

    if final >= 80:
        st.info("You're in the **Top 25%** based on predicted scores.")
    elif final >= 60:
        st.info("You're in the **Middle 50%** — keep pushing!")
    else:
        st.info("You're in the **Bottom 25%** — take action early.")

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Final Score Prediction", f"{final:.1f}%")
    col2.metric("Attendance", f"{attendance:.1f}%")
    col3.metric("Assignment Score", f"{assignment}/100")

    # Strengths & Suggestions
    st.subheader("Smart Insights")
    if midterm >= 75:
        st.success("✅ You're doing well in midterms!")
    if assignment < 50:
        st.warning("⚠️ Your assignment score is low. Focus here.")
    if attendance < 75:
        st.warning("⚠️ Low attendance might affect your performance.")

    # Personal Goal Tracker
    st.subheader("Your Goal Tracker")
    target_score = st.slider("Set your target final score:", min_value=50, max_value=100, value=80)
    progress = final / target_score * 100
    st.progress(min(progress / 100, 1.0), f"{progress:.1f}% of your target achieved")

    st.markdown("---")

    # Progress Timeline
    st.subheader("Performance Timeline")
    timeline_df = pd.DataFrame({
        'Stage': ['Midterm', 'Assignment', 'Final Prediction'],
        'Score': [midterm, assignment, final]
    })
    st.line_chart(timeline_df.set_index("Stage"))

else:
    st.error("No data found for that Student ID. Please check again.")

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
