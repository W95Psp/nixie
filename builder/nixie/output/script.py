from io         import BytesIO, StringIO
from pathlib    import Path
from shlex      import shlex
from dotenv     import dotenv_values

class NixieFeatures:
    extra_features: list[str]
    extra_substituters: list[str]
    extra_trusted_public_keys: list[str]

    source_cache: str
    sources_drv: str
    bins_drv: str

    def __init__(self):
        '''Create an empty features object.
        '''
        pass

    def __init__(self, file: StringIO):
        '''Populate object from parsed features file.
        '''
        kvs = dotenv_values(stream=file)
        self.extra_features = kvs["EXTRA_FEATURES"].split(' ')
        self.extra_substituters = kvs["EXTRA_SUBSTITUTERS"].split(' ')
        self.extra_trusted_public_keys = kvs["EXTRA_TRUSTED_PUBLIC_KEYS"].split(' ')
        self.source_cache = kvs["SOURCE_CACHE"]
        self.sources_drv = kvs["SOURCES_DERIVATION"]
        self.bins_drv = kvs["NIX_BINS_DERIVATION"]

    def print_features(self) -> str:
        return f'''
        EXTRA_FEATURES="{' '.join(self.extra_features)}"
        EXTRA_SUBSTITUTERS="{' '.join(self.extra_substituters)}"
        EXTRA_TRUSTED_PUBLIC_KEYS="{' '.join(self.extra_trusted_public_keys)}"
        SOURCE_CACHE={source_cache}
        SOURCES_DERIVATION={sources_drv}
        NIX_BINS_DERIVATION={bins_drv}
        '''

class NixieScript:
    features: NixieFeatures

    pinned_channels: dict[str, Path]
    include_sources: bool = False
    include_bins: bool = False

    def __init__(self, features: NixieFeatures):
        self.features = features

    def print_features(self) -> str:
        return features.print_features()

    def build(self) -> BytesIO:
        outstream = BytesIO()

