# import matplotlib.pyplot as plt

# # Data for the graph
# clinical_concepts = ['Erythema', 'Plaque', 'Papule', 'Brown (hyperpigmentation)', 'Scale', 'Crust', 'White (hypopigmentation)',
#                      'Yellow', 'Erosion', 'Nodule', 'Ulcer', 'Friable', 'Patch', 'Dome-shaped', 'Exudate', 'Scar', 'Pustule',
#                      'Telangiectasia', 'Black', 'Purple', 'Atrophy', 'Bulla']

# number_of_samples = [2139, 1966, 1169, 759, 686, 497, 257, 245, 200, 189, 154, 153, 149, 146, 144, 123, 103, 100, 90, 85, 69, 64]

# # Create the figure and axes
# plt.figure(figsize=(14, 8))

# # Plot bar graph
# plt.barh(clinical_concepts, number_of_samples, color='mediumseagreen')

# # Format the graph
# plt.xlabel('Number of Samples', fontsize=12)
# plt.ylabel('Clinical Concepts', fontsize=12)
# plt.title('Data Collection: Number of Samples for Each Clinical Concept', fontsize=14)

# # Adjust layout to prevent overlap
# plt.tight_layout()

# # Save the graph as an image (path where the file will be saved)
# file_path = 'data_collection_bar_graph.png'
# plt.savefig(file_path, bbox_inches='tight', dpi=300)
# plt.close()

# print(f"Graph saved as: {file_path}")


# agumented data

# import matplotlib.pyplot as plt

# # Data for the augmented data graph
# clinical_concepts = ['Erythema', 'Plaque', 'Papule', 'Brown (hyperpigmentation)', 'Scale', 'Crust', 'White (hypopigmentation)',
#                      'Yellow', 'Erosion', 'Nodule', 'Ulcer', 'Friable', 'Patch', 'Dome-shaped', 'Exudate', 'Scar', 'Pustule',
#                      'Telangiectasia', 'Black', 'Purple', 'Atrophy', 'Bulla']

# # Sample values for augmented data (example values – adjust as needed)
# augmented_samples = [3560, 3200, 1900, 1300, 1100, 850, 450, 400, 350, 320, 290, 270, 260, 250, 240, 220, 190, 180, 150, 140, 120, 100]

# # Create the figure and axes
# plt.figure(figsize=(14, 8))

# # Plot bar graph for augmented data
# plt.barh(clinical_concepts, augmented_samples, color='cornflowerblue')

# # Format the graph
# plt.xlabel('Number of Augmented Samples', fontsize=12)
# plt.ylabel('Clinical Concepts', fontsize=12)
# plt.title('Data Augmentation: Number of Samples for Each Clinical Concept', fontsize=14)

# # Adjust layout to prevent overlap
# plt.tight_layout()

# # Save the graph as an image (path where the file will be saved)
# file_path = 'augmented_data_bar_graph.png'
# plt.savefig(file_path, bbox_inches='tight', dpi=300)
# plt.close()

# print(f"Graph saved as: {file_path}")




# import matplotlib.pyplot as plt

# # Data for the feature extraction graph
# features = ['Texture', 'Color', 'Shape', 'Edge', 'Intensity', 'Frequency', 'Symmetry', 'Pattern']
# extracted_values = [85, 78, 90, 75, 88, 80, 84, 77]  # Example values – adjust as needed

# # Create the figure and axes
# plt.figure(figsize=(10, 6))

# # Plot line graph for feature extraction
# plt.plot(features, extracted_values, marker='o', linestyle='-', color='dodgerblue', linewidth=2)

# # Annotate values on the graph
# for i, value in enumerate(extracted_values):
#     plt.text(i, value + 1, f'{value}%', ha='center')

# # Format the graph
# plt.xlabel('Features', fontsize=12)
# plt.ylabel('Extraction Score (%)', fontsize=12)
# plt.title('Feature Extraction: Performance for Each Feature', fontsize=14)

# # Add grid
# plt.grid(True, linestyle='--', alpha=0.7)

# # Save the graph as an image
# file_path = 'feature_extraction_line_graph.png'
# plt.tight_layout()
# plt.savefig(file_path, bbox_inches='tight', dpi=300)
# plt.close()

# print(f"Graph saved as: {file_path}")


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Given clinical concepts and sample counts
clinical_concepts = [
    "Erythema", "Plaque", "Papule", "Brown (hyperpigmentation)", "Scale", "Crust",
    "White (hypopigmentation)", "Yellow", "Erosion", "Nodule", "Ulcer", "Friable",
    "Patch", "Dome-shaped", "Exudate", "Scar", "Pustule", "Telangiectasia", "Black",
    "Purple", "Atrophy", "Bulla"
]

# Matrix size
size = len(clinical_concepts)

# Initialize matrix with zeros
data_matrix = np.zeros((size, size))

# Fill diagonal with values between 0.91 and 0.96
np.fill_diagonal(data_matrix, np.random.uniform(0.91, 0.96, size))

# Fill a few off-diagonal values randomly between 0 and 0.2
for i in range(size):
    for j in range(size):
        if i != j and np.random.rand() < 0.05:  # 5% chance of having a small value
            data_matrix[i, j] = np.random.uniform(0, 0.2)

# Convert to DataFrame
df = pd.DataFrame(data_matrix, index=clinical_concepts, columns=clinical_concepts)

# Plot heatmap
plt.figure(figsize=(18, 8))
sns.heatmap(df, annot=True, fmt=".2f", cmap="Blues", linewidths=0.5, vmin=0, vmax=1)

# Adjust labels
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)
plt.title("Clinical Concept Heatmap (Diagonal: 91%-96%, Others: <0.2)")

# Save the figure
file_path = "heatmap.png"
plt.savefig(file_path, bbox_inches="tight", dpi=300)

# Show plot
plt.show()
