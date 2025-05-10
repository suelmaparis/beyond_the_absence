Beyond the Absence — Single Moms Data Dashboard

📊 Project Overview

This project aims to analyze and visualize data related to single mothers, focusing on postpartum depression and child health development. The goal is to raise awareness and provide insights through a clean, interactive dashboard.

🏗️ Project Structure

Backend: Python + Flask
Frontend: HTML, CSS, Flask templates (Jinja2)
Data Visualization: Pandas, Matplotlib, Seaborn (and/or Plotly)
Database: Cleaned CSV files merged from multiple datasets
📂 Data Cleaning & Preprocessing

We merged two main datasets:

Postpartum Depression Data (postpartum_depression.csv)
Child Health Development Data (child_health_development.csv)
Main cleaning steps:
✅ Renamed columns for consistency (e.g., Age → age)
✅ Dropped missing values (NaN)
✅ Converted age ranges (like '35-40') into numeric averages
✅ Split combined Timestamp into two columns:

date → stored as datetime.date
time → stored as datetime.time
✅ Removed non-numeric or text columns when computing correlations
✅ Saved the final cleaned and merged dataset as single_mom_dataset.csv
📊 Dashboard Features

Correlation heatmaps between variables
Summary statistics (mean, median, std deviation)
Interactive plots showing trends by age, marital status, and other factors
Insights into postpartum mental health and child outcomes
⚙️ How to Run the App

1️⃣ Clone the repository:

git clone https://github.com/yourusername/beyond-the-absence.git
cd beyond-the-absence
2️⃣ Install dependencies:

pip install -r requirements.txt
3️⃣ Run the Flask app:

python app.py
4️⃣ Open in your browser:

http://127.0.0.1:5000/
✨ About

Created by Suelma Paris as part of the Beyond the Absence podcast and project, empowering and giving voice to single mothers.
This project blends data science, storytelling, and advocacy to shed light on invisible challenges.

