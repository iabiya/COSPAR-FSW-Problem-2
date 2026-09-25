from counter import Counters


def test_counters_start_at_zero():
    counters = Counters()

    status = counters.get_status()

    assert status["telecommands_received"] == 0
    assert status["telecommands_rejected"] == 0
    assert status["frames_accepted"] == 0
    assert status["frames_rejected"] == 0
    assert status["packets_accepted"] == 0
    assert status["packets_rejected"] == 0


def test_counters_increment():
    counters = Counters()

    counters.tc_received()
    counters.tc_rejected()
    counters.frame_accepted()
    counters.frame_rejected()
    counters.packet_accepted()
    counters.packet_rejected()

    status = counters.get_status()

    assert status["telecommands_received"] == 1
    assert status["telecommands_rejected"] == 1
    assert status["frames_accepted"] == 1
    assert status["frames_rejected"] == 1
    assert status["packets_accepted"] == 1
    assert status["packets_rejected"] == 1