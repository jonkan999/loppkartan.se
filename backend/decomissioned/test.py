import re

test = "https://easyrecord.se/entry?D68E33.\ "

# Replace any inline links in the summary with anchor tags
match = re.search(r"(https?://|www\.)\S+", test)
if match:
    prefix = match.group(0)
    anchor_text = re.sub(r"^https?://(?:www\.)?([^\./]+)\..*", r"\1", test)
else:
    anchor_text = test

print(match)
print(anchor_text)