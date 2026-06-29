import sys

if __name__ == "__main__":
    agent = CivicAuditorAgent()
    # Check if a log message was passed via command line
    if len(sys.argv) > 2 and sys.argv[1] == "--log":
        command_log = sys.argv[2]
        agent.audit_event("SHELL_EXEC", {"cmd": command_log}, "RECORDED")
    else:
        agent.audit_event("SYSTEM_INIT", {"status": "ACTIVE"}, "SUCCESS")
