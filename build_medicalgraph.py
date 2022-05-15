#!/usr/bin/env python3
# coding: utf-8
# File: MedicalGraph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-3

import os
import json
from py2neo import Graph,Node

class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/kg_crime.json')
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="shz")

    '''读取文件'''
    def read_nodes(self):
        # 共７类节点
        crime_bigs = [] # 大罪
        crime_smalls = [] #小罪
        disease_infos = []#小罪概念
        rels_commonddrug = []


        count = 0
        for data in open(self.data_path, encoding='utf-8'):
            disease_dict = {}

            count += 1
            # print(count)
            data_json = json.loads(data)

            crime_small = data_json['crime_small']
            crime_smalls.append(crime_small)

            disease_dict['name'] = crime_small
            crime_big = data_json['crime_big']
            rels_commonddrug.append([crime_small, crime_big])
            # print(rels_commonddrug)


            crime_bigs.append(crime_big)
            # print(crime_bigs)
            disease_dict['gainian'] = data_json['gainian']
            disease_infos.append(disease_dict)
        return set(crime_bigs), set(crime_smalls), disease_infos, rels_commonddrug

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱小罪的节点'''
    def create_diseases_nodes(self, disease_infos):
        count = 0
        for disease_dict in disease_infos:
            node = Node("Crime_small", name=disease_dict['name'], gainian=disease_dict['gainian'])
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        Crime_big, Crime_small,disease_infos, rels_commonddrug = self.read_nodes()
        self.create_diseases_nodes(disease_infos)
        self.create_node('Crime_big', Crime_big)
        print(len(Crime_big))
        return


    '''创建实体关系边'''
    def create_graphrels(self):
        Crime_big, Crime_small,disease_infos ,rels_commonddrug= self.read_nodes()

        self.create_relationship("Crime_small", "Crime_big", rels_commonddrug,'belongs_to', "属于")


    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''

    def export_data(self):
        Crime_big, Crime_small, disease_infos, rels_commonddrug = self.read_nodes()
        f_drug = open('crime_big.txt', 'w+')
        f_drug1 = open('crime.txt', 'w+')
        f_drug.write('\n'.join(list(Crime_big)))
        f_drug1.write('\n'.join(list(Crime_small)))
        f_drug.close()
        f_drug1.close()



if __name__ == '__main__':
    handler = MedicalGraph()
    # handler.create_graphnodes()
    # handler.create_graphrels()
    # handler.export_data()
