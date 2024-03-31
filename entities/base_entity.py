from abc import ABC, abstractmethod

import grid
import pygame as pg

class BaseEntity(ABC):
    @abstractmethod
    def update(self, t_elapsed: float) -> bool:
        pass

    @abstractmethod
    def draw(self, surface: pg.Surface, grid: grid.Grid) -> None:
        pass