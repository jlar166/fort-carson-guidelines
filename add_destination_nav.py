import os
import re

root_dir = r"c:\Users\lara1\Downloads\fort carsson cloud"
pages_dir = os.path.join(root_dir, "pages")

# Link to insert
link_root = '<li><a href="pages/destination.html">Destination Guidelines</a></li>'
link_pages = '<li><a href="destination.html">Destination Guidelines</a></li>'

def update_nav(filepath, link_html):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Avoid duplicate
    if "Destination Guidelines" in content:
        print(f"Skipping {os.path.basename(filepath)} (already present)")
        return

    # Find General Section and insert
    # Pattern looks for <h3>General</h3> followed by <ul class="nav-list">
    # We want to insert after <ul class="nav-list">
    
    # Regex to find the opening of the General list
    pattern = r'(<h3>General</h3>\s*<ul class="nav-list">\s*)'
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, r'\1' + link_html + '\n                            ', content, count=1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(filepath)}")
    else:
        print(f"Could not find General nav in {os.path.basename(filepath)}")

# Update index.html
update_nav(os.path.join(root_dir, "index.html"), link_root)

# Update pages
for filename in os.listdir(pages_dir):
    if filename.endswith(".html"):
        update_nav(os.path.join(pages_dir, filename), link_pages)
