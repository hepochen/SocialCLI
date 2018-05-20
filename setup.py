from setuptools import find_packages, setup

setup(
    name="society",
    version="1.0",
    keywords=("social", "society"),
    description="Extract the world's info.",
    license="MIT License",

    author="realsky",
    author_emial="carotwang@126.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[],

    scripts=[],
    entry_points={
        'console_scripts': [
            'society = SocialCLI.command_line:start'
        ]
    },
    zip_safe=False
)
