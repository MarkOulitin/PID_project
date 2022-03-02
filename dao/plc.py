class Plc:
    def __init__(self, plc_id, name, type, sim_metadata):
        self.plc_id = plc_id
        self.name = name
        self.type = type
        self.sim_metadata = sim_metadata


def row_to_plc(row):
    return Plc(*tuple(row))
