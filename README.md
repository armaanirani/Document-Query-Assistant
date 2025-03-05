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

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required dependencies**

   ```bash
   pip install -r requirements.txt

4. **Set up an OpenAi api key**

5. **Run the application**

   ```bash
   streamlit run app.py

## Usage

- **Upload Documents:** Navigate to the "Manage Documents" tab to upload PDFs or text files. The system automatically detects duplicates and manages metadata.
- **Ask Questions:** Use the "Query Documents" tab to input natural language queries and receive answers based on the document contents.
- **Review Query History:** Check the "Query History" tab to view previous queries and responses, with options to delete individual or all entries.
- **Configure Models:** Use the "Model Configuration" tab to switch between different OpenAI models for optimal results.

## Tech Stack & Tools

- **Programming Language:** Python
- **Framework:** Streammlit
- **Document Processing:** PyPDF2
- **Vector Indexing & AI:** llama-index, OpenAI API
- **Version Control:** Git & GitHub
- **Utilities:** JSON for storage, hashlib for file integrity, datetime for timestammping.

## Skills & Learning Outcomes

- **Web Application Development:** Building interactive UIs with Streamlit.
- **Document Parsing & Processing:** Extracting and managing text data from PDFs and text files.
- **Vector Store Indexing:** Implementing vector-based search with document embeddings.
- **API Integration:** Configuring and integrating with the OpenAI API for natural language processing.
- **State Management & Persistence:** Handling session states and data storage with JSON.
- **Error Handling:** Developing robust error handling and debugging techniques.

## Project Impact

The Document Query Assistant not only provided a practical solution for document management and intelligent querying but also served as a significant learning experience. The project allowed me to bridge advanced AI techniques with user-centric design, significantly boosting my expertise in full-stack development and natural language processing.
