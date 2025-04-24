import csv
from datetime import datetime

CSV_FILE = "articles.csv"
README_FILE = "README.md"

def load_articles():
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return sorted(reader, key=lambda x: x['date'], reverse=True)

def format_markdown_table(articles):
    table = "| Title | Author | Date | Link |\n"
    table += "|-------|--------|------|------|\n"
    for article in articles:
        title = article['title'].strip().replace('\n', ' ')
        author = article['author'].strip()
        date = format_date(article['date'].strip())
        link = f"[Read More]({article['link'].strip()})"
        table += f"| {title} | {author} | {date} | {link} |\n"
    return table

def format_date(raw_date):
    try:
        dt = datetime.strptime(raw_date, "%a, %d %b %Y %H:%M:%S %Z")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return raw_date

def write_readme(content):
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write("# 📰 Latest Articles\n\n")
        f.write(content)

def main():
    articles = load_articles()
    markdown_table = format_markdown_table(articles)
    write_readme(markdown_table)
    print("✅ README.md updated.")

if __name__ == "__main__":
    main()
