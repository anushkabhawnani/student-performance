import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

st.set_page_config(page_title="Stats", layout="wide")

st.title("📊 Data Stats Dashboard")

df = st.session_state.file

# Check if file was uploaded
st.write("Uploaded dataset preview:")
st.dataframe(df.head())

# Show basic info
st.subheader("Dataset Summary")
st.write(df.describe())

# Plot correlation heatmap
st.subheader("Correlation Heatmap")
numeric_df = df.select_dtypes(include=['float64', 'int64'])

if not numeric_df.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
else:
    st.write("No numeric columns to show correlation.")

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
