import sys
import yaml

def service_config(config_file='environments/running.yml'):
    # profile = 'environment/' + sys.argv[1] + '.yml'
    with open(config_file) as f:
        _vars = yaml.full_load(f)
    return _vars
