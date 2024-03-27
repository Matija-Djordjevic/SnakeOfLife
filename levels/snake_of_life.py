from levels.base_level import BaseLevel
import pygame as pg


class SnakeOfLifeDemoLevel(BaseLevel):
    def __init__(self, surface: pg.Surface) -> None:
        super().__init__(surface)
    
    def update(self, t_elapsed: float, events: list[pg.event.Event]) -> bool:
        raise NotImplemented
    
    def draw(self) -> None:
        raise NotImplemented