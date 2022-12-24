#!/usr/bin/env python3
import sys
import pygame as pg
from pygame.locals import *
import time

PIXEL_SIZE = 10
ROCK_COLOR = (255,0,0)
GRAIN_COLOR = (255,255,255)
GAIN_SPAWN = (0, 500)

scene = None
surf = None
sand_grains = []

is_part2 = True
is_paused = False

def empty_board(n_rows, n_cols):
    return [['.'] * n_cols for i in range(n_rows)]

def init():
    pg.init()
    pg.display.set_caption('Day14')
    surf = pg.display.set_mode((scene.n_cols * PIXEL_SIZE, scene.n_rows * PIXEL_SIZE))
    return surf

class GameScene:
    def __init__(self, board, j_offset) -> None:
        self.board = board
        self.n_rows = len(board)
        self.n_cols = len(board[0])

        self.j_offset = j_offset

    def expand(self, is_left):
        print(f"Expanding board {'left' if is_left else 'right'}")
        new_board = empty_board(self.n_rows, self.n_cols + 1)

        for i in range(self.n_rows):
            for j in range(self.n_cols):
                j_new = j + 1 if is_left else j
                new_board[i][j_new] = self.board[i][j]
        
        if is_left:
            self.j_offset -= 1
            for grain in sand_grains:
                grain.j += 1

        self.board = new_board
        self.n_cols += 1

        for j in range(self.n_cols):
            self.board[self.n_rows - 1][j] = '#'

        init()

def make_game_scene(input_file):
    with open(input_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

        coords = list(map(lambda x: [[int(i) for i in cord.strip().split(',')] for cord in x.split('->')], lines))

        min_j = min(map(lambda line: min([ij[0] for ij in line]), coords))
        max_j = max(map(lambda line: max([ij[0] for ij in line]), coords))

        max_i = max(map(lambda line: max([ij[1] for ij in line]), coords))

        if is_part2:
            max_i += 2

        print(f"min_j: {min_j} max_j: {max_j}")

        n_rows = max_i + 1
        n_cols = max_j - min_j + 1

        print(f"n_rows: {n_rows} n_cols: {n_cols}")
        game_scene = empty_board(n_rows, n_cols)
        for line in coords:
            cord_prev = line[0]
            for cord_next in line[1:]:
                print(f"prev: {cord_prev} next: {cord_next}")
                
                j0, i0 = cord_prev
                j1, i1 = cord_next

                j0 -= min_j
                j1 -= min_j

                if i0 == i1:
                    cord_gen = map(lambda j: (i0, j), range(min(j0, j1), max(j0, j1) + 1))
                else:
                    cord_gen = map(lambda i: (i, j0), range(min(i0, i1), max(i0, i1) + 1))

                for i, j in cord_gen:
                    game_scene[i][j] = '#'

                cord_prev = cord_next
        
        if is_part2:
            for j in range(n_cols):
                game_scene[n_rows - 1][j] = '#'

        for i,row in enumerate(game_scene):
            print("%2i %s" % (i, ''.join(row)))

        return GameScene(game_scene, min_j)

def draw_board():
    surf.fill((0,0,0))
    for i, row in enumerate(scene.board):
        for j, cell in enumerate(row):
            x0 = j * PIXEL_SIZE
            y0 = i * PIXEL_SIZE
            if cell == '#':
                pg.draw.rect(surf, ROCK_COLOR, pg.Rect(x0, y0, PIXEL_SIZE, PIXEL_SIZE))
            if cell == 'x':
                pg.draw.rect(surf, GRAIN_COLOR, pg.Rect(x0, y0, PIXEL_SIZE, PIXEL_SIZE))
    pg.display.update()


class SandGrain:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.stuck = False

    def is_stuck(self):
        return self.stuck

    def move(self):
        scene.board[self.i][self.j] = '.'
        self.stuck = True
        
        if self.i + 1 < scene.n_rows and scene.board[self.i + 1][self.j] == '.':
            self.i += 1
            self.stuck = False
        elif self.i + 1 < scene.n_rows and self.j - 1 >= 0 and scene.board[self.i + 1][self.j - 1] == '.':
            self.i += 1
            self.j -= 1
            self.stuck = False
        elif self.i + 1 < scene.n_rows and self.j + 1 < scene.n_cols and scene.board[self.i + 1][self.j + 1] == '.':
            self.i += 1
            self.j += 1
            self.stuck = False

        if self.j == 0 or self.j == scene.n_cols - 1 or self.i == scene.n_rows - 1:
            return False
        else:
            scene.board[self.i][self.j] = 'x'
            return True

def grain_gen():
    return SandGrain(GAIN_SPAWN[0], GAIN_SPAWN[1] - scene.j_offset)

def main():
    global is_paused
    while True: # main game loop
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    is_paused = not is_paused

        if not is_part2 or len(sand_grains) == 0 or sand_grains[-1].is_stuck():
            draw_board()

        if is_paused:
            continue

        if len(sand_grains) == 0 or (sand_grains[-1].is_stuck() and sand_grains[-1].i != 0):
            sand_grains.append(grain_gen())
            print(f"Grains: {len(sand_grains) - 1}")

        last_grain = sand_grains[-1]
        if not last_grain.move():
            
            if is_part2:
                if last_grain.j <= 0:
                    scene.expand(True)
                elif last_grain.j >= scene.n_cols - 1:
                    scene.expand(False)
            else:
                sand_grains.pop()

        if is_part2 and sand_grains[-1].i == 0:
            print(f"Grains: {len(sand_grains)}")
            is_paused = True

        #time.sleep(0.01)

if __name__ == "__main__":
    scene = make_game_scene(sys.argv[1])
    
    surf = init()
    main()
