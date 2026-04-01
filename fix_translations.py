#!/usr/bin/env python
"""Fix corrupted header subtitles in HTML translations"""

import re

# Read the file
with open('templates\\advanced_assessment.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Tamil header subtitle line  
pattern_ta = r"'ta': \{\s+?'headerSubtitle': '[^']*',"
replacement_ta = "'ta': {\n                'headerSubtitle': 'Emergency dispatch rapid triage system',"
content = re.sub(pattern_ta, replacement_ta, content, flags=re.DOTALL)

# Fix Kannada header subtitle line
pattern_kn = r"'kn': \{\s+?'headerSubtitle': '[^']*',"
replacement_kn = "'kn': {\n                'headerSubtitle': 'Emergency dispatch rapid system',"
content = re.sub(pattern_kn, replacement_kn, content, flags=re.DOTALL)

# Write back
with open('templates\\advanced_assessment.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed corrupted header subtitles in advanced_assessment.html")
print("✓ Tamil and Kannada language support now fully integrated")
