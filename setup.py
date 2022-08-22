import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simhash",
    version="0.0.1",
    author="Qyokizzzz",
    license='MIT',
    author_email="Ldazecc@gmail.com",
    description="Extracting document or image fingerprints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'mmh3',
        'numpy',
        'opencv-python',
        'pandas',
        'pyhanlp'
    ],
    url="https://github.com/Qyokizzzz/simhash",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
