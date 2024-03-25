from levels.base_level import BaseLevel
from levels.git_activity import GitActivity
from levels.snake_of_life_demo import SnakeOfLifeDemoLevel
from levels.game_of_life_demo import GameOfLifeDemoLevel

import pygame as pg

class LevelFactory():
    def __init__(self, surface: pg.Surface) -> None:
        self.surface = surface
    
    def create_level(self, choice: str) -> BaseLevel:
        match choice:
            case "git-activity": return self._create_git_activity_level()
            case "sol-demo": return self._create_snake_of_life_demo()
            case "gol-demo": return self._create_game_of_life_demo()
    
    def _create_git_activity_level(self) -> GitActivity:
        return GitActivity(self.surface)
    
    def _create_snake_of_life_demo(self) -> SnakeOfLifeDemoLevel:
        return SnakeOfLifeDemoLevel(self.surface)
    
    def _create_game_of_life_demo(self) -> GameOfLifeDemoLevel:
        return GameOfLifeDemoLevel(self.surface)
        
        
    