nonstdlib
=========

Isn't it strange that a lot of Python libraries are bundled with a particular version of the interpreter, instead of packaged? The nonstdlib package imagines a mirror universe where that is not the case.

Build
-----

- Check out the repository and the cpython git submodule
- Install enscons >= 0.20, pytoml, SCons. Tested in a Python 3.6+ environment or pypy.
- Run scons
- Enjoy wheels in dist/

Get Involved
------------

I can't do this project by myself. If you want to get involved, we will need some of these.

- More interesting per standard library module metadata
- More sophisticated splitting; current rule is per name or folder.
- A Python that has no standard library.
- A Python that searches site-packages before its standard library.
- An installer that either sets PYTHONPATH to "folder with lots of packages" so it can itself run, or an installer that can install into a different Python than the one it's running under. These simple wheels will be pretty friendly to the standard unzip command.
