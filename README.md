# file_cache
文件缓存服务，把文件缓存到本地，业务服务可以通过文件的uuid在这个服务获取到文件的地址。

主要使用的场景：
web要上传文件，先把文件传到本服务器，获取到文件uuid之后，请求目标服务器。
目标服务器可根据uuid查询文件路径。
本服务器也可以做文件的反向代理用于显示。