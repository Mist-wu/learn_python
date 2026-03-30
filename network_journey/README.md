# 网络学习路线

这个目录按你要的顺序来：

1. `step1_echo_server.py` / `step1_echo_client.py`
   先感受最基础的 TCP 连接、收发数据。
2. `step1_framed_server.py` / `step1_framed_client.py`
   继续感受粘包和拆包，以及为什么应用层必须自己定义“消息边界”。

## 第一步先学什么

先记住一句话：

- TCP 只保证“字节流”可靠到达
- TCP 不保证你 `send` 了几次，对方就一定 `recv` 几次

这就是后面会遇到“粘包拆包”的根本原因。

## 1. 最小 TCP 连接

先开服务端：

```bash
python3 network_journey/step1_echo_server.py
```

再开客户端：

```bash
python3 network_journey/step1_echo_client.py
```

你会看到：

- client 先 `connect`
- server `accept` 到一个连接
- client `sendall`
- server `recv`
- server 再把响应发回去
- client 再 `recv`

建议你先自己改几次消息内容，体会“连接建立后，可以来回发很多次数据”。

## 2. 粘包拆包演示

运行服务端：

```bash
python3 network_journey/step1_framed_server.py
```

再运行客户端：

```bash
python3 network_journey/step1_framed_client.py
```

这个例子故意把一段完整数据拆成很多小块发出去，服务端也故意每次只 `recv(8)`。

你会看到：

- 一条消息可能被拆成多次 `recv`
- 多条消息也可能挤在一次 `recv` 里
- 所以不能把“一次 `recv`”当成“一条完整消息”

这里我们用“4 字节长度前缀”解决消息边界问题：

- 先读 4 字节，表示消息体长度
- 再按这个长度继续从缓冲区里取出完整消息

## 建议你按这个顺序观察

1. 先运行 echo 版本，只看连接和来回收发
2. 再运行 framed 版本，只盯住 `buffer` 是怎么累计的
3. 想一想：如果没有长度前缀，服务端怎么知道一条消息什么时候结束

## 下一步预告

等你把这一步跑通，下一步就可以在同一个 TCP 连接上手写 HTTP：

- 请求行
- 请求头
- 空行
- body

再下一步，就在你自己写的 HTTP 解析结果上做最小路由：

- `GET /`
- `GET /hello`
- `POST /login`
