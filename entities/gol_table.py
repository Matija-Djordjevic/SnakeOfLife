'''
    Game logic: "https://en.wikipedia.org/wiki/Conway's_Game_of_Life"
'''
import pygame as pg
from typing import Optional
import numpy as np
import numpy.typing as npt

from numba import njit

from grid import Grid

class GOLTable():
    ALIVE = True
    DEAD = False
    
    def __init__(self, clmns: int, rows: int, loop: bool = False) -> None:
        self.rows = rows
        self.clmns = clmns
        self.loop = loop
        self.table = np.zeros(shape=(self.rows, self.clmns), dtype=np.bool_)
        self.tmp_table = self.table[:]
        
        self.generation_count = 1
    
    @property
    def generation(self): return self.generation_count
    
    def advance_generation(self) -> None: _GOLTableAdvancer.get_next_generation(self)
    
    def new_generation_differs(self) -> Optional[bool]: return None if self.advance_generation == 1 else (self.table != self.tmp_table).any()
    
    def draw_table_to_screen(self, grid: Grid, surface: pg.Surface, alive_color: tuple[int, int, int], dead_color: tuple[int, int, int]) -> None: _GOLTableDrawer.draw_table_to_screen(self, grid, surface, alive_color, dead_color)
    
    @staticmethod
    def try_load_from_binary(f_path: str) -> Optional['GOLTable']: return _GOLTableLoader.try_load_from_binary(f_path)
    
    def try_save_to_binary(self, f_path: str) -> bool: return _GOLTableLoader.try_save_to_binary(self, f_path) 
    
    def randomize_cells(self) -> None: self.table = np.random.randint(0, 2, size=(self.rows, self.clmns), dtype=np.bool_)

    def set_cells_to_alive(self, cells) -> None:
        for row, clmn in cells: self.table[row][clmn] = GOLTable.ALIVE
    
    def set_cells_to_dead(self, cells) -> None:
        for row, clmn in cells: self.table[row][clmn] = GOLTable.DEAD
    
    def flip_cells(self, cells) -> None:
        for row, clmn in cells: self.table[row][clmn] = not self.table[row][clmn]
    
    def __str__(self) -> str:
        frame_char = '#'
        alive_char = chr(ord('█'))
        dead_char = ' '

        s = ''.join([frame_char for _ in range(self.clmns + 2)])
        s += '\n'
        for row in self.table:
            s += frame_char
            for cell in row:
                s += alive_char if cell else dead_char
            s += frame_char
            s += '\n'
        s += ''.join([frame_char for _ in range(self.clmns + 2)])
        
        return s

class _GOLTableAdvancer():
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

    @staticmethod
    def get_next_generation(table: GOLTable) -> None:
        table.generation_count += 1
        _GOLTableAdvancer.advance_frame(table, 0, table.rows, 0, table.clmns)
        table.table, table.tmp_table = table.tmp_table, table.table
        
    @staticmethod
    def advance_frame(table: GOLTable, start_row: int, end_row: int, start_clmn: int, end_clmn: int) -> None:
        '''
            [start_row, end_row)
            [start_clmn, end_clmn)
        '''
        if _GOLTableAdvancer.are_invalid_coords(table, start_row, start_clmn) or _GOLTableAdvancer.are_invalid_coords(table, end_row - 1, end_clmn - 1):
            raise ValueError(f"Invalid coordinates") # Log this better 
   
        for clmn in range(table.clmns):
            alive_neighbours = _GOLTableAdvancer.alive_neighbours_on_parimeter_count(table, 0, clmn)
            table.tmp_table[0][clmn] = _GOLTableAdvancer.next_cell_state(table.table[0][clmn], alive_neighbours)
        
        for clmn in range(table.clmns):
            alive_neighbours = _GOLTableAdvancer.alive_neighbours_on_parimeter_count(table, table.rows - 1, clmn)
            table.tmp_table[table.rows - 1][clmn] = _GOLTableAdvancer.next_cell_state(table.table[table.rows - 1][clmn], alive_neighbours)

        for row in range(table.rows):
            alive_neighbours = _GOLTableAdvancer.alive_neighbours_on_parimeter_count(table, row, 0)
            table.tmp_table[row][0] = _GOLTableAdvancer.next_cell_state(table.table[row][0], alive_neighbours)

        for row in range(table.rows):
            alive_neighbours = _GOLTableAdvancer.alive_neighbours_on_parimeter_count(table, row, table.clmns - 1)
            table.tmp_table[row][table.clmns - 1] = _GOLTableAdvancer.next_cell_state(table.table[row][table.clmns - 1], alive_neighbours)
        
        _GOLTableAdvancer.advance_inner_table(table.table, table.tmp_table)
        
    # TODO rename        
    @staticmethod
    @njit
    def advance_inner_table(table: npt.NDArray[np.bool_], tmp_table: npt.NDArray[np.bool_]):
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
        
        for row in range(1, len(table) - 1):
            for clmn in range(1, len(table[0]) - 1):
                alive_neighbours = 0
                for row_off, clmn_off in OFFSETS:
                    nabr_row, nabr_clmn = row + row_off, clmn + clmn_off
                    if table[nabr_row][nabr_clmn]:
                        alive_neighbours += 1
                
                next_cell_state = table[row][clmn]
                
                if table[row][clmn] and (alive_neighbours < 2 or alive_neighbours > 3):
                    next_cell_state = DEAD
                if not table[row][clmn] and alive_neighbours == 3:
                    next_cell_state = ALIVE
                
                tmp_table[row][clmn] = next_cell_state          

    @staticmethod
    def are_invalid_coords(table: GOLTable, row: int, clmn: int) -> bool: return row < 0 or row >= table.rows or clmn < 0 or clmn >= table.clmns 
    
    @staticmethod
    def alive_neighbours_on_parimeter_count(table: GOLTable, row: int, clmn: int) -> int:
        count = 0
        for row_off, clmn_off in _GOLTableAdvancer.OFFSETS:
            nabr_row, nabr_clmn = row + row_off, clmn + clmn_off
            if table.loop:
                nabr_row, nabr_clmn = _GOLTableAdvancer.adjut_coords_for_looping(table, nabr_row, nabr_clmn)            
            if _GOLTableAdvancer.are_invalid_coords(table, nabr_row, nabr_clmn):
                continue
            if table.table[nabr_row][nabr_clmn]: # is alive
                count += 1
                
        return count
    
    @staticmethod
    def adjut_coords_for_looping(table: GOLTable, row: int, clmn: int) -> tuple[int, int]:
        if row == table.rows:
            row = 0
        if row == -1:
            row = table.rows - 1
            
        if clmn == table.clmns:
            clmn = 0
        if clmn == -1:
            clmn = table.clmns - 1
        
        return row, clmn
    
    @staticmethod
    def alive_neighbours_count(table: GOLTable, row: int, clmn: int) -> int:
        count = 0
        for row_off, clmn_off in _GOLTableAdvancer.OFFSETS:
            nabr_row, nabr_clmn = row + row_off, clmn + clmn_off
            if table.table[nabr_row][nabr_clmn]:
                count += 1

        return count

    @staticmethod
    def next_cell_state(cell_is_alive: bool, alive_neighbours: int) -> bool: 
        '''
            Rules: "https://en.wikipedia.org/wiki/Conway's_Game_of_Life#Rules"
        '''
        if cell_is_alive and (alive_neighbours < 2 or alive_neighbours > 3):
            return GOLTable.DEAD
        if not cell_is_alive and alive_neighbours == 3:
            return GOLTable.ALIVE
        
        return cell_is_alive

class _GOLTableLoader():
    @staticmethod
    def try_load_from_binary(f_path: str) -> GOLTable | None:
        try:
            with open(f_path, 'rb') as f:
                clmns = int.from_bytes(f.read(4))
                rows = int.from_bytes(f.read(4))
                loop = bool.from_bytes(f.read(1))

                gol_table = GOLTable(rows=rows, clmns=clmns, loop=loop)

                table = np.empty(shape=(rows, clmns), dtype=np.bool_)
                
                for row in range(rows): # TODO do this directly
                    table[row] = np.array([bool.from_bytes(f.read(1)) for _ in range(clmns)])
                gol_table.table = table
                
                return gol_table
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
                
                for row in table.table: 
                    f.write(bytearray([cell for cell in row]))
                
                return True
        finally:
            return False
            
class _GOLTableDrawer():
    
    @staticmethod
    def draw_table_to_screen(table: GOLTable, grid: Grid, surface: pg.Surface, alive_color: tuple[int, int, int], dead_color: tuple[int, int, int]) -> None:
        rows_clmns_colors = ((row, clmn, alive_color if table.table[row][clmn] else dead_color) for clmn in range(table.clmns) for row in range(table.rows))
        grid.draw_cells_to_screen(surface, rows_clmns_colors)
        
    @staticmethod
    def table_and_grid_dont_match(table: GOLTable, grid: Grid) -> bool: return table.rows, table.clmns == grid.rows, grid.clmns
