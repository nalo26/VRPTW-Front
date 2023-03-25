def parse_header(content):
    data = {}
    for line in content.split("\n"):
        s = line.split(":")
        value = s[1].strip()
        data[s[0].strip()] = int(value) if value.isnumeric() else value

    return data


def parse_depots(content):
    data = {}
    for line in content.split("\n")[1:]:
        id_name, x, y, ready_time, due_time = line.split()
        data[id_name] = {
            "x": int(x),
            "y": int(y),
            "ready_time": int(ready_time),
            "due_time": int(due_time),
        }

    return data


def parse_clients(content):
    data = {}
    for line in content.split("\n")[1:]:
        if line == "":
            continue
        id_name, x, y, ready_time, due_time, demand, service = line.split()
        data[id_name] = {
            "x": int(x),
            "y": int(y),
            "ready_time": int(ready_time),
            "due_time": int(due_time),
            "demand": int(demand),
            "service": int(service),
        }

    return data


def parse(file_path):
    data = {}
    with open(file_path, "r") as f:
        content = f.read().split("\n\n")
        data["headers"] = parse_header(content[0])
        data["depots"] = parse_depots(content[1])
        data["clients"] = parse_clients(content[2])

    return data
