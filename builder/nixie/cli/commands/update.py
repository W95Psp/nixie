import tempfile

from rich.console import Console
from logging      import debug, error
from os           import path

from ...output    import script
from ..           import common

def _open_default_paths() -> script.NixieScript:
    common.goto_git_root()
    try:
        debug("Trying ./nix")
        return script.NixieScript('./nix')
    except:
        try:
            debug("Trying ./nix-shell")
            return script.NixieScript('./nix-shell')
        except:
            error("No nix script found in this repository. Run 'nixie init' to generate one.")
            exit(1)

def _cmd(console: Console, **args):
    ns: script.NixieScript
    newchns = dict()

    with console.status("Retrieving Nix channels...", spinner='earth') as st:
        for chn in args['with_channel']:
            chn_name = chn[:chn.index('=')]
            st.update(f"Retrieving Nix channel '{chn_name}'")
            newc = common.nix_chn_from_arg(chn)
            debug(f"Channel '{chn_name}' resolved to: {newc}")
            newchns.update({chn_name: newc})

    with console.status("Reading Nix script configuration...", spinner='dots12') as st:
        if args['script'] is not None:
            try:
                ns = script.NixieScript(args['script'])
            except FileNotFoundError:
                error(f"'{args['script']}': No such file or directory.")
                exit(1)
            except Exception:
                error(f"'{args['script']}' does not appear to be a valid script generated by Nixie.")
                exit(1)
        else:
            ns = _open_default_paths()

    debug(ns.features.print_features())
    if ns.features.include_sources:
        debug("This script includes sources.")
    if ns.features.include_bins:
        debug("This script includes binaries.")
    debug("Included channels: %s" %list(ns.features.pinned_channels.keys()))
    ns.features = common.features_from_args(args, ns.features)

    if len(args['with_channel']) > 0:
        ns.features.pinned_channels.update(newchns)

    with console.status("Updating Nix script...", spinner='dots12') as st:
        with open(ns.fname, mode='wb') as fi:
            ns.build(fi)
