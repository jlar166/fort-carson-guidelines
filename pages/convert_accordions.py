from bs4 import BeautifulSoup
import os

FILE_PATH = "med-description.html"

def convert_to_accordion():
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found.")
        return

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Find all guideline cards
    cards = soup.find_all("div", class_="guideline-card")

    count = 0
    for card in cards:
        # Check if it's a medication card (has an ID and contains an h2)
        if card.get("id") and card.find("h2"):
            # Add accordion-item class
            existing_classes = card.get("class", [])
            if "accordion-item" not in existing_classes:
                existing_classes.append("accordion-item")
                card["class"] = existing_classes

            # Find the header (h2)
            h2 = card.find("h2")
            title_text = h2.get_text(strip=True)

            # Create the new button header
            button = soup.new_tag("button", attrs={"class": "accordion-header"})
            button.string = title_text
            
            # Create the chevron icon
            icon = soup.new_tag("i", attrs={"class": "fas fa-chevron-down"})
            button.append(icon)

            # Create the panel div
            panel = soup.new_tag("div", attrs={"class": "accordion-panel"})

            # Move all content after h2 into the panel
            # We collect siblings first to avoid modifying the tree while iterating
            siblings = list(h2.next_siblings)
            for sibling in siblings:
                panel.append(sibling)

            # Replace h2 with button
            h2.replace_with(button)

            # Append panel to the card
            card.append(panel)
            
            count += 1
            print(f"Converted: {title_text}")

    # Write back to file
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"Conversion complete. {count} items processed.")

if __name__ == "__main__":
    convert_to_accordion()
