class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.is_dark = False

    def toggle_theme(self):
        if self.is_dark:
            self.root.configure(bg="white")
        else:
            self.root.configure(bg="gray20")
        self.is_dark = not self.is_dark