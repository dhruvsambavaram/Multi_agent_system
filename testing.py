class shape:
    def __init__(self, name):
        self.name = name

class rectangle(shape):
    def __init__(self, length, breadth):
        super().__init__("rectangle")
        self.length = length
        self.breadth = breadth

    def area(self):
        return self.length * self.breadth

if __name__ == "__main__":
    r = rectangle(6, 14)
    area = r.area()
    print(f"Shape: {r.name}")
    print(f"Area: {area}")
