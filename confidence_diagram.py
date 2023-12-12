import matplotlib.pyplot as plt

data = {
    "One Change Short": 4,
    "Two Change Short": 0.3,
    "Three Change Short": 2.7,
    "One Change Long": 2.96,
    "Two Change Long": 3.2,
    "Three Change Long": 2.1
}

categories = list(data.keys())
percentages = list(data.values())

fig, ax = plt.subplots(figsize=(10, 6))
bars = plt.barh(categories, percentages, color=['green' if p >= 0 else 'red' for p in percentages])

# Add data values next to each bar
for bar, percentage in zip(bars, percentages):
    xval = percentage + 0.1 if percentage >= 0 else percentage - 0.5
    plt.text(xval, bar.get_y() + bar.get_height() / 2, f"{percentage:.2f}%", va='center')

plt.title('Average Percent Decrease in GPT-4 Confidence Level on Movie Inputs')
plt.xlabel('Percentage Change')
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Add legend for positive and negative changes
# plt.legend(['Positive Change', 'Negative Change'], loc='lower right')

# Reduce space between columns
plt.tight_layout()

plt.show()
