import sys
import pygame as pg
import json
import argparse
import os

from typing import Any

from level_factory import LevelFactory
from levels.dev_level_wrapper import DevLevelWrapper

DATA_FILE_PATH = 'data.json'

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    level_choices = [
        'git-activity', 
        'sol-demo', 
        'gol-demo'
    ]
    parser.add_argument('-l', '--level', type=str, nargs=1, choices=level_choices, help="IDK")

    return parser.parse_args()

def get_game_data() -> Any:
    try:
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
            game_data = json.load(f)
    except Exception as e:
        sys.exit(e)
    
    return game_data

def start_game() -> None:
    args = get_args()
    chosen_lvl = 'gol-demo' if args.level is None else args.level[0]

    game_data = get_game_data()
    
    pg.init()

    # TODO use mapper...
    icon_path = os.path.join(game_data['icon']['folder'], game_data['icon']['name'])
    icon = pg.image.load(icon_path)
    pg.display.set_icon(icon)

    pg.display.set_caption(game_data['window_name'])
    
    
    lvl_factry = LevelFactory()
    curr_lvl = lvl_factry.create_level(chosen_lvl)

    t_acc = 0.
    t_slice = 1. / game_data['game_ticks']
    max_fps = game_data['fps_cap']
    max_ups = game_data['updates_per_cycle']
    
    clock = pg.time.Clock()
    curr_lvl = DevLevelWrapper(curr_lvl, clock)
    clock.tick()

    while True:
        t_elapsed = clock.tick(max_fps) / 1_000
        t_acc += t_elapsed
        
        ups_left = max_ups
        while t_acc > t_slice and ups_left != 0:
            events = pg.event.get() # TODO to seperate thread
            done = curr_lvl.update(t_elapsed, events)
            if done:
                raise NotImplementedError

            t_acc, ups_left = t_acc - t_slice, ups_left - 1
        
        curr_lvl.draw()
        pg.display.update()
        
if __name__ == '__main__':
    start_game()