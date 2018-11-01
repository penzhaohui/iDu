#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laiyu'

import json
import time

from globalpkg.log import logger
from testcase import  TestCase
from testsuite import TestSuite
from httpprotocol import MyHttp
from globalpkg.global_var import *

 # 根据用例行某个用例
def run_testcase_by_id(testcase_id, testplan='无计划'):
    try:
        testcase_info = mytestlink.getTestCase(testcase_id)  # 获取测试用例基本信息
        logger.info('获取测试用例信息 %s' % testcase_info)
    except Exception as e:
        logger.error('获取用例信息失败 %s,,暂停执行该用例' % e)
        return ('Fail',[('global_funtion_module','获取用例信息失败 %s' % e)])
    # 获取用例所在套件和项目名称
    response = mytestlink.getFullPath([int(testcase_id)])
    response = response[str(testcase_id)]
    testsuite_name = ''
    for suit in response[1:]:
        testsuite_name = testsuite_name + '-' + suit
        testsuite_name = testsuite_name.lstrip('-')
    project_name = response[0]

    # 构造测试用例对象
    testcase_name = testcase_info[0]['name']
    testcase_steps = testcase_info[0]['steps']
    testcase_isactive = int(testcase_info[0]['active'])
    testcase_obj = TestCase(testcase_id, testcase_name, testcase_steps, testcase_isactive,project_name)

    testsuite_id = int(testcase_info[0]['testsuite_id'])
    logger.info('正在读取套件[id=%s]的协议，host，端口配置...' % (testsuite_id))

    testsuite_info = mytestlink.getTestSuiteByID(testsuite_id)
    testsuite_name = testsuite_info['name']
    testsuite_details = other_tools.conver_date_from_testlink(testsuite_info['details'])
    project = mytestlink.getFullPath(testsuite_id)
    project = project[str(testsuite_id)][0]
    testsuite_obj = TestSuite(testsuite_id, testsuite_name, testsuite_details, project)
    testsuite_conf = testsuite_obj.get_testsuite_conf()  # 获取套件基本信息
    if '' == testsuite_conf:
        logger.error('测试套件[id=%s ,name=%s]未配置协议，host，端口信息，暂时无法执行' % (testsuite_id, testsuite_name))
        return ('Fail', [('golbal_function_module', '测试套件[id=%s ,name=%s]未配置协议，host，端口信息，暂时无法执行' % (testsuite_id, testsuite_name))])

    try:
        details = json.loads(testsuite_conf)
        protocol = details['protocol']
        host = details['host']
        port = details['port']
    except Exception as e:
        logger.error('测试套件[id=%s ,name=%s]协议，host，端口信息配置错误,未执行：%s'% (testsuite_id, testsuite_name, e))
        return ('Fail',[('golbal_function_module', '测试套件[id=%s ,name=%s]协议，host，端口信息配置错误,未执行：%s'% (testsuite_id, testsuite_name, e))])

    # 构造http对象
    myhttp = MyHttp(protocol, host, port)

    try:
        sql_insert = 'INSERT INTO '+testcase_report_tb +'(executed_history_id, testcase_id, testcase_name, testsuit, testplan, project, runresult, runtime)' \
                                                        ' VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
        data = (executed_history_id, testcase_id, testcase_name, testsuite_name, testplan, project_name, 'Block','0000-00-00 00:00:00')
        logger.info('记录测试用例到测试用例报表')
        testdb.execute_insert(sql_insert, data)

        logger.info('开始执行测试用例[id=%s，name=%s]' % (testcase_id, testcase_name))
        run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 记录运行时间
        testcase_run_result = testcase_obj.run_testcase(myhttp, testplan)

        logger.info('正在更新用例执行结果')
        sql_update = 'UPDATE '+testcase_report_tb +' SET runresult=\"%s\", runtime=\"%s\"' \
                                                   ' WHERE executed_history_id = %s and testcase_id = %s' \
                                                   ' AND project=\'%s\' AND testplan=\'%s\''
        data = (testcase_run_result[0], run_time, executed_history_id, testcase_id, project_name, testplan)
        testdb.execute_update(sql_update, data)

        logger.info('指定用例[%s]已执行完' % testcase_id)

        return testcase_run_result
    except Exception as e:
        logger.error('运行用例出错 %s' % e)
        return ('Fail',[('golbal_function_module', '%s' % e)])

