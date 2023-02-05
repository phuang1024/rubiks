__all__ = (
    "Color",
)


class Color:
    """Color of a Rubik's Cube piece."""
    YELLOW = 0
    BLUE = 1
    RED = 2
    GREEN = 3
    ORANGE = 4
    WHITE = 5

    ANSI_W = "\033[97m"
    ANSI_Y = "\033[93m"
    ANSI_G = "\033[92m"
    ANSI_B = "\033[94m"
    ANSI_R = "\033[91m"
    ANSI_O = "\033[38;5;214m"
    ANSI_RESET = "\033[0m"

    @staticmethod
    def col_to_char(col: int) -> str:
        match col:
            case Color.WHITE: return "W"
            case Color.YELLOW: return "Y"
            case Color.GREEN: return "G"
            case Color.BLUE: return "B"
            case Color.RED: return "R"
            case Color.ORANGE: return "O"
            case _: raise ValueError("Invalid color")

    @staticmethod
    def char_to_col(char: str) -> int:
        match char:
            case "W": return Color.WHITE
            case "Y": return Color.YELLOW
            case "G": return Color.GREEN
            case "B": return Color.BLUE
            case "R": return Color.RED
            case "O": return Color.ORANGE
            case _: raise ValueError("Invalid color")

    @staticmethod
    def col_to_ansi(col: int) -> str:
        match col:
            case Color.WHITE: return Color.ANSI_W
            case Color.YELLOW: return Color.ANSI_Y
            case Color.GREEN: return Color.ANSI_G
            case Color.BLUE: return Color.ANSI_B
            case Color.RED: return Color.ANSI_R
            case Color.ORANGE: return Color.ANSI_O
            case _: raise ValueError("Invalid color")
