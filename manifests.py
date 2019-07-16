#!/usr/bin/env python
# Generate lists of files for each package.
import subprocess
import re
from collections import defaultdict

packagename = re.compile(r"Lib/(?P<path>(?P<name>[^\/\.]*)(.*))$")


def get_manifests():
    output = subprocess.check_output(
        ["git", "ls-files", "Lib"], cwd="./cpython"
    ).decode("utf-8")

    packages = defaultdict(list)

    for line in output.splitlines():
        match = packagename.match(line)
        if match:
            packages[match.group("name")] += ["cpython/" + match.group(0)]

    return packages
