import pygame as pg

from abc import ABC, abstractmethod


class BaseLevel():
    def __init__(self) -> None:
        pass

    @abstractmethod
    def update(self, t_elapsed: float, events: list[pg.event.Event]) -> bool:
        pass
        
    @abstractmethod
    def draw(self) -> None:
        pass