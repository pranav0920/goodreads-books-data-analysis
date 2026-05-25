import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load and clean data
df = pd.read_csv('books.csv', on_bad_lines='skip')
df.columns = df.columns.str.strip()

# 1. Advanced Data Cleaning & Feature Engineering
df['average_rating'] = pd.to_numeric(df['average_rating'], errors='coerce')
df['num_pages'] = pd.to_numeric(df['num_pages'], errors='coerce')
df['ratings_count'] = pd.to_numeric(df['ratings_count'], errors='coerce')
df['text_reviews_count'] = pd.to_numeric(df['text_reviews_count'], errors='coerce')

# Extract Year from publication_date
df['publication_year'] = df['publication_date'].apply(lambda x: str(x).split('/')[-1] if pd.notnull(x) else np.nan)
df['publication_year'] = pd.to_numeric(df['publication_year'], errors='coerce')
# Filter out unreasonable years (e.g., typing errors like 2099 or very old books if they skew plots, but let's keep 1900-2026)
df = df[(df['publication_year'] >= 1950) & (df['publication_year'] <= 2026)]

# 2. Analysis: Author Impact (Total engagement vs Average Rating)
# Filter authors with at least 5 books for reliable statistics
author_stats = df.groupby('authors').agg(
    book_count=('title', 'count'),
    avg_rating=('average_rating', 'mean'),
    total_ratings=('ratings_count', 'sum')
).reset_index()
top_engaged_authors = author_stats[author_stats['book_count'] >= 5].nlargest(10, 'total_ratings')

print("--- TOP ENGAGED AUTHORS (min 5 books) ---")
print(top_engaged_authors)

# 3. Analysis: Publisher Market Share
publisher_stats = df.groupby('publisher').size().reset_index(name='count').nlargest(10, 'count')
print("\n--- TOP PUBLISHERS BY BOOK COUNT ---")
print(publisher_stats)

# 4. Correlation Matrix
corr = df[['average_rating', 'num_pages', 'ratings_count', 'text_reviews_count']].corr()
print("\n--- CORRELATION MATRIX ---")
print(corr)

# Set style for professional plots
sns.set_theme(style="whitegrid")

# Plot 1: Correlation Heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Heatmap of Book Metrics', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.close()

# Plot 2: Top Engaged Authors (Total Ratings)
plt.figure(figsize=(10, 5))
sns.barplot(data=top_engaged_authors, x='total_ratings', y='authors', palette='mako')
plt.title('Top 10 Authors by Total Reader Engagement (Total Ratings)', fontsize=14, fontweight='bold')
plt.xlabel('Total Ratings (in Tens of Millions)', fontsize=11)
plt.ylabel('Author', fontsize=11)
plt.tight_layout()
plt.savefig('top_engaged_authors.png')
plt.close()

# Plot 3: Trend of Book Publications Over Years
plt.figure(figsize=(10, 4))
sns.histplot(data=df, x='publication_year', bins=35, kde=True, color='#2b5c8f')
plt.title('Trend of Book Publications Over Time (1950 - 2020+)', fontsize=14, fontweight='bold')
plt.xlabel('Publication Year', fontsize=11)
plt.ylabel('Number of Books Published', fontsize=11)
plt.tight_layout()
plt.savefig('publication_trend.png')
plt.close()