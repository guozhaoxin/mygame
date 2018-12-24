#encoding:utf8
__author__ = 'gold'

def trans(s):
    if not s:
        return
    if s[0] == '"' or s[0] == "'":
        s = s[1:len(s) - 1]
    if s[0] == '#':
        s = s[1:]
    index = 0
    a = []
    try:
        while index < len(s):
            a.append(int(s[index:index + 2],16))
            index += 2
        return tuple(a)
    except:
        return

if __name__ == '__main__':
    print(trans('fsdsf'))