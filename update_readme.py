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
        title = article.get("title", "N/A").replace("|", "-")
        author = article.get("author", "N/A").replace("|", "-")
        link = article.get("link", "").strip()

        link_display = f"[Read More]({link})" if link and link != "N/A" else "N/A"
        row = f"| {date} | {title} | {author} | {link_display} |"
        rows.append(row)

    return header + separator + "\n".join(rows)

def write_readme(table_content):
    with open(README_FILE, "w", encoding="utf-8") as readme:
        readme.write("# 📝 Latest Articles\n\n")
        readme.write("A list of the latest fetched articles from RSS feeds.\n\n")
        readme.write(table_content)

def main():
    articles = read_articles()
    articles = sorted(articles, key=lambda x: x.get("date", ""), reverse=True)  # newest first
    markdown_table = format_markdown_table(articles)
    write_readme(markdown_table)

if __name__ == "__main__":
    main()
