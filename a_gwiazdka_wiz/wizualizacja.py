import pygame
import numpy as np

# Import functions from the original script
from sciezka_terminal import wczytaj_grid, a_gwiazdka

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_FILE = 'pliki/grid.txt'

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)


class PathVisualization:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('A* Path Finding Visualization')
        self.clock = pygame.time.Clock()

        # Load grid
        self.grid = wczytaj_grid(GRID_FILE)

        # Grid parameters
        self.rows, self.cols = self.grid.shape
        self.cell_width = SCREEN_WIDTH // self.cols
        self.cell_height = SCREEN_HEIGHT // self.rows

        # Path finding parameters
        self.start = (19, 0)
        self.goal = (0, 19)

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    col * self.cell_width,
                    row * self.cell_height,
                    self.cell_width,
                    self.cell_height
                )

                if self.grid[row, col] == 5:  # Obstacle
                    pygame.draw.rect(self.screen, BLACK, rect)
                elif self.grid[row, col] == 0:  # Free space
                    pygame.draw.rect(self.screen, WHITE, rect)
                elif self.grid[row, col] == 1:  # Path
                    pygame.draw.rect(self.screen, GREEN, rect)

                pygame.draw.rect(self.screen, GRAY, rect, 1)

    def find_and_draw_path(self):
        # Create a copy of the grid for path finding
        grid_path = np.copy(self.grid)

        # Find the path
        path = a_gwiazdka(grid_path, self.start, self.goal)

        self.path_coordinates = []  # Store path coordinates

        if path:
            # Draw start and goal
            start_rect = pygame.Rect(
                self.start[1] * self.cell_width,
                self.start[0] * self.cell_height,
                self.cell_width,
                self.cell_height
            )
            goal_rect = pygame.Rect(
                self.goal[1] * self.cell_width,
                self.goal[0] * self.cell_height,
                self.cell_width,
                self.cell_height
            )
            pygame.draw.rect(self.screen, GREEN, start_rect)
            pygame.draw.rect(self.screen, RED, goal_rect)

            # Draw path
            for x, y in path:
                path_rect = pygame.Rect(
                    y * self.cell_width,
                    x * self.cell_height,
                    self.cell_width,
                    self.cell_height
                )
                pygame.draw.rect(self.screen, GREEN, path_rect)

                # Store path coordinates
                self.path_coordinates.append((y, x))

                # Update the display
                pygame.display.flip()
                self.clock.tick(30)

                # Pause for a short duration between steps
                pygame.time.delay(80)

                # Clear the path rect
                pygame.draw.rect(self.screen, GREEN, path_rect)

    def run(self):
        running = True
        path_completed = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(WHITE)
            self.draw_grid()

            # Only find and draw path if it hasn't been completed before
            if not path_completed:
                self.find_and_draw_path()
                path_completed = True

            # Draw saved path coordinates
            for y, x in self.path_coordinates:
                path_rect = pygame.Rect(
                    y * self.cell_width,
                    x * self.cell_height,
                    self.cell_width,
                    self.cell_height
                )
                pygame.draw.rect(self.screen, GREEN, path_rect)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    visualization = PathVisualization()
    visualization.run()
