def color_text(color: str, text: str) -> str:
    colors = {
        "red": "\033[1;31m",
        "green": "\033[1;32m",
        "yellow": "\033[1;33m",
        "blue": "\033[1;34m",
        "cyan": "\033[1;36m",
        "white": "\033[0m",
    }

    # Par défaut en blanc si couleur inconnue
    color_code = colors.get(color.lower(), colors["white"])
    print(f"{color_code}{text}{colors['white']}")
