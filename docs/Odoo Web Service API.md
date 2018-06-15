
### Odoo Web Service API

#### When should I use XML-RPC instead of a Controller in Odoo?

If you are simply using CRUD (Create,Read,Update,Delete) you almost definitely want to use the xmlrpc/jsonrpc interfaces. You can even you xmlrpc/jsonrpc to execute custom commands on you models as well. So xmlrpc is a structured means of executing authenticated exchanges between your client and the server.

注：简单的增删改插，肯定使用XML-RPC/Json-RPC。需要进行身份验证

If you want to provide complex json data back to your client or make unauthenticated interactions from client->server then a controller is definitely the way to go.

注：复杂Json数据，且不需要进行身份验证的交互，则使用control

Controllers are also very useful for the Odoo Webpage services. Making redirecting to the proper page or loading the appropriate template and handling form data very easy.

注：Controller也是页面之间交互的方式

Whatever works for your design needs may be correct for you, however Odoo has created services for handling normal CRUD interactions and executing model functions and it is advisable to benefit from Odoo's work and use your hard programming time to create your own structures where needed.

----

Here is Odoo's docs.

service 对应的后端服务分别是

common， openerp.service.common
db，openerp.service.db
object , openerp.service.model
report, openerp.service.report

各服务提供的方法如下


1.common
- login
- authenticate
version
- about
- set_loglevel

2. db
- create_database
- duplicate_database
- drop
- dump
- restore
- rename
- change_admin_password
- migrate_database
- db_exist
- list
- list_lang
- list_countries
- server_version

3.object
- execute
- execute_kw
- execute_workflow

4. report
- report
- report_get
- render_report

实现自己的方法时，要按照约定，以 'exp_' 开头。

来自于：[Odoo Web Service API](http://www.cnblogs.com/odoouse/p/5882749.html)
