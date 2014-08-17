import yaml
try:
    config = yaml.load(open("easypc/config/config.yaml", 'r'))
except:
    config = {}
