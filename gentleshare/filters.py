"""
Jinja filters
"""

from markdown import markdown as md
from markdown.extensions.codehilite import CodeHiliteExtension
from bs4 import BeautifulSoup


def markdown_filter(text: str) -> str:
    """Converts markdown to HTML

    Args:
        text (str): Markdown text to convert

    Returns:
        str: HTML for this text
    """

    # Extensions utilisé:
    # - fenced_code: Allows code blocks with ```
    # - nl2br: remplaces \n by <br>
    # - CodeHiliteExtension: allows synthax highlighting in code blocks
    # - extra: Allows tables and footnotes
    # - markdown_mark: overline text with ==text==
    # - pymdownx.tasklist: github-style task lists
    # - pymdownx.tilde: ~~crossed out text~~ and subscript
    md_html = md(
        text,
        extensions=[
            "fenced_code",
            "nl2br",
            CodeHiliteExtension(guess_lang=True, linenums=None),
            # "extra",
            "markdown_mark",
            "pymdownx.tasklist",
            "pymdownx.tilde",
        ],
    )

    # Add bootstrap classes to prettify output
    soup = BeautifulSoup(md_html, "html.parser")

    # Could potentially be done with the tailwind-prose plugin

    # Fix headers to use the correct tailwind classes
    for i in range(1, 7):
        headers = soup.find_all(f"h{i}")
        for header in headers:
            nbr = (8 - i) // 2
            header["class"] = header.get("class", []) + [
                f"text-{nbr}xl",
                "font-bold",
                f"mt-{nbr}",
                f"mb-{nbr//2}",
            ]

    # Add style to urls
    for link in soup.find_all("a"):
        link["class"] = link.get("class", []) + ["text-blue-600"]

    # Find all table elements and add the "table" class
    tables = soup.find_all("table")
    for table in tables:
        table["class"] = table.get("class", []) + ["table"]

    # Find all blockquote elements and add the "blockquote" class
    tables = soup.find_all("blockquote")
    for table in tables:
        table["class"] = table.get("class", []) + ["blockquote"]

    # Return the modified HTML
    return soup.prettify()
