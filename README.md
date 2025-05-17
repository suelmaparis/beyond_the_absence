# Beyond the Absence — Single Moms Data Platform

## 💜 I built this as a single mom, for other single moms.

**Beyond the Absence** is now live.  
It’s a platform where our stories are seen.  
Where real data meets real pain.  
Where motherhood without support finds voice, strength, and direction.

🖥️ [Visit the Site](https://beyond-the-absence.onrender.com)  
🎙️ Listen to the podcast  
📊 Explore the dashboard  
🤝 Find resources  
💬 Share your story

> I hope it reaches the women who need it.  
> I hope it reminds you that you’re not invisible.

---

## 📊 Project Overview

This project analyzes and visualizes data related to **single mothers**, focusing on postpartum depression, mental health, and child development.  
It also gives space for real stories, reflections, and community support.

The goal is to combine **data science** and **lived experience** into one accessible platform for single moms everywhere.

---

## 🏗️ Tech Stack

- **Backend:** Python + Flask  
- **Frontend:** HTML, CSS, Bootstrap, Flask templates (Jinja2)  
- **Data Visualization:** Pandas, Plotly, Matplotlib  
- **Database:** Cleaned and merged CSV datasets  
- **Deployment:** Render  
- **Analytics:** Google Analytics (`G-3L8D1R8RQG`) for visitor tracking

---

## 📂 Data Cleaning & Preprocessing

We merged and cleaned two main datasets:

- `postpartum_depression.csv`
- `child_health_development.csv`

Main preprocessing steps:

- ✅ Renamed columns for consistency (e.g., `Age → age`)
- ✅ Converted age ranges into numeric averages
- ✅ Dropped rows with missing values (`NaN`)
- ✅ Split timestamps into `date` and `time`
- ✅ Removed irrelevant text columns for clean correlation
- ✅ Saved the final dataset as `single_mom_dataset.csv`

---

## 📊 Dashboard Features

- Correlation heatmaps between mental health and child outcomes  
- Summary statistics (mean, median, std deviation)  
- Interactive charts grouped by age, marital status, and emotional indicators  
- Health and anxiety indicators in postpartum moms  
- World View section with global comparison (2010 vs 2022)

---

## ✍️ New Features

- ✅ **Blog system**: built-in blog section with real stories, milestones, and mother-to-mother encouragement  
- ✅ **Likes and comments**: users can interact with posts and share experiences  
- ✅ **Email submission**: mothers can share their own stories securely  
- ✅ **Google Analytics**: added tracking to measure site reach and impact  
- ✅ **Podcast integration**: linked episodes to themes and content

---

## ⚙️ How to Run the App Locally

1️⃣ Clone the repository:

```bash
git clone https://github.com/yourusername/beyond-the-absence.git
cd beyond-the-absence
