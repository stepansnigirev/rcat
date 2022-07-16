from setuptools import setup, find_namespace_packages

with open("requirements.txt") as f:
    install_reqs = f.read().strip().split("\n")

# Filter out comments/hashes
reqs = []
for req in install_reqs:
    if req.startswith("#") or req.startswith("    --hash="):
        continue
    reqs.append(str(req).rstrip(" \\"))

setup(
    name="rcat",
    version="0.0.1",
    license="MIT license",
    url="https://github.com/stepansnigirev/rcat",
    description="alternative to cat with image support and syntax highlighting",
    long_description="alternative to can with image support and syntax highlighting",
    author="Stepan Snigirev",
    author_email="snigirev.stepan@gmail.com",
    packages=find_namespace_packages("src", include=["*"]),
    package_dir={"": "src"},
    install_requires=reqs,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
