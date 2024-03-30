import pygame as pg

from levels.base_level import BaseLevel

_BLACK = (0, 0, 0)
_WHITE = (255, 255, 255)
_GREEN = (0,230,0)
_RED = (230,0,0)

_COLORS = [_WHITE, _BLACK, _GREEN, _RED]

class _FontInfo:
    def __init__(self, name: str, size: int, bold: bool):
        self.name = name
        self.size = size
        self.bold = bold

class DevLevelWrapper():
    def __init__(self, level: BaseLevel, clock: pg.time.Clock) -> None:
        self.level = level
        self.clock = clock
        
        self.ups = 3
        self.t_acc = 0

        self.clr_i = 0
        self.fps = 0
        self.show_info = False
        
        self.f_info = _FontInfo('Arial', 40, True)

    @property
    def surface(self): return self.level.surface

    def update(self, t_elapsed: float, events: list[pg.event.Event]) -> bool:
        self._handle_events(events)
        
        self.t_acc += t_elapsed
        t_slice = 1. / self.ups
        while self.t_acc > t_slice:    
            self.fps = int(self.clock.get_fps())
            self.t_acc -= t_slice

        return self.level.update(t_elapsed, events)        
    
    def draw(self) -> None:
        self.level.draw()
        
        if self.show_info == True:
            self._do_show_info()
    
    def _do_show_info(self) -> None:
        s_x, s_y = 10, 10
        y_off = 0
        ls = self._get_info_list()
        inf = self.f_info
        for el in ls:
            img = pg.font.SysFont(inf.name, inf.size, inf.bold)\
                .render(el, True, _COLORS[self.clr_i])
            self.level.surface.blit(img, (s_x, s_y + y_off))
            y_off += inf.size

    def _get_info_list(self) -> list[str]:
        ls = []
        
        ls.append(f'{self.fps} fps')
        
        w, h = self.level.surface.get_size()
        ls.append(f'{w}p x {h}p')
        
        return ls
    
    def _handle_events(self, events: list[pg.event.Event]) -> None:
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_F1: self.show_info = not self.show_info
                    case pg.K_F2:
                        self.clr_i += 1
                        print(self.clr_i)
                        if self.clr_i == len(_COLORS): self.clr_i = 0
                        self.font_color = _COLORS[self.clr_i]
                    case pg.K_F3:
                        self.f_info.bold = True if not self.f_info.bold else False
                    case pg.K_F4:
                        self.f_info.size = max(32, self.f_info.size - 10)
                    case pg.K_F5:
                        self.f_info.size = min(100, self.f_info.size + 10)
