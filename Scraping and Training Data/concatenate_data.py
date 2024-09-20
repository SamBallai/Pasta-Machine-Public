import json

# Load the JSON data
with open('rinsed_spaghetti.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check if the data is a list or a dictionary
comments = []
if isinstance(data, dict):
    # If data is a dictionary and 'comments' is a key
    comments = data.get('comments', [])
elif isinstance(data, list):
    # If data is a list, iterate over each item to extract 'comments'
    for item in data:
        if isinstance(item, dict) and 'comments' in item:
            comments.extend(item['comments'])  # Add all comments to the list

# Save the comments into a text file, skipping any None values
with open('cleaned_corpus.txt', 'w', encoding='utf-8') as f:
    for comment in comments:
        if comment is not None:  # Check if the comment is not None
            f.write(comment + '\n')
