

#
import random as rnd

class Direction:
    def __init__(self, dirNumber, prob):
        self.__dirNumber = dirNumber
        self.__prob = prob

    @property
    def direction(self):
        return self.__dirNumber

    @property
    def prob(self):
        return self.__prob

def wheel(directions):
    max = sum(direction.prob for direction in directions)
    pick = rnd.uniform(0, max)
    current = 0
    for direction in directions:
        current += direction.prob
        if current > pick:
            return direction


if __name__ == '__main__':
    directionsList = [Direction(1, 20), Direction(2, 15), Direction(3, 5), Direction(4, 60)]
    for i in range(0, 20):
        direction = wheel(directionsList)
        print("try: ", i, " direction #: ", direction.direction, " direction prob ", direction.prob)
