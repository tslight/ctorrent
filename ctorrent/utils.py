def get_hr_size(bytes):
    """
    Return the given bytes as a human friendly KB, MB, GB, or TB string
    """
    bytes = float(bytes)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    if bytes < KB:
        return "{0} {1}".format(bytes, "Bytes" if 0 == bytes > 1 else "Byte")
    elif KB <= bytes < MB:
        return "{0:.2f} KB".format(bytes / KB)
    elif MB <= bytes < GB:
        return "{0:.2f} MB".format(bytes / MB)
    elif GB <= bytes < TB:
        return "{0:.2f} GB".format(bytes / GB)
    elif TB <= bytes:
        return "{0:.2f} TB".format(bytes / TB)


def get_longest_list_in_dict(dictionary):
    """
    Return the longest list in a dictionary of lists.
    """
    lengths = [len(v) for k, v in dictionary.items()]
    return max(lengths)


def list_of_dicts_to_dict_of_lists(list_of_dicts, key_order):
    """
    Transform a list of dictionaries into a dictionary of lists.
    """
    keys = list(set().union(*(list(d.keys()) for d in list_of_dicts)))
    columns = {}

    for key in keys:
        columns[key] = [d[key] for d in list_of_dicts if key in d]

    return {k: columns[k] for k in key_order}
