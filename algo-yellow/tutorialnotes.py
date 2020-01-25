import gamelib
import random
import math
import warnings
from sys import maxsize
import json


"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips:

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical
  board states. Though, we recommended making a copy of the map to preserve
  the actual current map state.
"""


class TutorialBot(gamelib.AlgoCore):
    def on_game_start(self,config):
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER, UNIT_TO_ID
        FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER = \
        [config['unitInformation'][idx]["shorthand"] for idx in range(6)]

    def on_turn(self, turn_state):
        game_state = gamelib.GameState(self.config, turn_state)
        game_state.enable_warnings = False
        self.defense(game_state)
        self.attack(game_state)

        game_state.submit_turn()

    def build_defences(self, Location_list, firewall_unit, game_state, row = None):
        for location in Location_list:
            if not type(location) == list:
                location = [location, row]

            if game_state.can_spawn(firewall_unit, location):
                game_state.attempt_spawn(firewall_unit, location)
                gamelib.debug_write(f"{firewall_unit} deployed")
                game_state._player_resources[0]['cores'] -= game_state.type_cost(firewall_unit)
            elif not game_state.contains_stationary_unit(location):
                return False

            return True

    def defense(self, game_state):
        filters = [[0,13], [27, 13], [1,12], [26,12]]
        if not self.build_defences(filters, FILTER, game_state):
            return
        row = 11
        destructors = [2, 25, 6, 21, 11, 16]
        if not self.build_defences(destructors, DESTRUCTOR, game_state, row = row):
            return
        row = 13
        filters = [5,6,7,8,9,10]
        if not self.build_defences(destructors, DESTRUCTOR, game_state, row = row):
            return

    def attack(self, game_state):
        pass

if __name__ == "__main__":
    algo = TutorialBot()
    algo.start()
