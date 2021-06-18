import random
import numpy


def get_it_with_probability(probability: float, item_a, item_b):
    return item_a if random.randint(1, 100) <= probability * 100 else item_b


def get_with_probability(items: list, probability: list[float]):
    return numpy.random.choice(items, p=probability)


def is_with_probability(probability: float):
    return numpy.random.choice([True, False], p=[probability, 1 - probability])


def rand_from_set(items: list):
    if len(items) == 0:
        return None
    return items[random.randint(0, len(items) - 1)]


def get_value_with_variation(value, variation, to_int=False):
    if value - variation < 0:
        raise Exception("value - variation < 0")
    if to_int:
        return random.randint(value - variation, value + variation)
    return random.uniform(value - variation, value + variation)
