"Config file loading and convenience properties."
import tomli

DEFAULTS = dict(
    site_dir = 'site',
    docs_dir = 'docs'
)

class RibbityConfig:
    "Loaded configuration, with defaults. Supports .attribute access"

    def __init__(self, config_d):
        self.config_d = config_d

    def __getattr__(self, name):
        "Provide access to all contents of 'config_d' + DEAFUTLS default"
        try:
            if name in self.config_d:
                return self.config_d.get(name)

            if name in DEFAULTS:
                return DEFAULTS[name]
        except KeyError:
            raise AttributeError(name)
        
    @classmethod
    def load(cls, filename):
        "Load a TOML config file from 'filename'"
        with open(filename, "rb") as fp:
            config_d = tomli.load(fp)

        return cls(config_d)
