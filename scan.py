#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import nmap
import threading
from load_sheet import load_excel
from load_sheet import get_ip_list
from load_sheet import get_port_list
from result import Result
from info import Info

result = []
batchs = 20


def do(index, ip, port):
    nm = nmap.PortScanner()
    nm.scan(ip, port, '-T4 -Pn')
    s = nm[ip]['tcp'][int(port)]['state']
    print("{:^10d}{:^20s}{:^10s}{:^20s}".format(index, ip, port, s))
    r = Result(index, ip, port, s)
    result.append(r)


def write2txt(result):
    inf = Info("Sorting result")
    inf.out_start()
    result = sorted(result, key=lambda x: x.index)
    inf.out_end()
    f = open('./reslut.txt', 'w')
    e = Info("Save result")
    e.out_start()
    s = []
    for i in result:
        s = str(i.index) + ' ' + i.ip + ' ' + i.port + ' ' + i.state
        f.write(s)
        f.write('\n')
    f.close()
    e.out_end()

class myThread(threading.Thread):
    def __init__(self, index,  ip, port):
        threading.Thread.__init__(self)
        self.index = index
        self.ip = ip
        self.port = port

    def run(self):
        do(self.index, self.ip, self.port)


# def action(ip_batch, port_batch):
#     bat = 0


if __name__ == '__main__':
    sheet = load_excel()
    ip_list = get_ip_list(sheet)
    port_list = get_port_list(sheet)

    ip_batch = [ip_list[i:i + batchs] for i in range(0, len(ip_list), batchs)]
    port_batch = [port_list[i:i + batchs] for i in range(0, len(ip_list), batchs)]

    threads = []
    bat = 0
    index = 1
    s = Info("Scanning ports")
    s.out_start()
    for ip_b in ip_batch:
        inx = 0
        for ip in ip_b:
            t = myThread(index, ip, port_batch[bat][inx])
            # do(ip, port_batch[bat][inx])
            threads.append(t)
            index += 1
            inx += 1
        bat += 1
    # thread = threading.Thread(target=action(ip_batch, port_batch), args=ip_batch)
    for thr in threads:
        thr.start()

    for thr in threads:
        if thr.is_alive():
            thr.join()
    s.out_end()
    write2txt(result)
