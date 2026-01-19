
import os
from bs4 import BeautifulSoup

# Define the root directory to start the update (current directory)
root_dir = os.path.dirname(os.path.abspath(__file__))
pages_dir = os.path.join(root_dir, 'pages')

# Files to update
files_to_update = [os.path.join(root_dir, 'index.html')]
if os.path.exists(pages_dir):
    files_to_update.extend([os.path.join(pages_dir, f) for f in os.listdir(pages_dir) if f.endswith('.html')])

def update_nav(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Link to add: 
        is_index = file_path.endswith('index.html')
        link_href = "pages/maam.html" if is_index else "maam.html"
        
        # Check if link already exists
        if soup.find('a', href=link_href):
            print(f"MAAM link already exists in {os.path.basename(file_path)}")
            return

        new_li = soup.new_tag('li')
        new_a = soup.new_tag('a', href=link_href)
        new_a.string = "MAAM"
        new_li.append(new_a)
        
        # Find where to insert
        # Search for "Airway Management" link
        airway_link = soup.find('a', href=lambda x: x and 'airway.html' in x)
        
        if airway_link:
            # Insert after Airway Management's parent li
            airway_li = airway_link.parent
            airway_li.insert_after(new_li)
            new_li.insert_after('\n')
            
            print(f"Updated {os.path.basename(file_path)}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
        else:
            print(f"Could not find Airway Management link in {os.path.basename(file_path)}")

    except Exception as e:
        print(f"Error updating {file_path}: {e}")

for file_path in files_to_update:
    if os.path.exists(file_path):
        update_nav(file_path)
