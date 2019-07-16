"""
enscons changes for multiple wheels, until we can figure out the right way for enscons.
"""

from enscons import *


def generate(env):
    """
    Set up enscons in Environment env
    """

    # pure-Python tar
    from enscons import pytar

    pytar.generate(env)

    if not hasattr(generate, "once"):
        AddOption(
            "--egg-base",
            dest="egg_base",
            type="string",
            nargs=1,
            action="store",
            metavar="DIR",
            help="egg-info target directory",
        )

        AddOption(
            "--wheel-dir",
            dest="wheel_dir",
            type="string",
            nargs=1,
            action="store",
            metavar="DIR",
            help="wheel target directory",
        )

        AddOption(
            "--dist-dir",
            dest="dist_dir",
            type="string",
            nargs=1,
            action="store",
            metavar="DIR",
            help="sdist target directory",
        )

        generate.once = True

    try:
        env["ROOT_IS_PURELIB"]
    except KeyError:
        env["ROOT_IS_PURELIB"] = env["WHEEL_TAG"].endswith("none-any")

    env["EGG_INFO_PREFIX"] = GetOption("egg_base")  # pip wants this in a target dir
    env["WHEEL_DIR"] = GetOption("wheel_dir") or "dist"  # target directory for wheel
    env["DIST_BASE"] = GetOption("dist_dir") or "dist"

    env["PACKAGE_NAME"] = env["PACKAGE_METADATA"]["name"]
    env["PACKAGE_NAME_SAFE"] = normalize_package(env["PACKAGE_NAME"])
    env["PACKAGE_VERSION"] = env["PACKAGE_METADATA"]["version"]

    # place egg_info in src_root if defined
    if not env["EGG_INFO_PREFIX"] and env["PACKAGE_METADATA"].get("src_root"):
        env["EGG_INFO_PREFIX"] = env["PACKAGE_METADATA"]["src_root"]

    # Development .egg-info has no version number. Needs to have
    # underscore _ and not hyphen -
    env["EGG_INFO_PATH"] = env["PACKAGE_NAME_SAFE"] + ".egg-info"
    if env["EGG_INFO_PREFIX"]:
        env["EGG_INFO_PATH"] = env.Dir(env["EGG_INFO_PREFIX"]).Dir(env["EGG_INFO_PATH"])

    egg_info = env.Command(egg_info_targets(env), "pyproject.toml", egg_info_builder)

    env.Clean(egg_info, env["EGG_INFO_PATH"])

    env.Alias("egg_info", egg_info)

    # This is the only conflict for multiple .Whl, one per environment:
    # pkg_info = env.Command(
    #     "PKG-INFO", egg_info_targets(env)[0].get_path(), Copy("$TARGET", "$SOURCE")
    # )  # TARGET and SOURCE are ''?

    env.AddMethod(Whl)
    env.AddMethod(WhlFile)
    env.AddMethod(SDist)
