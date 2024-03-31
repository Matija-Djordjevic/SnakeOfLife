import pygame as pg

import os

from entities import GOLTable as entities_GOLTable
from grid import Grid as gird_Grid
from grid import Builder as grid_Builder
from levels import BaseLevel as levels_BaseLevel

class GitActivity(levels_BaseLevel):
    def __init__(self) -> None:
        super().__init__()
        self.warmup()
        self.surface = pg.display.set_mode((1856, 387))
        self.bgd = pg.image.load(os.path.join('assets', 'GitBKGD.PNG'))
        self.surface.blit(self.bgd, (0, 0))
        
        self.rows, self.clmns = 7, 53
        self.grid = self.init_grid()
        self.dead = 22, 27, 34
        self.alive = 57, 211, 83
        self.table = entities_GOLTable(self.clmns, self.rows, True, self.alive, self.dead)
        self.table.randomize_cells()
        #self.table = entities_GOLTable.try_load_from_binary()
        
        self.t_acc = 0.
        self.ups = 7

    def warmup(self):
        entities_GOLTable(10, 10, False, (0, 0, 0), (0, 0, 0)).evolve()
        
    def init_grid(self) -> gird_Grid:
        builder = grid_Builder()\
            .set_clmns_and_rows_count(self.clmns, self.rows)\
            .set_available_width_and_height(1696, 224)\
            .set_draw_offsets(119, 78)\
            .set_border_color_and_width((0, 0, 0), 0)\
            .set_bkgd_color((144, 67, 17))\
            .set_cell_padding(3)\
            .set_color_cells_border_radius(4)\
            .keep_same_cell_width_and_height()\
            .force_consistent_cell_padding()
        
        return gird_Grid(builder)
            
    def update(self, t_elapsed: float, events: list[pg.event.Event]) -> bool:
        self.t_acc += t_elapsed
        t_slice = 1. / self.ups
        while self.t_acc > t_slice:
            self.table.evolve()
            self.t_acc -= t_slice
            
    def draw(self) -> None:
        self.table.draw(self.grid, self.surface)