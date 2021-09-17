class PathPoint:
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end
        self.stairsRequired = True if start.y != end.y else False

    def __str__(self) -> str:
        return f"PathPoint({self.start}, {self.end})"