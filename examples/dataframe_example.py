"""
DataFrame integration example for CommentWorks.

Demonstrates how to use CommentWorks with pandas DataFrames for analyzing
product and restaurant reviews at scale.

Note: pandas is NOT required for CommentWorks, but they work great together!
"""

import pandas as pd
import commentworks as cw

print("=" * 60)
print("CommentWorks - DataFrame Integration Example")
print("=" * 60)

# Load sample reviews
print("\nLoading reviews from CSV...")
df = pd.read_csv('examples/reviews.csv')
print(f"Loaded {len(df)} reviews")
print(f"\nCategories: {df['category'].value_counts().to_dict()}")

# Example 1: Detect themes across all reviews
print("\n\n1. DETECT THEMES ACROSS ALL REVIEWS")
print("-" * 60)
all_themes = cw.detect_themes(df['review_text'].tolist())
print(f"Detected {len(all_themes)} unique themes:")
for theme in all_themes:
    print(f"  - {theme}")

# Example 2: Detect themes by category
print("\n\n2. DETECT THEMES BY CATEGORY")
print("-" * 60)

for category in df['category'].unique():
    category_reviews = df[df['category'] == category]['review_text'].tolist()
    themes = cw.detect_themes(category_reviews)
    print(f"\n{category.title()} themes ({len(category_reviews)} reviews):")
    for theme in themes:
        print(f"  - {theme}")

# Example 3: Assign themes to each review
print("\n\n3. ASSIGN THEMES TO EACH REVIEW")
print("-" * 60)

# Define possible themes based on what we detected
possible_themes = [
    "food quality", "service", "wait times", "ambiance", "pricing",
    "product quality", "shipping", "customer service", "durability",
    "ease of use", "value for money"
]

print(f"Using {len(possible_themes)} possible themes...")
print("Processing reviews...")

# Use apply for row-by-row processing
df['assigned_themes'] = df['review_text'].apply(
    lambda x: cw.assign_themes(x, possible_themes)
)

# Show results for a few reviews
print("\nSample results:")
for idx in [0, 5, 10]:
    row = df.iloc[idx]
    print(f"\nReview {row['review_id']} ({row['category']}) - Rating: {row['rating']}/5")
    print(f"Text: {row['review_text'][:80]}...")
    print(f"Themes: {', '.join(row['assigned_themes'])}")

# Example 4: Analyze themes by rating
print("\n\n4. THEME DISTRIBUTION BY RATING")
print("-" * 60)

# Count theme occurrences per rating level
for rating in sorted(df['rating'].unique()):
    rating_df = df[df['rating'] == rating]
    all_themes_for_rating = [theme for themes in rating_df['assigned_themes'] for theme in themes]
    theme_counts = pd.Series(all_themes_for_rating).value_counts()

    print(f"\n{rating}-star reviews (n={len(rating_df)}):")
    print(theme_counts.head(3).to_string())

# Example 5: Export results
print("\n\n5. EXPORT RESULTS")
print("-" * 60)
output_file = 'examples/reviews_with_themes.csv'

# Convert list of themes to comma-separated string for CSV export
df['themes_csv'] = df['assigned_themes'].apply(lambda x: ', '.join(x))
df[['review_id', 'category', 'review_text', 'rating', 'themes_csv']].to_csv(
    output_file, index=False
)
print(f"Results saved to: {output_file}")

print("\n" + "=" * 60)
print("Done!")
print("=" * 60)
