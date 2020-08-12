#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from concurrent.futures.thread import ThreadPoolExecutor

import nmap
import threading
from load_sheet import load_excel
from load_sheet import get_ip_list
from load_sheet import get_port_list
from result import Result
from info import Info

result = []
max_threads = 50


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
    for i in result:
        s = str(i.index) + ' ' + i.ip + ' ' + i.port + ' ' + i.state
        f.write(s)
        f.write('\n')
    f.close()
    e.out_end()


if __name__ == '__main__':
    sheet = load_excel()
    ip_list = get_ip_list(sheet)
    port_list = get_port_list(sheet)

    threads = []
    # index = 0
    s = Info("Scanning ports")
    s.out_start()
    with ThreadPoolExecutor(max_workers=max_threads) as t:
        for i in ip_list:
            t.submit(do, ip_list.index(i), i, port_list[ip_list.index(i)])
            # index += 1
        # all_task = [t.submit(do, i) for i in ip_list]
    s.out_end()
    write2txt(result)
    # do(0, '39.134.108.171', '1443')
