import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

# Load in video data, filtering out unnecessary columns
df = pd.read_csv("data/metadata.csv", header=0, usecols=["video_id", "video_description", "data_user"])

# Datasets for each user
user_0001 = df[df['data_user'] == "user_0001"].copy()
user_0002 = df[df['data_user'] == "user_0002"].copy()
user_0003 = df[df['data_user'] == "user_0003"].copy()
user_0004 = df[df['data_user'] == "user_0004"].copy()
user_0005 = df[df['data_user'] == "user_0005"].copy()
user_0006 = df[df['data_user'] == "user_0006"].copy()
user_0007 = df[df['data_user'] == "user_0007"].copy()

# Function to count the occurrences of news hashtags for each row
def count_news_tags(row):
    # Dataframe of news hashtags
    hashtag_df = pd.read_csv("data/news_hashtags.csv", header=0)

    if not row['hashtags']:  # If no hashtags, return an empty dictionary
        return {}
    hashtags = [tag.strip() for tag in row['hashtags'].split(',') if tag.strip()]  # Split and strip hashtags
    news_hashtags = {hashtag: 0 for hashtag in set(hashtag_df['hashtag'])}
    for hashtag in hashtags:
        if hashtag in set(hashtag_df['hashtag']):
            news_hashtags[hashtag] += 1
    return news_hashtags

def news_hashtags(df):
    # Function to extract hashtags from a string
    def extract_hashtags(description):
        if pd.isna(description):  # Check if description is NaN
            return ""
        hashtags = re.findall(r'#(\w+)', description)
        return ', '.join(hashtags)

    df['hashtags'] = df['video_description'].apply(extract_hashtags)

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

    return top5_news_hashtags

# Plot the top 5 most common news hashtags (change based on user)
top5_news_hashtags = news_hashtags(df)

# Creating color palette
color_mapping = ['#a6cee3','#1f78b4','#ff66b2','#33a02c','#fc8d59']

sns.barplot(x=list(top5_news_hashtags.keys()), y=list(top5_news_hashtags.values()), palette=color_mapping)

# Add labels and title (change the x label for data user you are running)
plt.xlabel('News-Related Hashtags', fontweight='bold')
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

# Save the plot as a PNG file (change the filename for data user you are running)
plt.savefig("visualizations/plots/news_hashtags/hashtags_meta.png")
