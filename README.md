# Tata Capital Loan Data Transformation Suite

## Overview

A Streamlit-based application that automates the processing of Tata Capital loan application JSON files.

The application extracts business-critical information from ZIP/7Z archives containing nested JSON files and converts them into structured Excel reports.

## Features

* Upload ZIP or 7Z archives
* Automatic JSON extraction
* Loan application data processing
* Decision and eligibility extraction
* Rule-engine output extraction
* Scorecard information extraction
* Excel report generation
* Interactive Streamlit dashboard

## Tech Stack

* Python
* Streamlit
* Pandas
* OpenPyXL
* Py7zr

## Project Structure

* app.py → Streamlit UI
* parser.py → JSON parsing logic
* excel_generator.py → Excel report generation

## Deployment

Deployed using Streamlit Community Cloud.

## Author

Anshika Gupta
