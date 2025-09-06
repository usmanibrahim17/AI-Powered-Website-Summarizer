# IMPORTS AND SETUP
import os
import requests
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from IPython.display import Markdown, display

# LOAD ENVIRONMENT VARIABLES
load_dotenv(override=True)

# CREATE OPENAI CLIENT
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# WEBSITE CLASS
class Website:
    url: str
    title: str
    text: str

    def __init__(self, url):
        self.url = url

        # FETCH PAGE
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except Exception as e:
            self.title = "Error fetching url"
            self.text = f"Could not fetch {url}: {e}"
            return

        # PARSE HTML
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else "No title found"
        )
        body = soup.body
        if body:
            for tag in body.find_all(["script", "style", "img", "input"]):
                tag.decompose()
            self.text = body.get_text(separator="\n", strip=True)
        else:
            self.text = soup.get_text(separator="\n", strip=True)


# SYSTEM PROMPT
system_prompt = (
    "you are an assistant that analyzes the contents of a website "
    "and provides a short summary, ignoring text that may be navigational related. "
    "Respond in markdown "
)

# USER PROMPT
def user_prompt_for(website: Website) -> str:
    user_prompt = f"You are looking at a website called {website.title}\n"
    user_prompt += (
        "The contents of this website are as follows; please provide a short summary "
        "of this website in markdown. If it includes news and announcements, then summarize these too.\n\n"
    )
    user_prompt += website.text
    return user_prompt

def messages_for(website: Website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)},
    ]

# SUMMARIZE
def summarize(url: str) -> str:
    website = Website(url)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_for(website)
    )
    try:
        return response.choices[0].message.content
    except Exception:
        return response.choices[0].message["content"]

def display_summary(url: str):
    summary = summarize(url)
    display(Markdown(summary))


# Example run
if __name__ == "__main__":
    display_summary("https://ai2x.org")
