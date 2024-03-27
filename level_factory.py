import levels as lsl

import pygame as pg

class LevelFactory():
    def __init__(self, surface: pg.Surface) -> None:
        self.surface = surface
    
    def create_level(self, choice: str) -> lsl.BaseLevel:
        match choice:
            case "git-activity": return self._create_git_activity_level()
            case "sol-demo": return self._create_snake_of_life_demo()
            case "gol-demo": return self._create_game_of_life_demo()
            case _: raise ValueError()
    
    def _create_git_activity_level(self) -> lsl.GitActivity:
        return lsl.GitActivity(self.surface)
    
    def _create_snake_of_life_demo(self) -> lsl.SnakeOfLifeDemoLevel:
        return lsl.SnakeOfLifeDemoLevel(self.surface)
    
    def _create_game_of_life_demo(self) -> lsl.GameOfLifeDemoLevel:
        return lsl.GameOfLifeDemoLevel(self.surface)
        
        
    