import json
import re

# Assume jsonData is a string containing your JSON data
with open('backend/URL_Summary.json', encoding='utf-8') as f:
    summaries = json.load(f)


processedData = []

# Loop through each key-value pair in the object
for url, summary in summaries.items():
    # Create a dictionary with the url and summary values
    item = {"url": url, "summary": summary}

    # Remove any occurrences of "[...]" from the summary
    item["summary"] = re.sub(r"\[\.\.\.\]", "", item["summary"])

    # find all anchor tags and extract the href attribute as test
    urls = re.findall(r"(?:(?:https?://|www\.)\S+/?)", item["summary"])
    print(urls)
    # loop through each test and replace the anchor element with the first word between https:// or www. and .
    for url in urls:
        match = re.search(r"(https?://|www\.)\S+", url)
        if match:
            prefix = match.group(0)
            anchor_text = re.sub(r"^https?://(?:www\.)?([^\./]+)\..*", r"\1", url)
            print(anchor_text)
        else:
            anchor_text = url

        # replace the anchor element with the desired text
        item["summary"] = item["summary"].replace(url, f'<a href="{url}" target="_blank" class="inline-link">{anchor_text}</a>')
    # Cap the summary to 500 characters (including whitespace)
    if len(item["summary"]) > 900:
        # Split the summary into sentences using the "." separator
        sentences = re.split(r"\.", item["summary"])

        # Keep removing sentences until the summary is less than or equal to 500 characters
        while len(item["summary"]) > 500:
            # Remove the last sentence from the list of sentences
            sentence = sentences.pop().strip()

            # Remove any trailing whitespace and the final "."
            sentence = sentence.rstrip(". ")


            # If there are no more sentences, break out of the loop
            if not sentences:
                break

            # Rejoin the remaining sentences with "."
            item["summary"] = ". ".join(sentences) + "."
        
        # If the summary is still too long, truncate it
        if len(item["summary"]) > 500:
            item["summary"] = item["summary"][:500].rstrip() + "…"

    # Add the processed item to the list
    processedData.append(item)

# Save the url_summary dictionary as a JSON file
with open("backend/URL_Summary_Formatted.json", "w", encoding='utf-8') as f:
    json.dump(processedData, f, ensure_ascii=False)