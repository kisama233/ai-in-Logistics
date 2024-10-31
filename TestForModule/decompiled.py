import pyshark

# 加载 pcap 文件进行分析
capture = pyshark.FileCapture('f9809647382a42e5bfb64d7d447b4099.pcap')

# 显示前几条数据包的摘要
for packet in capture[:5]:
    print(packet)
