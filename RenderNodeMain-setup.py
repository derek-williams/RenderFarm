from distutils.core import setup
import py2exe

setup(console=["RenderNodeMain.py"],
      data_files = [('.', ['hydraSettings.cfg'])],
      )
