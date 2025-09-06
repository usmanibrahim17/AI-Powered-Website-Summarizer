# 🌐 Website Summarizer with OpenAI

This project is a simple Python tool that fetches the contents of a website and generates a **short summary in Markdown** using OpenAI’s GPT models.  
It removes unnecessary navigation text (like menus, ads, or scripts) and focuses on the actual content.

---

## ✨ Features
- Fetches a website’s **title and text** using `requests` + `BeautifulSoup`
- Cleans out unwanted HTML tags (scripts, styles, etc.)
- Summarizes the website using **OpenAI GPT** (`gpt-4o-mini`)
- Outputs the summary in **Markdown format**
- Includes a `display_summary()` function for quick Jupyter display

---

## 🛠️ Requirements
Install dependencies with:

```bash
pip install -r requirements.txt
