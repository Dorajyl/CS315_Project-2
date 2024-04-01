import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load in video data, filtering out unnecessary columns
df = pd.read_csv("data/metadata.csv", header=0, usecols=["video_id", 
                                                         "video_locationcreated", 
                                                         "video_description", 
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

# Function to get top countries for a given user
def get_top_countries(user_df):
    # Create a new DataFrame with the aggregated count of videos per country
    videos_per_country = user_df['video_locationcreated'].value_counts().reset_index()

    # Rename the columns for clarity
    videos_per_country.columns = ['Country', 'VideoCount']

    # Identify countries with at most 5 videos and combine them into the 'OTHER' category
    threshold = 15
    videos_per_country['Country'] = videos_per_country.apply(
        lambda row: row['Country'] if row['VideoCount'] > threshold else 'OTHER', axis=1
    )

    # Aggregate the counts again after combining countries
    videos_per_country = videos_per_country.groupby('Country')['VideoCount'].sum().reset_index()

    # Combine 'OTHER' and 'FAKE-AD' into one row
    videos_per_country.loc[videos_per_country['Country'].isin(['OTHER', 'FAKE-AD']), 'VideoCount'] = videos_per_country['VideoCount'].sum()
    videos_per_country = videos_per_country.drop_duplicates(subset='Country', keep='first')

    videos_per_country['Country'] = videos_per_country.apply(
        lambda row: 'OTHER' if row['Country'] in ['OTHER', 'FAKE-AD'] else row['Country'], axis=1
    )

    # Sort the DataFrame alphabetically by the 'Country' column
    videos_per_country = videos_per_country.sort_values('Country')
    videos_per_country = pd.concat([videos_per_country[videos_per_country['Country'] != 'OTHER'], videos_per_country[videos_per_country['Country'] == 'OTHER']])

    # Reset index
    videos_per_country = videos_per_country.reset_index(drop=True)

    # Return top 10 countries
    return videos_per_country.head(10)

# Loop through each user
for user, user_df in users.items():
    # Get top countries for the user
    top_countries = get_top_countries(user_df)

    # Set up the Seaborn style
    sns.set(style="whitegrid", rc={"grid.linewidth": 0.5, "grid.alpha": 0.5})

    # Ensure y-values over 110 are set to 110
    top_countries['VideoCount'] = top_countries['VideoCount'].clip(upper=110)

    # Define specific color codes for specific countries
    color_mapping = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fc8d59', 
                     '#ff66b2', '#e41a1c', '#ff7f00', '#cba0d5', '#6a3d9a']

    # Create the bar plot using seaborn
    plt.figure(figsize=(12, 8))
    sns.barplot(data=top_countries, x='Country', y='VideoCount', hue='Country', palette=color_mapping)
    plt.title(f'Top Countries for {user}', fontweight='bold', fontsize=14)
    plt.xlabel(f'Top Countries for {user}', fontweight='bold')
    plt.ylabel('Number of Videos', fontweight='bold')
    plt.xticks(rotation=45, ha='right')

    # Set and order axis ticks
    plt.yticks([20, 30, 40, 50, 60, 70, 80, 90, 100, 110], labels=["20", "30", "40", "50", "60", "70", "80", "90", "100", "100+"])

    # Set y-axis range to 0-1000+
    plt.ylim(10, 115)

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
    plt.savefig(f"visualizations/plots/top_countries/countries_{user}.png")

# Plot for all users
# Get top countries for all users combined
all_users_top_countries = pd.concat([get_top_countries(user_df) for user, user_df in users.items()])

# Aggregate the counts again after combining countries
all_users_top_countries = all_users_top_countries.groupby('Country')['VideoCount'].sum().reset_index()

# Sort the DataFrame alphabetically by the 'Country' column
all_users_top_countries = all_users_top_countries.sort_values('Country')
all_users_top_countries = pd.concat([all_users_top_countries[all_users_top_countries['Country'] != 'OTHER'], all_users_top_countries[all_users_top_countries['Country'] == 'OTHER']])

# Reset index
all_users_top_countries = all_users_top_countries.reset_index(drop=True)

# Set up the Seaborn style
sns.set(style="whitegrid", rc={"grid.linewidth": 0.5, "grid.alpha": 0.5})

# Ensure y-values over 110 are set to 110
all_users_top_countries['VideoCount'] = all_users_top_countries['VideoCount'].clip(upper=110)

# Create the bar plot using seaborn
plt.figure(figsize=(12, 8))
sns.barplot(data=all_users_top_countries, x='Country', y='VideoCount', hue='Country', palette=color_mapping)
plt.title('Top Countries for All Users', fontweight='bold', fontsize=14)
plt.xlabel('Country', fontweight='bold')
plt.ylabel('Number of Videos', fontweight='bold')
plt.xticks(rotation=45, ha='right')

# Set and order axis ticks
plt.yticks([20, 30, 40, 50, 60, 70, 80, 90, 100, 110], labels=["20", "30", "40", "50", "60", "70", "80", "90", "100", "100+"])

# Set y-axis range to 0-1000+
plt.ylim(10, 115)

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
plt.savefig("visualizations/plots/top_countries/countries_meta.png")
