# 📚 Document Query Assistant

A Streamlit-powered web application that enables users to upload documents (PDFs and text files), extract their content, and perform intelligent queries over the data using vector-based search and OpenAI language models. This project demonstrates full-stack development, document processing, and AI integration.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Tech Stack & Tools](#tech-stack--tools)
- [Skills & Learning Outcomes](#skills--learning-outcomes)
- [Project Impact](#project-impact)
- [License](#license)

---

## Overview

The **Document Query Assistant** is designed to help users interact with and search through their documents using natural language queries. By leveraging modern AI techniques and vector store indexing, the app offers an intuitive interface to extract meaningful answers from uploaded files. It also includes features such as query history tracking, document management (upload, duplicate detection, and removal), and dynamic model configuration for customized responses.

---

## Features

- **Document Upload & Management:**  
  Upload PDFs and text files with automatic duplicate detection and metadata management.

- **PDF Text Extraction:**  
  Extract text from PDFs reliably using [PyPDF2](https://github.com/py-pdf/PyPDF2).

- **Intelligent Querying:**  
  Leverage vector-based search and OpenAI-powered language models (including GPT-4 variants and GPT-3.5 Turbo) to answer natural language questions.

- **Query History:**  
  Track previous queries with timestamps and detailed responses for future reference.

- **Model Configuration:**  
  Dynamically switch between available OpenAI models to suit different query requirements.

- **Session Persistence:**  
  Save and reload document metadata and query history for a seamless user experience.

---

## Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/document-query-assistant.git
   cd document-query-assistant

2. **Create and activate a virtual environment**

   ```python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required dependencies**

   ```pip install -r requirements.txt

4. **Set up an OpenAi api key**

5. **Run the application**

   ```streamlit run app.py

