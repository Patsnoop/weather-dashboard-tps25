class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.current_theme = "Light"

        # Define all your available themes here
        self.themes = {
            "Light": {"bg": "white"},
            "Dark": {"bg": "gray20"},
            "Ocean": {"bg": "#2E8BC0"},
            "Sunset": {"bg": "#FF6F61"},
            "Forest": {"bg": "#228B22"},
        }

    def apply_theme(self, theme_name):
        # Get the theme colors, fallback to Light theme
        theme = self.themes.get(theme_name, self.themes["Light"])
        self.root.configure(bg=theme["bg"])
        self.current_theme = theme_name