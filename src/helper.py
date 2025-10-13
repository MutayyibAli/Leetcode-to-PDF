import os
import shutil
import markdown
from bs4 import BeautifulSoup
from pygments import highlight, lexers, formatters


def clear_folder(folder_path: str):
    """Delete all files and sub-folders inside a folder, but keep the folder."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)  # remove file or symlink
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # remove subfolder
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


def remove_small_files(folder_path, max_size=100):
    """Recursively remove all files in a folder (and sub-folders) that are <= max_size bytes."""
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                if os.path.getsize(file_path) <= max_size:
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")


def markdown_to_html(md_text):
    htmlText = markdown.markdown(
        md_text,
        extensions=["fenced_code"],
    )

    return htmlText


def highlight_code_blocks(html):
    soup = BeautifulSoup(html, "html.parser")

    # Create a Pygments formatter (with CSS classes)
    formatter = formatters.HtmlFormatter(style="colorful", cssclass="codehilite")

    for code_tag in soup.find_all("code"):
        code_text = code_tag.get_text().strip()

        # Skip single-line code blocks
        if len(code_text.splitlines()) < 2:
            continue

        detected = True

        if code_tag.get("class") == ["language-cpp"]:
            lexer = lexers.CppLexer()
        elif code_tag.get("class") == ["language-python"]:
            lexer = lexers.PythonLexer()
        elif code_tag.get("class") == ["language-java"]:
            lexer = lexers.JavaLexer()
        elif code_tag.get("class") == ["language-javascript"]:
            lexer = lexers.JavascriptLexer()
        else:
            detected = False
            lexer = lexers.PythonLexer()

        # Highlight using Pygments
        highlighted_code = highlight(code_text, lexer, formatter)

        # Create a new <p> tag for the language
        style = "margin:0 20px; padding:0; font-weight:bold;"
        p = soup.new_tag("p", style=style)
        if detected:
            p.string = lexer.name
        else:
            p.string = "Code"
        code_tag.insert_before(p)

        wrapper_div = soup.new_tag("div", **{"class": "formatted-code"})
        code_tag.wrap(wrapper_div)

        # Replace the <code> tag with highlighted HTML
        code_tag.replace_with(BeautifulSoup(highlighted_code, "html.parser"))

    css = formatters.HtmlFormatter().get_style_defs(".codehilite")

    return str(soup), css
