import sys
from levels.base_level import BaseLevel
import pygame as pg

import numpy as np 

from grid import Grid as gird_Grid
from grid import Builder as grid_Builder

from entities import GOLBodyPart as entities_GOLBodyPart
from entities import ColorBodyPart as entities_ColorBodyPart
from entities import MovingSnake as entities_MovingSnake
from entities import FogSnake as entities_FogSnake
from entities import SnakeDirection as entities_SnakeDirection
from entities import GOLTable as entities_GOLTable

class SnakeOfLifeDemoLevel(BaseLevel):
    def __init__(self, rows: int, clmns: int, req_width: int, req_height: int) -> None:
        super().__init__()
        self.warmup()
        self.req_width, self.req_height = req_width, req_height
        self.rows, self.clmns = rows, clmns
        
        self.grid = self.init_grid()
        
        self.surface = pg.display.set_mode(self.grid.get_actual_grid_size())
        
        self.snake = entities_FogSnake(0, 0, 1)\
            .add_parts([
                entities_GOLBodyPart(0, 1, self.grid),
                entities_GOLBodyPart(0, 2, self.grid),
                entities_GOLBodyPart(0, 3, self.grid),
                entities_ColorBodyPart(0, 4, (1, 123, 232)),
                entities_ColorBodyPart(0, 4, (1, 123, 232)),
                entities_ColorBodyPart(0, 4, (1, 123, 232)),
                entities_ColorBodyPart(0, 4, (1, 123, 232)),
                entities_ColorBodyPart(0, 4, (1, 123, 232)),
                entities_GOLBodyPart(0, 5, self.grid),
                entities_GOLBodyPart(0, 6, self.grid),
                entities_GOLBodyPart(0, 6, self.grid),
                entities_GOLBodyPart(0, 6, self.grid),
                entities_GOLBodyPart(0, 6, self.grid),
                entities_GOLBodyPart(0, 6, self.grid),
                entities_GOLBodyPart(0, 6, self.grid),
                entities_GOLBodyPart(0, 6, self.grid),
                entities_GOLBodyPart(0, 6, self.grid),
                entities_GOLBodyPart(0, 6, self.grid),
                entities_GOLBodyPart(0, 6, self.grid)
            ])
        self.ups = 10
        self.t_acc = 0
        
        self.food = None
    
    def warmup(self):
        entities_GOLTable(10, 10, False, (0, 0, 0), (0, 0, 0)).evolve()
    
    def init_grid(self) -> gird_Grid:
        builder = grid_Builder()\
            .set_clmns_and_rows_count(self.clmns, self.rows)\
            .set_available_width_and_height(self.req_width, self.req_height)\
            .set_draw_offsets(0, 0)\
            .set_border_color_and_width((139,0,0), 10)\
            .set_bkgd_color((0, 0, 0))\
            .set_cell_padding(2)\
            .set_color_cells_border_radius(4)\
            .keep_same_cell_width_and_height()\
            .force_consistent_cell_padding()

        return gird_Grid(builder)
        
    def handle_events(self, events: list[pg.event.Event]) -> None:
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_s: self.snake.try_cnage_dir(entities_SnakeDirection.DOWN)
                    case pg.K_d: self.snake.try_cnage_dir(entities_SnakeDirection.RIGHT)
                    case pg.K_w: self.snake.try_cnage_dir(entities_SnakeDirection.UP)
                    case pg.K_a: self.snake.try_cnage_dir(entities_SnakeDirection.LEFT)
        
    def update(self, t_elapsed: float, events: list[pg.event.Event]) -> bool:
        snake = self.snake
        self.handle_events(events)
        snake.update(t_elapsed)
        self.adj_snake()        
        
        if self.food is None:
            r, c = self.grid.rows, self.grid.clmns
            pos = np.random.randint(r), np.random.randint(c)
            
        
        if snake.biting_tail():
            sys.exit()
            
    def adj_snake(self):
        tr, tc = r, c = self.snake.body[0].get_pos()
        gw, gh = self.grid._options.clmns, self.grid._options.rows
        
        if r >= gh: r = 0
        if r < 0: r = gh - 1
        
        if c >= gw: c = 0
        if c < 0: c = gw - 1

        if (tr, tc) != (r, c):
            self.snake.move(r, c)
        
    def draw(self) -> None:
        self.surface.fill(0)
        self.snake.draw(self.surface, self.grid)
                