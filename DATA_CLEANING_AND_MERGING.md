# Data Cleaning and Merging Report

This document describes the key cleaning, transformation, and merging steps applied to combine and prepare the datasets for analysis in the **Beyond the Absence** project.

---

## 📦 Datasets Used

- Postpartum Depression Survey Data
- Child Health and Development Data

---

## 🔧 Cleaning Steps

1. **Column Renaming**
   - Renamed `Age` to `age` in postpartum dataset for consistency.

2. **Handling Missing Values**
   - Dropped rows with missing (`NaN`) values in both datasets to ensure clean merges.

3. **Age Field Standardization**
   - In postpartum dataset, converted age ranges (e.g., `'35-40'`) to the mean numeric value (e.g., `37`).
   - Ensured both datasets' `age` columns were integers for merging.

4. **Datetime Separation**
   - Separated `'Timestamp'` column into:
     - `'date'`: date part (stored as `datetime`)
     - `'time'`: time part (stored as `datetime.time`)

---

## 🔗 Merging Steps

- Merged postpartum and child health datasets using `age` as the common key.
- Used `inner` join to retain only overlapping age records.

---

## 🔍 Correlation Analysis Preparation

1. **Categorical Encoding**
   - Converted all `'Yes'` / `'No'` columns to binary values (`1` / `0`).

2. **Numeric Filtering**
   - Selected only numeric columns for correlation analysis using:
     ```python
     numeric_df = single_mom_df.select_dtypes(include=['number'])
     ```

3. **Correlation Matrix**
   - Computed the correlation matrix:
     ```python
     corr = numeric_df.corr()
     ```

---

## 💾 Final Dataset

- Saved the cleaned and merged dataset as:
