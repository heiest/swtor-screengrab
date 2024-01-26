from .error import Error

class OcrError(Error):
    def __init__(self, message):
        self.message = message