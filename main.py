# Main Telecommand Reception and Routing System


from frame import (extract_space_packet, extract_frame_from_stream, extract_all_frames_from_stream,
    FrameError
)

from decoder import (
    decode_space_packet,
    decode_pus_secondary_header,
    DecodeError
)

from validator import (
    validate_space_packet,
    validate_pus_header,
    ValidationError
)

from router import (
    route_apid,
    dispatch,
    RoutingError
)

from verification import (
    handler_entry,
    handler_success,
    handler_failure
)

from counter import Counters

from state_machine import StateMachine, ReceiverState

from logger_config import setup_logger

from packet_builder import build_space_packet

from frame import build_frame


# -----------------------------------------
# Create system counters
# -----------------------------------------

counters = Counters()

state_machine = StateMachine()

logger = setup_logger()

def process_frame(frame):
    print("\n================================")
    print(" RECEIVING TELECOMMAND FRAME")
    print("================================")

    state_machine.set_state(ReceiverState.WAITING_FOR_START)
    logger.info("Telecommand received")

    counters.tc_received()
    

    try:
        state_machine.set_state(ReceiverState.RECEIVING_FRAME)
        
        print("State:", state_machine.get_state().name)

        # -----------------------------------------
        # 1. Extract Space Packet from frame
        # -----------------------------------------

        packet = extract_space_packet(frame)

        counters.frame_accepted()
        
        logger.info("Telecommand frame accepted")

        print("\nFrame accepted")


        # -----------------------------------------
        # 2. Decode Space Packet
        # -----------------------------------------
        state_machine.set_state(ReceiverState.VALIDATING_FRAME)
        print("State:", state_machine.get_state().name)

        decoded = decode_space_packet(packet)

        print("\nSpace Packet decoded")

        print("APID:", decoded["apid"])
        print("Version:", decoded["version"])
        print("Type:", decoded["type"])


        # -----------------------------------------
        # 3. Validate Space Packet
        # -----------------------------------------

        validate_space_packet(
            packet,
            decoded
        )

        print("Space Packet validation: SUCCESS")
        
        logger.info("Space Packet validation successful")


        # -----------------------------------------
        # 4. Decode PUS-C header
        # -----------------------------------------

        pus_header = decode_pus_secondary_header(
            decoded["data"]
        )

        print("\nPUS-C Header")

        print(
            "PUS Version:",
            hex(pus_header["pus_version"])
        )

        print(
            "Service:",
            pus_header["service"]
        )

        print(
            "Subtype:",
            pus_header["subtype"]
        )


        # -----------------------------------------
        # 5. Validate PUS-C header
        # -----------------------------------------

        validate_pus_header(
            pus_header
        )

        print("PUS-C validation: SUCCESS")
        
        state_machine.set_state(ReceiverState.EXTRACTING_PACKET)
        print("State:", state_machine.get_state().name)


        # -----------------------------------------
        # 6. Route by APID
        # -----------------------------------------
        
        state_machine.set_state(ReceiverState.ROUTING)
        print("State:", state_machine.get_state().name)

        application = route_apid(
            decoded["apid"]
        )

        print("\nAPID Routing")

        print(
            f"APID {decoded['apid']} -> {application}"
        )
        
        logger.info(
            f"APID {decoded['apid']} routed to {application}")


        # -----------------------------------------
        # 7. Packet accepted
        # -----------------------------------------

        counters.packet_accepted()


        # -----------------------------------------
        # 8. Generate ST[1,3]
        # -----------------------------------------

        entry_report = handler_entry(
            pus_header["service"],
            pus_header["subtype"]
        )

        print("\nST[1,3] Handler Entry")

        print(entry_report)
        
        print("ST[1,3] Packet:")
        
        print(entry_report["packet"].hex())


        # -----------------------------------------
        # 9. Dispatch command
        # -----------------------------------------
        
        state_machine.set_state(ReceiverState.DISPATCHING)
        print("State:", state_machine.get_state().name)
        logger.info(
            f"Dispatching Service={pus_header['service']}, "
            f"Subtype={pus_header['subtype']}"
            )

        result = dispatch(
            pus_header["service"],
            pus_header["subtype"],
            pus_header["user_data"],
            counters
        )

        print("\nHandler Result")

        print(result)
        
        if "response_packet" in result:
            print("\nST[17,2] Response Packet Generated")
            print(result["response_packet"].hex())


        # -----------------------------------------
        # 10. Generate ST[1,7] or ST[1,8]
        # -----------------------------------------

        if result["status"] == "SUCCESS":
            logger.info("Telecommand handler executed successfully")

            success_report = handler_success(
                pus_header["service"],
                pus_header["subtype"]
            )

            print("\nST[1,7] Handler Success")

            print(success_report)
            
            print("ST[1,7] Packet:")
            
            print(success_report["packet"].hex())

        else:

            failure_report = handler_failure(
                pus_header["service"],
                pus_header["subtype"],
                "COMMAND_FAILED"
            )

            print("\nST[1,8] Handler Failure")

            print(failure_report)
            
            print("ST[1,8] Packet:")
            
            print(failure_report["packet"].hex())
            
        state_machine.set_state(ReceiverState.COMPLETE)
        print("State:", state_machine.get_state().name)

        return result



    except FrameError as error:
        
        state_machine.set_state(ReceiverState.ERROR)
        print("State:", state_machine.get_state().name)
        logger.error(f"Frame rejected: {error}")

        counters.frame_rejected()
        counters.tc_rejected()

        print("\nFRAME REJECTED")
        print("Reason:", error)

        return {
            "status": "FAILURE",
            "message": str(error)
        }


    except (
        DecodeError,
        ValidationError,
        RoutingError
    ) as error:
        
        state_machine.set_state(ReceiverState.ERROR)
        print("State:", state_machine.get_state().name)
        logger.error(f"Telecommand rejected: {error}")

        counters.packet_rejected()
        counters.tc_rejected()

        print("\nTELECOMMAND REJECTED")
        print("Reason:", error)

        failure_report = handler_failure(
            0,
            0,
            str(error)
        )

        print("\nST[1,8] Failure Report")

        print(failure_report)

        return {
            "status": "FAILURE",
            "message": str(error)
        }


# =========================================
# STREAM PROCESSING
# =========================================

# Create a test Space Packet
def process_stream(stream: bytes):
    """
    Process a noisy incoming telecommand byte stream.
    """

    try:
        logger.info("Searching for telecommand frame in uplink stream")

        frame = extract_frame_from_stream(stream)

        logger.info("Telecommand frame detected")

        return process_frame(frame)

    except FrameError as error:
        logger.error(f"Stream processing failed: {error}")

        state_machine.set_state(ReceiverState.ERROR)

        counters.tc_rejected()

        return {
            "status": "FAILURE",
            "message": str(error)
        }
        
def process_multiple_frames(stream: bytes):
    """
    Find and process all complete telecommand frames
    present in a noisy uplink stream.
    """

    try:
        logger.info("Searching for multiple telecommand frames")

        frames = extract_all_frames_from_stream(stream)

        results = []

        for frame in frames:
            result = process_frame(frame)
            results.append(result)

        logger.info(
            f"Processed {len(results)} telecommand frame(s)"
        )

        return results

    except FrameError as error:
        logger.error(f"Multiple-frame processing failed: {error}")

        state_machine.set_state(ReceiverState.ERROR)

        counters.tc_rejected()

        return [{
            "status": "FAILURE",
            "message": str(error)
        }]
# =========================================
# DEVELOPMENT TEST
# =========================================
if __name__ == "__main__":
    test_packet = build_space_packet(
        apid=17,
        service=17,
        subtype=1,
        user_data=b"PING"
    )

    test_frame = build_frame(test_packet)
    result = process_frame(test_frame)

    print("\n================================")
    print(" SYSTEM COUNTERS")
    print("================================")
    print(counters.get_status())