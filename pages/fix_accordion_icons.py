from bs4 import BeautifulSoup
import os

FILE_PATH = "med-description.html"

def remove_redundant_icons():
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found.")
        return

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Find all accordion headers
    headers = soup.find_all("button", class_="accordion-header")

    count = 0
    for header in headers:
        # Find the icon inside
        icon = header.find("i", class_="fa-chevron-down")
        if icon:
            icon.decompose() # Remove the tag
            count += 1

    # Write back to file
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"Cleanup complete. {count} redundant icons removed.")

if __name__ == "__main__":
    remove_redundant_icons()
