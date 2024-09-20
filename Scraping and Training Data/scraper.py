import praw
import json

reddit = praw.Reddit("Scraper", user_agent="Scraper user agent by u/RaleighElectroQuest")

subreddit = reddit.subreddit('copypasta')
posts_data = []
count = 0

# Iterate over the top posts
for submission in subreddit.top(limit=1000):
    post_info = {
        'title': submission.title,
        'score': submission.score,
        'url': submission.url,
        'num_comments': submission.num_comments,
        'body': submission.selftext,  # The text content of the post
        'comments': []
    }

    # Fetch the top level comments
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        post_info['comments'].append(comment.body)
            
    # Append post info to list
    posts_data.append(post_info)
    count+=1
    if count % 100 == 0:
        print('scraped 100 posts')    
    
    
# Write data to JSON file
with open('spaghetti_dishes.json', 'w', encoding='utf-8') as f:
    json.dump(posts_data, f, ensure_ascii=False, indent=4)
    
print("Data saved to spaghetti_dishes.json")
