def parse_log_line(log_line: str):
    # Check for None or empty string
    if not log_line or not isinstance(log_line, str):
        return None

    parts = log_line.split(" ", 2)  # split into max 3 parts: timestamp, [LEVEL], message

    # Must have at least 3 parts
    if len(parts) < 3:
        return None

    timestamp, log_level_raw, message = parts

    # log_level must be inside [ ]
    if not (log_level_raw.startswith("[") and log_level_raw.endswith("]")):
        return None

    # Remove brackets: [INFO] -> INFO
    log_level = log_level_raw[1:-1]

    return {
        "timestamp": timestamp,
        "log_level": log_level,
        "message": message
    }

parse_log_line("2024-05-20T13:45:10Z [INFO] User logged in")
