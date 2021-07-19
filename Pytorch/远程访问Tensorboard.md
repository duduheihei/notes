## windows下关联端口
```shell
ssh -L 16006:127.0.0.1:6006 account@server.address
```

## 服务器端打开tensorboard
```shell
tensorboard --logdir="/path/to/log-directory"
```