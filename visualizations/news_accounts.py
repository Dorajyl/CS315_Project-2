import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load in video data, filtering out unnecessary columns
df = pd.read_csv("data/metadata.csv", header=0, usecols=["video_id", 
                                                         "video_timestamp",
                                                         "author_username",
                                                         "author_name",
                                                         "data_user"])

# Datasets for each user
users = {
    "user_0001": df[df['data_user'] == "user_0001"].copy(),
    "user_0002": df[df['data_user'] == "user_0002"].copy(),
    "user_0003": df[df['data_user'] == "user_0003"].copy(),
    "user_0004": df[df['data_user'] == "user_0004"].copy(),
    "user_0005": df[df['data_user'] == "user_0005"].copy(),
    "user_0006": df[df['data_user'] == "user_0006"].copy(),
    "user_0007": df[df['data_user'] == "user_0007"].copy()
}

# Dataframe of news accounts
accounts_df = pd.read_csv("data/news_accounts.csv", header=0)

# Function to check if a username is a news account
def is_news_account(username):
    return username in set(accounts_df['Username'])

# Function to get top accounts for a given user
def get_top_accounts(user_df, n=5):
    # Filter the dataframe to include only news-related accounts
    news_df = user_df[user_df['author_username'].apply(is_news_account)]

    # Group by news account and count the number of videos each account appears in
    news_account_counts = news_df['author_username'].value_counts()

    # Select the top news-related accounts
    top_news_accounts = news_account_counts.head(n)

    return top_news_accounts

# Loop through each user
for user, user_df in users.items():
    # Get top accounts for the user
    top_accounts = get_top_accounts(user_df)

    # Plot the top accounts
    plt.figure(figsize=(10, 8))

    # Define specific color codes for specific countries
    color_mapping = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fc8d59', 
                     '#ff66b2', '#e41a1c', '#ff7f00', '#cba0d5', '#6a3d9a']

    sns.barplot(x=top_accounts.index, y=top_accounts.values, palette=color_mapping)

    # Add labels and title
    plt.xlabel(f'News Accounts for {user}', fontweight='bold')
    plt.ylabel('Videos', fontweight='bold')
    plt.title(f'Top News-Related Account for {user}', fontweight='bold', fontsize=14)

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

    # Saving the plot as a PNG file
    plt.savefig(f"visualizations//plots/news_accounts/accounts_{user}.png")

# Plot for all users
# Get top 10 accounts for all users combined
all_users_top10_accounts = get_top_accounts(df, n=10)

# Plot the top 10 accounts for all users
plt.figure(figsize=(10, 8))
sns.barplot(x=all_users_top10_accounts.index, y=all_users_top10_accounts.values, palette=color_mapping)

# Add labels and title
plt.xlabel('News Account', fontweight='bold')
plt.ylabel('Videos', fontweight='bold')
plt.title('Top News-Related Account for All Users', fontweight='bold', fontsize=14)

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

# Rotate x-axis labels
plt.xticks(rotation=20)

# Saving the plot as a PNG file
plt.savefig("visualizations/plots/news_accounts/accounts_meta.png")
