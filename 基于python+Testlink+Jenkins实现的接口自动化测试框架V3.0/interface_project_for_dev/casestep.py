#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import unittest
import re
import json
from collections import OrderedDict

from globalpkg.log import logger
from globalpkg.global_var import  *
from interface.InterfaceUnittestTestCase import *
from interface.wecharno_card_coupon import *

class CaseStep:
    outputs_list = []  # 专门用于存放数据库服务器返回的sql单条记录查询结果
    def __init__(self, step_id, step_number, expected_result, action, testcase_id):
        self.step_id = step_id
        self.expected_result= expected_result
        self.action = action
        self.step_number = step_number
        self.testcase_id = testcase_id

    def get_step_id(self):
        return self.step_id

    def get_expected_result(self):
        return self.expected_result

    def set_expected_result(self, expected_result):
        self.expected_result = expected_result

    def get_action(self):
        return  self.action

    def set_action(self, action):
        self.action = action

    def set_function_of_action(self,function):
        self.action['函数'] = function


    def set_method_of_action(self, method):
        self.action['方法'] = method

    def get_method_of_action(self):
        return  self.action['方法']

    def set_params_of_action(self, params):
        self.action['参数'] = params

    def get_params_of_action(self):
        return self.action['参数']

    def get_url_of_action(self):
        return self.action['url']

    def set_url_of_action(self, url):
        self.action['url'] = url

    def get_step_number(self):
        return  self.step_number

    def get_preconditions(self):
        return  self.get_preconditions

    def get_summary(self):
        return self.summary

    def get_tasecase_id(self):
        return  self.testcase_id

    # 接口请求参数中动态参数转换成具体的参数值
    def __repalce_value_of_parmas_in_quest(self, params):
        str_dic = '{"key":"value"}'
        temp_re = json.loads(str_dic, object_pairs_hook=OrderedDict)
        is_ordered_dict = 0
        if type(params) == type(temp_re):  # step_action为OrderdDict
            params = json.dumps(params)
            is_ordered_dict = 1

        if type(params) == type({}): # json串
            # 遍历查找动态参数
            for key, value in params.items():
                if type(value) == type(''): # 值为动态参数的前提
                    if value.find('[') == 0 and value.find(']') == len(value) -1 and value.find('global_') == -1: # 非全局参数
                        logger.info('从json字典串中找到待替换的非全局动态参数：%s' % value)
                        value = value.lstrip('[')
                        value = value.rstrip(']')
                        if value.find('.') == -1:
                            class_name = 'InterfaceUnittestTestCase'
                            param_name = value
                        else:
                            class_name, param_name = value.split('.')
                        output_list = (globals()[class_name]).outputs_list
                        for item in output_list:
                            if param_name in item.keys():
                                # 替换参数
                                params[key] = item.get(param_name)
                    elif value.find('[') == 0 and value.find(']') == len(value) -1 and value.find('global_') != -1: # 全局参数
                        logger.info('从json字典串中找到待替换的全局动态参数：%s' % value)
                        param_name = value.lstrip('[')
                        param_name = param_name.rstrip(']')

                        try:
                            params[key] = globals()[param_name]
                        except Exception as e:
                            logger.error('转换全局动态参数出错 %s' % e)

            logger.info('转换后的参数体为：%s' % params)
            return  params
        elif type(params) == type(''): # 字符串类型的参数
            # 遍历查找动态参数
            var_params = re.findall('\[.+?\]', params)
            if var_params == []:
                logger.info('没找到需要替换的动态参数')
                if is_ordered_dict == 1:
                    params = json.loads(params, object_pairs_hook=OrderedDict)
                return params

            new_params = params
            for item in var_params:
                if item.find('global_') == -1:
                    logger.info('从字符串中找到待替换的非全局动态参数：%s' % item)
                    value = item.lstrip('[')
                    value = value.rstrip(']')
                    if value.find('.') != -1:
                        class_name, param_name = value.split('.')
                    else:
                        class_name = 'InterfaceUnittestTestCase'
                        param_name = value
                    output_list = (globals()[class_name]).outputs_list
                    for output in output_list:
                        if param_name in output.keys():
                            # 替换参数
                            new_params = new_params.replace(item,str(output.get(param_name)))
                elif item.find('global_') != -1:
                    logger.info('从字符串中找到待替换的全局动态参数：%s' % item)
                    param_name = item.lstrip('[')
                    param_name = param_name.rstrip(']')

                    try:
                        new_params = new_params.replace(item, str(globals()[param_name]))
                    except Exception as e:
                        logger.error('转换全局动态参数出错 %s' % e)

            if is_ordered_dict == 1:
                new_params = json.loads(new_params, object_pairs_hook=OrderedDict)				
            logger.info('转换后的参数体为：%s' % new_params)
            return  new_params
        else:
            logger.info('没找到需要替换的动态参数')
            return  params

    def run_step(self, http=None):
        if  '步骤类型' in self.action and (self.action['步骤类型']).lower() == '执行sql':
            # 执行sql脚本
            step_run_result = self.run_sql_in_action()
            logger.debug('step_run_result：error, %s' % step_run_result[1])
            return  (step_run_result[0], [('CaseStep',step_run_result[1])])
        else:
            try:
                if '类名' in self.action.keys():
                    class_name = self.action['类名']
                else:
                    class_name = 'InterfaceUnittestTestCase'
                if '函数' in self.action.keys():
                    function = self.action['函数']
                else:
                    function = 'test_interface_of_urlencode'
                logger.info('调用的方法为：%s.%s' % (class_name, function))
            except Exception as e:
                logger.error('步骤[%s]信息填写不正确: %e，执行失败' % (self.step_number,e))
                return ('Error',[('CaseStep','%s' % e)])

            # 替换动态参数
            self.action['参数'] = self.__repalce_value_of_parmas_in_quest(self.action['参数'])
            self.action['url'] = self.__repalce_value_of_parmas_in_quest(self.action['url'])
            if  '请求头' in self.action.keys():
                self.action['请求头'] = self.__repalce_value_of_parmas_in_quest(self.action['请求头'])
                self.action['请求头'] = json.dumps(self.action['请求头'])
                self.action['请求头'] = json.loads(self.action['请求头'])

            runner = unittest.TextTestRunner()
            test_step_action = unittest.TestSuite()
            test_step_action.addTest((globals()[class_name])(function, http, self))
            step_run_result = runner.run(test_step_action)

            logger.debug('step_run_result：%s, errors：%s，failures：%s' % (step_run_result, step_run_result.errors, step_run_result.failures))
            if 0 != len(step_run_result.errors):
                return ('Error', step_run_result.errors)
            elif 0 != len(step_run_result.failures):
                return ('Fail', step_run_result.failures)
            else:
                return ('Pass', '')

    # 执行sql
    def run_sql_in_action(self):
        if '单条查询' in self.action:
            self.action['参数'] =  self.__repalce_value_of_parmas_in_quest(self.action['参数'])
            self.action['参数'] = eval(self.action['参数']) # 字符串类型的元组转为元组
            query_result, flag = saofudb.select_one_record(self.action['单条查询'],self.action['参数'])
            logger.info('数据库服务器返回的查询结果为为 query_result:%s, flag:%s' % (query_result,flag))
            if flag == True:
                logger.info('正在保存服务器返回结果到自定义变量')
                self.save_onesql_query_result(query_result) # 保存查询记录
                return ('Pass','')
            else:
                return ('Error',str(query_result))
        elif '更新' in self.action:
            self.action['参数'] = self.__repalce_value_of_parmas_in_quest(self.action['参数'])
            self.action['参数'] = eval(self.action['参数'])
            query_result,flag = saofudb.execute_update(self.action['更新'],self.action['参数'])
            if flag == True:
                return ('Pass','')
            else:
                return ('Error',str(query_result))


    # 保存从数据库服务器返回中的内容
    def save_onesql_query_result(self, sql_record):
        if '输出' in self.expected_result.keys(): # 需要提取服务器返回内容
            output = self.expected_result['输出']

            counter = 0
            while counter < len(sql_record):
                for var_name, var_number in output.items():
                    var_number = int(var_number) #以防错误输入了字符串编号
                    temp_var_number = var_number - 1
                    if temp_var_number == counter:
                        key_value = {var_name:sql_record[counter]}
                        if self.outputs_list.count(key_value): # 已有存在值，替换已经存在的值
                            index = CaseStep.outputs_list.index(key_value) + 1
                            CaseStep.outputs_list.insert(index, key_value)
                            CaseStep.outputs_list.remove(key_value)
                        else:# 不存在值,添加到列表
                            CaseStep.outputs_list.append(key_value) # 存储变量到列表[{var_name:var_value}]
                counter = counter + 1

            logger.info('提取的输出结果(key-value对)为:%s' % CaseStep.outputs_list)
        else:
            logger.warn('未检测到从数据库服务器返回中提取内容的要求，请检查是否正确填写预期结果')


