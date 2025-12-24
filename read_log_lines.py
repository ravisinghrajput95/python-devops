def read_log_lines(filepath):
    """
    Creates a generator that reads a log file, yielding valid, non-comment lines.

    Args:
        filepath (str): The path to the log file.

    Yields:
        str: A stripped, non-empty, non-comment line from the file.
    """
    # 1. Open the file safely
    with open(filepath, "r") as file:
        # 2. Iterate through each line
        for line in file:
            stripped_line = line.strip()

            # Skip empty lines
            if not stripped_line:
                continue

            # Skip comment lines (ignoring leading whitespace)
            if stripped_line.startswith("#"):
                continue

            # 3. Yield valid log line
            yield stripped_line

for log_line in read_log_lines("sample.log"):
    print(log_line)
