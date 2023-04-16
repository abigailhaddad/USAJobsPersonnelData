

# **Data Science Job Scraper and Classifier**

This repository contains two Python scripts, `job_scraper.py` and `job_classifier.py`, that work together to scrape data science-related federal job listings and classify them according to their suitability for someone interested in data science tasks.


## **Features**



* Scrapes job listings from the USAJOBS API.
* Filters job listings based on specific keywords and occupation codes.
* Utilizes OpenAI GPT-3.5-turbo to classify job listings based on their relevance to data science.
* Extracts and saves additional information such as job duties and qualifications in an Excel file.


## **Installation**



1. Clone this repository.
2. Install the required packages by running `pip install -r requirements.txt` in your terminal or command prompt.


## **Usage**



1. Run `python job_scraper.py` to scrape job listings from the USAJOBS API.
2. Run `python job_classifier.py` to classify the job listings using OpenAI GPT-3.5-turbo, and save the results in an Excel file.


## **Scripts Overview**


### **job_scraper.py**

This script scrapes federal job listings from the USAJOBS API. It filters the listings based on specific keywords related to data science and saves the results in a pickle file.


### **job_classifier.py**

This script reads the scraped job listings from the pickle file, concatenates specific columns into a new 'info' column, and filters the listings based on occupation codes. It further filters the listings by checking if they contain the word "data", takes a random sample of 1,000 rows, and processes them using OpenAI GPT-3.5-turbo to classify their relevance to data science. The script then extracts additional information such as job duties and qualifications and saves the results in an Excel file.


## **Dependencies**



* Python 3.6 or later
* pandas
* openai
* requests
* pickle


## **Note**

You need to provide your own OpenAI API key and USAJOBS API key for these scripts to work. Save the OpenAI API key in the `key.txt` file within the `key` directory, and update the `job_scraper.py` script with your USAJOBS API key.
