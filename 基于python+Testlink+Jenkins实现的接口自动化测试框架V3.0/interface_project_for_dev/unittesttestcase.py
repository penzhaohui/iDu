#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import  unittest
import json
import re

from globalpkg.log import logger
from globalpkg.global_var import other_tools

class MyUnittestTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest', http=None, casestep=None):
        super(MyUnittestTestCase, self).__init__(methodName)
        self.http = http
        if '请求头' in casestep.get_action().keys():
            self.headers = casestep.get_action()['请求头']
        else:
            self.headers = {}
        self.method =casestep.get_action()['方法']
        self.url = casestep.get_action()['url']
        self.params = casestep.get_action()['参数']
        self.testcase_id = casestep.get_tasecase_id()
        self.step_id = casestep.get_step_id()
        self.expected_result = casestep.get_expected_result()
        self.casestep = casestep

    # 断言
    def assert_result(self, response_to_check):
        if self.expected_result != '':
            if self.expected_result['匹配规则'] == '包含成员':
                if type(response_to_check) not in [type(''), type([]), type(()), type(set()), type({})]:
                    logger.error('服务器返回内容为不可迭代对象')
                    self.assertEqual(1, 0, msg='服务器返回内容为不可迭代对象')

                # 遍历条件列表， 形如 "条件":[{"模式":"\"success\"", "消息":"创建储值卡支付订单失败,返回json串不包含key - success"},{"模式":"\"attach\"", "消息":"创建储值卡支付订单失败,返回json串不包含key - attach"}]
                for item in self.expected_result['条件']:
                    member = item['模式']
                    logger.info('要匹配的模式（成员）为：%s' % member)
                    self.assertIn (member, response_to_check,msg=item['消息'])

            elif self.expected_result['匹配规则'] == '不包含成员':
                if type(response_to_check) not in [type(''), type([]), type(()), type(set()), type({})]:
                    logger.error('服务器返回内容为不可迭代对象')
                    self.assertEqual(1, 0, msg='服务器返回内容为不可迭代对象')

                # 遍历条件列表，形如 "条件":[{"模式":"\"success\"", "消息":"创建储值卡支付订单失败,返回json串包含key - success"},{"模式":"\"attach\"", "消息":"创建储值卡支付订单失败,返回json串包含key - attach"}]
                for item in self.expected_result['条件']:
                    member = item['模式']
                    logger.info('要匹配的模式（成员）为：%s' % member)
                    self.assertNotIn (member, response_to_check, msg=item['消息'])

            elif self.expected_result['匹配规则'] == '包含字符串':
                if type(response_to_check) in [type({}), type(set()), type(()), type([]), type(1), type(0.01)]:
                    response_to_check = str(response_to_check)
                elif type(response_to_check) != type(''):
                    logger.error('服务器返回内容不为字符串类型')
                    self.assertEqual(1, 0, msg='服务器返回内容不为字符串类型')

                # 遍历条件列表, 形如："条件":[{"模式":"\"success\":true", "消息":"创建储值卡支付订单失败，success不为True"},{"模式":"\"success\":false", "消息":"创建储值卡支付订单失败，success不为false"}]
                for item in self.expected_result['条件']:
                    pattern_str = item['模式']
                    logger.info('要匹配的模式（子字符串）为：%s' % pattern_str)
                    self.assertIn(pattern_str, response_to_check, item['消息'])

            elif self.expected_result['匹配规则'] == '不包含字符串':
                if type(response_to_check) in [type({}), type(set()), type(()), type([]), type(1), type(0.01)]:
                    response_to_check = str(response_to_check)
                elif type(response_to_check) != type(''):
                    logger.error('服务器返回内容不为字符串类型')
                    self.assertEqual(1, 0, msg='服务器返回内容不为字符串类型')

                # 遍历条件列表, 形如："条件":[{"模式":"\"success\":true", "消息":"创建储值卡支付订单失败，success不为True"},{"模式":"\"success\":false", "消息":"创建储值卡支付订单失败，success不为false"}]
                for item in self.expected_result['条件']:
                    pattern_str = item['模式']
                    logger.info('要匹配的模式（子字符串）为：%s' % pattern_str)
                    self.assertNotIn(pattern_str, response_to_check, item['消息'])

            elif self.expected_result['匹配规则'] == '键值相等':
                if type(response_to_check) == type(''): # 字符串类型的字典、json串
                    try:
                        response_to_check = json.loads(response_to_check) # //转字符串为json
                    except Exception as e:
                        logger.error('转换服务器返回内容为字典失败')
                        self.assertEqual(1, 0 ,msg='转换服务器返回内容为字典失败')

                if type(response_to_check) == type([]): # 格式[{}]的json串
                    try:
                        response_to_check = response_to_check[0]
                        response_to_check = json.loads(response_to_check) # //转字符串为json
                    except Exception as e:
                        logger.error('转换服务器返回内容为字典失败')
                        self.assertEqual(1, 0 ,msg='转换服务器返回内容为字典失败')

                if type(response_to_check) != type({}):
                    logger.error('服务器返回内容不为字典、字符串类型的字典')
                    self.assertEqual(1, 0, msg='服务器返回内容不为字典、字符串类型的字典')

                # 遍历条件列表, 形如："条件":[{"模式":{"success":true}, "消息":"创建储值卡支付订单失败，success不为True"},{"模式":{"success":false}, "消息":"创建储值卡支付订单失败，success不为false"}]
                for item in self.expected_result['条件']:
                    pattern_dic = item['模式']
                    # 获取list方式标识的key,value层级值
                    dict_level_list = other_tools.get_dict_level_list(pattern_dic)
                    other_tools.set_dict_level_list([])
                    logger.info('要匹配的字典key,value层级为：%s' % dict_level_list)

                    last_value = other_tools.find_dict_last_leve_value(dict_level_list, response_to_check)
                    logger.info('找到的对应字典层级的最后值为：%s' % last_value)
                    other_tools.set_key_index(0)

                    # 比较同层级，相同key对应的value值
                    self.assertEqual(dict_level_list[len(dict_level_list) -1], last_value, item['消息'])

            elif self.expected_result['匹配规则'] == '匹配正则表达式':
                if type(response_to_check) in [type({}), type(set()), type(()), type([]), type(1), type(0.01)]:
                    response_to_check = str(response_to_check)
                elif type(response_to_check) != type(''):
                    logger.error('服务器返回内容不为字符串类型')
                    self.assertEqual(1, 0, msg='服务器返回内容不为字符串类型')

                # 遍历条件列表, 形如( "条件":[{"模式":"\"success\":true", "消息":"创建储值卡支付订单失败，success不为True"},{"模式":"\"success\":false", "消息":"创建储值卡支付订单失败，success不为false"}]
                for item in self.expected_result['条件']:
                    pattern_str = item['模式']

                    logger.info('要匹配的模式（正则表达式）为：%s' % pattern_str)
                    self.assertRegex(response_to_check, pattern_str, msg=item['消息'])

            elif self.expected_result['匹配规则'] == '不匹配正则表达式':
                if type(response_to_check) in [type({}), type(set()), type(()), type([]), type(1), type(0.01)]:
                    response_to_check = str(response_to_check)
                elif type(response_to_check) != type(''):
                    logger.error('服务器返回内容不为字符串类型')
                    self.assertEqual(1, 0, msg='服务器返回内容不为字符串类型')

                # 遍历条件列表，形如  "条件":[{"模式":"\"success\":true", "消息":"创建储值卡支付订单失败，success为True"},{"模式":"\"success\":false", "消息":"创建储值卡支付订单失败，success为false"}]
                for item in self.expected_result['条件']:
                    pattern_str = item['模式']

                    logger.info('要匹配的模式（正则表达式）为：%s' % pattern_str)
                    self.assertNotRegex(response_to_check, pattern_str, msg=item['消息'])

            elif self.expected_result['匹配规则'] == '完全匹配字典':
                if type(response_to_check) == type(''): # 字符串类型的字典、json串
                    try:
                        response_to_check = json.loads(response_to_check) # //转字符串为json
                    except Exception as e:
                        logger.info('转换服务器返回内容为字典失败')
                        self.assertEqual(1, 0 ,msg='转换服务器返回内容为字典失败')
                elif type(response_to_check) != type({}):
                    logger.error('服务器返回内容不为字典')
                    self.assertEqual(1, 0 , msg='服务器返回内容不为字典')

                # 遍历条件列表 "条件":[{"模式":{"success":true}, "消息":"创建储值卡支付订单失败,返回结果和字典模式不匹配"}]
                for item in self.expected_result['条件']:
                    pattern_dic = item['模式']

                    logger.info('要匹配的模式（字典）为：%s' % pattern_dic)
                    self.assertDictEqual (response_to_check, pattern_dic, msg=item['消息'])

            elif self.expected_result['匹配规则'] == '完全匹配列表':
                if type(response_to_check) == type(''): # 字符串类型的列表
                    try:
                        response_to_check = eval(response_to_check)
                    except Exception as e:
                        logger.info('转换服务器返回内容为列表失败')
                        self.assertEqual(1, 0 ,msg='转换服务器返回内容为列表失败')

                if type(response_to_check) != type([]):
                    logger.info('服务器返回内容不为列表或列表的字符串表示')
                    self.assertEqual(1, 0, msg='服务器返回内容不为列表或列表的字符串表示')

                # 遍历条件列表，形如 "条件":[{"模式":"[\"success\",\"shouke\",2016]", "消息":"创建储值卡支付订单失败,返回结果和列表模式不匹配"}]
                for item in self.expected_result['条件']:
                    pattern_list = eval(item['模式'])

                    logger.info('要匹配的模式（列表）为：%s' % pattern_list)
                    self.assertListEqual (response_to_check, pattern_list, msg=item['消息'])

            elif self.expected_result['匹配规则'] == '完全匹配集合':
                if type(response_to_check) == type(''): # 字符串类型的集合
                    try:
                        response_to_check = eval(response_to_check)
                    except Exception as e:
                        logger.error('转换服务器返回内容为集合失败')
                        self.assertEqual(1, 0 ,msg='转换服务器返回内容为集合失败')

                if type(response_to_check) != type(set()):
                    logger.error('服务器返回内容不为集合或集合的字符串表示')
                    self.assertEqual(1, 0, msg='服务器返回内容不为集合或集合的字符串表示')

                # 遍历条件列表,形如 "条件":[{"模式":"[\"success\",\"shouke\",2016]", "消息":"创建储值卡支付订单失败,返回结果和列表模式不匹配"}]
                for item in self.expected_result['条件']:
                    pattern_set = eval(item['模式'])

                    logger.info('要匹配的模式（集合）为：%s' % pattern_set)
                    self.assertSetEqual (response_to_check, pattern_set, msg=item['消息'])

            elif self.expected_result['匹配规则'] == '完全匹配元组':
                if type(response_to_check) == type(''): # 字符串类型的元组
                    try:
                        response_to_check = eval(response_to_check)
                    except Exception as e:
                        logger.error('转换服务器返回内容为元组失败')
                        self.assertEqual(1, 0 ,msg='转换服务器返回内容为元组失败')

                if type(response_to_check) != type(()):
                    logger.error('服务器返回内容不为元组或元组的字符串表示')
                    self.assertEqual(1, 0, msg='服务器返回内容不为元组或元组的字符串表示')

                # 遍历条件列表,形如 "条件":[{"模式":"[\"success\",\"shouke\",2016]", "消息":"创建储值卡支付订单失败,返回结果和列表模式不匹配"}]
                for item in self.expected_result['条件']:
                    pattern_tuple = eval(item['模式'])

                    logger.info('要匹配的模式（元组）为：%s' % str(pattern_tuple))
                    self.assertTupleEqual(response_to_check, pattern_tuple, msg=item['消息'])

    # 提取服务器返回内容
    def extrator(self,extrator,response_to_check=''):
        if type(extrator) == type({}):  # 获取键值
            #  获取list方式标识的key,value层级值
            dict_level_list = other_tools.get_dict_level_list(extrator)
            other_tools.set_dict_level_list([])

            logger.info('要提取的字典key,value层级为：%s' % dict_level_list)

            if type(response_to_check) == type(''): # 字符串类型的字典、json串
                try:
                    response_to_check = json.loads(response_to_check) # //转字符串为json
                except Exception as e:
                    logger.error('转换服务器返回内容为字典失败：%s' % e)
                    return []

            if type(response_to_check) != type({}):
                logger.error('服务器返回内容不为字典、字符串类型的字典')
                return []

            value_get = other_tools.find_dict_last_leve_value(dict_level_list, response_to_check)
            logger.info('找到的对应字典层级的key的值为：%s' % value_get)
            other_tools.set_key_index(0)

            return value_get
        elif type(extrator) == type(''): # 获取正则表达式匹配的内容
            if type(response_to_check) in [type({}), type(set()), type(()), type([]), type(1), type(0.01)]:
                response_to_check = str(response_to_check)
            elif type(response_to_check) != type(''):
                logger.error('服务器返回内容不为字符串类型')
                return []
            result = re.findall(extrator, response_to_check)
            return  result
        else:
            logger.error('提取器不为字典或者字符串类型的正则表达式')
            return []

    # 保存从服务器返回中提取的内容
    def save_result(self, response_to_check):
        if '输出' in self.expected_result.keys(): # 需要提取服务器返回内容
            output = self.expected_result['输出']
            if type(output) == type({}):
                for var_name, extrator in output.items():
                    if type(extrator) == type({}): # 如果为字典,获取键值
                        value_get = self.extrator(extrator, response_to_check) # 获取键对应值
                        logger.info('获取到的变量的值为：%s' % value_get)

                        key_value = {var_name:value_get}
                        if self.outputs_list.count(key_value): # 已有存在值，替换已经存在的值
                            index = self.outputs_list.index(key_value) + 1
                            self.outputs_list.index(index, key_value)
                            self.outputs_list.remove(key_value)
                        else:# 不存在值,添加到列表
                            self.outputs_list.append(key_value)

                    else: # 正则表达式式提取
                        value_get = self.extrator(extrator, response_to_check)

                        index = 1
                        for item in value_get:
                            logger.info('获取到的变量的值为：%s' % value_get)

                            var_name = var_name + '_' + str(index)
                            index = index + 1
                            key_value = {var_name:item}
                            if self.outputs_list.count(key_value): # 已有存在值，替换已经存在的值
                                index = self.outputs_list.index(key_value) + 1
                                self.outputs_list.insert(index, key_value)
                                self.outputs_list.remove(key_value)
                            else:# 不存在值,添加到列表
                                self.outputs_list.append(key_value)

            logger.info('提取的输出结果(key-value对)为:%s' % self.outputs_list)
        else:
            logger.warn('未检测到从服务器返回中提取内容的要求，请检查是否正确填写预期结果')

    def tearDown(self):
        pass


