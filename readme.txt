# Pharmacy Customer Analytics Dashboard

## Project Overview
This project analyzes pharmacy retail sales transactions to identify high-value customers, repeat customers, and customer purchase interests.  
Using Python and Pandas, raw transactional data was cleaned, transformed, and converted into actionable customer insights that support marketing, operations, and inventory planning decisions.

The dataset contains customer purchases between **21 Oct – 31 Oct 2025**, including sales amount, city, product category, cashier, store, and transaction details.

---

## Business Objective
Transform raw POS sales data into customer intelligence dashboards to help management answer:

- Who are the highest revenue customers?
- Who are the most frequent returning customers?
- What product categories are most preferred by each customer?
- Which cities generate stronger customer activity?
- How can customer segmentation support promotions and stock planning?

---

## Tools & Technologies
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Excel Export Automation

---

## Data Cleaning & Preparation
Performed full data wrangling process:

- Converted transaction date column into datetime format
- Removed missing customer phone numbers
- Standardized phone number format
- Filled null values in category / sub-category / supervisor
- Validated customer transaction records

---

## Key Analysis Performed

### 1. Unique Customer Count
Calculated total active customers during the period:

- **285,436 unique customers**

---

### 2. Customer Interest Profiling
Created a customer segmentation table showing:

- Most purchased category
- Most purchased sub-category
- Main customer city
- Number of orders
- Total sales per customer

---

### 3. Top Revenue Customers
Identified customers with sales greater than **1000 SAR**.

Used for:

- VIP customer targeting
- Loyalty campaigns
- High-value retention strategy

---

### 4. Most Frequent Customers
Identified customers with **4+ transactions**.

Used for:

- Repeat purchase behavior analysis
- Membership / loyalty programs
- Retention campaigns

---

### 5. Sales Distribution Analysis
Built histograms to understand:

- Customer spending behavior
- Order frequency behavior
- Outlier detection

---

## Deliverables
Generated 3 business-ready Excel reports:

- `Top_customer_sales.xlsx`
- `Top_customer_frequancy.xlsx`
- `customer_interests.xlsx`

---

## Business Impact

This project can support:

### Sales & Marketing
- Personalized offers based on customer interests
- Retargeting repeat customers
- VIP customer programs

### Supply Chain & Planning
- Demand forecasting by category
- Fast-moving item replenishment
- City-level inventory allocation

### Quality / Operations
- Customer complaint prioritization for top-value customers
- Service performance tracking by branch

---

## Key Skills Demonstrated

- Data Cleaning
- Exploratory Data Analysis (EDA)
- Customer Segmentation
- KPI Dashboarding
- Business Intelligence
- Retail Analytics
- Supply Chain Thinking
- Report Automation

---

## Future Improvements

- Build interactive Power BI dashboard
- Add RFM customer segmentation
- Predict customer churn
- Forecast category demand
- Store performance benchmarking

---

# Author
Prepared by: [Your Name]  
Role Target: Data Analyst | Supply Chain Analyst | Business Analyst
