#### ODOO 单元测试

##### 开发步骤
1. 创建文件及文件夹
```
├─controllers
├─demo
├─models
├─security
├─static
│  ├─description
│  └─images
├─tests
│  ├─__init__.py
│  └─test_Course.py
└─views
```
2. 编写测试用例

__init__.py

```
from . import test_Course
```
test_Course.py

```
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase

class TestCourse(TransactionCase):

    def test_some_action(self):
        env = self.env['openacademy.course']
        records = env.search([])
        for record in records:
            self.assertEqual(record.name, "test")
```


3. 执行测试用例
<br/>修改运行参数为：
<br/>-c file path> -d db name> --stop-after-init --log-level=test --test-enable -i
<br/>例如：-c C:\odoo\openerp-server.
<br/>--config=..\odoo.conf -d demo  --stop-after-init --log-level=test --test-enable -i openacademy

4. 分析测试结果

```
2018-05-31 07:38:06,732 6204 INFO demo odoo.modules.module: odoo.addons.openacademy.tests.test_Course running tests.
2018-05-31 07:38:06,733 6204 INFO demo odoo.addons.openacademy.tests.test_Course: test_some_action (odoo.addons.openacademy.tests.test_Course.TestCourse)
2018-05-31 07:38:06,802 6204 ERROR demo odoo.addons.openacademy.tests.test_Course: FAIL
2018-05-31 07:38:06,803 6204 INFO demo odoo.addons.openacademy.tests.test_Course: ======================================================================
2018-05-31 07:38:06,805 6204 ERROR demo odoo.addons.openacademy.tests.test_Course: FAIL: test_some_action (odoo.addons.openacademy.tests.test_Course.TestCourse)
2018-05-31 07:38:06,805 6204 ERROR demo odoo.addons.openacademy.tests.test_Course: Traceback (most recent call last):
2018-05-31 07:38:06,805 6204 ERROR demo odoo.addons.openacademy.tests.test_Course: `   File "D:\ODOOEnv\ODOO10.0\odoo-10.0\myaddons\openacademy\tests\test_Course.py", line 13, in test_some_action
2018-05-31 07:38:06,805 6204 ERROR demo odoo.addons.openacademy.tests.test_Course: `     self.assertEqual(record.name, "test")
2018-05-31 07:38:06,805 6204 ERROR demo odoo.addons.openacademy.tests.test_Course: ` AssertionError: u'\u4e2d\u56fd\u6587\u5316\u901a\u8bba' != 'test'
2018-05-31 07:38:06,805 6204 INFO demo odoo.addons.openacademy.tests.test_Course: Ran 1 test in 0.070s
2018-05-31 07:38:06,805 6204 ERROR demo odoo.addons.openacademy.tests.test_Course: FAILED
2018-05-31 07:38:06,805 6204 INFO demo odoo.addons.openacademy.tests.test_Course:  (failures=1)
2018-05-31 07:38:06,805 6204 ERROR demo odoo.modules.module: Module openacademy: 1 failures, 0 errors
```


##### 遗留问题
- 如何生成测试报告？
- 如何批量执行单元测试用例？
