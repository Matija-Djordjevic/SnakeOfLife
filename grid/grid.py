'''
'''

import pygame as pg

class GridOptions():
    def __init__(self) -> None:
        self.rows = 0
        self.clmns = 0
        
        self.x_offset = 0
        self.y_offset = 0
        
        self.avail_width = 0
        self.avail_height = 0
        
        self.cell_padding = 0
        
        self.color_cells_border_radius = 0
        
        self.border_color = (0, 0, 0)
        self.border_width = 0
        
        self.bkgd_color = (0, 0, 0)
        
        self.same_cell_dims = False

        self.consistent_padding = False
        
# split into many files?
class Builder():
    def __init__(self) -> None:
        self._options = GridOptions()
        
    def set_clmns_and_rows_count(self, clmns: int, rows: int) -> 'Builder':
        if clmns <= 0 or rows <= 0:
            raise ValueError()
        self._options.rows, self._options.clmns = rows, clmns        
        return self
    
    def set_draw_offsets(self, x_offset: int, y_offset: int) -> 'Builder':
        self._options.x_offset, self._options.y_offset = x_offset, y_offset
        return self
    
    def set_available_width_and_height(self, avail_x: int, avail_y: int) -> 'Builder':
        if avail_x <= 0 or avail_y <= 0:
            raise ValueError()
        self._options.avail_width, self._options.avail_height = avail_x, avail_y
        return self
    
    def set_cell_padding(self, padding: int) -> 'Builder':
        if padding < 0:
            raise ValueError()
        self._options.cell_padding = padding
        return self

    def set_border_color_and_width(self, color: tuple[int, int, int], width: int) -> 'Builder':
        if width < 0 or self._invalid_color(*color):
            raise ValueError()
        self._options.border_color, self._options.border_width = color, width
        return self
    
    def set_bkgd_color(self, color: tuple[int, int, int]) -> 'Builder':
        if self._invalid_color(*color):
            raise ValueError()
        
        self._options.bkgd_color = color
        return self
    
    def keep_same_cell_width_and_height(self) -> 'Builder':
        self._options.same_cell_dims = True
        return self
    
    def force_consistent_cell_padding(self) -> 'Builder':
        self._options.consistent_padding = True
        return self
    
    def set_color_cells_border_radius(self, radius: int) -> 'Builder':
        self._options.color_cells_border_radius = radius
        return self 

    def _invalid_color(self, r: int, g: int, b: int) -> bool: return r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255

class Grid():
    def __init__(self, builder: Builder) -> None:
        # immutable for speed!
        self._options = builder._options

    def draw_bkgd_and_border(self, surface: pg.Surface) -> None: GridDrawer.draw_bkgd_and_border(self, surface)

    def get_available_cell_width_and_height(self) -> tuple[float, float] | tuple[int, int]: return GridDrawer.get_available_cell_width_and_height(self)
    
    def get_cell_width_and_height(self) -> tuple[float, float] | tuple[int, int]: return GridDrawer.get_cell_width_and_height(self)
    
    def get_cell_x_y_off(self, row: int, clmn: int) -> tuple[float, float] | tuple[int, int]: return GridDrawer.get_cell_x_y_off(self, row, clmn)
    
    def get_cell_x_y_off(self, row_and_clmn: tuple[int, int]) -> tuple[float, float] | tuple[int, int]: return GridDrawer.get_cell_x_y_off(self, *row_and_clmn)   
    
    def draw_colored_cells_to_screen(self, surface: pg.Surface, rows_clmns_colors: list[tuple[int, int, tuple[int, int, int]]]) -> None: GridDrawer.draw_colored_cells_to_screen(self, surface, rows_clmns_colors)

    def get_actual_grid_size(self) -> tuple[int, int]: return GridDrawer.get_actual_grid_size(self)
    
class EmbededGrid(Grid):
    def __init__(self, builder: Builder, parent: Grid, row_in_parent: int, clmn_in_parent: int) -> None:
        '''
            This grid will have no offset :(
        '''
        super().__init__(builder)
        self._parent = parent
        self._row, self._clmn = 0,0
        self.move_to(row_in_parent, clmn_in_parent)
    
    def move_to(self, new_row, new_clmn) -> None:
        self._row = new_row
        self._clmn = new_clmn
        self._adjust_grid()
    
    def _adjust_grid(self) -> None: 
        self._options.x_offset, self._options.y_offset = GridDrawer.get_cell_x_y_off(self._parent, self._row, self._clmn)
        self._options.avail_width, self._options.avail_height = GridDrawer.get_cell_width_and_height(self._parent)
    
class GridDrawer:
    @staticmethod
    def draw_bkgd_and_border(grid: Grid, surface: pg.Surface) -> None:
        opt = grid._options
        w, h = GridDrawer.get_actual_grid_size(grid)
        r = pg.rect.Rect(opt.x_offset, opt.y_offset, w, h)
        pg.draw.rect(surface, opt.border_color, r)

        r.top += opt.border_width
        r.left += opt.border_width
        r.width -= 2 * opt.border_width
        r.height -= 2 * opt.border_width
        pg.draw.rect(surface, opt.bkgd_color, r)

    @staticmethod 
    def get_available_cell_width_and_height(grid: Grid) -> tuple[float, float] | tuple[int, int]:
        w = (grid._options.avail_width - 2 * grid._options.border_width) / grid._options.clmns
        h = (grid._options.avail_height - 2 * grid._options.border_width) / grid._options.rows
        
        if grid._options.consistent_padding:
            w, h = int(w), int(h)        
        
        if grid._options.same_cell_dims:
            smaller = min(w, h)
            return smaller, smaller
        
        return w, h
    
    @staticmethod
    def get_cell_width_and_height(grid: Grid) -> tuple[float, float] | tuple[int, int]: 
        aw, ah = GridDrawer.get_available_cell_width_and_height(grid)
        w, h = aw - 2 * grid._options.cell_padding, ah - 2 * grid._options.cell_padding
        return w, h
    
    @staticmethod
    def get_cell_x_y_off(grid: Grid, row: int, clmn: int) -> tuple[float, float] | tuple[int, int]:
        aw, ah = GridDrawer.get_available_cell_width_and_height(grid)
        x = clmn * aw + grid._options.cell_padding + grid._options.x_offset + grid._options.border_width
        y = row * ah + grid._options.cell_padding + grid._options.y_offset + grid._options.border_width
        return x, y
    
    @staticmethod
    def draw_colored_cells_to_screen(grid: Grid, surface: pg.Surface, rows_clmns_colors: list[tuple[int, int, tuple[int, int, int]]]) -> None:
        w, h = GridDrawer.get_cell_width_and_height(grid)
        rect = pg.Rect(0, 0, w, h)

        radius = grid._options.color_cells_border_radius
        aw, ah = GridDrawer.get_available_cell_width_and_height(grid)

        const_x_off = grid._options.cell_padding + grid._options.x_offset + grid._options.border_width
        const_y_off = grid._options.cell_padding + grid._options.y_offset + grid._options.border_width
        for row, clmn, color in rows_clmns_colors:
            x_off = clmn * aw + const_x_off
            y_off = row * ah + const_y_off
            rect.x, rect.y = x_off, y_off
            pg.draw.rect(surface, color, rect, border_radius=radius)
    
    @staticmethod
    def get_actual_grid_size(grid: Grid) -> tuple[int, int]:
        wpc, hpc = grid.get_available_cell_width_and_height()    
        width, height = wpc * grid._options.clmns, hpc * grid._options.rows
        
        bw = grid._options.border_width
        width, height = width + 2 * bw, height + 2 * bw
        
        return width, height