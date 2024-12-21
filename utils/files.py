import re


def split_and_map(func, split_on, lines):
    """
    Splits each line on the given delimiter and maps a function to each split element.

    Args:
        func (callable): Function to apply to each element after splitting.
        split_on (str): Delimiter to split each line.
        lines (list): List of strings to process.

    Returns:
        list: List of processed lines as lists of mapped elements.
    """
    result = []
    for line in lines:
        if line.strip():  # Skip empty lines
            split_line = line.split(split_on)
            if len(split_line) > 1 or split_on in line:
                result.append(list(map(func, split_line)))
            else:
                result.append([func(line)])
    return result


def read_data(day, file):
    """
    Reads the content of a data file.

    Args:
        day (int): Day of the challenge.
        file (str): Filename to read.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an issue reading the file.
    """
    try:
        with open(f"./data/{day}_{file}", "r") as file:
            return file.read().strip()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e.filename}")
    except IOError as e:
        raise IOError(f"Error reading file: {e}")


def read_data_as_lines(day, file, clean_line=True):
    """
    Reads the content of a data file and splits it into lines.

    Args:
        day (int): Day of the challenge.
        file (str): Filename to read.
        clean_line (bool): Whether to strip whitespace from each line.

    Returns:
        list: List of lines in the file.
    """
    lines = read_data(day, file).splitlines()
    return [line.strip() for line in lines if line.strip()] if clean_line else lines


def parse_with_regex(day, file, pattern):
    """
    Parses a file using a regex pattern.

    Args:
        day (int): Day of the challenge.
        file (str): Filename to read.
        pattern (str): Regex pattern to match lines.

    Returns:
        list: Matches found in the file.
    """
    content = read_data(day, file)
    return re.findall(pattern, content)
