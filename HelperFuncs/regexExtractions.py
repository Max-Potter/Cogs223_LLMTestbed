import re

def get_integer_ratings(statements, responseText):
    integers = re.findall(r"\s*([0-9]+)\s*", responseText)
    integers = [int(entry) for entry in integers]
    ratings = {statements[x]:integers[x] for x in range(len(statements))}
    return ratings

