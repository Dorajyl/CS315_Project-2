import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load in video data, filtering out unnecessary columns
df = pd.read_csv("cs315project2datacollection/results.csv", header=0, usecols=["video_id", 
                                                                               "video_timestamp",
                                                                               "author_username",
                                                                               "author_name"])

# Dataframe of news accounts
accounts_df = pd.read_csv("data/news_accounts.csv", header=0)

# Function to check if a username is a news account
def is_news_account(username):
    return username in set(accounts_df['Username'])

# Mark news_account column as True if the username is a news account
df['news_account'] = df['author_username'].apply(is_news_account)

# Filter the dataframe to include only news-related accounts
news_df = df[df['news_account']]

# Group by news account and count the number of videos each account appears in
news_account_counts = news_df['author_username'].value_counts()

# Select the top 5 news-related accounts
top5_news_accounts = news_account_counts.head(5)

# Plot the top 5 most common news accounts
color_mapping = {
    'brutamerica': '#a6cee3',
    'yahooaustralia': '#1f78b4',
    'espn': '#ff66b2',
    'dailymail': '#33a02c',
    'nfl': '#fc8d59',
}

# Plot the bar graph
plt.figure(figsize=(10, 6))
sns.barplot(x=top5_news_accounts.index, y=top5_news_accounts.values, palette=color_mapping)

# Add labels and title
plt.xlabel('News Account', fontweight='bold')
plt.ylabel('Videos', fontweight='bold')
plt.title('Top News-Related Account', fontweight='bold', fontsize=14)

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
plt.savefig("visualizations/news_accounts.png", transparent=True)
plt.show()

