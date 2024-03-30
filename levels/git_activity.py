import pygame as pg

import levels

class GitActivity(levels.BaseLevel):
    def __init__(self) -> None:
        self.surface = ...
        self.gol_board_lvl = levels.GameOfLifeBoardLevel(self.surface, 53, 7)

    def update(self, t_elapsed: float, events: list[pg.event.Event]) -> bool:
        raise NotImplemented
    
    def draw(self) -> None:
        raise NotImplemented