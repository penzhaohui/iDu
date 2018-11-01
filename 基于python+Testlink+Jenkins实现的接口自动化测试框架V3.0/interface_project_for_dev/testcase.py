#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import json
import time
from collections import OrderedDict

from globalpkg.log import logger
from globalpkg.global_var import other_tools
from globalpkg.global_var import case_step_report_tb
from globalpkg.global_var import executed_history_id
from globalpkg.global_var import testdb
from casestep import CaseStep
import globalpkg.global_function

class TestCase:
    def __init__(self, testcase_id, testcase_name, steps, active_status, testproject):
        self.testcase_id = testcase_id
        self.testcase_name = testcase_name
        self.steps = steps
        self.active_status = active_status # 用例是否禁用 1 - 活动 0 - 禁用
        self.testproject = testproject

    def run_testcase(self, http, testplan):
        if 0 == self.active_status:
            logger.warning('用例[name=%s]处于禁用状态[active=0]，不执行' % self.testcase_name)
            return ('Block','用例处于禁用状态，不执行')

        protocol_all = http.get_protocol()
        host_all = http.get_host()
        port_all = http.get_port()

        for step in self.steps:
            # 构造测试步骤对象
            step_id = int(step['id'])
            step_number = int(step['step_number'])
            step_action = other_tools.conver_date_from_testlink(step['actions'])
            logger.info('转换来自test_link 的step_action值为：%s' % step_action)
            expected_results = other_tools.conver_date_from_testlink(step['expected_results'])
            logger.info('转换来自test_link 的expected_results值为：%s' % expected_results)
            logger.debug('step_action： %s' % step_action)

            sql_insert = 'INSERT INTO '+ case_step_report_tb +'(executed_history_id, testcase_id, testcase_name, testplan, project, step_id, step_num, protocol_method, protocol, host, port, ' \
                                                               'step_action, expected_results, runresult, reason, runtime)' \
                         ' VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            if step_action.find('步骤类型')  != -1 and step_action.find('执行用例') != -1: # 待执行步骤为用例
                data = (executed_history_id, self.testcase_id, self.testcase_name, testplan, self.testproject, step_id, step_number, '无', '无', '无', '无',
                step_action, expected_results, 'Block', '', '0000-00-00 00:00:00')
                logger.info('记录测试步骤到测试步骤报告表')
                testdb.execute_insert(sql_insert, data)
            elif step_action.find('步骤类型') != -1 and (step_action.find('执行sql') != -1 or step_action.find('执行SQL') != -1): #: # 待执行步骤为sql
                data = (executed_history_id, self.testcase_id, self.testcase_name, testplan, self.testproject, step_id, step_number, '', '', testdb.get_host(), testdb.get_port(),
                    step_action, expected_results, 'Block', '', '0000-00-00 00:00:00')
                logger.info('记录测试步骤到测试步骤报告表')
                testdb.execute_insert(sql_insert, data)
            elif  step_action.find('步骤类型') == -1: # 待执行步骤为普通用例步骤
                data = (executed_history_id, self.testcase_id, self.testcase_name, testplan, self.testproject, step_id, step_number, '', protocol_all, host_all, port_all,
                    step_action, expected_results, 'Block', '', '0000-00-00 00:00:00')
                logger.info('记录测试步骤到测试步骤报告表')
                testdb.execute_insert(sql_insert, data)
				
            run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 记录运行时间
            try:
                step_action = json.loads(step_action, object_pairs_hook=OrderedDict)
                if '步骤类型' not in step_action:
                    protocol_method = step_action['方法']
                else:
                    protocol_method = '无'

                if expected_results != '':
                    expected_results = json.loads(expected_results)
                step_obj = CaseStep(step_id, step_number, expected_results, step_action, self.testcase_id)
            except Exception as e:
                logger.error('步骤[%s]信息填写错误: %s,停止执行用例[id=%s, name=%s]' % (step_number, e, self.testcase_id, self.testcase_name))
                sql_update = 'UPDATE '+ case_step_report_tb +' SET runresult=\"%s\",reason=\"%s\", protocol_method=\"%s\", runtime=\"%s\"' \
                                                                 ' WHERE executed_history_id = %s AND testcase_id = %s AND step_id = %s' \
                                                                 ' AND project=\'%s\' AND testplan=\'%s\''
                data =  ('Block','%s' % e, protocol_method, run_time, str(executed_history_id), self.testcase_id, step_id, self.testproject, testplan)
                logger.info('正在更新步骤执行结果')
                testdb.execute_update(sql_update, data)
                return ('Error',[('TestCase', '步骤[%s]信息填写错误: %s,停止执行用例[id=%s, name=%s]' % (step_number, e, self.testcase_id, self.testcase_name))])

            logger.info('开始执行步骤操作[第%s步]'% step_number)
            run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 记录运行时间
            if '步骤类型' in step_action:
                if step_action['步骤类型'] == '执行用例':
                    step_run_result = globalpkg.global_function.run_testcase_by_id(step_action['用例id'], testplan)
                else:
                    step_run_result = step_obj.run_step() # 运行sql,或者是普通用例步骤
            else:
                step_run_result = step_obj.run_step(http) # 运行普通用例步骤

            try:# 转换 “ 为 ‘ ，防止数据库存储出错
                action_of_step = step_obj.get_action()
                if type(action_of_step) == type(b''):
                    action_of_step = action_of_step.decode('utf-8')
                elif type(action_of_step) == type({}):
                    action_of_step = str(action_of_step)

                action_of_step = json.dumps(action_of_step)
                action_of_step = action_of_step.replace('"', "'")

                result_of_step = step_obj.get_expected_result()
                if type(result_of_step) == type(b''):
                    result_of_step = result_of_step.decode('utf-8')
                elif type(result_of_step) == type({}):
                    result_of_step = str(result_of_step)

                result_of_step = result_of_step.replace('"', "'")
				# except Exception as e:
            #     logger.error('获取step action、expected_result出错 %s' % e)
            #     action_of_step = ''
            #     result_of_step = ''
            finally:
                if step_run_result[0] == 'Error':
                    fail_or_error_reason = step_run_result[1][0][1]
                    fail_or_error_reason = fail_or_error_reason.replace('\n', '')
                    fail_or_error_reason = fail_or_error_reason.replace('\"', '')
                    fail_or_error_reason = fail_or_error_reason.replace('\'', '')
                    logger.error('步骤[%s]执行出错,停止执行用例[id=%s, name=%s]' % (step_number, self.testcase_id, self.testcase_name))
                    sql_update = 'UPDATE '+ case_step_report_tb +' SET runresult=\"%s\",reason=\"%s\", protocol_method=\"%s\", runtime=\"%s\",' \
                                                                 'step_action=\"%s\", expected_results=\"%s\"' \
                                                                 ' WHERE executed_history_id = %s AND testcase_id = %s AND step_id = %s' \
                                                                 ' AND project=\'%s\' AND testplan=\'%s\''
                    data = (step_run_result[0], fail_or_error_reason, protocol_method, run_time, action_of_step, result_of_step, str(executed_history_id),self.testcase_id, step_id,
                                                                  self.testproject, testplan)
                    logger.info('正在更新步骤执行结果')
                    testdb.execute_update(sql_update, data)
                    return step_run_result
                elif step_run_result[0] == 'Fail':
                    fail_or_error_reason = step_run_result[1][0][1]
                    fail_or_error_reason = fail_or_error_reason.replace('\n', '')
                    fail_or_error_reason = fail_or_error_reason.replace('\"', '')
                    fail_or_error_reason = fail_or_error_reason.replace('\'', '')
                    logger.info('步骤[%s]执行失败,停止执行用例[id=%s, name=%s]' % (step_number, self.testcase_id, self.testcase_name))
                    sql_update = 'UPDATE '+ case_step_report_tb +' SET runresult=\"%s\",reason=\"%s\", protocol_method=\"%s\", runtime=\"%s\",' \
                                                                 'step_action=\"%s\", expected_results=\"%s\"' \
                                                                 ' WHERE executed_history_id = %s AND testcase_id = %s AND step_id = %s' \
                                                                 ' AND project=\'%s\' AND testplan=\'%s\''
                    data = (step_run_result[0], fail_or_error_reason, protocol_method, run_time, action_of_step, result_of_step, str(executed_history_id),self.testcase_id, step_id,
                                                                  self.testproject, testplan)
                    logger.info('正在更新步骤执行结果')
                    testdb.execute_update(sql_update, data)
                    return step_run_result
                elif step_run_result[0] == 'Block':
                    fail_or_error_reason = step_run_result[1]
                    logger.info('步骤[%s]执行失败,停止执行用例[id=%s, name=%s]' % (step_number, self.testcase_id, self.testcase_name))
                    sql_update = 'UPDATE '+ case_step_report_tb +' SET runresult=\"%s\",reason=\"%s\", protocol_method=\"%s\", runtime=\"%s\"' \
                                                                 ' WHERE executed_history_id = %s AND testcase_id = %s AND step_id = %s' \
                                                                 ' AND project=\'%s\' AND testplan=\'%s\''
                    data =  (step_run_result[0], fail_or_error_reason, '无', run_time, str(executed_history_id), self.testcase_id, step_id,
                                                                  self.testproject, testplan)
                    logger.info('正在更新步骤执行结果')
                    testdb.execute_update(sql_update, data)
                    return  step_run_result
                else:
                    fail_or_error_reason = ''
                    sql_update = 'UPDATE '+ case_step_report_tb +' SET runresult=\"%s\",reason=\"%s\", protocol_method=\"%s\", runtime=\"%s\",' \
                                 'step_action=\"%s\", expected_results=\"%s\"'\
                                 ' WHERE executed_history_id = %s AND testcase_id = %s AND step_id = %s'\
                                 ' AND project=\'%s\' AND testplan=\'%s\''
                    data = (step_run_result[0], fail_or_error_reason, protocol_method, run_time, action_of_step, result_of_step, str(executed_history_id),self.testcase_id, step_id,
                                     self.testproject, testplan)
                    logger.info('正在更新步骤执行结果')
                    testdb.execute_update(sql_update, data)

        logger.info('测试用例[id=%s, name=%s]执行成功' % (self.testcase_id, self.testcase_name))
        return ('Pass', '')

