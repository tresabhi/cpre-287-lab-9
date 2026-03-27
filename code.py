import simulation
import time
import utils
import node_config
import sensing

if __name__ == "__main__":
    sim = simulation.get_instance()

    while True:
        sim.loop()
        time.sleep(0)

        values = [
            f"t = {sim.last_t:.2f}s\t",
            f"Outside: {utils.c_to_f(sim.outside_temp):.2f}°f",
        ]

        for zone in range(node_config.num_zones):
            values.append(
                f"{node_config.zone_names[zone]}: {sensing.get_current_temperature_f(zone):.2f}°f"
            )

        values += [
            f"Heating: {sim.heating}",
            f"Cooling: {sim.cooling}",
        ]

        for zone in range(node_config.num_zones):
            # values.append(f"theta_{zone} = {sim.angles[zone]:.2f}")
            values.append(f"x_{zone} = {sim.xs[zone]:.2f}")

        print("\t".join(values))
