class SimulationConfig:
    interval = 0
    word_size = (400, 400)
    pane_size = (800, 800)

    population_size = 10000
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
    has_symptoms_probability = 0.8
    has_symptoms_probability_variation = 0.1
    quarantine_probability = 0.7
    quarantine_duration = 10
    wearing_mask_probability = 0.5
    wearing_mask_self_protection_factor = 0.15
    wearing_mask_other_protection_factor = 0.7
    symptom_infection_factor = 0.2
    symptom_protection_factor = 0.2
    talk_probability = 0.1
    talk_infection_probability_factor = 0.3
    talk_duration = 5
    talk_duration_variation = 3
    stand_probability = 0.2
