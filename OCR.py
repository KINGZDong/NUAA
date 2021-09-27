#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# pip:pip install library_you_need -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
'''
#--------------------------------------------------------------#
#                                                              #
#--------------------------------------------------------------#
#
#                   @Project Name：Auto_Clock_in_NUAA                    #
#
#                   @File Name：OCR.py                           #
#
#                   @Programmer：Wangzhidong                   #
#
#                   @Start Date：2021/9/27 0027 11:29          #
#
#                   @Last Update：2021/9/27 0027 11:29         #
#-------------------------------------------------------------#   
#Class:
#                  MyOCR
#-------------------------------------------------------------#
'''

import base64
import requests

API_KEY = 'cOltTmmGmYGZzEVLUVkPz0Ln' # 自行获取
SECRET_KEY = '7NprO0gn5PW1L4kpbZ58qGxQTU49AMpN'  # 自行获取
OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"  # OCR接口
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'  # TOKEN获取接口


class MyOCR():

    def fetch_token(self):
        # 获取token
        params = {'grant_type': 'client_credentials',
                  'client_id': API_KEY,
                  'client_secret': SECRET_KEY}
        try:
            f = requests.post(TOKEN_URL, params, timeout=5)
            if f.status_code == 200:
                result = f.json()
                if 'access_token' in result.keys() and 'scope' in result.keys():
                    if not 'brain_all_scope' in result['scope'].split(' '):
                        return None, 'please ensure has check the  ability'
                    return result['access_token'], ''
                else:
                    return None, '请输入正确的 API_KEY 和 SECRET_KEY'
            else:
                return None, '请求token失败: code {}'.format(f.status_code)
        except BaseException as err:
            return None, '请求token失败: {}'.format(err)

    def read_file(self, image_path):
        f = None
        try:
            f = open('location.png', 'rb')  # 二进制读取图片信息
            return f.read(), ''
        except BaseException as e:
            return None, '文件({0})读取失败: {1}'.format(image_path, e)
        finally:
            if f:
                f.close()

    def pic2text(self, img_path):
        def request_orc(img_base, token):
            """
            调用百度OCR接口，图片识别文字
            :param img_base: 图片的base64转码后的字符
            :param token: fetch_token返回的token
            :return: 返回一个识别后的文本字典
            """
            try:
                req = requests.post(
                    OCR_URL + "?access_token=" + token,
                    data={'image': img_base},
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
                if req.status_code == 200:
                    result = req.json()
                    if 'words_result' in result.keys():
                        return req.json()["words_result"], ''
                    elif 'error_msg' in result.keys():
                        return None, '图片识别失败: {}'.format(req.json()["error_msg"])

                else:
                    return None, '图片识别失败: code {}'.format(req.status_code)
            except BaseException as err:
                return None, '图片识别失败: {}'.format(err)

        file_content, file_error = self.read_file(img_path)
        if file_content:
            token, token_err = self.fetch_token()
            if token:
                results, result_err = request_orc(base64.b64encode(file_content), token)
                if result_err:  # 打印失败信息
                    # print(result_err)
                    return result_err
                for result in results:  # 打印处理结果
                    # print(result)
                    return result
