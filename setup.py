from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="better-git-of-theseus",
    version="0.4.0",
    description="Plot stats on Git repositories with interactive Plotly charts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Erik Bernhardsson",
    author_email="mail@erikbern.com",
    url="https://github.com/onewesong/better-git-of-theseus",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "gitpython",
        "numpy",
        "tqdm",
        "wcmatch",
        "pygments",
        "plotly",
        "streamlit",
        "python-dateutil",
        "scipy"
    ],
    entry_points={
        "console_scripts": [
            "git-of-theseus-analyze=git_of_theseus.analyze:analyze_cmdline",
            "git-of-theseus-survival-plot=git_of_theseus:survival_plot_cmdline",
            "git-of-theseus-stack-plot=git_of_theseus:stack_plot_cmdline",
            "git-of-theseus-line-plot=git_of_theseus:line_plot_cmdline",
            "git-of-theseus-visualize=git_of_theseus.cmd:main",
        ]
    },
)
