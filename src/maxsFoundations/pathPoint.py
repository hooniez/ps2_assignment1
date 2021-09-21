class PathPoint:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.stairsRequired = True if start.y != end.y else False

    def __str__(self):
        return f"PathPoint({self.start}, {self.end})"