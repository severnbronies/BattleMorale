from utils import get_ordered_yaml


class Tree:
    def __init__(self, filename):
        data = get_ordered_yaml("levels", filename)
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
