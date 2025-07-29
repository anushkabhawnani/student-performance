import streamlit as st
import pandas as pd

st.set_page_config(page_title="Upload CSV", layout="wide")

st.title("📂 Upload Your CSV File")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.session_state["uploaded_df"] = df

    st.success("✅ File uploaded successfully! You can now check your stats!")

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
