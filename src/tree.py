from utils import ordered_load
from constants import ASSET_DIRECTORY
import os.path

class Tree:
    def __init__(self, filename):
        data = ordered_load(open(os.path.join(ASSET_DIRECTORY, 'levels', filename), "r"))
        self.nodes = data["nodes"]
        self.current_node_name = list(self.nodes.keys())[0]
        self.current_action_index = 0

    def pre_update(self, game):
        # obtain current action and arguments
        current_node = self.nodes[self.current_node_name]
        current_action = current_node[self.current_action_index]
        action_func = current_action["type"]
        kwargs = dict(current_action.items())
        del kwargs["type"]

        # call action func with arguments
        getattr(game, action_func)(**kwargs)

    def post_update(self, state):
        # obtain current action name
        current_node = self.nodes[self.current_node_name]
        current_action = current_node[self.current_action_index]
        current_action_name = current_action["type"]

        # return choice
        if current_action_name == "add_pc_choices":
            self.current_node_name = state
            self.current_action_index = 0
        else:
            self.current_action_index += 1
