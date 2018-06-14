# -*- encoding: utf-8 -*-
import xmlrpclib #导入xmlrpc库，这个库是python的标准库。

username ='admin' #用户登录名
pwd = 'admin' #用户的登录密码，测试时请换成自己的密码
dbname = 'odo' #数据库帐套名，测试时请换成自己的帐套名

# 第一步，取得uid
sock_common = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

# 调用res.partner对象的create方法在数据库中插入一个业务伙伴
partner = {
           'name': '测试', #字段
           'lang': 'zh_CN',
           }
partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'create',partner)

# 删除一条或多条记录
deleteID = [94,93] #需要删除的ID，一个list
result = sock.execute(dbname, uid, pwd, 'res.partner', 'unlink',deleteID)

#更新一条或多条记录
updateID = [78,79]
values = {
          'name': '更新'
          }
result1 = sock.execute(dbname, uid, pwd, 'res.partner', 'write',updateID,values)

#查询一条或多条记录,返回id
args = [('name','=','更新')]
result2 = sock.execute(dbname, uid, pwd, 'res.partner', 'search',args)
print(result2)

#读取字段记录
ids = [96,97]
fields = ['name','company_id']
data = sock.execute(dbname, uid, pwd, 'res.partner', 'read',ids,fields)
print(data)

#查找所有字段，无需传ID
data1 = sock.execute(dbname, uid, pwd, 'res.partner', 'search_read')
print(data1)