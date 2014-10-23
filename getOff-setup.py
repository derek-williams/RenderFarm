from distutils.core import setup
import py2exe

setup(
    options = {
        "py2exe": {
            "dll_excludes": ["MSVCP90.dll"] # py2exe keeps trying to include this dll even though it isn't needed to run the program
        }
    },
    console=["getOff.py"]
)
