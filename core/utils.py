def extract_headers(headers):
    """
    parses headers provided through command line
    returns dict
    """
    headers = headers.replace('\\n', '\n')
    return parse_headers(headers)


def parse_headers(string):
    """
    parses headers
    return dict
    """
    result = {}
    for line in string.split('\n'):
        if len(line) > 1:
            splitted = line.split(':')
            result[splitted[0]] = ':'.join(splitted[1:]).strip()
    return result
