__all__ = (
    "Color",
)


class Color:
    """
    Color of a Rubik's Cube piece.
    Also used to represent faces e.g. YELLOW = Up, BLUE = Front, etc.
    """

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
    def opposite(col: int) -> int:
        match col:
            case Color.WHITE: return Color.YELLOW
            case Color.YELLOW: return Color.WHITE
            case Color.GREEN: return Color.BLUE
            case Color.BLUE: return Color.GREEN
            case Color.RED: return Color.ORANGE
            case Color.ORANGE: return Color.RED
            case _: raise ValueError("Invalid color")

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
    def col_to_name(col: int) -> str:
        match col:
            case Color.WHITE: return "White"
            case Color.YELLOW: return "Yellow"
            case Color.GREEN: return "Green"
            case Color.BLUE: return "Blue"
            case Color.RED: return "Red"
            case Color.ORANGE: return "Orange"

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

    @staticmethod
    def col_to_face(col: int) -> str:
        """
        YELLOW -> U, BLUE -> F, etc.
        """
        match col:
            case Color.WHITE: return "D"
            case Color.YELLOW: return "U"
            case Color.GREEN: return "B"
            case Color.BLUE: return "F"
            case Color.RED: return "R"
            case Color.ORANGE: return "L"
            case _: raise ValueError("Invalid color")

    @staticmethod
    def face_to_col(face: str) -> int:
        """
        U -> YELLOW, F -> BLUE, etc.
        """
        match face:
            case "D": return Color.WHITE
            case "U": return Color.YELLOW
            case "B": return Color.GREEN
            case "F": return Color.BLUE
            case "R": return Color.RED
            case "L": return Color.ORANGE
            case _: raise ValueError("Invalid color")
