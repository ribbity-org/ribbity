"Config file loading and convenience properties."
import tomli

DEFAULTS = dict(
    site_dir = 'site',
    docs_dir = 'docs',
    site_templates = 'site-templates',

    issue_title_prefix = "Example: "
)

class RibbityConfig:
    "Loaded configuration, with defaults. Supports .attribute access"

    def __init__(self, config_d):
        self.config_d = config_d

    def __getattr__(self, name):
        "Provide access to all contents of 'config_d' + DEFAULTS default vals"
        if name in self.config_d:
            return self.config_d.get(name)

        if name in DEFAULTS:
            return DEFAULTS[name]

        raise AttributeError(name)

    def get(self, name, default=None):
        "Provide access to contents of 'config_d' + DEFAULTS, w/add'l def val."
        try:
            x = self.__getattr__(name)
            return x
        except AttributeError:
            pass

        return default
        
    @classmethod
    def load(cls, filename):
        "Load a TOML config file from 'filename'"
        with open(filename, "rb") as fp:
            config_d = tomli.load(fp)

        return cls(config_d)
