import yaml


def parse_vars(data, dependency_data):

    if isinstance(data, dict):
        for k, v in data.iteritems():
            data[k] = parse_vars(v, dependency_data)
    if isinstance(data, list):

        tmp = []
        for v in data:
            tmp.append(parse_vars(v, dependency_data))
        data = tmp

    if isinstance(data, str):
        if data.startswith('$'):
            key = data[1:].split(":", 1)[0]

            if not dependency_data.get(key):
                raise Exception("dependency_data did not contain '%s'" % key)
            return {data[1:]: dependency_data.get(key)}

    return data


def power_yaml(file, base_dir="easypc/data"):

    base = yaml.load(open("%s/%s" % (base_dir, file), 'r'))

    dependency_data = {}
    for key, include_file in base.get('includes', {}).iteritems():
        dependency_data.update(power_yaml(include_file))

    parse_vars(base, dependency_data)

    return base['data']

pf_data = {
    "attributes": power_yaml("attributes.yaml"),

    # TODO: Pull from a yaml file
    "alignments": {
        "Lawful Good": None,
        "Neutral Good": None,
        "Chatic Good": None,
        "Lawful Neutral": None,
        "Neutral": None,
        "Chatic Neutral": None,
        "Lawful Evil": None,
        "Neutral Evil": None,
        "Chatic Evil": None
    },

    "races": {
        "dwarf": power_yaml("races/dwarves.yaml"),
        "elf":  power_yaml("races/elves.yaml"),
        "gnome":  power_yaml("races/gnomes.yaml"),
        "half-elf":  power_yaml("races/half-elves.yaml"),
        "halfling":  power_yaml("races/halflings.yaml"),
        "half-orc":  power_yaml("races/halforcs.yaml"),
        "human":  power_yaml("races/humans.yaml")
    }
}
