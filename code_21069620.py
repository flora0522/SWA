# -*- coding: utf-8 -*-
"""Copy of Yet another copy of SWA REAL Assignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17wSVYc9coglbW_UMdou5vhiM8i8BiFiB

# **Jobstreet Job Vacancy Scraping**

In this assignment, we scrape at least 50 data objects and 5 data variables based on the search of job title: "Data Analyst"  and location: "Kuala Lumpur". To start off, we ensure that the project's requirements are satisfied by installing the necessary packages. For instance:

1.   requests: For making HTTP requests to fetch data from web pages,
2.   beautifulsoup4: For parsing HTML and extracting data from web pages,
3.   pandas: For data manipulation and analysis,
"""

# Install necessary and additional packages
!pip install requests beautifulsoup4 pandas

# Import required libraries
# For data understanding and data preprocessing
import pandas as pd
import requests
import re
import numpy as np
from bs4 import BeautifulSoup

# For data visualization
import matplotlib.pyplot as plt
import seaborn as sns

"""# **Data Understanding**

The purpose of performing data understanding is to gain general insights about the data that will potentially be helpful for the further steps in the data analysis process.

"""

# Function to fetch job data from the Jobstreet API
def fetch_job_data(page):
    api_url = f'https://www.jobstreet.com.my/api/chalice-search/v4/search?siteKey=MY-Main&sourcesystem=houston&userqueryid=f15f804c0333e59ed04904501dcb0a1d-0222597&userid=571146a2-6e5c-45e5-90ac-596d754bcc1a&usersessionid=571146a2-6e5c-45e5-90ac-596d754bcc1a&eventCaptureSessionId=571146a2-6e5c-45e5-90ac-596d754bcc1a&where=Kuala+Lumpur&page={page}&seekSelectAllPages=true&keywords=data+analyst&pageSize=30&include=seodata&locale=en-MY&solId=ef00f46c-f1c0-47b5-9dd2-db3fdb8e28a7'
    response = requests.get(api_url) # Send a GET request to the API
    if response.status_code == 200: # Check if the request was successful
        return response.json().get('data', [])
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

# Lists to store the data
job_titles = []
company_names = []
locations = []
salaries = []
job_types = []

page = 1 # Start with the first page
while len(job_titles) < 150: # Loop to fetch and process data until we have at least 150 job postings with salaries
    data_items = fetch_job_data(page)
    if not data_items:
        break  # Stop if no more data is returned

    for item in data_items: # Process each job item in the returned data
        if isinstance(item, dict): # Extract relevant fields from the job item
            job_title = item.get('title', '')
            company_name = item.get('advertiser', {}).get('description', '')
            location = item.get('location', '')
            salary = item.get('salary', '')
            job_type = item.get('workType', '')

            # Only add the job if it has a salary
            if salary:
                job_titles.append(job_title)
                company_names.append(company_name)
                locations.append(location)
                salaries.append(salary)
                job_types.append(job_type)

                if len(job_titles) >= 150:
                    break  # Break the inner loop if we have enough data
    page += 1 # Increment the page number to fetch the next page of data

# Create a DataFrame from the collected job data
df = pd.DataFrame({
    'Job Title': job_titles,
    'Company Name': company_names,
    'Location': locations,
    'Salary': salaries,
    'Job Type': job_types
})

"""### **Exploratory Data Analysis (EDA)**

EDA is used to analyze dataset to extract characteristic information and to obtain a bird's eye view on the features of our data. It usually help us to gain insights into the data and identify patterns, trends, relationships, anomalies, and potential issues or challenges that may need to be addressed during the following sections.
"""

# Summary of Pandas DataFrame
df.info()

# Print the DataFrame
df

"""# **Data Preprocessing**
Here, we convert raw data into a tidy dataset in order to improve data quality and enable effective data analysis. This involves identifying and handling missing data and other inconsistencies in the dataset before feeding it into an algorithm for further analysis.

### **Data Cleaning**

**Standard and Non Standard Missing Values**

Standard missing values are values that are intentionally left blank or null, usually because the data was not collected or is not available.
Whereas non-standard missing values are values that are not recognized as missing values by software or algorithms such as data entry errors, encoding problems and data format issues.
"""

# Check for missing values
df.isnull().sum()

#Since there are no standard blank missing values for pandas function to detect,
# we will need to identify the number of non standard blank missing values in this dataframe
# Identify the non standard missing value of '?' in each column by descending order
print("Number of non standard '?' missing value in the dataset: ")
df_replaced = df.replace(['?', '!'], np.NaN)
df_replaced.head(15)
print(df_replaced.isna().sum().sort_values(ascending=False))

"""**Duplicated Values**"""

# Show true if there are duplicated values, False if there are none
print('Are there any duplicated values in this dataset?', df.duplicated().any())

# Total number of duplicated values
print('Number of total duplicated records in this dataset:', df.duplicated().sum())

# To check number of duplicated values compared with non-duplicated values
print('Number of non-duplicated records in this dataset:', len(df) - df.duplicated().sum())

# Define the pattern for the common salary range and single salary
common_salary_pattern = r'^(RM\s*\d{1,3}(,\d{3})*\s*–\s*RM\s*\d{1,3}(,\d{3})*\s*per\s*month$|RM\s*\d{1,3}(,\d{3})*\s*per\s*month$|RM\s*\d+\s*per\s*month$)'

# Create a boolean mask for rows that match the common salary range pattern
mask = df['Salary'].str.match(common_salary_pattern, na=False)

# Filter the DataFrame to keep only rows with common salary ranges
df_cleaned = df[mask]

# Print the number of rows before and after cleaning
print(f'Number of rows before cleaning: {len(df)}')
print(f'Number of rows after cleaning: {len(df_cleaned)}')

# Save the cleaned DataFrame to a new Excel file
df_cleaned.to_excel('cleaned_job_listings.xlsx', index=False)
print("Cleaned data saved to 'cleaned_job_listings.xlsx' successfully.")

# Show information about the cleaned dataframe
df_cleaned.info()

"""### **Exploratory Data Analysis (EDA)**"""

# Load the DataFrame from your source (e.g., CSV, Excel)
df = pd.read_excel('cleaned_job_listings.xlsx')

# Heatmap of Job Type by Location
plt.figure(figsize=(14, 10))
job_type_location = df_cleaned.pivot_table(index='Location', columns='Job Type', aggfunc='size', fill_value=0)
sns.heatmap(job_type_location, cmap='viridis', annot=True, fmt="d")
plt.title('Heatmap of Job Type by Location')
plt.xlabel('Job Type')
plt.ylabel('Location')
plt.show()

# Top Companies Hiring
plt.figure(figsize=(10, 6))
top_companies = df['Company Name'].value_counts().head(10)
sns.barplot(y=top_companies.index, x=top_companies.values)
plt.title('Top 10 Companies Hiring')
plt.xlabel('Number of Job Listings')
plt.ylabel('Company Name')

plt.show()

# Job Listings by Location with numbers annotated
plt.figure(figsize=(10, 6))
top_locations = df['Location'].value_counts().head(10)
ax = sns.barplot(y=top_locations.index, x=top_locations.values)
plt.title('Job Listings by Location')
plt.xlabel('Number of Job Listings')
plt.ylabel('Location')

# Annotate each bar with the count value
for p in ax.patches:
    width = p.get_width()
    plt.text(width + 1,  # x-coordinate for the text (slightly offset from the bar)
             p.get_y() + p.get_height() / 2,  # y-coordinate for the text (centered vertically in the bar)
             int(width),  # The text to display (the count value)
             ha='center',  # Horizontal alignment
             va='center')  # Vertical alignment

plt.show()

# Job Type Analysis
job_types_count = df['Job Type'].value_counts()

# Function to display percentage and count
def autopct_format(values):
    def inner_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{:.1f}%\n({:d})'.format(pct, val)
    return inner_autopct

# Job Types Pie Chart
plt.figure(figsize=(8, 8))
plt.pie(job_types_count, labels=job_types_count.index, autopct=autopct_format(job_types_count), startangle=140)
plt.title('Job Types Distribution')

# Display the chart
plt.tight_layout()
plt.show()

# Function to extract salary values from the salary string
def extract_salary(salary_str):
    if '–' in salary_str:
        min_salary, max_salary = re.findall(r'\d+', salary_str.replace(',', ''))
        return (int(min_salary) + int(max_salary)) / 2
    else:
        salary = re.findall(r'\d+', salary_str.replace(',', ''))[0]
        return int(salary)

# Apply the function to the Salary column
df_cleaned['Average Salary'] = df_cleaned['Salary'].apply(extract_salary)

# Group by Job Title and compute the average salary
avg_salary_by_title = df_cleaned.groupby('Job Title')['Average Salary'].mean().sort_values(ascending=False)

# Get the top 10 job titles with the highest average salaries
top_10_avg_salary_by_title = avg_salary_by_title.head(10)

# Plot the results
plt.figure(figsize=(12, 8))
sns.barplot(x=top_10_avg_salary_by_title.values, y=top_10_avg_salary_by_title.index)
plt.xlabel('Average Salary (RM)')
plt.ylabel('Job Title')
plt.title('Top 10 Job Titles with Highest Average Salary')
plt.show()