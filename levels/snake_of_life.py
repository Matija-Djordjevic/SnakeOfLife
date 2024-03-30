import sys
from levels.base_level import BaseLevel
import pygame as pg

import entities as ents
import grid

class SnakeOfLifeDemoLevel(BaseLevel):
    DIR_CHANGES = [

    ]
    
    def __init__(self, surface: pg.Surface) -> None:
        super().__init__(surface)
        self.warmup()
        self.rows, self.clmns = 20, 20
        self.bkd_clr = (255, 255, 255)
        self.grid = self.init_grid()

        self.moving_snake = ents.MovingSnake()
        self.moving_snake.add_body_part(ents.GOLBodyPart(4, 5, self.grid))
        self.moving_snake.add_body_part(ents.GOLBodyPart(5, 5, self.grid))
        self.moving_snake.add_body_part(ents.GOLBodyPart(6, 5, self.grid))
        self.moving_snake.add_body_part(ents.GOLBodyPart(7, 5, self.grid))
        self.moving_snake.add_body_part(ents.GOLBodyPart(8, 5, self.grid))
        
        self.ups = 10
        self.t_acc = 0
        
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
                    case pg.K_s: self.moving_snake.try_cnage_dir(ents.MovingSnake.Direction.DOWN)
                    case pg.K_d: self.moving_snake.try_cnage_dir(ents.MovingSnake.Direction.RIGHT)
                    case pg.K_w: self.moving_snake.try_cnage_dir(ents.MovingSnake.Direction.UP)
                    case pg.K_a: self.moving_snake.try_cnage_dir(ents.MovingSnake.Direction.LEFT)
        
    def update(self, t_elapsed: float, events: list[pg.event.Event]) -> bool:
        self.handle_events(events)
        self.moving_snake.update(t_elapsed)
        self.adj_snake()
        if self.moving_snake.is_biting_itself():
            sys.exit()
        
        if self.moving_snake.body[0].get_pos() == (0, 0):
            r, c = self.moving_snake.body[-1].get_pos()
            self.moving_snake.add_body_part(ents.ColorBodyPart(r, c, (12, 156, 255)))
            
    def adj_snake(self):
        r, c = self.moving_snake.body[0].get_pos()
        tr, tc = r, c
        gw, gh = self.grid._options.clmns, self.grid._options.rows
        
        if r == gh:
            r = 0
        if r == -1:
            r = gh - 1
        
        if c == gw:
            c = 0
        if c == -1:
            c = gw - 1
        
        if (tr, tc) != (r, c):
            self.moving_snake.move(r, c)
        
    def draw(self) -> None:
        self.moving_snake.draw(self.surface, self.grid)
                