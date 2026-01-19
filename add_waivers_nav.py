import os
import re

base_dir = r"c:\Users\lara1\Downloads\fort carsson cloud"
pages_dir = os.path.join(base_dir, "pages")

files = [os.path.join(base_dir, "index.html")]
if os.path.exists(pages_dir):
    files += [os.path.join(pages_dir, f) for f in os.listdir(pages_dir) if f.endswith(".html")]

print(f"Processing {len(files)} files...")

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Determine relative link
        is_index = os.path.basename(file_path) == "index.html"
        link_href = "pages/waivers.html" if is_index else "waivers.html"
        new_link_item = f'<li><a href="{link_href}">Waivers</a></li>'

        # Check for duplication
        if f'href="{link_href}">Waivers</a>' in content:
            print(f"Skipping {os.path.basename(file_path)}: Link already exists.")
            continue

        # Regex to find the General section's UL and insert at the end
        pattern = r'(<h3>General</h3>\s*<ul class="nav-list">.*?)(</ul>)'
        
        # Check if match exists
        if not re.search(pattern, content, re.DOTALL):
            print(f"Warning: Could not find General navigation section in {os.path.basename(file_path)}")
            continue
            
        new_content = re.sub(
            pattern, 
            f'\\1    {new_link_item}\n\\2', 
            content, 
            count=1, 
            flags=re.DOTALL
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(file_path)}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
