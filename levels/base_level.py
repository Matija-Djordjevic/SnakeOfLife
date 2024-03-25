import pygame as pg

class BaseLevel():
    def __init__(self, surface: pg.Surface) -> None:
        self.surface = surface
    
    def update(self, t_elapsed: float, events: list[pg.event.Event]) -> bool:
        raise NotImplemented
    
    def draw(self) -> None:
        raise NotImplemented