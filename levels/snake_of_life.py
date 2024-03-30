import sys
from levels.base_level import BaseLevel
import pygame as pg

import numpy as np 

import entities as ents
import grid

class SnakeOfLifeDemoLevel(BaseLevel):
    def __init__(self, rows: int, clmns: int, width: int, height: int) -> None:
        self.surface = pg.display.set_mode((width, height))
        self.warmup()
        self.rows, self.clmns = rows, clmns
        self.bkd_clr = (255, 255, 255)
        self.grid = self.init_grid()
        self.snake = ents.MovingSnake(0, 0)\
            .add_body_part(ents.GOLBodyPart(0, 1, self.grid))\
            .add_body_part(ents.GOLBodyPart(0, 2, self.grid))\
            .add_body_part(ents.GOLBodyPart(0, 3, self.grid))\
            .add_body_part(ents.GOLBodyPart(0, 4, self.grid))\
            .add_body_part(ents.GOLBodyPart(0, 5, self.grid))
        
        self.ups = 10
        self.t_acc = 0
        
        self.food = None
    
    def warmup(self):
        ents.GOLTable(10, 10, False, (0, 0, 0), (0, 0, 0)).evolve()
    
    def init_grid(self) -> grid.Grid:
        builder = grid.Builder()\
            .set_clmns_and_rows_count(self.clmns, self.rows)\
            .set_available_width_and_height(*self.surface.get_size())\
            .set_draw_offsets(0, 0)\
            .set_border_color_and_width(self.bkd_clr, 10)\
            .set_bkgd_color((0, 0, 0))\
            .set_cell_padding(2)\
            .set_color_cells_border_radius(4)\
            .keep_same_cell_width_and_height()\
            .force_consistent_cell_padding()

        return grid.Grid(builder)
        
    def handle_events(self, events: list[pg.event.Event]) -> None:
        for event in events:
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_s: self.snake.try_cnage_dir(ents.SnakeDirection.DOWN)
                    case pg.K_d: self.snake.try_cnage_dir(ents.SnakeDirection.RIGHT)
                    case pg.K_w: self.snake.try_cnage_dir(ents.SnakeDirection.UP)
                    case pg.K_a: self.snake.try_cnage_dir(ents.SnakeDirection.LEFT)
        
    def update(self, t_elapsed: float, events: list[pg.event.Event]) -> bool:
        snake = self.snake
        self.handle_events(events)
        snake.update(t_elapsed)
        self.adj_snake()        
        
        if self.food is None:
            r, c = self.grid.rows, self.grid.clmns
            pos = np.random.randint(r), np.random.randint(c)
            
        
        if snake.is_biting_itself():
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
        self.snake.draw(self.surface, self.grid)
                