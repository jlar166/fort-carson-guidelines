import os
from bs4 import BeautifulSoup

ROOT_DIR = r"c:\Users\lara1\Downloads\fort carsson cloud"
PAGES_DIR = os.path.join(ROOT_DIR, "pages")

# HTML snippet to insert
IMG_TAG_TEMPLATE = '<img src="{path}" alt="Fort Carson Mountain Post" style="max-width: 100%; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">'

def update_file(file_path, is_root=False):
    print(f"Processing {file_path}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")
        header = soup.find("header")

        if not header:
            print(f"  No <header> found in {file_path}. Skipping.")
            return

        # Check if image already exists
        if header.find("img", attrs={"alt": "Fort Carson Mountain Post"}):
            print(f"  Header image already exists in {file_path}. Skipping.")
            return

        # Prepare new tag
        img_path = "assets/images/header_banner.png" if is_root else "../assets/images/header_banner.png"
        new_tag = BeautifulSoup(IMG_TAG_TEMPLATE.format(path=img_path), "html.parser")

        # Insert as first child of header
        header.insert(0, new_tag)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"  Updated {file_path}.")

    except Exception as e:
        print(f"  Error processing {file_path}: {e}")

def main():
    # Update index.html
    index_path = os.path.join(ROOT_DIR, "index.html")
    if os.path.exists(index_path):
        update_file(index_path, is_root=True)

    # Update pages
    if os.path.exists(PAGES_DIR):
        for filename in os.listdir(PAGES_DIR):
            if filename.endswith(".html"):
                update_file(os.path.join(PAGES_DIR, filename), is_root=False)

if __name__ == "__main__":
    main()
