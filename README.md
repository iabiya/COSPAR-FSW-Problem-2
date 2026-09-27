# COSPAR-I Program 2026 – FSW Problem 2

## Onboard Telecommand Reception and Routing

This project implements a software prototype for **Problem Statement 2 – Onboard Telecommand Reception and Routing** of the COSPAR-I Program 2026 FSW challenge.

The system processes a development telecommand byte stream, detects and validates the telecommand frame, extracts and validates the Space Packet, routes the packet using its APID, dispatches commands using Service/Subtype, executes the corresponding handler, and generates PUS-C verification reports.

---

## 1. Architecture

```text
Incoming Telecommand Stream
            |
            v
     Frame Detection
            |
            v
     Frame Validation
     - Start Sequence
     - Tail Sequence
     - Credentials
            |
            v
    Space Packet Decoder
            |
            v
    Packet Validation
     - Version
     - Type
     - Data Length
     - CRC
            |
            v
      PUS-C Validation
     - PUS Version
     - Service
     - Subtype
            |
            v
        APID Routing
            |
            v
 Service / Subtype Dispatch
            |
            v
      Command Handler
            |
            v
    Verification Report
            |
            v
       Counters / Logs