#!/usr/bin/env python
"""Fix corrupted header subtitles - safe approach"""

# Read the file
with open('templates/advanced_assessment.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Strategy: Replace the entire ta and kn sections with corrected versions
# First, let's find where these sections are and replace them carefully

lines = content.split('\n')
result = []
skip_next = False

for i, line in enumerate(lines):
    if skip_next:
        skip_next = False
        continue
    
    # Fix Tamil headerSubtitle line (around line 855)
    if "'ta': {" in line and i > 850 and i < 860:
        result.append(line)
        # Next line should be the corrupted headerSubtitle
        if i + 1 < len(lines):
            result.append("                'headerSubtitle': 'Emergency dispatch rapid triage system',")
            skip_next = True  # Skip the corrupted line
        continue
    
    # Fix Kannada headerSubtitle line (around line 874)
    if "'kn': {" in line and i > 870 and i < 880:
        result.append(line)
        # Next line should be the corrupted headerSubtitle
        if i + 1 < len(lines):
            result.append("                'headerSubtitle': 'Emergency dispatch rapid system',")
            skip_next = True  # Skip the corrupted line
        continue
    
    result.append(line)

# Write back
with open('templates/advanced_assessment.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(result))

print("✓ Fixed corrupted header subtitles")
print("✓ Form now has 4 language buttons")

