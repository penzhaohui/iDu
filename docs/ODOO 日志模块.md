#### ODOO的日志模块

##### 问题背景
需要同时将系统运行日志显示在控制台和文件中。显示在控制台，主要方便查看；显示在日志文件中，主要方便寻找类似的问题

##### 日志的配置

- logfile：日志文件名，比如opt/odoo.log.如果不设置，则默认为stdout，即输出到控制台

- logrotate：True/False.如果设置True,每天创建一个文件，并且保存30天的日志文件

- log_level：日志级别 ，可以为列表中的任意一项 ['debug_rpc_answer', 'debug_rpc', 'debug', 'debug_sql', 'info', 'warn', 'error', 'critical']. Odoo 设置此日志级别选项的意义在于因为这些级别值被映射到了一个预先定义好的"module:log_level"键值对集合，即使这个选项没有被设置，Odoo则会使用预先定义的设置作为默认设置。

- log_handler： 值可以为"module:log_level"键值 对。“Module”表示模块名，比如：“openerp.addons.account” 或者 “openerp.addons.*”。"log_level"默认值为“INFO”, 也即是对所有模块来说，默认的日志级别就是'INFO'

##### 日志的实现
Odoo日志功能被定义在“openerp/netsvc.py”中，日志的初始化定义在方法“init_logger()”中，在“tools.translated.resetlocal()“被调用之后，日志被设置为包含以下字段的格式：

```
time，process id，logging level,database name,module name,logging message
```
1. 如果配置了一个日志文件选项"logfile"，Odoo 日志会使用一个文件处理器(TimedRotatingFileHandler，WatchedFileHandler 和FileHandler三者之一)将日志信息写入文件。(译者增加)处理器不需要显示设置，如果logrotate被设置为True，则处理器为TimedRotatingFileHandler；如果设置为False，则处理器为FileHandler或者WatchedFileHandler
2. 如果没有配置日志文件选项"logfile"，日志信息会被输出到控制台
3. 如果配置了日志数据库选项”log_db“，日志信息会被写入数据库中的”ir.logging“表中

<br/>Odoo从Odoo中预先配置的映射键值对象PSEUDOCONFIG_MAPPER中读取针对不同模块的日志级别

##### 解决办法
在\odoo-10.0\odoo\netsvc.py文件中，增加如下几行代码，就可以实现同时输出日志到控制台和日志文件
```
    logging.getLogger().addHandler(handler)

    if tools.config['log_console']:
        # Preserve stream handler
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        logging.getLogger().addHandler(streamHandler)
```

##### 参考资料
- [odoo源码阅读笔记：关于log及其logrotate](http://blog.sina.com.cn/s/blog_53d318170102wnsc.html)
- [Odoo/OpenERP 日志配置、使用及实现](https://www.cnblogs.com/chjbbs/p/5575105.html)





