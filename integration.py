import matplotlib.pyplot as plt
import timeit
import numpy as np
import quadtree as qt

#--------------------------------define entities (particles)--------------------------------
class Particle:
    def __init__(self, mass, x, y, vx, vy):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    # def draw_particle(self, ax, c = 'k', s = 4):
    #     ax.scatter(self.x, self.y, c = c, s = s)

    def show_particle_properties(self):
        print('Particle properties (mass, x_pos, y_pos, vx, vy): ')
        print('\t', Particle.mass, Particle.x, Particle.y, Particle.vx, Particle.vy)

#------------------------------generate particles-------------------------------
def create_particles(num_particles, xsize, ysize, seed) :
    particles = []
    ii = 0

    np.random.seed(seed)

    while ii < num_particles:
        mass = np.random.uniform(0.1, 10.0)
        x = np.random.uniform(0, xsize)
        y = np.random.uniform(0, ysize)
        vx, vy = np.random.uniform(0.0, 100.0, size = 2)
        particles.append(Particle(mass, x, y, vx, vy))

        ii += 1
    return particles

#------------------------------will create the tree-----------------------------

def build_quadtree(particles, x_size, y_size):
    root = qt.Rectangle(qt.Point(0,0), xsize, ysize)
    
    QuadTree = qt.TreeNode(root)
    for particle in particles:
        QuadTree.insert(particle)

    print(f'{len(QuadTree)}/{len(particles)} particles were inserted!')
    return QuadTree

#---------------------------------main method----------------------------------

if __name__ == '__main__':
    xsize, ysize = 800, 80
    NumOfParticles = 2000

    t0_particle = timeit.default_timer()#timeit
    seed = int(1000*np.random.uniform())
    #seed = 498
    #note that with this seed definition we are able to expand or reduce the number of particles holding some positions 
    particles = create_particles(NumOfParticles, xsize, ysize, seed)
    elapsed_particles = timeit.default_timer() - t0_particle#timeit

    t0_tree_build = timeit.default_timer()#timeit
    tree = build_quadtree(particles, xsize, ysize)
    elapsed_build_tree = timeit.default_timer() - t0_tree_build#timeit

    print(f'This sample was generated with seed = {seed}')

    #PLOT

    t0_plotting = timeit.default_timer()#timeit
    DPI = 72
    fig = plt.figure(figsize = (700/DPI, 500/DPI), dpi = DPI)
    
    ax = plt.subplot()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(xsize)
    ax.set_ylim(ysize)
    ax.set_facecolor('#030821')

    #draw QuadTree
    tree.draw(ax, c = 'w')

    #draw particles
    ax.scatter([particle.x for particle in particles],[particle.y for particle in particles], s=4, c = 'w')
    ax.invert_yaxis()
    ax.invert_xaxis()

    plt.tight_layout()
    plt.savefig('figures/QuadTree_visualization.png', dpi = DPI)

    elapsed_plotting = timeit.default_timer() - t0_plotting#timeit

    total_elapsed = timeit.default_timer() - t0_particle#timeit

    print(f'\nReport:\n\ttime elapsed generating particles: {elapsed_particles:.4f}s ({100*elapsed_particles/total_elapsed:.3f}% of the total)')
    print(f'\ttime elapsed building the tree: {elapsed_build_tree:.4f}s ({100*elapsed_build_tree/total_elapsed:.3f}% of the total)')
    print(f'\ttime elapsed plotting: {elapsed_plotting:.4f}s ({100*elapsed_plotting/total_elapsed:.3f}% of the total)')
    print(f'\ttotal elapsed time: {total_elapsed:.4f}s')

    plt.show()