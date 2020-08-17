import sys
import re


def parseblock(block):
    linenum = 1
    insert = []
    delete = []
    update = []
    startscn = 0
    stopscn = 0
    xid = 0

    for line in block.split('\n'):
        if linenum == 3:
            startscn = line[5:].strip()
        if line.startswith('### INSERT INTO'):
            insert.append(line[16:].replace('`', '').strip())
        if line.startswith('### UPDATE'):
            update.append(line[11:].replace('`', '').strip())
        if line.startswith('### DELETE FROM'):
            delete.append(line[16:].replace('`', '').strip())
        mat = re.match(r'.*server id.*end_log_pos(.*)Xid =(.*)', line.strip())
        if mat:
            stopscn = mat.group(1).strip()
            xid = mat.group(2).strip()
        linenum = linenum + 1

    alllist = insert
    alllist.extend(update)
    alllist.extend(delete)
    alllist = list(set(alllist))

    size = int(stopscn) - int(startscn)
    dml = len(insert)+len(update)+len(delete)
    print('Xid:%s Size:%s(bytes) DML:%s INSERT:%s UPDATE:%s DELETE:%s' % (xid, size, dml, len(insert), len(update), len(delete)))
    print('-------------------------------------------------------------')
    for key in alllist:
        print('Table:%s INSERT:%s UPDATE:%s DELETE:%s \n' % (key, insert.count(key), update.count(key), delete.count(key)))
    print('\n')
    print('\n')


def parseblocks(file):
    with open(file, 'r') as f:
        a = f.read()
        block = re.compile(r'BEGIN./\*!\*/;.*?COMMIT/\*!\*/;', re.DOTALL)
        tm = re.compile(r'([0-9].*)')
        blocks = block.findall(a)

        for i in blocks:
            parseblock(i)


if __name__ == '__main__':
    parseblocks(sys.argv[1])
