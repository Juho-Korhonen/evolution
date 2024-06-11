import matplotlib.pyplot as plt
import imageio
import numpy as np
import os
from matplotlib.colors import ListedColormap, BoundaryNorm

def create_video(grid_history, labels, colors, fps, grid_size):
    def process_matrix(matrix):
        # Process the matrix to handle both integer and RGB values
        processed_matrix = np.zeros((len(matrix), len(matrix[0]), 3), dtype=np.uint8)
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if isinstance(matrix[i][j], list) and len(matrix[i][j]) == 3:
                    # If the value is an RGB array, use it directly
                    processed_matrix[i, j] = matrix[i][j]
                elif matrix[i][j] == 1:
                    # If the value is 1, use the color for 1
                    processed_matrix[i, j] = colors["one"]
                elif matrix[i][j] == 0:
                    # If the value is 0, use the color for 0
                    processed_matrix[i, j] = colors["zero"]
        return processed_matrix

    def create_frame(matrix, second):
        # Transpose the matrix to switch x and y axes
        matrix = np.transpose(matrix, (1, 0, 2))

        flattened_matrix = matrix.reshape(-1, matrix.shape[-1])

        # Count the number of 1s and 0s
        count_of_ones = np.count_nonzero((flattened_matrix == colors["one"]).all(axis=1))
        count_of_zeros = np.count_nonzero((flattened_matrix == colors["zero"]).all(axis=1))
        count_of_others = grid_size - (count_of_ones + count_of_zeros)

        fig, ax = plt.subplots()
        im = ax.imshow(matrix, vmin=0, vmax=1)

        # Hide x and y axis numbers
        ax.set_xticks([])
        ax.set_yticks([])

        # Invert the y-axis to start from the bottom
        ax.invert_yaxis()

        plt.title(f"Second {second}")
        ax.text(-0.2, -0.15, 'creatures: ' + str(count_of_others), horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=12)
        ax.text(1.2, -0.15, 'grass: ' + str(count_of_ones), horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=12)
        
        # Create a discrete color map for the colorbar
        # Create a discrete color map for the colorbar
        cmap = ListedColormap([colors["zero"], colors["one"]])
        norm = BoundaryNorm([0, 0.5, 1], cmap.N)
        cbar = fig.colorbar(im, ax=ax, cmap=cmap, norm=norm, boundaries=[0, 0.5, 1], ticks=[0.25, 0.75])
        cbar.ax.set_yticklabels([labels["zero"], labels["one"]])

        plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.2)
        plt.savefig(f"assets/frames/frame_{second}.png")
        plt.close()

    # Ensure the frames directory exists
    os.makedirs('assets/frames', exist_ok=True)

    # Create frames
    for second, matrix in enumerate(grid_history):
        processed_matrix = process_matrix(matrix)
        create_frame(processed_matrix, second)

    # Combine frames into a video
    with imageio.get_writer('assets/matrix_evolution.mp4', fps=fps) as writer:
        for second in range(len(grid_history)):
            image = imageio.imread(f"assets/frames/frame_{second}.png")
            writer.append_data(image)