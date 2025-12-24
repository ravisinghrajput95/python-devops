def read_config_file(filepath):
    """
    Validates the filepath and yields each line from the file.

    Args:
        filepath (str): The path to the configuration file.

    Yields:
        str: A single line from the file.
    """
    with open(filepath, "r") as file:
        for line in file:
            yield line



def filter_config_lines(lines):
    """
    Filters an iterable of lines, yielding stripped, non-empty, non-comment lines.

    Args:
        lines (iterable): An iterable producing string lines.

    Yields:
        str: A line that is not a comment or empty.
    """
    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        # Skip comments (even if indented)
        if stripped.startswith("#"):
            continue

        yield stripped



def parse_config_lines(lines):
    """
    Parses an iterable of clean config lines into (section, key, value) tuples.

    Args:
        lines (iterable): An iterable producing clean config lines.

    Yields:
        tuple: A tuple in the format (section, key, value).
    """
    current_section = None

    for line in lines:
        # Section header
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip()
            continue

        # Key-value pair
        if "=" in line:
            key, value = line.split("=", 1)
            yield (current_section, key.strip(), value.strip())


lines = read_config_file("config.conf")
filtered = filter_config_lines(lines)
parsed = parse_config_lines(filtered)

for item in parsed:
    print(item)
