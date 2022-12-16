import bs4
import datetime
import jinja2
import requests

BLOG_URL = "https://mpewsey.github.io"
README_TEMPLATE = "README_Template.md"
README_PATH = "README.md"
NEW_TEXT = ":sparkles:New"
POST_COUNT = 5

MONTHS = {
    "Jan" : 1,
    "Feb" : 2,
    "Mar" : 3,
    "Apr" : 4,
    "May" : 5,
    "Jun" : 6,
    "Jul" : 7,
    "Aug" : 8,
    "Sep" : 9,
    "Oct" : 10,
    "Nov" : 11,
    "Dec" : 12,
}


"""
Returns a list of date times parsed from a list of date strings.
"""
def parse_dates(dates) -> list:
    split = [x.split(" ") for x in dates]
    return [datetime.datetime(int(x[2]), MONTHS[x[1]], int(x[0])) for x in split]


"""
Returns the new string text for a list of date strings.
"""
def get_new_strings(dates) -> list:
    now = datetime.datetime.now()
    delta = datetime.timedelta(days = -7)
    deltas = [x - now for x in parse_dates(dates)]
    return [NEW_TEXT if x >= delta else "" for x in deltas]


"""
Returns a list of strings for the blog posts.
"""
def fetch_blog_post_links() -> list:
    request = requests.get(BLOG_URL)
    soup = bs4.BeautifulSoup(request.content, "html.parser")
    headers = soup.find_all("h3")
    meta = soup.find_all("span", class_="post-meta")
    links = [x.find("a") for x in headers]
    dates = [x.contents[0][:11] for x in meta]
    new_strings = get_new_strings(dates)
    return [f"* {y} [{''.join(x.contents).strip()}]({BLOG_URL + x['href']}) {z}" for x, y, z in zip(links, dates, new_strings)]


"""
Returns the blog posts string.
"""
def get_blog_posts_string() -> str:
    links = fetch_blog_post_links()

    if not links:
        return "No Posts Available"

    return "\n".join(links[:POST_COUNT])


"""
Returns the current time string.
"""
def current_datetime_string() -> str:
    now = datetime.datetime.utcnow()
    return now.strftime("%d %b %Y, %I:%M %p UTC")


"""
Writes the README file.
"""
def write_readme():
    with open(README_TEMPLATE, "rt") as fh:
        template = jinja2.Template(fh.read())

    blog_posts = get_blog_posts_string()
    readme = template.render(blog_posts = blog_posts)

    with open(README_PATH, "wt") as fh:
        fh.write(readme)


if __name__ == "__main__":
    write_readme()
