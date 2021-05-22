import random
import numpy


def get_it_with_probability(probability: float, item_a, item_b):
    return item_a if random.randint(1, 100) <= probability * 100 else item_b


def get_with_probability(items: list, probability: list[float]):
    return numpy.random.choice(items, p=probability)


def is_with_probability(probability: float):
    return numpy.random.choice([True, False], p=[probability, 1 - probability])


def rand_from_set(items: list):
    return items[random.randint(0, len(list) - 1)]
