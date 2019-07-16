import pytoml as toml
import enscons_patch
import sys

import manifests

metadata = dict(toml.load(open("pyproject.toml")))["tool"]["enscons"]

full_tag = "py3-none-any"


def make_environment(package):
    package_metadata = dict(metadata)  # copy
    package_metadata["name"] = metadata["name"] + "_" + package
    env = Environment(
        tools=["default", enscons_patch.generate],
        PACKAGE_METADATA=package_metadata,
        WHEEL_TAG=full_tag,
    )
    env.VariantDir(package, ".")
    return env


packages = manifests.get_manifests()
for package in packages:
    if package.startswith("_"):
        continue
    # TODO one Environment should be better at multiple wheels...
    # .Whl or .WhlFile could set up the targets that generate metadata,
    # instead of Environment.
    env = make_environment(package)
    py_source = packages[package]
    print(py_source)
    purelib = env.Whl("purelib", py_source, root="cpython/Lib")
    whl = env.WhlFile(purelib)
