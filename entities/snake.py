import pygame as pg
import entities as ents

from enum import IntEnum
from itertools import chain

from grid import Grid as grid_Grid
from grid import EmbededGrid as grid_EmbededGrid
from grid import Builder as grid_Builder

from abc import ABC, abstractmethod

from collections import deque
from typing import Deque

import itertools

from typing import Iterator

class BodyPart(ents.BaseEntity, ABC):
    def __init__(self, row: int, clmn: int) -> None:
        super().__init__()
        self.row, self.clmn = row, clmn

    def get_pos(self) -> tuple[int, int]:
        return self.row, self.clmn
    
    @abstractmethod
    def set_pos(self, row_clmn: tuple[int, int]) -> tuple[int, int]:
        pass
    
class ColorBodyPart(BodyPart):
    def __init__(self, row: int, clmn: int, color: tuple[int, int, int]) -> None:
        super().__init__(row, clmn)
        self.color = color

    def update(self, t_elapsed: float) -> bool:
        pass
    
    def set_pos(self, row_clmn: tuple[int, int]) -> tuple[int, int]:
        old_pos = self.get_pos()
        self.row, self.clmn = row_clmn
        return old_pos
    
    def draw(self, surface: pg.Surface, grid: grid_Grid) -> None:
        grid.draw_colored_cells_to_screen(surface, [(self.row, self.clmn, self.color)])



class GOLBodyPart(BodyPart):
    count = 0
    
    def __init__(self, row: int, clmn: int, parent_grid: grid_Grid) -> None:
        super().__init__(row, clmn)
        
        self.ups = 6
        self.t_acc = 0
        self.bkd_clr = (0, 0, 0)


        alive_cells = [
            # Classic glider in a 12×12 grid (top‐left corner)
            (0, 1),
            (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]

        
        self.table_rows, self.table_clmns = 12, 12
        self.gol_table = ents.GOLTable(self.table_clmns, self.table_rows, True, (0, 255, 0), self.bkd_clr)


        self.gol_table.randomize_cells() if type(self).count is not 5 else self.gol_table.set_cells_to_alive(alive_cells)

        type(self).count += 1
        
        self.parent_grid = parent_grid
        self.e_grid = self.get_e_grid()

    def update(self, t_elapsed: float) -> bool:
        self.t_acc += t_elapsed
        t_slice = 1. / self.ups
        while self.t_acc > t_slice:
            self.gol_table.evolve()
            self.t_acc -= t_slice
    
    def set_pos(self, row_clmn: tuple[int, int]) -> tuple[int, int]:
        old_pos = self.get_pos()
        self.row, self.clmn = row_clmn
        self.e_grid.move_to(*(row_clmn))
        return old_pos
    
    def draw(self, surface: pg.Surface, grid: grid_Grid) -> None:
        self.e_grid.draw_bkgd_and_border(surface)
        self.gol_table.draw(self.e_grid, surface)

    def get_e_grid(self) -> grid_EmbededGrid:
        builder = grid_Builder()\
            .set_clmns_and_rows_count(self.table_clmns, self.table_rows)\
            .set_border_color_and_width((0, 255, 0), 1)\
            .set_bkgd_color(self.bkd_clr)\
            .set_cell_padding(1)\
            .set_color_cells_border_radius(0)\
            
        e_grid = grid_EmbededGrid(builder, self.parent_grid, self.row, self.clmn)
        
        return e_grid

class Snake(ents.BaseEntity):
    def __init__(self, head_r, head_c) -> None:
        super().__init__()
        self.body = [ ColorBodyPart(head_r, head_c, (0, 255, 0)) ]
        self.pending_body: Deque[BodyPart] = deque()
    
    @property
    def length(self): return len(self.body)
    
    def get_tail_tip(self) -> BodyPart: return self.body[-1]
    
    def get_head(self) -> BodyPart: return self.body[0]
    
    def get_tail(self) -> Iterator[BodyPart]: return itertools.islice(self.body, 1, len(self.body))
        
    def biting_tail(self) -> bool:
        head_pos = self.get_head().get_pos()
        for part in self.get_tail():
            if part.get_pos() == head_pos: return True
        
        return False
    
    def get_head(self) -> BodyPart:
        return self.body[0]
    
    def update(self, t_elapsed: float) -> bool:
        for part in chain(self.body, self.pending_body):
            part.update(t_elapsed)
        return True
        
    def draw(self, surface: pg.Surface, grid: grid_Grid) -> None:
        for part in self.body: part.draw(surface, grid)
    
    def add_parts(self, p: list[BodyPart]) -> 'Snake':
        self.pending_body.extend(p)
        return self
    
    def move(self, row: int, clmn: int) -> 'Snake':
        body = self.body
        
        next_pos = (row, clmn)

        for part in body:
            next_pos = part.set_pos(next_pos)
        
        if len(self.pending_body) != 0:
            pp = self.pending_body.popleft()
            pp.set_pos(next_pos)
            self.body.append(pp)
        
        return self
 
class SnakeDirection(IntEnum):
    UP = 0,
    LEFT = 1,
    DOWN = 2,
    RIGHT = 3 
            
class MovingSnake(Snake):
    _NC_DIRS = [ # non competable dirrections
        SnakeDirection.DOWN,
        SnakeDirection.RIGHT,
        SnakeDirection.UP,
        SnakeDirection.LEFT
    ]
    _OFFS = [
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1)
    ]
    
    def __init__(self, head_r, head_c) -> None:
        super().__init__(head_r, head_c)
        self.mps = 3
        self.t_acc = 0
        self.t_slice = 1. / self.mps

        self.dir = SnakeDirection.DOWN 

    def try_cnage_dir(self, nd: SnakeDirection) -> bool:
        if MovingSnake._NC_DIRS[nd] == self.dir: return False
        self.dir = nd
        return True

    def update(self, t_elapsed: float) -> bool:
        super().update(t_elapsed)
        self.t_acc += t_elapsed
        while self.t_acc > self.t_slice:
            oh, ow = MovingSnake._OFFS[self.dir]
            h, w = self.get_head().get_pos()
            self.move(h + oh, w + ow)

            self.t_acc -= self.t_slice
            
        return True

class FogSnake(MovingSnake):
    def __init__(self, head_r, head_c, view_radius: int) -> None:
        super().__init__(head_r, head_c)
        self.view_radius = view_radius
        
    def draw(self, surface: pg.Surface, grid: grid_Grid) -> None:
        hr, hc = self.get_head().get_pos()
        r_from, r_to = max(hr - self.view_radius, 0), min(hr + self.view_radius, grid.rows - 1)
        c_from, c_to = max(hc - self.view_radius, 0), min(hc + self.view_radius, grid.clmns - 1)
        
        self.get_head().draw(surface, grid)
        for p in self.get_tail():
            r, c = p.get_pos()
            if r < r_from or r > r_to\
                or c < c_from or c > c_to:
                continue
            p.draw(surface, grid)