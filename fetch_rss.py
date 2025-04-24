import feedparser
import csv
import os
import requests
from datetime import datetime
import html2text

CSV_FILE = "articles.csv"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

RSS_FEEDS = [
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

def load_existing_guids():
    """Load GUIDs from existing CSV to avoid duplicates."""
    if not os.path.exists(CSV_FILE):
        return set()

    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        return {row["guid"] for row in csv.DictReader(csvfile)}

def html_to_markdown(html):
    """Convert HTML to clean markdown."""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0
    return h.handle(html).strip()

def truncate_description(description):
    """Get the last 5 lines from the description."""
    lines = description.strip().splitlines()
    return "\n".join(lines[-5:])

def notify_discord(entry):
    """Send a nicely formatted message to Discord."""
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook URL is not set.")
        return

    emoji = "📰"
    markdown_description = html_to_markdown(entry["description"])

    # Remove lines that contain only [](...)
    cleaned_lines = []
    for line in markdown_description.splitlines():
        if not re.match(r"^\[\]\(.*?\)$", line.strip()):
            cleaned_lines.append(line)
    cleaned_description = "\n".join(cleaned_lines)

    short_desc = truncate_description(cleaned_description)

    message = f"""\
# {emoji} {entry['title']}

{short_desc}

by **{entry['author']}** at `{entry['date']}`
"""

    payload = {
        "content": message
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        print(f"Failed to send Discord message: {response.status_code}, {response.text}")

def save_entry(entry):
    """Save new entry to the CSV file."""
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["title", "author", "description", "date", "guid"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

def fetch_and_process_feeds():
    seen_guids = load_existing_guids()

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            guid = entry.get("id") or entry.get("link")
            if guid in seen_guids:
                continue

            new_entry = {
                "title": entry.get("title", "No Title"),
                "author": entry.get("author", "Unknown"),
                "description": entry.get("summary", "No Description"),
                "date": entry.get("published", datetime.utcnow().isoformat()),
                "guid": guid
            }

            save_entry(new_entry)
            notify_discord(new_entry)
            seen_guids.add(guid)

if __name__ == "__main__":
    fetch_and_process_feeds()
