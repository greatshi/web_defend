# coding=utf-8
# 用strip(),split()两个方法都可以判断空行


infile = open('ruanzhu.txt', 'r')
outfile = open('ruanzhu_null_line.txt', 'w')
for li in infile.readlines():
    # if li.strip():
    if li.split():
        outfile.writelines(li)

infile.close()
outfile.close()
