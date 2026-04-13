import re
import os

base_path = r"e:\document\work\AI\vibecoding\product\jimeng-tutorial"
html_file = os.path.join(base_path, "即梦AI操作说明.html")
sections_dir = os.path.join(base_path, "sections")

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Section patterns and their positions (from previous analysis)
sections = [
    ("s0-toc", 29049),
    ("s1-platform", 30353),
    ("s2-quickstart", 38294),
    ("s3-image", 43810),
    ("s4-video", 59520),
    ("s5-agent", 71957),
    ("s6-motion", 75559),
    ("s7-voice", 78926),
    ("s8-digital", 82891),
    ("s9-canvas", 88505),
    ("s10-prompt", 118007),
    ("s11-font", 121797),
    ("s12-reference", 130230),
    ("s-links", 134425),
    ("s-appendix", 147477),
]

# Extract each section
for i, (name, start_pos) in enumerate(sections):
    # End position is the start of next section or end of file
    end_pos = sections[i + 1][1] if i + 1 < len(sections) else len(content)
    
    # Extract section content
    section_html = content[start_pos:end_pos]
    
    # Create section file
    section_file = os.path.join(sections_dir, f"{name}.html")
    with open(section_file, 'w', encoding='utf-8') as f:
        f.write(section_html)
    
    print(f"Extracted: {name}.html ({len(section_html)} chars)")

print("\nAll sections extracted successfully!")
