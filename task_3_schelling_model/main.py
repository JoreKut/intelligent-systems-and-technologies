from schelling_model import EntitiesFractionConfig, SchellingModel


def main():
    entity_fraction_config = EntitiesFractionConfig(
        red_fraction=0.5,
        blue_fraction=0.5,
    )
    model_map = SchellingModel(
        n=20,
        entity_fraction_config=entity_fraction_config,
        empty_fraction=0.1
    )

    max_iteration_count = 150
    for i in range(max_iteration_count):
        model_map.do_iteration()
        model_map.recalculate_ranks()

        if model_map.is_everyone_satisfied():
            break

    model_map.print_info()


if __name__ == '__main__':
    main()
