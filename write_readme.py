import requests
from bs4 import BeautifulSoup
from jinja2 import Template

BLOG_URL = "https://mpewsey.github.io"
README_TEMPLATE = "README_Template.md"
README_PATH = "README.md"


def fetch_blog_post_links() -> list:
    request = requests.get(BLOG_URL)
    soup = BeautifulSoup(request.content, "html.parser")
    headers = soup.find_all("h3")
    meta = soup.find_all("span", class_="post-meta")
    links = [x.find("a") for x in headers]
    dates = [x.contents[0][:11] for x in meta]
    return [f"* {y} [{''.join(x.contents).strip()}]({BLOG_URL + x['href']})" for x, y in zip(links, dates)]


def get_blog_posts_string() -> str:
    links = fetch_blog_post_links()

    if not links:
        return "No Posts Available"

    return "\n".join(links)


def write_readme():
    with open(README_TEMPLATE, "rt") as fh:
        template = Template(fh.read())

    blog_posts = get_blog_posts_string()
    readme = template.render(blog_posts = blog_posts)

    with open(README_PATH, "wt") as fh:
        fh.write(readme)


if __name__ == "__main__":
    write_readme()
