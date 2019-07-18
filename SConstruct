import pytoml as toml
import enscons
import sys

import manifests

metadata = dict(toml.load(open("pyproject.toml")))["tool"]["enscons"]

full_tag = "py3-none-any"

base_environment = Environment(
    tools=["default", enscons.generate], PACKAGE_METADATA=metadata, WHEEL_TAG=full_tag
)


def make_environment(package):
    package_metadata = dict(metadata)  # copy
    package_metadata["name"] = metadata["name"] + "_" + package
    env = base_environment.Clone(PACKAGE_METADATA=package_metadata)
    return env


packages = manifests.get_manifests()
for package in packages:
    if package.startswith("_"):
        continue
    env = make_environment(package)
    py_source = packages[package]
    purelib = env.Whl("purelib", py_source, root="cpython/Lib")
    whl = env.WhlFile(source=purelib)
