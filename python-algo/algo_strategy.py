import gamelib
import random
import math
import warnings
from sys import maxsize
import json
import os

"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips:

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical
  board states. Though, we recommended making a copy of the map to preserve
  the actual current map state.
"""



class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        """
        Read in config and perform any initial setup here
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER, BITS, CORES, PLAYERINDEX, OPPONENTINDEX
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]
        BITS = 1
        CORES = 0
        PLAYERINDEX = 0
        OPPONENTINDEX = 1
        # This is a good place to do initial setup
        self.scored_on_locations = []
        self.enemy_unit_death_locations = []
        # self.launch
        # print("i am currrently in", os.getcwd())
        f = open("weights.txt", "r")
        line = f.readline()
        self.weights = list(map(float, line.split(" ")))


    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.

        # launch_pos = [4, 9]

        # num_start_destructors = int(self.weights[0] * 10)
        # self.build_defences([random.randint(3, 24) for i in range(num_start_destructors)], DESTRUCTOR, game_state, row=10)

        num_launch_pos = 28

        num_pos = int(self.weights[1] * num_launch_pos)
        edge_locs = [[[i, 13 - i]] for i in range(14)] + [[[i, i - 14]] for i in range(14, 27)]
        # gamelib.debug_write("There are {} launch_pos".format(len(edge_locs)))
        gamelib.debug_write("launchs pos are {}".format(edge_locs))
        launch_pos = edge_locs[num_pos]

        # print("launch_pos is ", launch_pos)
        gamelib.debug_write("Trying to launch at {}".format(launch_pos))
        # if game_state.get_resources(0)[0] > 0:
        num_spawned = game_state.attempt_spawn(PING, launch_pos, 30)
        gamelib.debug_write("spawned {} at launch_pos {} ".format(num_spawned, launch_pos))


        # for location in self.scored_on_locations:
        #     # Build destructor one space above so that it doesn't block our own edge spawn locations
        #     if location[0] >= 14:
        #         build_location = [location[0] - 2, location[1]+2]
        #     else:
        #         build_location = [location[0] + 2, location[1]+2]
        #
        #
        #     game_state.attempt_spawn(DESTRUCTOR, build_location)
        #     game_state.attempt_spawn(SCRAMBLER, location)
        #
        # if game_state.turn_number >= 2:
        #     filter_row = self.get_enemy_front_row(game_state, DESTRUCTOR) - 3
        #     if filter_row <= 13:
        #         filter_locations = [i for i in range(13 - filter_row, 23 - (13 - filter_row) * 2)]
        #         if game_state.get_resources(0)[0] > len(filter_locations):
        #             self.build_defences(filter_locations, FILTER, game_state, filter_row)
        #             game_state.attempt_spawn(EMP, [launch_pos], 2)
        #     else:
        #         # print("check ", game_state.get_resources(0)[0])
        #         if game_state.get_resources(0)[0] > 6:
        #             game_state.attempt_spawn(PING, [launch_pos], 15)
        #
        # if game_state.turn_number >= 4 and game_state.get_resources(0)[1] > 8:
        #     encrpytor_locations = [[launch_pos[0] + 1 + k, launch_pos[1] - 1] for k in range(3)]
        #     game_state.attempt_spawn(ENCRYPTOR, encrpytor_locations)
        game_state.submit_turn()


    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """

    def starter_strategy(self, game_state):
        """Imitating Madroxfactor4 boss
        """
        # First, place base defenses
        if game_state.turn_number >= 0: #If already there, rebuild destroyed defenses
            row = 13
            destructor_locations = [2,3,10,17,24,25]
            self.build_defences(destructor_locations, DESTRUCTOR, game_state, row = row)
        # Filters and additional defenses:
        if game_state.turn_number >= 4:
            #Calculate the filters so EMP is 4 or 5 away from enemy destructor, but not in range of destructor
            filter_row = self.get_enemy_front_row(game_state, DESTRUCTOR) - 3
            #filter_locations = [5,6,7,8,9,11,12,13,14,15,16,18,19,20,21,22,23, 26, 27] #19 filters in total
            filter_locations = [i for i in range(13-filter_row, 23 - (13-filter_row)*2)]
            self.build_defences(filter_locations, FILTER, game_state, row = filter_row)
            #game_state.attempt_upgrade(destructor_locations)
            encryptor_locations = [5,6]
            encryptor_row = 8
            self.build_defences(encryptor_locations, ENCRYPTOR, game_state, row = encryptor_row)
            if filter_row == 13:
                additional_filters_locations = [26, 27]
                self.build_defences(additional_filters_locations, FILTER, game_state, filter_row)

            additional_destructor_locations = [[25,12],[24, 11], [24, 10], [10, 11], [21,8],
                                               [17,11], [12,9], [15,9], [12,6], [15,6]]
            additional_encryptor_locations = [[7,8], [3,10],[4,10], [5, 10], [6,10]]
            for j in range(len(additional_encryptor_locations)):
                self.build_defences([additional_destructor_locations[j]], DESTRUCTOR, game_state)
                self.build_defences([additional_encryptor_locations[j]], ENCRYPTOR, game_state)
            #Build as much as remaining destructors as possible
            self.build_defences([additional_destructor_locations], DESTRUCTOR, game_state)
        #encryptor at [24,10]

        #Attack:
        if game_state.turn_number % 8 == 1:
            # To simplify we will just check sending them from back left and right
            ping_spawn_location_options = [[4, 9], [6, 7]]
            best_location = self.least_damage_spawn_location(game_state, ping_spawn_location_options)
            game_state.attempt_spawn(PING, best_location, 15)

        if game_state.turn_number >= 4:
            game_state.attempt_spawn(EMP, [4, 9], 10)

    def get_enemy_front_row(self, game_state, unit_type = None):
        front_row = 17
        for row in range(14, 16):
            for col in range(3 + row-14, 27 - 3 - (row-14)):
                if game_state.contains_stationary_unit([col, row]):
                    for unit in game_state.game_map[col, row]:
                        if unit.player_index == 1 \
                                and (unit_type is None or unit.unit_type == unit_type):
                            return row
        return front_row

    def build_defences(self, location_list, firewall_unit, game_state, row = None):
        for location in location_list:
            if not type(location) == list:
                location = [location, row]

            #if game_state.can_spawn(firewall_unit, location):
            game_state.attempt_spawn(firewall_unit, location)

        return True

    def build_reactive_defense(self, game_state):
        """
        This function builds reactive defenses based on where the enemy scored on us from.
        We can track where the opponent scored by looking at events in action frames
        as shown in the on_action_frame function
        """
        for location in self.scored_on_locations:
            # Build destructor one space above so that it doesn't block our own edge spawn locations
            build_location = [location[0], location[1]+1]
            game_state.attempt_spawn(DESTRUCTOR, build_location)

    def stall_with_scramblers(self, game_state):
        """
        Send out Scramblers at random locations to defend our base from enemy moving units.
        """
        # We can spawn moving units on our edges so a list of all our edge locations
        friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)

        # Remove locations that are blocked by our own firewalls
        # since we can't deploy units there.
        deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)

        # While we have remaining bits to spend lets send out scramblers randomly.
        while game_state.get_resource(BITS) >= game_state.type_cost(SCRAMBLER)[BITS] and len(deploy_locations) > 0:
            # Choose a random deploy location.
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]

            game_state.attempt_spawn(SCRAMBLER, deploy_location)
            """
            We don't have to remove the location since multiple information
            units can occupy the same space.
            """

    def emp_line_strategy(self, game_state):
        """
        Build a line of the cheapest stationary unit so our EMP's can attack from long range.
        """
        # First let's figure out the cheapest unit
        # We could just check the game rules, but this demonstrates how to use the GameUnit class
        stationary_units = [FILTER, DESTRUCTOR, ENCRYPTOR]
        cheapest_unit = FILTER
        for unit in stationary_units:
            unit_class = gamelib.GameUnit(unit, game_state.config)
            if unit_class.cost[game_state.BITS] < gamelib.GameUnit(cheapest_unit, game_state.config).cost[game_state.BITS]:
                cheapest_unit = unit

        # Now let's build out a line of stationary units. This will prevent our EMPs from running into the enemy base.
        # Instead they will stay at the perfect distance to attack the front two rows of the enemy base.
        for x in range(27, 5, -1):
            game_state.attempt_spawn(cheapest_unit, [x, 11])

        # Now spawn EMPs next to the line
        # By asking attempt_spawn to spawn 1000 units, it will essentially spawn as many as we have resources for
        game_state.attempt_spawn(EMP, [24, 10], 1000)

    def least_damage_spawn_location(self, game_state, location_options):
        """
        This function will help us guess which location is the safest to spawn moving units from.
        It gets the path the unit will take then checks locations on that path to
        estimate the path's damage risk.
        """
        damages = []
        # Get the damage estimate each path will take
        for location in location_options:
            path = game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                # Get number of enemy destructors that can attack the final location and multiply by destructor damage
                damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(DESTRUCTOR, game_state.config).damage_i
            damages.append(damage)

        # Now just return the location that takes the least damage
        return location_options[damages.index(min(damages))]

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x = None, valid_y = None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if unit.player_index == 1 and (unit_type is None or unit.unit_type == unit_type) and (valid_x is None or location[0] in valid_x) and (valid_y is None or location[1] in valid_y):
                        total_units += 1
        return total_units

    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at: https://docs.c1games.com/json-docs.html
        """
        # Let's record at what position we get scored on
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        deaths = events["death"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            # When parsing the frame data directly,
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                # gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append(location)
                # gamelib.debug_write("All locations: {}".format(self.scored_on_locations))
        for death in deaths:
            # print("death: ", death)
            location = death[0]
            unit_owner_self = True if death[3] == 1 else False
            # When parsing the frame data directly,
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                # gamelib.debug_write("Enemy unit died at: {}".format(location))
                self.enemy_unit_death_locations.append(location)
                # gamelib.debug_write("All locations: {}".format(self.scored_on_locations))


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
