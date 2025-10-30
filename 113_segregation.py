import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)

rng = np.random.default_rng()


class Family:
    def __init__(self, color: str):
        self.color = color
        self.x = round(rng.uniform(),3)
        self.y = round(rng.uniform(),3)

    def move(self, x, y):
        self.x = x
        self.y = y


class Grid:
    families: list[Family] = []

    def populate(self, count):
        for _ in range(count):
            color = 'black' if rng.choice(2) else 'white'
            self.families.append(Family(color))

    def count_same_colored_neighbors(self, family: Family, count: int) -> int:
        closest = sorted(
            self.families,
            key=lambda f: np.sqrt((f.x-family.x)**2 + (f.y-family.y)**2) # euclidean distance
        )[:count+1]

        colors = [f.color for f in closest]
        return colors.count(family.color)

    def get_empty_coordinates(self) -> tuple[float,float]:
        while True:
            x = round(rng.uniform(), 3)
            y = round(rng.uniform(), 3)
            points = [(f.x, f.y) for f in self.families]
            if (x,y) not in points:
                return (x,y)

    def draw(self):
        x = [f.x for f in self.families]
        y = [f.y for f in self.families]
        colors = [f.color for f in self.families]

        sns.scatterplot(x=x,y=y,hue=colors)
        plt.show()

def main():
    P = 1000
    grid = Grid()
    grid.populate(P)
    grid.draw()
    
    for t in range(15000):
        if t % 500 == 0:
            logging.info(f"Period: {t}")
        random_family = grid.families[rng.choice(P)]
        if grid.count_same_colored_neighbors(random_family, 10) < 5:
            new_place = grid.get_empty_coordinates()
            random_family.move(*new_place)


    for family in grid.families:
        if grid.count_same_colored_neighbors(family, 10) < 5:
            logging.warning(f"At the end of the simulation, family in ({family.x},{family.y}) is unhappy")
            


    grid.draw()


if __name__=='__main__':
    main()
