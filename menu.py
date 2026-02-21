import json
from pygame import *

def save_to_json_file(data):
    with open("pygame/data.json","w", encoding="utf-8") as f:
        json.dump(data,f, ensure_ascii=False)

def load_from_json_file():
    try:
        with open("pygame/data.json","r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        save_to_json_file({"level":"легкий"})
        return {"level":"легкий"}

init()
screen = display.set_mode((500, 500))
clock = time.Clock()
FPS = 60
running = True

class button():
    def __init__(self, x, y, w, h, text, font, bg_color, text_color):
        self.rect = Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color

    def draw(self, screen):
        draw.rect(screen, self.bg_color, self.rect)
        draw.rect(screen, (0,0,0), self.rect, 2)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

font_btn = font.SysFont(None, 36)
font_text = font.SysFont(None, 28)

play_btn = button(150,150,200,60,"Грати", font_btn, (100,200,100),(0,0,0))
difficulty_btn = button(150,230,200,60,"Складність", font_btn, (200,200,100),(0,0,0))
exit_btn = button(150,310,200,60,"Вийти", font_btn, (200,100,100),(0,0,0))

buttons = [play_btn, difficulty_btn, exit_btn]

levels = ["легкий","середній","важкий"]
settings = load_from_json_file()
current_level = settings.get("level","легкий")

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if play_btn.is_clicked(e):
            print(f"Гра запущена! Поточна складність: {current_level}")
        if difficulty_btn.is_clicked(e):
            idx = levels.index(current_level)
            current_level = levels[(idx + 1) % len(levels)]
            save_to_json_file({"level":current_level})
            print(f"Складність змінено на: {current_level}")
        if exit_btn.is_clicked(e):
            running = False

    screen.fill((255,0,0))
    level_text = font_text.render(f"Поточна складність: {current_level}", True, (255,255,255))
    screen.blit(level_text, (150,100))
    for btn in buttons:
        btn.draw(screen)
    display.flip()
    clock.tick(FPS)

quit()
