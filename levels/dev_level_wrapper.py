import pygame as pg

from levels.base_level import BaseLevel

class DevLevelWrapper():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    def __init__(self, level: BaseLevel, clock: pg.time.Clock) -> None:
        self.level = level
        self.clock = clock
        
        self._display_info = False
        
        self.font_size = 35
        self.font_color = (255, 255, 255)
        self._info_font = pg.font.SysFont("Arial", size=self.font_size, bold=False)
    
    def update(self, t_elapsed: float, events: list[pg.event.Event]) -> bool:
        self._handle_events(events)
        return self.level.update(t_elapsed, events)        
    
    def draw(self) -> None:
        self.level.draw()
        
        if self._display_info == True:
            self._do_display_info()
    
    def _do_display_info(self) -> None:
        ls = self._get_info_list()

        s_x, s_y = 20, 20
        y_off = 0
        for el in ls:
            img = self._info_font.render(el, True, self.font_color)
            self.level.surface.blit(img, (s_x, s_y + y_off))
            y_off +=  self.font_size

    def _get_info_list(self) -> list[str]:
        ls = []
        
        fps = int(self.clock.get_fps())
        ls.append(f'{fps} fps')
        
        w, h = self.level.surface.get_size()
        ls.append(f'{w}p X {h}p')
        
        return ls
    
    def _handle_events(self, events: list[pg.event.Event]) -> None:
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_F1: self._display_info = not self._display_info
                    case pg.K_F2:
                        blck, white = DevLevelWrapper.BLACK, DevLevelWrapper.WHITE
                        self.font_color = blck if self.font_color == white else white
                    case pg.K_F3:
                        self._info_font.bold = True if not self._info_font.bold else False