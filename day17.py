#!/usr/bin/env python3

global debug


class Rock:
    def __init__(self, i, j, blocks):
        self.i = i
        self.j = j
        self.blocks = blocks
        self.width = max([j for i,j in self.blocks]) + 1
        self.height = max([i for i,j in self.blocks]) + 1
        self.is_moving = True

    def block_positions(self):
        return [(self.i + i, self.j + j) for i,j in self.blocks]

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.i}, {self.j})"
    
    def draw(self, board):
        for i,j in self.blocks:
            board[self.i + i][self.j + j] = '@' if self.is_moving else '#'

    def is_collision(self, board):
        for i,j in self.block_positions():
            if i < 0 or board[i][j] != '.':
                return True
        return False

    def right(self, board):
        if self.j + self.width < 7:
            self.j += 1
            if self.is_collision(board):
                self.j -= 1
        return False
        
    def left(self, board):
        if self.j > 0:
            self.j -= 1
            if self.is_collision(board):
                self.j += 1
        return False

    def down(self, board):
        self.i -= 1
        if self.is_collision(board):
            self.i += 1
            return True
        else:
            return False

class HBar(Rock):
    def __init__(self, i, j):
        super().__init__(i, j, blocks = ((0,0), (0,1), (0,2), (0,3)))

class Cross(Rock):
    def __init__(self, i, j):
        super().__init__(i, j, blocks = ((0,1), (1,0), (1,1), (1,2), (2,1)))

class MirrorL(Rock):
    def __init__(self, i, j):
        super().__init__(i, j, blocks = ((2,2), (1,2), (0,0), (0,1), (0,2)))

class VBar(Rock):
    def __init__(self, i, j):
        super().__init__(i, j, blocks = ((0,0), (1,0), (2,0), (3,0)))

class Block(Rock):
    def __init__(self, i, j):
        super().__init__(i, j, blocks = ((0,0), (0,1), (1,0), (1,1)))

class ListLooper:
    def __init__(self, l):
        self.l = l
        self.last_returned_i = 0

    def __iter__(self):
        while True:
            yield self.l[self.last_returned_i]
            self.last_returned_i += 1
            if self.last_returned_i == len(self.l):
                self.last_returned_i = 0

class Scene:
    def __init__(self, moves, width=7):
        self.width = width
        self.rocks = []
        self.jets_state = ListLooper([*moves])
        self.jets = iter(self.jets_state)

        self.rockgen_state = ListLooper((HBar, Cross, MirrorL, VBar, Block))
        self.rockgen = iter(self.rockgen_state)


    def build_floor(self):
        floor = [-1 for _ in range(self.width)]
        for rock in self.rocks:
            for i,j in rock.block_positions():
                floor[j] = max(floor[j], i)
        return floor

    def build_board(self, floor_append =[]):
        floor = self.build_floor()
        for rock in floor_append:
            for i,j in rock.block_positions():
                floor[j] = max(floor[j], i)

        board = [['.' for _ in range(self.width)] for _ in range(max(floor) + 1,)]

        for rock in self.rocks:
            rock.draw(board)

        return board

    def max_row(self):
        return max(self.build_floor())

    def new_rock(self):
        rock = next(self.rockgen)(self.max_row() + 4, 2)

        board = self.build_board(floor_append=[rock])
        self.rocks.append(rock)

        move_i = 0
        if debug: print(self)
        while True:
            if move_i % 2 == 0:
                m = next(self.jets)
            else:
                m = 'd'

            if m == '>':
                collision = rock.right(board)
            elif m == '<':
                collision = rock.left(board)
            elif m == 'd':
                collision = rock.down(board)
            else:
                raise Exception(f"bad move: {m}")
            
            if collision:
                rock.is_moving = False
                break

            if debug: print(f"move {move_i} {m}: {rock}")
            if debug: print(self)
            move_i += 1
        

    def __repr__(self) -> str:
        board = self.build_board()
        return "\n".join(["|"+"".join(row)+"|" for row in reversed(board)])


if __name__ == "__main__":
    global debug
    debug = False

    if False:
        file_name = "day17_test.txt"  
    else:
        file_name = "day17.txt"

    with open(file_name) as f:
        moves = f.read().strip()   

    loop_detector = []
    rocks_counts = []
    heights = []

    scene = Scene(moves)
    is_part1 = False
    if is_part1:
        rock_stop = 2022
    else:
        rock_stop = 1000000000000
    rock_i = 0
    skipped_height = 0

    while rock_i < rock_stop:
        if scene.rockgen_state.last_returned_i == 0 and skipped_height == 0:
            #print(f"{rock_i} {scene.rockgen_state.last_returned_i} {scene.jets_state.last_returned_i} {scene.max_row()}")
            loop_detector.append(scene.jets_state.last_returned_i)
            rocks_counts.append(rock_i)
            heights.append(scene.max_row())

            for i in range(len(loop_detector) // 2):
                sub_loop = loop_detector[i:]
                #print("\t", i,  sub_loop, rocks_counts[i:], heights[i:])
                n_sub_loop = len(sub_loop)
            
                if not n_sub_loop % 2 == 0:
                    continue
                loop_size = n_sub_loop // 2

                if len([x for x, y in zip(sub_loop[:loop_size], sub_loop[loop_size:]) if x == y]) == loop_size:
                    end_i = i + loop_size 
                    rocks_left = rock_stop - rock_i

                    rocks_per_skip = rocks_counts[end_i] - rocks_counts[i]

                    possible_skips = rocks_left // rocks_per_skip
                    height_per_skip = heights[end_i] - heights[i]
                    skipped_height = height_per_skip * possible_skips
                    rock_next = rock_i + (rocks_per_skip * possible_skips)
                    print(f"loop {rock_i} {rock_next}", 
                        sub_loop[loop_size:], 
                        "n_rocks", rocks_per_skip,
                        "heights", height_per_skip,
                        "skips", possible_skips,
                        "rocks_left", rocks_left,
                        "skipped_height", skipped_height)
                    rock_i = rock_next
                    break
            
        scene.new_rock()
        rock_i += 1

    print("Done:")
    #print(scene)

    floor = scene.build_floor()

    print(floor)
    print(max(floor) + 1, max(floor) + 1 + skipped_height)
