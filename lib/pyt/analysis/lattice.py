from lib.pyt.analysis.constraint_table import constraint_table
from lib.pyt.core.node_types import AssignmentNode


def get_lattice_elements(cfg_nodes):
    """Returns all assignment nodes as they are the only lattice elements
    in the reaching definitions analysis.
    """
    for node in cfg_nodes:
        if isinstance(node, AssignmentNode):
            yield node


class Lattice:
    def __init__(self, cfg_nodes):
        self.el2bv = {}
        self.bv2el = []
        for i, e in enumerate(get_lattice_elements(cfg_nodes)):
            # Give each element a unique shift of 1
            self.el2bv[e] = 0b1 << i
            self.bv2el.insert(0, e)

    def get_elements(self, number):
        if number == 0:
            return []

        # Turn number into a binary string of length len(self.bv2el)
        binary_string = format(number, f"0{len(self.bv2el)}b")
        return [self.bv2el[i] for i, bit in enumerate(binary_string) if bit == "1"]

    def in_constraint(self, node1, node2):
        """Checks if node1 is in node2's constraints
        For instance, if node1 = 010 and node2 = 110:
        010 & 110 = 010 -> has the element."""
        constraint = constraint_table[node2]
        if constraint == 0b0:
            return False

        try:
            value = self.el2bv[node1]
        except KeyError:
            return False

        return constraint & value != 0
