# 📊 AI-Powered Student Performance Predictor

The **Student Dashboard** is an interactive and user-friendly web application built using Streamlit. It provides students with personalized insights into their academic performance, offering both core functionalities like grade prediction and attendance tracking, and add-on features such as visual analytics, performance alerts and an AI chatbot.

## 🚀 Features

### ✅ Core Features
- **Grade Predictor**  
  Uses machine learning to forecast final grades based on continuous internal assessment scores.

- **Performance Overview**  
  A clean visual summary of subject-wise marks, final score estimations, and academic trends.

- **Attendance Analysis**  
  Displays attendance data and correlates it with academic performance, helping students understand patterns.

### ✨ Add-On Features
- **Interactive Graphs**  
  Beautiful Plotly charts that visualize marks, trends, and predictions for deeper insights.

- **Personal Alerts**  
  System-generated alerts when performance falls below a threshold (e.g., below 70%).

- **AI chatbot**  
  Powered by the Groq API, this provides personalized recommendations and help to teachers and students.

- **Minimal & Intuitive UI**  
  Designed for ease of use with a clean layout that helps students focus on insights.

## 🧠 Tech Stack

| Tool                 | Use Case                         |
|----------------------|----------------------------------|
| `Python`             | Core programming                 |
| `Pandas`, `NumPy`    | Data processing & transformation |
| `Streamlit`          | Interactive web app              |
| `Plotly`             | Data visualizations              |
| `scikit-learn`       | Predictive Analysis              |

## 🧠 How It Works

1. Students enter their test and assignment scores.
2. The model runs a linear regression to estimate the final score.
3. Dashboard visuals are updated instantly with current predictions and insights.

## 📂 Project Structure
```
student-dashboard/
│
├── pages/
│ ├── 1_Stats.py
│ ├── 2_Grade_Predictor.py
│ ├── 3_Attendance.py
│ └── 4_Ask_AI.py
├── Student Performance Sample.csv
├── Dashboard.py
└── requirements.txt
```
## 📥 How to Run It Locally
1. Clone the repository:
```
git clone https://github.com/anushkabhawnani/student-dashboard.git
cd student-dashboard
```
2. Install the required packages:
```
pip install -r requirements.txt
```
3. Run the app:
```
streamlit run Dashboard.py
```
## 📷 Demo

Try out the app here!
[Performnce Predictor](https://student-performance-pzy47aaaf2wgxxtvmtcwbd.streamlit.app/)

### Student Dashboard

[student dashboard](https://github.com/user-attachments/assets/a57db5d7-02f4-4e24-b9a7-71af899cb87c)

### Teacher Dashboard

[teacher dashboard](https://github.com/user-attachments/assets/fb0e5d08-3cd4-456e-83d5-ff953f793b71)

## 🚀 Future Work
* Real-time integration with ERP
* Deploy for a large dataset using SQL

## 🙌 Acknowledgements
* **Streamlit** — for making data apps effortless to deploy and share.
* **Plotly** — for interactive and beautiful visualizations.
* **Groq API** — for providing the API to run the chatbot.
* **Pandas** — for being the heart of all data wrangling.
* **Kaggle** — for providing an open source data set to analyze.

## 👥 Contributors

- [@AnushkaBhawnani](https://github.com/anushkabhawnani) - UI, Dashboard Architecture, Data Visualizations
- [@VaaniJain](https://github.com/TheirUsername) - Grade Prediction Model


