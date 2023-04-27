def parse_header(content):
    data = {}
    for line in content.split("\n"):
        s = line.split(":")
        value = s[1].strip()
        data[s[0].strip()] = int(value) if value.isnumeric() else value

    return data


def parse_depot(content):
    id_name, x, y, ready_time, due_time = content.split("\n")[1].split()
    data = {
        "id_name": id_name,
        "x": int(x),
        "y": int(y),
        "ready_time": int(ready_time),
        "due_time": int(due_time),
    }
    return data


def parse_clients(content):
    data = []
    for line in content.split("\n")[1:]:
        if line == "":
            continue
        id_name, x, y, ready_time, due_time, demand, service = line.split()
        data.append(
            {
                "id_name": id_name,
                "x": int(x),
                "y": int(y),
                "ready_time": int(ready_time),
                "due_time": int(due_time),
                "demand": int(demand),
                "service": int(service),
            }
        )

    return data


def parse(content):
    data = {}
    content = content.split("\r\n\r\n") if "\r" in content else content.split("\n\n")
    data["headers"] = parse_header(content[0])
    data["clients"] = parse_clients(content[2])
    data["clients"].insert(0, parse_depot(content[1]))

    return data
