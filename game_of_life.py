import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
ON = 255
OFF = 0
vals = [ON, OFF]
N = 100

def random_grid(N):
    """returns a grid of N x N values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)


def add_glider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""

    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider


def update(frameNum, img, grid, N):
    #copy grid since we reequire 8 neighbros for calculation
    #and we go line by line

    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # compute 8-neighbor sum usinf toroidal boundary condition
            # x and y wrap around so that the simulation
            #takes place on toroidal surface

            total = int((grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
                         grid[(i - 1) % N, j] + grid[(i + 1) % N, j] +
                         grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, (j + 1) % N] +
                         grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, (j + 1) % N]) / 255)
            #apply Conway's rule
            if grid[i, j] == ON:
                if(total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON
        #update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main() funktion
def main():
    # command line arguments are in sys.argv[1], sys.argv[2], ..
    # sys.argv[0] is the script name and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of life simulation")

    #add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--move-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)

    args = parser.parse_args()

    #set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    #set animation update intervall
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    #declare grid
    grid = np.array([])

    #check if "glider demo flag is specified
    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        add_glider(i=1, j=1, grid=grid)
    else:
        #populate grid with random on/off - more off than on
        grid = random_grid(N)

    #set up the animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)

    #number of frames ?
    #set the output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


# call main
if __name__ == '__main__':
    main()