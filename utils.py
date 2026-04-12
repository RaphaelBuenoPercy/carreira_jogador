import random

def clamp(value, min_value=0, max_value=100):
    return max(min_value, min(max_value, value))

def weighted_choice(prob):
    return random.random() < prob