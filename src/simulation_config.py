class SimulationConfig:
    interval = 0
    word_size = (10, 10)
    pane_size = (400, 400)

    population_size = 10
    fixed_sick_cases = False
    fixed_cases_count = 3
    create_sick_agent_probability = 0.5

    cough_radius = 3
    sneeze_radius = 6

    sickness_duration = 10
    sickness_duration_variation = 2
    infection_probability = 0.5
    infection_probability_variation = 0.1
    agent_resistance = 0.1
    agent_resistance_variation = 0.1
    infection_duration = 5
    infection_duration_variation = 1
    recovered_duration = 5
    recovered_duration_variation = 1
    death_probability = 0.01
    death_probability_variation = 0.01
    cough_probability = 0.1
    cough_probability_variation = 0.1
    sneeze_probability = 0.1
    sneeze_probability_variation = 0.1
    has_symptoms_probability = 0.1
    has_symptoms_probability_variation = 0.1
