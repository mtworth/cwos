"""
Basic usage example for CommentWorks.

Demonstrates theme detection and assignment using simple Python lists.
No pandas or other dependencies required.
"""

import commentworks as cw

# Sample restaurant reviews
reviews = [
    "The pasta was perfectly cooked and the sauce was incredible. However, we waited nearly 40 minutes for our appetizers.",
    "Our waiter was attentive and gave great wine recommendations. The ambiance was romantic and cozy.",
    "Food was cold when it arrived at our table. Manager comped our meal and apologized profusely.",
    "Portions are huge, great value for money. The decor is a bit dated but who cares when the food is this good.",
    "Reservation system is a nightmare, tried calling for three days. Once we got in, the food was just okay.",
]

print("=" * 60)
print("CommentWorks - Basic Usage Example")
print("=" * 60)

# Example 1: Detect themes across all reviews
print("\n1. THEME DETECTION")
print("-" * 60)
print("Analyzing", len(reviews), "reviews...")
themes = cw.detect_themes(reviews)
print("\nDetected themes:")
for theme in themes:
    print(f"  - {theme}")

# Example 2: Assign themes to individual reviews
print("\n\n2. THEME ASSIGNMENT (Single Review)")
print("-" * 60)
single_review = "Great food but service was slow and prices were high"
possible_themes = ["food quality", "service", "ambiance", "pricing", "wait times"]

print(f"Review: {single_review}")
print(f"\nPossible themes: {', '.join(possible_themes)}")

assigned = cw.assign_themes(single_review, possible_themes)
print(f"\nAssigned themes: {', '.join(assigned)}")

# Example 3: Batch assign themes to multiple reviews
print("\n\n3. THEME ASSIGNMENT (Batch)")
print("-" * 60)
batch_reviews = [
    "Amazing atmosphere and friendly staff",
    "Food was overpriced for the quality",
    "Long wait time but worth it for the quality"
]

print(f"Processing {len(batch_reviews)} reviews...")
batch_results = cw.assign_themes(batch_reviews, possible_themes)

for i, (review, themes) in enumerate(zip(batch_reviews, batch_results), 1):
    print(f"\n  Review {i}: {review}")
    print(f"  Themes: {', '.join(themes)}")

print("\n" + "=" * 60)
print("Done!")
print("=" * 60)
