import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="certbot-extra-formats",
    version="0.1.4",
    author="Pellegrino Prevete",
    author_email="pellegrinoprevete@gmail.com",
    description=("Writes a 'Let's Encrypt' certificate "
                 "compatible with a given application"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tallero/certbot-extra-formats",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'certbot-extra-formats = certbot_extra_formats:main']
    },
    install_requires=[
        'certbot',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: Unix",
    ],
)
