- 一键编译：拉取框架代码，编译；
- 一键测速：拉取框架模型，测速。拉取框架模型，框架模型存放于不同的代码仓库中，执行测速过程会自动完成拉取。

## 开发须知

首次提交代码需执行以下命令，安装钩子。安装成功后，每次执行`git commit`后会自动检查`.pre-commit-config.yaml`里设定的检查项，如目前是针对Python代码做格式检查。

```shell
# 第一次执行钩子可能会比较慢
pre-commit install

# 若找不到则需要先安装pre-commit
pip install pre-commit

# 如需卸载则执行
pre-commit uninstall
```
