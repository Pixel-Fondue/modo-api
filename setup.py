from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


from modo import __version__ as version


setup(
    name="modo-api",
    version=version,
    author="Shawn Frueh",
    description=f"Dumped API for Modo {version}",
    long_description=long_description,
    url="https://github.com/ShawnFrueh/modo-api",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent", ],
    packages=["lx", "lxu", "lxu.meta", "lxifc", "lxserv", "lxguid", "modo"]
)
