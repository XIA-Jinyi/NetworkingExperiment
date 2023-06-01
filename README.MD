# 邮件代理服务器

## 构建

在 Windows 平台上通过以下指令构建。

```bat
mkdir build
cd build
cmake ..
msbuild MailProxy.sln
```

## Python 环境依赖

使用指令下面的指令为程序安装 python 依赖库。

```bat
pip install -r requirements.txt
```

## 运行

完成上面两个步骤后，在命令行通过下面的指令启动代理程序。

```bat
python proxy.py
```