# Counters for the Telecommand Reception and Routing system


class Counters:

    def __init__(self):
        self.telecommands_received = 0
        self.telecommands_rejected = 0

        self.frames_accepted = 0
        self.frames_rejected = 0

        self.packets_accepted = 0
        self.packets_rejected = 0

    # -------------------------------
    # Telecommand counters
    # -------------------------------

    def tc_received(self):
        self.telecommands_received += 1

    def tc_rejected(self):
        self.telecommands_rejected += 1

    # -------------------------------
    # Frame counters
    # -------------------------------

    def frame_accepted(self):
        self.frames_accepted += 1

    def frame_rejected(self):
        self.frames_rejected += 1

    # -------------------------------
    # Packet counters
    # -------------------------------

    def packet_accepted(self):
        self.packets_accepted += 1

    def packet_rejected(self):
        self.packets_rejected += 1

    # -------------------------------
    # Get all counter values
    # -------------------------------

    def get_status(self):

        return {
            "telecommands_received": self.telecommands_received,
            "telecommands_rejected": self.telecommands_rejected,

            "frames_accepted": self.frames_accepted,
            "frames_rejected": self.frames_rejected,

            "packets_accepted": self.packets_accepted,
            "packets_rejected": self.packets_rejected,
        }