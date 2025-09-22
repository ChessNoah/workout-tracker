import sys
import random

import pygame


CELL_SIZE = 24
GRID_WIDTH = 25
GRID_HEIGHT = 25
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

BACKGROUND_COLOR = (18, 18, 18)
GRID_COLOR = (30, 30, 30)
SNAKE_COLOR = (0, 200, 120)
SNAKE_HEAD_COLOR = (0, 240, 160)
FOOD_COLOR = (220, 70, 90)
TEXT_COLOR = (230, 230, 230)

INITIAL_FPS = 10
MAX_FPS = 20


def draw_grid(surface: pygame.Surface) -> None:
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))


def random_empty_cell(snake: list[tuple[int, int]]) -> tuple[int, int]:
    occupied = set(snake)
    while True:
        cell = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if cell not in occupied:
            return cell


def draw_snake(surface: pygame.Surface, snake: list[tuple[int, int]]) -> None:
    for index, (x, y) in enumerate(snake):
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        color = SNAKE_HEAD_COLOR if index == 0 else SNAKE_COLOR
        pygame.draw.rect(surface, color, rect, border_radius=4)


def draw_food(surface: pygame.Surface, food: tuple[int, int]) -> None:
    x, y = food
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, FOOD_COLOR, rect, border_radius=6)


def draw_text(surface: pygame.Surface, text: str, size: int, center: tuple[int, int]) -> None:
    font = pygame.font.SysFont("consolas", size)
    label = font.render(text, True, TEXT_COLOR)
    rect = label.get_rect(center=center)
    surface.blit(label, rect)


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Snake")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    def reset_game() -> tuple[list[tuple[int, int]], tuple[int, int], tuple[int, int], int, int, bool]:
        start = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        snake = [start, (start[0] - 1, start[1]), (start[0] - 2, start[1])]
        direction = (1, 0)
        next_direction = direction
        food = random_empty_cell(snake)
        score = 0
        fps = INITIAL_FPS
        game_over = False
        return snake, food, next_direction, score, fps, game_over

    snake, food, next_direction, score, fps, game_over = reset_game()
    direction = next_direction

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE,):
                    pygame.quit()
                    sys.exit(0)
                if game_over and event.key == pygame.K_r:
                    snake, food, next_direction, score, fps, game_over = reset_game()
                    direction = next_direction
                    continue
                if event.key in (pygame.K_UP, pygame.K_w):
                    if direction != (0, 1):
                        next_direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if direction != (0, -1):
                        next_direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if direction != (1, 0):
                        next_direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if direction != (-1, 0):
                        next_direction = (1, 0)

        if not game_over:
            direction = next_direction
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            if (
                new_head[0] < 0
                or new_head[0] >= GRID_WIDTH
                or new_head[1] < 0
                or new_head[1] >= GRID_HEIGHT
                or new_head in snake
            ):
                game_over = True
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_empty_cell(snake)
                    fps = min(MAX_FPS, INITIAL_FPS + score // 2)
                else:
                    snake.pop()

        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen)
        draw_snake(screen, snake)
        draw_food(screen, food)
        draw_text(screen, f"Score: {score}", 22, (90, 18))

        if game_over:
            draw_text(screen, "Game Over", 42, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            draw_text(screen, "Trykk R for å starte på nytt", 22, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    main()


