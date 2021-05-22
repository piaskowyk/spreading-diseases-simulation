class SimulationConfig:
    # graphic
    interval = 0.5
    word_size = (10, 10)
    pane_size = (400, 400)

    population_size = 10
    fixed_sick_cases = False
    fixed_cases_count = 3
    create_sick_agent_probability = 0.5

    sickness_cool_down = 10
    sickness_cool_down_variation = 2
    infection_probability = 0.5
    infection_probability_variation = 0.1
    agent_resistance = 0.1
    agent_resistance_variation = 0.1
