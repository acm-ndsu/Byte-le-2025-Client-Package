import random

from game.engine import Engine
from game.utils.generate_game import generate


if __name__ == '__main__':
    # for x in range(100):
    #     print(f'\n\nStarting game {x + 1}\n\n')
    generate(random.randint(0, 1000000000))
    engine = Engine(False)
    engine.loop()