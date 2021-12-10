import requests
from bs4 import BeautifulSoup
from jinja2 import Template
from datetime import datetime
from zoneinfo import ZoneInfo

BLOG_URL = "https://mpewsey.github.io"
README_TEMPLATE = "README_Template.md"
README_PATH = "README.md"
TIMEZONE = ZoneInfo("US/Eastern")


def fetch_blog_post_links() -> list:
    request = requests.get(BLOG_URL)
    soup = BeautifulSoup(request.content, "html.parser")
    headers = soup.find_all("h3")
    links = [x.find("a") for x in headers]
    return [f"* [{strip(''.join(x.contents))}]({BLOG_URL + x['href']})" for x in links]


def get_blog_posts_string() -> str:
    links = fetch_blog_post_links()

    if not links:
        return "No Posts Available"

    return "\n".join(links)


def write_readme():
    with open(README_TEMPLATE, "rt") as fh:
        template = Template(fh.read())

    blog_posts = get_blog_posts_string()
    date_time = datetime.now().astimezone(TIMEZONE).strftime("%d %b %Y, %I:%M %p EST")
    readme = template.render(blog_posts = blog_posts, date_time = date_time)

    with open(README_PATH, "wt") as fh:
        fh.write(readme)


if __name__ == "__main__":
    write_readme()
