import os
import json
try:
    # python 3.7+
    import importlib.resources as config_loader
except ImportError:
    # python <= 3.6
    import importlib_resources as config_loader


# get the configuration
config_name = os.environ.get('PROGRAM_ARGS', 'wm-sasl-example.json')
if not config_loader.is_resource('pystreams.resources.env', config_name):
    if not config_name.endswith('.json'):
        config_name += '.json'
config = json.loads(
    config_loader.read_text('pystreams.resources.env', config_name)
)


def replace_envs(conf, composite_key=''):
    for key, val in conf.items():
        new_composite_key = f'{composite_key}.{key}' if composite_key else key
        if isinstance(val, dict):
            replace_envs(val, new_composite_key)
        else:
            if val == '_env_':
                conf[key] = os.environ[new_composite_key.replace('.', '_').upper()]


try:
    replace_envs(config)
except KeyError as e:
    raise RuntimeError(f'Environment variable {e} is missing!')