import feedparser
import csv
from datetime import datetime
import os
import requests

FEED_URLS = [
    "https://medium.com/feed/tag/bug-bounty",
    "https://medium.com/feed/tag/security",
    "https://medium.com/feed/tag/vulnerability",
    "https://medium.com/feed/tag/cybersecurity",
    "https://medium.com/feed/tag/penetration-testing",
    "https://medium.com/feed/tag/hacking",
    "https://medium.com/feed/tag/information-technology",
    "https://medium.com/feed/tag/infosec",
    "https://medium.com/feed/tag/web-security",
    "https://medium.com/feed/tag/bug-bounty-tips",
    "https://medium.com/feed/tag/bugs",
    "https://medium.com/feed/tag/pentesting",
    "https://medium.com/feed/tag/xss-attack",
    "https://medium.com/feed/tag/information-security",
    "https://medium.com/feed/tag/cross-site-scripting",
    "https://medium.com/feed/tag/hackerone",
    "https://medium.com/feed/tag/bugcrowd",
    "https://medium.com/feed/tag/bugbounty-writeup",
        "https://medium.com/feed/tag/bug-bounty-writeup",
        "https://medium.com/feed/tag/bug-bounty-hunter",
        "https://medium.com/feed/tag/bug-bounty-program",
        "https://medium.com/feed/tag/ethical-hacking",
        "https://medium.com/feed/tag/application-security",
        "https://medium.com/feed/tag/google-dorking",
        "https://medium.com/feed/tag/dorking",
        "https://medium.com/feed/tag/cyber-security-awareness",
        "https://medium.com/feed/tag/google-dork",
        "https://medium.com/feed/tag/web-pentest",
        "https://medium.com/feed/tag/vdp",
        "https://medium.com/feed/tag/information-disclosure",
        "https://medium.com/feed/tag/exploit",
        "https://medium.com/feed/tag/vulnerability-disclosure",
        "https://medium.com/feed/tag/web-cache-poisoning",
        "https://medium.com/feed/tag/rce",
        "https://medium.com/feed/tag/remote-code-execution",
        "https://medium.com/feed/tag/local-file-inclusion",
        "https://medium.com/feed/tag/vapt",
        "https://medium.com/feed/tag/dorks",
        "https://medium.com/feed/tag/github-dorking",
        "https://medium.com/feed/tag/lfi",
        "https://medium.com/feed/tag/vulnerability-scanning",
        "https://medium.com/feed/tag/subdomain-enumeration",
        "https://medium.com/feed/tag/cybersecurity-tools",
        "https://medium.com/feed/tag/bug-bounty-hunting",
        "https://medium.com/feed/tag/ssrf",
        "https://medium.com/feed/tag/idor",
        "https://medium.com/feed/tag/pentest",
        "https://medium.com/feed/tag/file-upload",
        "https://medium.com/feed/tag/file-inclusion",
        "https://medium.com/feed/tag/security-research",
        "https://medium.com/feed/tag/directory-listing",
        "https://medium.com/feed/tag/log-poisoning",
        "https://medium.com/feed/tag/cve",
        "https://medium.com/feed/tag/xss-vulnerability",
        "https://medium.com/feed/tag/shodan",
        "https://medium.com/feed/tag/censys",
        "https://medium.com/feed/tag/zoomeye",
        "https://medium.com/feed/tag/recon",
        "https://medium.com/feed/tag/xss-bypass",
        "https://medium.com/feed/tag/bounty-program",
        "https://medium.com/feed/tag/subdomain-takeover",
        "https://medium.com/feed/tag/bounties",
        "https://medium.com/feed/tag/api-key",
        "https://medium.com/feed/tag/cyber-sec"
]

CSV_FILE = "articles.csv"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")  # Store this in GitHub Secrets

def fetch_articles():
    entries = []
    for url in FEED_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title.strip()
            author = entry.get("author", "Unknown").strip()
            description = entry.get("summary", "").strip()
            pub_date = entry.get("published", "").strip()
            entries.append({
                "title": title,
                "author": author,
                "description": description,
                "date": pub_date
            })
    return entries

def load_existing_titles():
    if not os.path.exists(CSV_FILE):
        return set()
    with open(CSV_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return set(row["Title"] for row in reader)

def save_to_csv(entries):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Author", "Description", "Date"])
        if not file_exists:
            writer.writeheader()
        for entry in entries:
            writer.writerow({
                "Title": entry["title"],
                "Author": entry["author"],
                "Description": entry["description"],
                "Date": entry["date"]
            })

def truncate_description(desc):
    lines = desc.splitlines()
    return "\n".join(lines[-5:]) if len(lines) > 5 else desc

def notify_discord(entry):
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook URL is not set.")
        return

    message = f"""**{entry['title']}**

{truncate_description(entry['description'])}

by {entry['author']} at {entry['date']}
"""
    response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    if response.status_code != 204:
        print(f"Failed to send message to Discord: {response.text}")

if __name__ == "__main__":
    all_articles = fetch_articles()
    seen_titles = load_existing_titles()
    new_articles = [a for a in all_articles if a["title"] not in seen_titles]

    if new_articles:
        save_to_csv(new_articles)
        for article in new_articles:
            notify_discord(article)
