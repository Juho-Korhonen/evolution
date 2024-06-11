import matplotlib.pyplot as plt
import imageio
import numpy as np
import os
from matplotlib.colors import LinearSegmentedColormap

def create_video(grid_history, labels, colors, fps):
    data = [np.array(matrix) for matrix in grid_history]  # Ensure all matrices are numpy arrays
    
    

    # Define a custom colormap with proper range 0 to 1
    cmap_colors = [
        (0.0, colors["zero"]),  # Color for 0
        (0.2, colors["one"]),   # Color for 1
        (0.4, colors["two"]),   # Color for 2
        (1.0, colors["two_to_cyan"])  # Color for 10
    ]
    
    cmap = LinearSegmentedColormap.from_list("custom_cmap", cmap_colors)

    def process_matrix(matrix):
        # Scale values greater than 2 to fall within the range 2 to 10
        matrix = np.where(matrix > 2, 2 + (matrix - 2) / 8 * 8, matrix)
        return matrix

    def create_frame(matrix, second):
        # Transpose the matrix to switch x and y axes
        matrix = np.transpose(matrix)
        
        flattened_matrix = matrix.flatten()

        # Count the number of 1s and 2s
        count_of_ones = np.count_nonzero(flattened_matrix == 1)
        count_of_twos = np.count_nonzero(flattened_matrix > 1)
        
        fig, ax = plt.subplots()
        cax = ax.matshow(matrix, cmap=cmap, vmin=0, vmax=10)

        # Add a colorbar to indicate the meaning of colors
        cbar = fig.colorbar(cax, ticks=[0, 1, 2, 10])
        cbar.ax.set_yticklabels([labels["zero"], labels["one"], labels["two"], "10 (cyan)"])

        # Hide x and y axis numbers
        ax.set_xticks([])
        ax.set_yticks([])

        # Invert the y-axis to start from the bottom
        ax.invert_yaxis()

        plt.title(f"Second {second}")
        ax.text(-0.2, -0.15, 'creatures: ' + str(count_of_twos), horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=12)
        ax.text(1.2, -0.15, 'grass: ' + str(count_of_ones), horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=12)
        
        plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.2)
        plt.savefig(f"assets/frames/frame_{second}.png")
        plt.close()

    # Ensure the frames directory exists
    os.makedirs('assets/frames', exist_ok=True)

    # Create frames
    for second, matrix in enumerate(data):
        processed_matrix = process_matrix(matrix)
        create_frame(processed_matrix, second)

    # Combine frames into a video
    with imageio.get_writer('assets/matrix_evolution.mp4', fps=fps) as writer:
        for second in range(len(data)):
            image = imageio.imread(f"assets/frames/frame_{second}.png")
            writer.append_data(image)
