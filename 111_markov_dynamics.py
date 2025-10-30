import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

rng = np.random.default_rng()

class Person:
    transition_matrix = np.array([
        # poor, middle rich
        [0.9, 0.1, 0.0], # poor
        [0.4, 0.2, 0.4], # middle
        [0.1, 0.1, 0.8], #rich
    ])

    def __init__(self, state: int):
        self.state = state #0=poor,1=middle,2=rich
        self.history = []
        logger.debug('created a person')

    def change(self):
        probs = self.transition_matrix[self.state]
        self.history.append(self.state)
        self.state = rng.choice((0,1,2), p=probs)


def main():
    # set parameters
    N = 1000
    psi_0 = (0.0, 1.0, 0.0)

    # randomly draw states
    initial_states = rng.choice((0,1,2), N, p=psi_0)
    
    # create people
    people = []
    for i in initial_states:
        person = Person(i)
        people.append(person)

    # run for 100 periods
    T = 100
    for t in range(T):
        logger.info(f"round {t}")
        for person in people:
            person.change()

    # get results
    final_states = [person.state for person in people]

    # plot histogram (cross sectional at last time step)
    sns.histplot(final_states)
    plt.show()

    # plot histogram (time series)
    sns.histplot(people[1].history)
    plt.show()


if __name__=='__main__':
    main()
