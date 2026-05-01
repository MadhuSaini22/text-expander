from setuptools import find_packages, setup


setup(
    name="text-expander",
    version="0.1.0",
    description="Terminal-only cross-platform text expander with global shortcut expansion.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Madhu Saini",
    license="MIT",
    project_urls={
        "Homepage": "https://github.com/MadhuSaini22/text-expander",
        "Source": "https://github.com/MadhuSaini22/text-expander",
        "Issues": "https://github.com/MadhuSaini22/text-expander/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Desktop Environment",
        "Topic :: Utilities",
    ],
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.9",
    install_requires=[
        "pynput>=1.7.6",
        "pyperclip>=1.8.2",
        "pyobjc-core>=11.1,<12; sys_platform == 'darwin' and python_version < '3.10'",
        "pyobjc-framework-ApplicationServices>=11.1,<12; sys_platform == 'darwin' and python_version < '3.10'",
        "pyobjc-framework-Cocoa>=11.1,<12; sys_platform == 'darwin' and python_version < '3.10'",
        "pyobjc-framework-Quartz>=11.1,<12; sys_platform == 'darwin' and python_version < '3.10'",
        "pyobjc-core>=11.1; sys_platform == 'darwin' and python_version >= '3.10'",
        "pyobjc-framework-ApplicationServices>=11.1; sys_platform == 'darwin' and python_version >= '3.10'",
        "pyobjc-framework-Cocoa>=11.1; sys_platform == 'darwin' and python_version >= '3.10'",
        "pyobjc-framework-Quartz>=11.1; sys_platform == 'darwin' and python_version >= '3.10'",
    ],
    entry_points={
        "console_scripts": [
            "text-expander=text_expander.cli:main",
        ],
    },
)
