<div align="center">

# Better Git of Theseus

[![pypi badge](https://img.shields.io/pypi/v/better-git-of-theseus.svg?style=flat)](https://pypi.python.org/pypi/better-git-of-theseus)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/better-git-of-theseus)](https://pypi.org/project/better-git-of-theseus/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/better-git-of-theseus)](https://pypi.org/project/better-git-of-theseus/)
[![GitHub License](https://img.shields.io/github/license/onewesong/better-git-of-theseus)](https://github.com/onewesong/better-git-of-theseus/blob/master/LICENSE)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/onewesong/better-git-of-theseus)

[English Version](README.md)

</div>

**Better Git of Theseus** 是对原版 [git-of-theseus](https://github.com/erikbern/git-of-theseus) 的现代重构版。它通过 **Streamlit** 提供了一个全交互式的 Web Dashboard，并结合 **Plotly** 生成可缩放、可悬停查看数据的现代化图表，同时显著提升了易用性。

![Git of Theseus Dashboard](https://raw.githubusercontent.com/erikbern/git-of-theseus/master/pics/git-git.png) *(注：图表现在是交互式的！)*

## 核心改进

-   🚀 **一键可视化**：全新的 `git-of-theseus-visualize` 命令，自动扫描当前目录并启动 Web 界面。
-   📊 **交互式图表**：使用 Plotly 替换了静态的 Matplotlib 图像。支持缩放、平移和详细数据悬停展示。
-   🧠 **全内存处理**：分析结果直接在内存中传递，默认不再生成大量的临时 `.json` 文件。
-   ⚡ **智能缓存**：利用 Streamlit 缓存机制，对同一仓库的重复分析近乎瞬间完成。
-   🎨 **现代化 UI**：侧边栏实时调整参数（如 Cohort 格式、忽略规则、归一化等），无需反复运行命令行。

## 安装

运行以下命令安装：

```bash
pip install better-git-of-theseus
```

## 快速开始

在任何 Git 项目目录中运行：

```bash
git-of-theseus-visualize
```

它会自动打开浏览器，展示当前仓库的代码演进分析。

## 进阶玩法

### 传统命令行支持

我们保留并优化了原有的 CLI 工具，且它们现在支持更多的交互选项：

1.  **分析仓库**：`git-of-theseus-analyze <path to repo>` (支持 `--outdir` 保存结果)
2.  **堆叠面积图**：`git-of-theseus-stack-plot cohorts.json`
3.  **作者贡献分析**：`git-of-theseus-line-plot authors.json --normalize`
4.  **代码生存率**：`git-of-theseus-survival-plot survival.json`

### 分组(Cohort)格式设置

在可视化界面或命令行中，你可以自定义 `Cohort Format`（基于 Python strftime）：
-   `%Y`: 按 **年** 分组 (默认)
-   `%Y-%m`: 按 **月** 分组
-   `%Y-W%W`: 按 **周** 分组

### 多仓库生存曲线对比

如果你想对比多个项目的代码生命周期：
1. 分别分析并保存结果：`git-of-theseus-analyze repo1 --outdir out1`
2. 运行对比绘图：`git-of-theseus-survival-plot out1/survival.json out2/survival.json --exp-fit`

## 常见问题集锦

-   **Duplicate Authors?** 如果作者显示重复，建议在仓库根目录配置 [.mailmap](https://git-scm.com/docs/gitmailmap)。
-   **Performance?** 对于超大型仓库（如 Linux Kernel），首次分析可能需要一些时间，之后的查看由于缓存机制会非常快。

## 致谢

感谢 [Erik Bernhardsson](https://github.com/erikbern) 创作了原始的 `git-of-theseus`。

## License

MIT
