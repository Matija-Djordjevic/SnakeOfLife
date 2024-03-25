import pygame as pg

from levels.base_level import BaseLevel

class DevLevelWrapper():
    def __init__(self, level: BaseLevel, clock: pg.time.Clock) -> None:
        self.level = level
        self._surface = level.surface
        self.clock = clock
        self._display_info = False
        self._info_font = pg.font.SysFont("Arial", size=45, bold=True)
        self.font_color = (255, 255, 255)
    
    def update(self, t_elapsed: float, events: list[pg.event.Event]) -> bool:
        self._handle_events(events)
        return self.level.update(t_elapsed, events)        
    
    def draw(self) -> None:
        self.level.draw()
        
        if self._display_info == True:
            self._do_display_info()
    
    def _do_display_info(self) -> None:
        fps = self.clock.get_fps()
        fps = str(int(fps))
        img = self._info_font.render(fps, True, self.font_color)
        self._surface.blit(img, (0, 0))
    
    def _handle_events(self, events: list[pg.event.Event]) -> None:
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_F2:
                self._display_info = not self._display_info