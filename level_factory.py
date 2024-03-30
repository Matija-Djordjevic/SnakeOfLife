import levels as lsl

import pygame as pg

class LevelFactory():
    def __init__(self) -> None:
        pass
    
    def create_level(self, choice: str) -> lsl.BaseLevel:
        match choice:
            case "git-activity": return self._create_git_activity_level()
            case "sol-demo": return self._create_snake_of_life_demo()
            case "gol-demo": return self._create_game_of_life_demo()
            case _: raise ValueError()
    
    def _create_git_activity_level(self) -> lsl.GitActivity:
        return lsl.GitActivity()
    
    def _create_snake_of_life_demo(self) -> lsl.SnakeOfLifeDemoLevel:
        return lsl.SnakeOfLifeDemoLevel(15, 15, 1300, 1300)
    
    def _create_game_of_life_demo(self) -> lsl.GameOfLifeBoardLevel:
        return lsl.GameOfLifeBoardLevel(90, 90, 1300, 1300)
        
        
    