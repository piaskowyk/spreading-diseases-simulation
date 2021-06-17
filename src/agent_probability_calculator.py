from src.simulation_config import SimulationConfig
from src.util import get_value_with_variation


def calculate_sickness_duration():
    return get_value_with_variation(
        SimulationConfig.sickness_duration,
        SimulationConfig.sickness_duration_variation,
        True
    )


def calculate_infection_probability():
    return get_value_with_variation(
        SimulationConfig.infection_probability,
        SimulationConfig.infection_probability_variation
    )


def calculate_resistance():
    return get_value_with_variation(
        SimulationConfig.agent_resistance,
        SimulationConfig.agent_resistance_variation
    )


def calculate_infection_duration():
    return get_value_with_variation(
        SimulationConfig.infection_duration,
        SimulationConfig.infection_duration_variation,
        True
    )


def calculate_recovered_duration():
    return get_value_with_variation(
        SimulationConfig.recovered_duration,
        SimulationConfig.recovered_duration_variation,
        True
    )


def calculate_death_probability():
    return get_value_with_variation(
        SimulationConfig.death_probability,
        SimulationConfig.death_probability_variation
    )


def calculate_cough_probability():
    return get_value_with_variation(
        SimulationConfig.cough_probability,
        SimulationConfig.cough_probability_variation
    )


def calculate_sneeze_probability():
    return get_value_with_variation(
        SimulationConfig.sneeze_probability,
        SimulationConfig.sneeze_probability_variation
    )


def calculate_symptoms_probability():
    return get_value_with_variation(
        SimulationConfig.has_symptoms_probability,
        SimulationConfig.has_symptoms_probability_variation
    )

