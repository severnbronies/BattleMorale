import yaml
from collections import OrderedDict
import os.path
from constants import ASSET_DIRECTORY


def get_ordered_yaml(*location):
    class OrderedLoader(yaml.Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)

    return get_yaml(*location, loader=OrderedLoader)


def get_yaml(*location, loader=yaml.Loader):
    return yaml.load(open(os.path.join(ASSET_DIRECTORY, *location)), loader)
