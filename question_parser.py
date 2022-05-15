#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        # print(entity_dict)
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('crime'))

            elif question_type == 'symptom_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('crime_big'))

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('crime'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询罪的概念
        if question_type == 'disease_cause':
            sql = ["MATCH (m:Crime_small) where m.name = '{0}' return m.name, m.gainian ".format(i) for i in entities]

        # 查询小罪属于哪种大罪
        elif question_type == 'disease_symptom':
            sql = ["MATCH (m:Crime_small)-[r:belongs_to]->(n:Crime_big) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询大罪包括哪些小罪
        elif question_type == 'symptom_disease':
            sql = ["MATCH (m:Crime_small)-[r:belongs_to]->(n:Crime_big) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]


        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
