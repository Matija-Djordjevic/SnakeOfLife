import pygame as pg

import entities as ents

import grid

class BodyPart(ents.BaseEntity):
    def __init__(self, row: int, clmn: int) -> None:
        self.row, self.clmn = row, clmn
        super().__init__()

    def move(self, row: int, clmn: int) -> tuple[int, int]:
        oldr, oldc = self.row, self.clmn
        self.row, self.clmn = row, clmn
        return oldr, oldc
    
    def get_pos(self) -> tuple[int, int]:
        return self.row, self.clmn
    
class ColorBodyPart(BodyPart):
    def __init__(self, row: int, clmn: int, color: tuple[int, int, int]) -> None:
        super().__init__(row, clmn)
        self.color = color

    def update(self, t_elapsed: float) -> bool:
        pass
    
    def draw(self, surface: pg.Surface, grid: grid.Grid) -> None:
        grid.draw_colored_cells_to_screen(surface, [(self.row, self.clmn, self.color)])
    
class GOLBodyPart(BodyPart):
    def __init__(self, row: int, clmn: int, parent_grid: grid.Grid) -> None:
        super().__init__(row, clmn)
        self.ups = 6
        self.t_acc = 0
        
        self.table_rows, self.table_clmns = 7, 7
        self.gol_table = ents.GOLTable(self.table_clmns, self.table_rows, True, (57, 211, 83), (22, 27, 34))
        self.gol_table.randomize_cells()
        
        self.bkd_clr = (0, 0, 0)
        self.parent_grid = parent_grid
        self.e_grid = self.get_e_grid()
        
    def update(self, t_elapsed: float) -> bool:
        self.t_acc += t_elapsed
        t_slice = 1. / self.ups
        while self.t_acc > t_slice:
            self.gol_table.evolve()
            self.t_acc -= t_slice
    
    def move(self, row: int, clmn: int) -> tuple[int, int]:
        super().move(row, clmn)
        self.e_grid.move_to(row, clmn)
    
    def draw(self, surface: pg.Surface, grid: grid.Grid) -> None:
        self.e_grid.draw_bkgd_and_border(surface)
        self.gol_table.draw(self.e_grid, surface)
    
    def get_e_grid(self) -> grid.EmbededGrid:
        builder = grid.GridBuilder()\
            .set_clmns_and_rows_count(self.table_clmns, self.table_rows)\
            .set_border_color_and_width((0, 255, 0), 2)\
            .set_bkgd_color(self.bkd_clr)\
            .set_cell_padding(1)\
            .set_color_cells_border_radius(1)\
            .keep_same_cell_width_and_height()\
            .force_consistent_cell_padding()
            
        e_grid = grid.EmbededGrid(builder, self.parent_grid, self.row, self.clmn)
        
        return e_grid
    
class Snake(ents.BaseEntity):
    def __init__(self) -> None:
        super().__init__()
        color = (123, 123, 123)
        self.body = [
            ColorBodyPart(0, 0, (0, 255, 0)),
            ColorBodyPart(0, 1, color),
            ColorBodyPart(0, 2, color),
            ColorBodyPart(0, 3, color),
            ColorBodyPart(0, 4, color),
            ColorBodyPart(0, 5, color),
            ColorBodyPart(1, 5, color),
            ColorBodyPart(2, 5, color),
            ColorBodyPart(3, 5, color),
        ]
    
    def update(self, t_elapsed: float) -> bool:
        for part in self.body: part.update(t_elapsed)
        #r, c = self.body[0].get_pos()
        #self.move(r, c + 1)
        
    def draw(self, surface: pg.Surface, grid: grid.Grid) -> None:
        for part in self.body: part.draw(surface, grid)
    
    def add_body_part(self, p: BodyPart):
        self.body.append(p)
    
    def move(self, row: int, clmn: int) -> None:
        body = self.body
        
        next_row, next_clmn = row, clmn
        for part in body:
            next_row, next_clmn = part.move(next_row, next_clmn)