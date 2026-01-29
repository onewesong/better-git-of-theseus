.PHONY: build clean publish install-dev

# 默认目标
all: build

# 核心构建命令
build: clean
	python3 -m build

# 清理构建产物
clean:
	rm -rf build/ dist/ *.egg-info/

# 发布到 PyPI
# 注意：这会提示输入用户名 (__token__) 和密码 (API Token)
publish: build
	twine upload dist/*

# 本地以可编辑模式安装，方便开发调试
install-dev:
	pip install -e .

# 检查包内容
check: build
	twine check dist/*
