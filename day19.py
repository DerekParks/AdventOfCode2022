#!/usr/bin/env python3
import re

class Blueprint:
    def __init__(self, ore_ore, clay_ore, obs_ore, obs_clay, geode_ore, geode_obs):
        self.ore_ore = ore_ore
        self.clay_ore = clay_ore
        self.obs_ore = obs_ore
        self.obs_clay = obs_clay
        self.geode_ore = geode_ore
        self.geode_obs = geode_obs
    
    def __repr__(self) -> str:
        return f"Blueprint(ore_ore={self.ore_ore}, clay_ore={self.clay_ore}, obs_ore={self.obs_ore}, obs_clay={self.obs_clay}, geode_ore={self.geode_ore}, geode_obs={self.geode_obs})"

regex = r".*ore robot costs (\d+) ore.*clay robot costs (\d+) ore.*obsidian robot costs (\d+) ore and (\d+) clay.* geode robot costs (\d+) ore and (\d+) obsidian.*"

def line_to_blueprint(line):
    m = re.match(regex, line.strip())
    assert m, f"Failed to match {line}"
    print(m.groups())
    blueprint = Blueprint(*map(int, m.groups()))
    return blueprint

if __name__ == "__main__":

    if True:
        file_name = "day19_test.txt"  
    else:
        file_name = "day19.txt"

    with open(file_name) as f:
        lines_in = f.readlines()

    blueprints = list(map(line_to_blueprint, lines_in))
    print(blueprints)

