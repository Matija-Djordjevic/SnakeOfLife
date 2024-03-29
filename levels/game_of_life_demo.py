from levels.base_level import BaseLevel
import pygame as pg

import entities as ents
import grid
class GameOfLifeDemoLevel(BaseLevel):
    def __init__(self, surface: pg.Surface) -> None:
        super().__init__(surface)
        self.rows, self.clmns = 50, 50
        self.t: ents.GOLTable = ents.GOLTable(self.clmns, self.rows, True, (57, 211, 83), (22, 27, 34))
        self.bkd_clr = (255, 255, 255)
        self.t.randomize_cells()
        self.grid = self.init_grid()
        
        self.ups = 10
        self.t_acc = 0

        self.font_size = 45
        self.font_color = (57, 211, 83)
        self._info_font = pg.font.SysFont("Arial", size=self.font_size, bold=False)
        
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
        
    def update(self, t_elapsed: float, events: list[pg.event.Event]) -> bool:
        self.const_events(events)
        
        self.t_acc += t_elapsed
        t_slice = 1. / self.ups
        while self.t_acc > t_slice:
            self.t.evolve()
            self.t_acc -= t_slice
        
    def draw(self) -> None:
        self.grid.draw_bkgd_and_border(self.surface)
        self.t.draw(self.grid, self.surface)
        self.display_generation_count()
        
    def const_events(self, events: list[pg.event.Event]) -> None:
        for event in events:
            if event.type == pg.QUIT:
                exit()

    def display_generation_count(self):    
        gen_txt = f"Gen: {str(self.t.generation_count)}"
        img = self._info_font.render(gen_txt, True, self.font_color)
        bw = self.grid._options.border_width
        _, h = self.grid.get_actual_grid_size()
        self.surface.blit(img, (bw, h - bw - self.font_size))