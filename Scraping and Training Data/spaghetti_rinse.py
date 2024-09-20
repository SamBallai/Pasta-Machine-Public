import json
import re

# Function to remove None fields from a dictionary
def remove_none_fields_from_dict(data_dict):
    keys_to_remove = [key for key, value in data_dict.items() if value is None]
    
    # Remove the keys that have None values
    for key in keys_to_remove:
        del data_dict[key]
    
    # Process nested dicts or lists
    for key, value in data_dict.items():
        if isinstance(value, dict):
            remove_none_fields_from_dict(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    remove_none_fields_from_dict(item)

# Function to clean comments
def clean_comments(comment):
    # Remove URLs
    comment = re.sub(r'http\S+|www\S+|https\S+', '', comment, flags=re.MULTILINE)
    
    # Remove HTML tags
    comment = re.sub(r'<.*?>', '', comment)
    
    # Remove @mentions
    comment = re.sub(r'@\w+', '', comment)
    
    # Remove non-ASCII characters but keep emojis
    comment = re.sub(r'[^\x00-\x7F\u263a-\U0001FAFF]+', '', comment)
    
    # Remove any instance of '[deleted]' and '[removed]'
    comment = re.sub(r'\s*\[?deleted\]?\s*', '', comment, flags=re.IGNORECASE)
    comment = re.sub(r'\s*\[?removed\]?\s*', '', comment, flags=re.IGNORECASE)
    
    # Clean up excessive spaces and line breaks
    comment = re.sub(r'\s+', ' ', comment).strip()
    comment = re.sub(r'\n+', '\n', comment).strip()
    comment = re.sub(r',\s*,+', ',', comment).strip()
    comment = re.sub(r',\s*\n', '\n', comment).strip()
    
    return comment

# Function to remove potential ASCII art
def remove_ascii_art(comment):
    comment = re.sub(r'[^\w\s]{10,}', '', comment)
    comment = re.sub(r'[^\s]{40,}', '', comment)
    comment = re.sub(r'^(.)\1{10,}$', '', comment, flags=re.MULTILINE)
    comment = re.sub(r'\n+', '\n', comment).strip()
    return comment

# Function to clean invalid control characters
def clean_invalid_chars(file_content):
    file_content = re.sub(r'[\x00-\x1f\x7f]', '', file_content)
    return file_content

# Recursive function to clean comment structure and remove empty strings
def clean_comment_structure(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = clean_comment_structure(value)
    elif isinstance(data, list):
        # Filter out empty strings from the list
        return [clean_comment_structure(item) for item in data if item != ""]
    elif isinstance(data, str):
        data = clean_comments(data)
        data = remove_ascii_art(data)
        return data if data else None  # Return None if the string is empty after cleaning
    return data

# Main function to clean the JSON file
def clean_json_file(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        file_content = f.read()
    
    # Clean invalid control characters
    cleaned_content = clean_invalid_chars(file_content)
    
    try:
        data = json.loads(cleaned_content)
        print("JSON file loaded successfully")
    except json.JSONDecodeError as e:
        print(f"Error loading JSON: {e}")
        return
    
    fields_to_remove = ['score', 'url', 'num_comments']
    
    for index, item in enumerate(data):
        # Remove unnecessary fields
        for field in fields_to_remove:
            if field in item:
                del item[field]
        
        # Remove None fields
        if isinstance(item, dict):
            remove_none_fields_from_dict(item)
        
        # Clean the entire item, including nested structures
        data[index] = clean_comment_structure(item)
    
    # Filter out None or empty items from the top level
    data = [item for item in data if item]

    with open(output_path, 'w', encoding='utf-8', errors='ignore') as f:
        json.dump(data, f, indent=4)
    
    print(f"Cleaned JSON file saved to {output_path}")

# Example usage
clean_json_file('spaghetti_dishes.json', 'rinsed_spaghetti.json')

