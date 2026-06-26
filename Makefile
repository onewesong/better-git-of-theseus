.PHONY: build clean publish install-dev release version

# 版本号由 setuptools-scm 从 git tag 自动派生（见 pyproject.toml）。
# 发布新版只需打 tag，无需手改任何文件：
#   git tag v0.7.0 && git push origin master --tags
# 推送 tag 后 .github/workflows/release.yml 会自动构建并发布到 PyPI。

# 默认目标
all: build

# 核心构建命令（版本号自动来自最近的 git tag）
build: clean
	python3 -m build

# 查看当前将要构建出的版本号
version:
	python3 -m setuptools_scm

# 清理构建产物
clean:
	rm -rf build/ dist/ *.egg-info/

# 手动发布到 PyPI（一般走 CI 自动发布即可，此处用于本地应急发布）
# 注意：这会提示输入用户名 (__token__) 和密码 (API Token)
publish: build
	twine upload dist/*

# 本地以可编辑模式安装，方便开发调试
install-dev:
	pip install -e .

# 检查包内容
check: build
	twine check dist/*
