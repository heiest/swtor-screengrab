from .error import Error

class ScreenshotAreaInvalidError(Error):
    def __init__(self, screenshot_rect, game_rect):
        self.screenshot_rect = screenshot_rect
        self.game_rect = game_rect