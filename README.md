📌 Project Description: Web Scraping Wuzzuf Job Listings
📝 Overview:
A Python project that performs Web Scraping on the Wuzzuf job site to extract job postings based on a search keyword entered by the user (e.g., "Python Developer").
The results are displayed in a formatted table and saved into a CSV file for later use or analysis.

🎯 Project Objectives:
Simplify the job search process.

Collect useful data about the labor market and job trends.

Enable future data analysis using tools like Excel or Power BI.

🔧 Tools and Technologies Used:
Tool	Purpose
requests	To send HTTP requests and fetch HTML content
BeautifulSoup	To parse and extract elements from HTML
pandas	To organize and clean data into table format
Google Colab (optional)	To display data interactively
CSV	To store the results in a structured file

📥 Inputs:
The user is prompted to enter a job title via input()
(e.g., "Flutter Developer", "Data Analyst", etc.)

📤 Outputs:
Display: The first 10 job listings shown as a formatted table.

File Save: All extracted results saved to jobs.csv.

Extracted Fields:

Field	Description
Title	Job title
Link	URL to the job post
Occupation	Career field or specialization
Company	Name of the hiring company
Specs	Short description or summary
Location	Location of the job
Company Address	Company address (if available)

✅ Project Features:
Fetches multiple pages of job listings, not just the first one.

Extracts accurate and useful job details.

Saves data in a CSV file for future use or visualization.

Supports interactive display in tools like Google Colab.

Highly flexible for future improvements such as:

Filtering by city or company

Scheduling daily job fetches

Adding email alerts or notifications


