# Better Git of Theseus

[![pypi badge](https://img.shields.io/pypi/v/better-git-of-theseus.svg?style=flat)](https://pypi.python.org/pypi/better-git-of-theseus)
[中文版](README_zh.md)

**Better Git of Theseus** is a modern refactor of the original [git-of-theseus](https://github.com/erikbern/git-of-theseus). It provides a fully interactive Web Dashboard powered by **Streamlit** and **Plotly**, making it easier than ever to visualize how your code evolves over time.

![Git of Theseus Dashboard](https://raw.githubusercontent.com/erikbern/git-of-theseus/master/pics/git-git.png) *(Note: Charts are now fully interactive!)*

## Key Enhancements

-   🚀 **One-Click Visualization**: New `git-of-theseus-visualize` command automatically scans your project and launches a Web UI.
-   📊 **Interactive Charts**: Replaced static Matplotlib plots with Plotly. Support for zooming, panning, and detailed data hovers.
-   🧠 **In-Memory Processing**: Data flows directly in memory. No more mandatory intermediate `.json` files cluttering your repo.
-   ⚡ **Smart Caching**: Leverages Streamlit's caching to make repeat analysis of large repos nearly instantaneous.
-   🎨 **Modern UI**: Adjust parameters (Cohort format, ignore rules, normalization, etc.) in real-time via the sidebar.

## Installation

Install via pip:

```bash
pip install better-git-of-theseus
```

## Quick Start

Run the following in any Git repository:

```bash
git-of-theseus-visualize
```

It will automatically open your browser to the interactive dashboard.

## Advanced Usage

### Traditional CLI Support

Original CLI commands are preserved and enhanced with Plotly support:

1.  **Analyze**: `git-of-theseus-analyze <path to repo>` (supports `--outdir` for saving data)
2.  **Stack Plot**: `git-of-theseus-stack-plot cohorts.json`
3.  **Line Plot**: `git-of-theseus-line-plot authors.json --normalize`
4.  **Survival Plot**: `git-of-theseus-survival-plot survival.json`

### Cohort Formatting

Customize how commits are grouped by year, month, or week (based on Python strftime):
-   `%Y`: Group by **Year** (Default)
-   `%Y-%m`: Group by **Month**
-   `%Y-W%W`: Group by **Week**

### Comparative Survival Analysis

To compare code survival across multiple projects:
1. Analyze and save: `git-of-theseus-analyze repo1 --outdir out1`
2. Run comparison: `git-of-theseus-survival-plot out1/survival.json out2/survival.json --exp-fit`

## FAQ

-   **Duplicate Authors?** Configure a [.mailmap](https://git-scm.com/docs/gitmailmap) file in your repo root to merge identities.
-   **Performance?** First-time analysis of very large repos (like the Linux Kernel) may take time, but subsequent views are extremely fast due to caching.

## Credits

Special thanks to [Erik Bernhardsson](https://github.com/erikbern) for creating the original `git-of-theseus`.

## License

MIT
