#!/usr/bin/env python3
"""
Script to update README.md with recent blog posts from RSS feed.
Inspired by https://simonwillison.net/2020/Jul/10/self-updating-profile-readme/
"""

import feedparser
import pathlib
import re

root = pathlib.Path(__file__).parent.resolve()
BLOG_FEED_URL = "https://lalitm.com/index.xml"


def replace_chunk(content, marker, chunk, inline=False):
    """
    Replace content between marker comments in the README.

    Args:
        content: The full README content
        marker: The marker name (e.g., 'blog_posts')
        chunk: The new content to insert
        inline: If True, keeps markers on same line as content
    """
    r = re.compile(
        r"<!-- {} start -->.*<!-- {} end -->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} start -->{}<!-- {} end -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


def fetch_blog_posts(feed_url, count=5):
    """
    Fetch recent blog posts from RSS feed.

    Args:
        feed_url: URL of the RSS/Atom feed
        count: Number of posts to fetch (default: 5)

    Returns:
        List of formatted markdown links
    """
    feed = feedparser.parse(feed_url)
    posts = []

    for entry in feed.entries[:count]:
        title = entry.title
        link = entry.link
        posts.append(f"- [{title}]({link})")

    return "\n".join(posts)


if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.read_text()

    # Fetch and update blog posts
    blog_posts = fetch_blog_posts(BLOG_FEED_URL)
    rewritten = replace_chunk(readme_contents, "blog_posts", blog_posts)

    # Write back to README
    readme.write_text(rewritten)
    print("README.md updated successfully!")
