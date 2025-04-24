import csv

ARTICLES_FILE = "articles.csv"
README_FILE = "README.md"

def read_articles():
    with open(ARTICLES_FILE, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def format_markdown_table(articles):
    table = "| Date | Title | Author | Link |\n"
    table += "|------|-------|--------|------|\n"
    for article in articles:
        link = article.get("link", "").strip()
        link_md = f"[Read More]({link})" if link else "N/A"
        table += f"| {article['date']} | {article['title']} | {article['author']} | {link_md} |\n"
    return table

def update_readme(table):
    try:
        with open(README_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = "# TheX Writeups\n\n## Recent Articles\n\n"

    if "## Recent Articles" in content:
        parts = content.split("## Recent Articles")
        content = parts[0] + "## Recent Articles\n\n" + table
    else:
        content += "\n## Recent Articles\n\n" + table

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    articles = read_articles()
    articles.reverse()  # Newest first
    markdown_table = format_markdown_table(articles)
    update_readme(markdown_table)

if __name__ == "__main__":
    main()
