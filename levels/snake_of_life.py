from levels.base_level import BaseLevel
import pygame as pg

import entities as ents
import grid

class SnakeOfLifeDemoLevel(BaseLevel):
    def __init__(self, surface: pg.Surface) -> None:
        super().__init__(surface)
        self.rows, self.clmns = 20, 20
        self.bkd_clr = (255, 255, 255)
        self.grid = self.init_grid()

        self.snake = ents.Snake()
        self.snake.add_body_part(ents.GOLBodyPart(4, 5, self.grid))
        self.snake.add_body_part(ents.GOLBodyPart(5, 5, self.grid))
        self.snake.add_body_part(ents.GOLBodyPart(6, 5, self.grid))
        self.snake.add_body_part(ents.GOLBodyPart(7, 5, self.grid))
        self.snake.add_body_part(ents.GOLBodyPart(8, 5, self.grid))
        
        self.ups = 10
        self.t_acc = 0

    def init_grid(self) -> grid.Grid:
        builder = grid.GridBuilder()\
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
        
    def update(self, t_elapsed: float, events: list[pg.event.Event]) -> bool:
        self.const_events(events)
        self.snake.update(t_elapsed)
        
    def draw(self) -> None:
        self.snake.draw(self.surface, self.grid)
                
    def const_events(self, events: list[pg.event.Event]) -> None:
        for event in events:
            if event.type == pg.QUIT:
                exit()
