
import grid
import pygame as pg

class BaseEntity:
    def update(self, t_elapsed: float) -> bool:
        raise NotImplemented
    
    def draw(self, surface: pg.Surface, grid: grid.Grid) -> None:
        raise NotImplemented