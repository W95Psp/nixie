from rich.console import Console
from logging      import debug, info, warn, error

from ...          import nix
from ..           import common

def _cmd(console: Console, **args):
    common.goto_git_root()
    nixes = []
    with console.status(f"Looking up commands...", spinner='arrow2') as ld:
        for cmd in args['command']:
            ld.update(f"Looking up command '{cmd}'...")
            try:
                cands = nix.findIndex(f'/bin/{cmd}')
                if len(cands) > 1:
                    ld.stop()
                    info(f"Several options found for command '{cmd}'.")
                    nixes.append(common.pick("Package to use: ", cands)[1])
                    ld.start()
                else:
                    nixes.append(cands[0])
            except FileNotFoundError:
                ld.stop()
                error(f"Could not find command '{cmd}' in Nixpkgs.")
                exit(1)
    debug(nixes)
    error("Command lookup is not implemented.")
