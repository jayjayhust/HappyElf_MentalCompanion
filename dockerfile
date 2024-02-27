# 选择基于pyhon基础镜像（https://hub.docker.com/上搜索镜像）
FROM python:3.10
# 为后续的RUN、CMD、ENTRYPOINT指定工作目录
WORKDIR /app
# 复制所有文件到镜像
COPY . .
# 安装支持（根据requirements.txt），这一步可能要开全局代理
RUN pip install -r requirements.txt
# 暴露應用程式所使用的端口
EXPOSE 7860
# CMD["要运行的程序"，"参数1"，"参数2""]
# 上面的是exec形式，shell形式:CMD命令参数1参数2
# 启动容器时默认执行的命令或者脚本，Dockerfile只能有一条CMD命令。如果指定多条命令，只执行最后一条命令。如果在docker run时指定了命令或者镜像中有ENTRYPOINT，那么CDM就会被覆盖。
# CMD可以为ENTRYPOINT指令提供默认参数。
CMD ["python", "app.py"]