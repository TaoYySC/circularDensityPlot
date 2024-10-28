import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Load the penguins dataset and drop missing values
df = sns.load_dataset('penguins').dropna()

# Create the plot
fig, ax = plt.subplots(figsize=(6, 6))

# Draw the 2D kernel density estimate (KDE) plot
kde_plot = sns.kdeplot(
    x=df.bill_length_mm,
    y=df.bill_depth_mm,
    cmap="Greens",
    fill=True,
    bw_adjust=0.5,
    ax=ax
)

# Set equal aspect ratio for the axes
ax.set_aspect('equal')

# Get axis limits
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# Calculate the center and radius for the circular mask
center_x = (xlim[0] + xlim[1]) / 2
center_y = (ylim[0] + ylim[1]) / 2
radius = min((xlim[1] - xlim[0]), (ylim[1] - ylim[0])) / 2

# Create a circular mask
circle = Circle((center_x, center_y), radius, transform=ax.transData)
for collection in ax.collections:
    collection.set_clip_path(circle)

# Set axis limits
ax.set_xlim(center_x - radius, center_x + radius)
ax.set_ylim(center_y - radius, center_y + radius)

# Add a colorbar for the KDE plot
# Get the first collection from kde_plot for colorbar scaling
if ax.collections:
    norm = plt.Normalize(vmin=0, vmax=ax.collections[0].get_array().max())
    sm = plt.cm.ScalarMappable(cmap="Greens", norm=norm)
    sm.set_array([])

    # Display colorbar
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical')
    cbar.set_label('Density Level')

# Hide the axes
ax.axis('off')

# Show the plot
plt.show()
