import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load in video data, filtering out unnecessary columns
df = pd.read_csv("cs315project2datacollection/results.csv", header=0, usecols=["video_id", 
                                                                               "video_locationcreated", 
                                                                               "video_description", 
                                                                               "author_username", 
                                                                               "author_name"])

# Create a new DataFrame with the aggregated count of videos per country
videos_per_country = df['video_locationcreated'].value_counts().reset_index()

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

print(videos_per_country)
# Set up the Seaborn style
sns.set(style="whitegrid", rc={"grid.linewidth": 0.5, "grid.alpha": 0.5})

# Ensure y-values over 110 are set to 110
videos_per_country['VideoCount'] = videos_per_country['VideoCount'].clip(upper=110)

# Define specific color codes for specific countries

color_mapping = {
    'AR': '#a6cee3',
    'AU': '#1f78b4',
    'BR': '#b2df8a',
    'CA': '#33a02c',
    'DE': '#fc8d59',
    'ES': '#ff66b2',
    'FR': '#e41a1c',
    'GB': '#ff7f00',
    'IE': '#cba0d5',
    'IL': '#6a3d9a',
    'IT': '#ffff99',
    'MX': '#af8dc3',
    'NL': '#4daf4a',
    'NO': '#fee08b',
    'PH': '#ff7f00',
    'PL': '#e41a1c',
    'SE': '#984ea3',
    'SG': '#ffeda0',
    'US': '#ff66b2',
    'ZA': '#91cf60',
    'OTHER': '#377eb8'
}

# Create the bar plot using seaborn
plt.figure(figsize=(12, 8))
sns.barplot(data=videos_per_country, x='Country', y='VideoCount', hue='Country', palette=color_mapping)
plt.title('Video Counts per Country', fontweight='bold', fontsize=14)
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
plt.savefig("visualizations/per_country.png", transparent=True)
plt.show()

