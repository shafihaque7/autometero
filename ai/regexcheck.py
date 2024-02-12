import re

text = """1. What kind of music do you enjoy singing the most?
2. Have you ever performed in any musical groups or bands?
3. Do you have any favorite singers or musical inspirations?"""

pattern = re.compile(r'\d+\.\s*(.*?)(?=\d+\.|$)')

matches = pattern.findall(text)

for match in matches:
    print(match.strip())