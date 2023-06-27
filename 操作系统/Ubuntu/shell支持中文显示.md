```shell
locale-gen zh_CN.UTF-8
vi ~/.bashrc
# 添加以下内容
LANG="zh_CN.UTF-8"
LANGUAGE="zh_CN:zh"

source ~/.bashrc
export LANG="zh_CN.UTF-8"
export LANGUAGE="zh_CN:zh"
```