import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    zip_safe=False,
    name="reamber",
    version="0.1.7",
    author="evening",
    author_email="dev_evening@hotmail.com",
    description="Vertical Scrolling Rhythm Game Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eve-ning/reamber_base_py",
    packages=setuptools.find_packages(),
    package_data={'reamber': ["py.typed",
                              "*.pyi",
                              "**/*.pyi",
                              "**/**/*.pyi",
                              "**/**/**/*.pyi",
                              "**/**/**/**/*.pyi",
                              "**/**/**/**/**/*.pyi"
                              ]},
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy',
        'pyyaml',
        'pandas',
        'matplotlib',
        'pillow',
        'osrparse==5.0.0',
        'unidecode'
    ]
)
