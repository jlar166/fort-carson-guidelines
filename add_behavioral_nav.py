
import os
from bs4 import BeautifulSoup

# Define the root directory to start the update (current directory)
root_dir = os.path.dirname(os.path.abspath(__file__))
pages_dir = os.path.join(root_dir, 'pages')

# Files to update
files_to_update = [os.path.join(root_dir, 'index.html')]
files_to_update.extend([os.path.join(pages_dir, f) for f in os.listdir(pages_dir) if f.endswith('.html')])

def update_nav(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Find the Nav Section
        # We want to insert into "Medical Protocols" section if it exists, roughly between Allergic and Cardiac
        # But my memory of nav structure might be slightly off on exact section names
        # Let's target the nav list
        
        # Actually, let's look for known links.
        # "Allergic Reaction" is likely a link.
        
        # Let's find the nav list that contains "Allergic Reaction" or similar.
        # Or just find all nav-lists.
        
        # Link to add: 
        # If file is index.html: pages/behavioral.html
        # If file is in pages/: behavioral.html
        
        is_index = file_path.endswith('index.html')
        link_href = "pages/behavioral.html" if is_index else "behavioral.html"
        new_li = soup.new_tag('li')
        new_a = soup.new_tag('a', href=link_href)
        new_a.string = "Behavioral Emergencies"
        new_li.append(new_a)
        
        # Find where to insert
        # Search for "Allergic Reaction" link
        allergic_link = soup.find('a', href=lambda x: x and 'allergic.html' in x)
        
        if allergic_link:
            # Insert after Allergic Reaction's parent li
            allergic_li = allergic_link.parent
            allergic_li.insert_after(new_li)
            # Add newline for formatting
            new_li.insert_after('\n')
            
            print(f"Updated {os.path.basename(file_path)}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
        else:
            print(f"Could not find Allergic Reaction link in {os.path.basename(file_path)}")

    except Exception as e:
        print(f"Error updating {file_path}: {e}")

for file_path in files_to_update:
    if os.path.exists(file_path):
        update_nav(file_path)
