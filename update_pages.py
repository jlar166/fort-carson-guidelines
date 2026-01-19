import os
import re

pages_dir = r"c:\Users\lara1\Downloads\fort carsson cloud\pages"
files_to_update = [
    "airway.html", "allergic.html", "burns.html", "cardiac.html", 
    "consent.html", "diabetes.html", "extremity.html", "hemorrhagic.html", 
    "med-list.html", "medications.html", "pain.html", "patient-determination.html", 
    "pediatric.html", "respiratory.html", "seizure.html", "stroke.html", 
    "supportive-care.html", "trauma-general.html"
]

header_controls = """            <div class="header-controls">
                <button class="header-btn" id="darkModeToggle">🌙 Dark</button>
                <button class="header-btn" id="printBtn">🖨️ Print</button>
            </div>"""

search_bar = """        <!-- Search Bar -->
        <div class="search-wrapper">
            <div class="search-container">
                <input type="text" class="search-box" id="searchInput" placeholder="🔍 Search guidelines, medications, procedures...">
                <div id="searchResults"></div>
            </div>
        </div>"""

recent_section = """<div class="nav-content" id="navContent">
                    <div class="recent-section" id="recentPages" style="display:none;">
                        <h4>📍 Recent</h4>
                        <ul class="recent-list"></ul>
                    </div>"""

tools_section = """                    <div class="nav-section">
                        <h3>Tools</h3>
                        <ul class="nav-list">
                            <li><a href="calculator.html">Pediatric Calculator</a></li>
                            <li><a href="quick-cards.html">Drug Quick Cards</a></li>
                            <li><a href="algorithms.html">Algorithm Flowcharts</a></li>
                        </ul>
                    </div>
                </div>"""

script_tag = """    <script src="../app.js"></script>
</body>"""

for filename in files_to_update:
    path = os.path.join(pages_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Add Header Controls
    if 'class="header-controls"' not in content:
        content = content.replace('<div class="revision-date">Revised: 5/19/2022</div>', 
                                  '<div class="revision-date">Revised: 5/19/2022</div>\n' + header_controls)
    
    # 2. Add Search Bar
    if 'class="search-wrapper"' not in content:
        content = content.replace('</header>', '</header>\n\n' + search_bar)
    
    # 3. Add Recent Section
    if 'id="recentPages"' not in content:
        content = content.replace('<div class="nav-content" id="navContent">', recent_section)

    # 4. Add Tools Section
    if '<h3>Tools</h3>' not in content:
        # Look for the closing div of nav-content matching the indentation
        # The previous file content has </div> closing nav-content.
        # We find the last nav-section and append after it.
        if '<h3>Medications</h3>' in content:
            # Replaces the closing of medications section AND the closing of nav-content
            # We look for the medication list block
            pattern = re.compile(r'(<h3>Medications</h3>\s*<ul class="nav-list">.*?</ul>\s*</div>\s*)</div>', re.DOTALL)
            match = pattern.search(content)
            if match:
                # Insert tools section before the final closing div
                med_section = match.group(1)
                replacement = med_section + '\n' + tools_section.replace('</div>\n                </div>', '</div>') + '\n                </div>'
                # The tools_section variable has the closing div for nav-content too.
                # Actually tools_section string ends with </div> which closes nav-content.
                
                # Simpler approach: find the last </div> that closes nav-content.
                # It is likely the one after Medication section.
                content = content.replace(med_section + '</div>', med_section + '\n' + tools_section.replace('                </div>', '')) 
                # Wait, tools_section has the closing div. The original code has </div> closing nav-content.
                # Regex replace might be safer.
                
                content = re.sub(r'(<h3>Medications</h3>\s*<ul class="nav-list">.*?</ul>\s*</div>)', r'\1\n\n' + tools_section.replace('                </div>', ''), content, flags=re.DOTALL)
                # Note: tools_section as defined above ENDS with </div>, so we just append it?
                # tools_section string: ... </div>\n                </div>
                # We want to insert the 
                # <div class="nav-section">...</div> 
                # INSIDE the nav-content.
                
                # Let's clean up tools_section variable to just be the inner part
                tools_inner = """
                    <div class="nav-section">
                        <h3>Tools</h3>
                        <ul class="nav-list">
                            <li><a href="calculator.html">Pediatric Calculator</a></li>
                            <li><a href="quick-cards.html">Drug Quick Cards</a></li>
                            <li><a href="algorithms.html">Algorithm Flowcharts</a></li>
                        </ul>
                    </div>"""
                
                content = re.sub(r'(<div class="nav-section">\s*<h3>Medications</h3>.*?</div>)', r'\1' + tools_inner, content, flags=re.DOTALL)


    # 5. Replace Script
    # Remove old inline script and add new src
    # Pattern: <script> ... </script></body>
    content = re.sub(r'<script>[\s\S]*?</script>\s*</body>', script_tag, content)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {filename}")
