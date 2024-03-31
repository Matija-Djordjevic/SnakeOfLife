'''
    Game logic: "https://en.wikipedia.org/wiki/Conway's_Game_of_Life"
'''
import numpy as np
from numpy import typing as npt
from numba import njit
from typing import Optional

import pygame as pg

from grid import Grid as grid_Grid

class GOLTable():
    ALIVE = True
    DEAD = False
    
    def __init__(self, clmns: int, rows: int, loop: bool, alive_color: tuple[int, int, int], dead_color: tuple[int, int, int]) -> None:
        self.loop = loop
        self.alive_c = alive_color
        self.dead_c = dead_color
        self.matrix = np.zeros(shape=(rows, clmns), dtype=np.bool_)
        self.t_matrix = self.matrix[:]
        
        self.generation_count = 1

    @property
    def generation(self): return self.generation_count

    def evolve(self) -> None: Advancer.evolve(self)

    def draw(self, grid: grid_Grid, surface: pg.Surface) -> None: Drawer.draw(self, grid, surface)

    @staticmethod
    def try_load_from_binary(f_path: str) -> Optional['GOLTable']: return Loader.try_load_from_binary(f_path)
 
    def try_save_to_binary(table: 'GOLTable', f_path: str) -> bool: return Loader.try_save_to_binary(table, f_path)

    def try_save_to_binary(self, f_path: str) -> bool: return Loader.try_save_to_binary(self, f_path)

    def randomize_cells(self) -> None: self.matrix = np.random.randint(0, 2, size=self.matrix.shape, dtype=np.bool_)

    def set_cells_to_alive(self, cells) -> None:
        for row, clmn in cells: self.matrix[row][clmn] = GOLTable.ALIVE
    
    def set_cells_to_dead(self, cells) -> None:
        for row, clmn in cells: self.matrix[row][clmn] = GOLTable.DEAD
    
    def flip_cells(self, cells) -> None:
        for row, clmn in cells: self.matrix[row][clmn] = not self.table[row][clmn]    

    def __str__(self) -> str:
        frame_char = '#'
        alive_char = chr(ord('█'))
        dead_char = ' '

        w = self.matrix.shape[1]
        s = ''.join([frame_char for _ in range(w + 2)])
        s += '\n'
        for row in self.matrix:
            s += frame_char
            for cell in row:
                s += alive_char if cell else dead_char
            s += frame_char
            s += '\n'
        s += ''.join([frame_char for _ in range(w + 2)])

        return s
    
class Advancer():
    OFFSETS = [
        [-1, -1],
        [-1, 0],
        [-1, 1],
        [0, -1],
        [0, 1],
        [1, -1],
        [1, 0],
        [1, 1]
    ]
    ALIVE = True
    DEAD = False

    @staticmethod
    def evolve(table: GOLTable) -> None:
        table.generation_count += 1
        Advancer.do_evolve(table)
        table.matrix, table.t_matrix = table.t_matrix, table.matrix

    @staticmethod
    def do_evolve(table: GOLTable) -> None:
        h, w = table.matrix.shape
        matrix, t_matrix = table.matrix, table.t_matrix
        
        # first row
        for clmn in range(w):
            nbs = Advancer.neighbours_count_parimeter(table, 0, clmn)
            t_matrix[0][clmn] = Advancer.next_cell_state(matrix[0][clmn], nbs)
        
        #last row
        for clmn in range(w):
            nbs = Advancer.neighbours_count_parimeter(table, h - 1, clmn)
            t_matrix[h - 1][clmn] = Advancer.next_cell_state(matrix[h - 1][clmn], nbs)

        #first clmn
        for row in range(h):
            nbs = Advancer.neighbours_count_parimeter(table, row, 0)
            t_matrix[row][0] = Advancer.next_cell_state(matrix[row][0], nbs)

        #last clmn
        for row in range(h):
            nbs = Advancer.neighbours_count_parimeter(table, row, w - 1)
            t_matrix[row][w - 1] = Advancer.next_cell_state(matrix[row][w - 1], nbs)
        
        # rest of the matrix
        # here we will waste most of the time!
        Advancer.advance_inner_matrix(table.matrix, t_matrix)

    @staticmethod
    def neighbours_count_parimeter(table: GOLTable, row: int, clmn: int):
        c = 0
        for row_off, clmn_off in Advancer.OFFSETS:
            nbr_row, nbr_clmn = row + row_off, clmn + clmn_off
            if table.loop:
                nbr_row, nbr_clmn = Advancer.adjust_for_looping(table, nbr_row, nbr_clmn)            
            if Advancer.are_invalid_coords(table, nbr_row, nbr_clmn):
                continue
            if table.matrix[nbr_row][nbr_clmn]:
                c += 1
        return c
    
    @staticmethod
    def adjust_for_looping(table: GOLTable, row: int, clmn: int) -> tuple[int, int]:
        h, w = table.matrix.shape
        if row == h: 
            row = 0
        if row == -1: 
            row = h - 1

        if clmn == w: 
            clmn = 0
        if clmn == -1: 
            clmn = w - 1
        
        return row, clmn
    
    @staticmethod
    @njit
    def advance_inner_matrix(matrix: npt.NDArray[np.bool_], tmp_matrix: npt.NDArray[np.bool_]) -> None:
        OFFSETS = [
            [-1, -1],
            [-1, 0],
            [-1, 1],
            [0, -1],
            [0, 1],
            [1, -1],
            [1, 0],
            [1, 1]
        ]
        ALIVE = True
        DEAD = False
        
        h, w = matrix.shape
        for row in range(1, h - 1):
            for clmn in range(1, w - 1):
                nbr_c = 0
                for row_off, clmn_off in OFFSETS:
                    nbr_row, nbr_clmn = row + row_off, clmn + clmn_off
                    if matrix[nbr_row][nbr_clmn]:
                        nbr_c += 1

                is_alive = matrix[row][clmn]
                if is_alive and (nbr_c < 2 or nbr_c > 3):
                    is_alive = DEAD
                if not is_alive and nbr_c == 3:
                    is_alive = ALIVE
                
                tmp_matrix[row][clmn] = is_alive
    
    @staticmethod
    def next_cell_state(is_alive: bool, alive_nbs: int) -> bool:
        '''
            Rules: "https://en.wikipedia.org/wiki/Conway's_Game_of_Life#Rules"
        '''
        if is_alive and (alive_nbs < 2 or alive_nbs > 3):
            return Advancer.DEAD
        if not is_alive and alive_nbs == 3:
            return Advancer.ALIVE
        
        return is_alive
    
    @staticmethod
    def are_invalid_coords(table: GOLTable, row: int, clmn: int) -> bool:
        h, w = table.matrix.shape
        return row < 0 or row >= h or clmn < 0 or clmn >= w

class Loader():
    @staticmethod
    def try_load_from_binary(f_path: str) -> GOLTable | None:
        try:
            with open(f_path, 'rb') as f:
                c = int.from_bytes(f.read(4))
                r = int.from_bytes(f.read(4))
                l = bool.from_bytes(f.read(1))

                # TODO fix, extra memory allocated for creating new matrix 
                matrix = np.empty(shape=(r, c), dtype=np.bool_)
                for row in range(r):
                    matrix[row] = np.array([bool.from_bytes(f.read(1)) for _ in range(c)])
                    
                tbl = GOLTable(c, r, l)
                tbl.matrix = matrix
                
                return  tbl
            
        except Exception as e:
            print(e)
            return None
        
    @staticmethod
    def try_save_to_binary(table: GOLTable, f_path: str) -> bool:
        try:
            with open(f_path, 'wb') as f:
                f.write(table.clmns.to_bytes(4))
                f.write(table.rows.to_bytes(4))
                f.write(table.loop.to_bytes(1))
                
                for row in table.matrix: 
                    f.write(bytearray([cell for cell in row]))
                
                return True
        finally:
            return False

# beutify!
class Drawer():
    @staticmethod
    def draw(table: GOLTable, grid: grid_Grid, surface: pg.Surface) -> None:
        mtrx = table.matrix
        h, w = mtrx.shape
        
        rows_clmns_colors = (
            (row, clmn, table.alive_c if mtrx[row][clmn] else table.dead_c) for row in range(h) for clmn in range(w)
        )
        
        grid.draw_colored_cells_to_screen(surface, rows_clmns_colors)