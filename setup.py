import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reamber",
    version="0.0.4",
    author="evening",
    author_email="dev_evening@hotmail.com",
    description="Vertical Scrolling Rhythm Game Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eve-ning/reamber_base_py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)