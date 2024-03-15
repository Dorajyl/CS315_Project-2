import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

# Load in video data, filtering out unnecessary columns
df = pd.read_csv("cs315project2datacollection/results.csv", header=0, usecols=["video_id", 
                                                                               "video_description"])

# Function to extract hashtags from a string
def extract_hashtags(description):
    if pd.isna(description):  # Check if description is NaN
        return ""
    hashtags = re.findall(r'#(\w+)', description)
    return ', '.join(hashtags)

df['hashtags'] = df['video_description'].apply(extract_hashtags)

# Dataframe of news hashtags
hashtag_df = pd.read_csv("data/news_hashtags.csv", header=0)

# Function to count the occurrences of news hashtags for each row
def count_news_tags(row):
    if not row['hashtags']:  # If no hashtags, return an empty dictionary
        return {}
    hashtags = [tag.strip() for tag in row['hashtags'].split(',') if tag.strip()]  # Split and strip hashtags
    news_hashtags = {hashtag: 0 for hashtag in set(hashtag_df['hashtag'])}
    for hashtag in hashtags:
        if hashtag in set(hashtag_df['hashtag']):
            news_hashtags[hashtag] += 1
    return news_hashtags

# Apply the function to each row in the DataFrame
df['news_tags'] = df.apply(count_news_tags, axis=1)

# Flatten the list of dictionaries into a single dictionary
news_hashtag_counts = {}
for row in df['news_tags']:
    for hashtag, count in row.items():
        if hashtag in news_hashtag_counts:
            news_hashtag_counts[hashtag] += count
        else:
            news_hashtag_counts[hashtag] = count

# Sort the dictionary by values in descending order
sorted_news_hashtags = sorted(news_hashtag_counts.items(), key=lambda x: x[1], reverse=True)

# Extract the top 5 most common news hashtags
top5_news_hashtags = dict(sorted_news_hashtags[:5])

# Plot the top 5 most common news hashtags
color_mapping = {
    'football': '#a6cee3',
    'news': '#1f78b4',
    'sports': '#ff66b2',
    'oscars': '#33a02c',
    'learnontiktok': '#fc8d59',
}

sns.barplot(x=list(top5_news_hashtags.keys()), y=list(top5_news_hashtags.values()), palette=color_mapping)

# Add labels and title
plt.xlabel('News-Related Hashtag', fontweight='bold')
plt.ylabel('Videos', fontweight='bold')
plt.title('Top News-Related Hashtags', fontweight='bold', fontsize=14)

# Remove top border and set x and y axis lines to black
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['right'].set_visible(False)

# Removing legend
plt.legend([],[], frameon=False)  # Hide legend for individual points

# Code for presentation formatting (comment out)
plt.title('')
plt.gca().set_facecolor('none')

# Save the plot as a PNG file
plt.savefig("visualizations/news_hashtags.png", transparent=True)
plt.show()

