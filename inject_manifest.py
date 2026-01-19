import os

pages_dir = r"c:\Users\lara1\Downloads\fort carsson cloud\pages"
index_file = r"c:\Users\lara1\Downloads\fort carsson cloud\index.html"

manifest_link_pages = '    <link rel="manifest" href="../manifest.json">'
manifest_link_index = '    <link rel="manifest" href="manifest.json">'

# Update pages
for filename in os.listdir(pages_dir):
    if filename.endswith(".html"):
        path = os.path.join(pages_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "manifest.json" not in content:
            content = content.replace('</head>', f'{manifest_link_pages}\n</head>')
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated {filename}")

# Update index
with open(index_file, "r", encoding="utf-8") as f:
    content = f.read()

if "manifest.json" not in content:
    content = content.replace('</head>', f'{manifest_link_index}\n</head>')
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated index.html")
