import csv
from datetime import datetime

CSV_FILE = "articles.csv"
README_FILE = "README.md"

def read_articles():
    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def format_markdown_table(articles):
    header = "| Date | Title | Author | Link |\n"
    separator = "|------|-------|--------|------|\n"
    rows = []

    for article in articles:
        date = article.get("date", "N/A")
        title = article.get("title", "N/A").replace("|", "-").strip()
        author = article.get("author", "N/A").replace("|", "-").strip()
        link = article.get("guid", "").strip()

        link_display = f"[Read More]({link})" if link and link != "N/A" else "N/A"
        row = f"| {date} | {title} | {author} | {link_display} |"
        rows.append(row)

    return header + separator + "\n".join(rows)

def write_readme(table_content):
    with open(README_FILE, "w", encoding="utf-8") as readme:
        readme.write("## 🌐 Let's Connect\n\n")
        readme.write("[![Discord](https://img.shields.io/badge/Discord-@thexnumb-1DA1F2?style=flat&logo=discord&logoColor=white)](https://discord.gg/evffhtjWR7) [![Twitter](https://img.shields.io/badge/X-@thexsecurity-1DA1F2?style=flat&logo=twitter&logoColor=white)](https://x.com/thexsecurity) [![Telegram](https://img.shields.io/badge/Telegram-@thexsecurity-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://t.me/thexsecurity) [![Instagram](https://img.shields.io/badge/Instagram-@thexnumb-E4405F?style=flat&logo=instagram&logoColor=white)](https://instagram.com/thexnumb) [![Infosec.exchange](https://img.shields.io/badge/Infosec.exchange-@thexnumb-E11BE9?style=flat&logo=mastodon&logoColor=white)](https://infosec.exchange/@thexnumb) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat&logo=linkedin)](#) [![Medium](https://img.shields.io/badge/Medium-@thexnumb-black?style=flat&logo=medium)](https://medium.com/@thexnumb) [![Blogger](https://img.shields.io/badge/Blogger-TheXSecurity-FF5722?style=flat&logo=blogger&logoColor=white)](https://thexsecurity.blogspot.com/) [![YouTube](https://img.shields.io/badge/YouTube-@theXNumb-FF0000?style=flat&logo=youtube&logoColor=white)](https://www.youtube.com/@theXNumb/)\n\n")
        readme.write("🚀 **Let's hack the planet!** 🔥\n\n")
        readme.write("# 📝 Latest Articles\n\n")
        readme.write("A list of the latest fetched articles from RSS feeds.\n\n")
        readme.write(table_content)

def main():
    articles = read_articles()
    articles = sorted(articles, key=lambda x: x.get("date", ""), reverse=True)
    markdown_table = format_markdown_table(articles)
    write_readme(markdown_table)

if __name__ == "__main__":
    main()
