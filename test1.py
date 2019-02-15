import test_slpa
import test_slpa2
import numpy as np
import networkx as nx
from collections import defaultdict
import os
import matplotlib.pyplot as plt
import scipy.io as sio
import gc



def label_Graph(datasetx,datasety):
    #无权重
    G=nx.Graph()
    labels_num=datasety.shape[1]
    node_num=datasetx.shape[0]
    for i in range(node_num):
        label=[]
        node_A = i
        G.add_node(node_A)
        for k in range(labels_num):
            if datasety[i][k]==1:
                label.append(k)
        for j in range(i+1,node_num):
            for k in label:
                if datasety[j][k] == 1:
                    node_A=i
                    node_B=j
                    G.add_edge(node_A,node_B)
        #end for j
    #end for i
    return G

def label_Graph2(datasetx,datasety):
    #包含权重
    G=nx.Graph()
    labels_num=datasety.shape[1]
    node_num=datasetx.shape[0]
    for i in range(node_num):
        label=[]
        node_A = i
        G.add_node(node_A)
        count1=0
        for k in range(labels_num):
            if datasety[i][k]==1:
                label.append(k)
                count1+=1
        for j in range(i+1,node_num):
            count=0
            for k in label:
                if datasety[j][k] == 1:
                    count+=1
            if count>0:
                count2 = 0
                for k in range(labels_num):
                    if datasety[j][k] == 1:
                        count2+=1
                node_A = i
                node_B = j
                G.add_edge(node_A, node_B,weight=count/(count1+count2-count))
        #end for j
    #end for i
    return G

def label_Graph3(datasetx,datasety):
    #画一个小图
    G=nx.Graph()
    labels_num=datasety.shape[1]
    node_num=30
    count=1
    for i in range(node_num):
        label=[]
        for k in range(labels_num):
            if datasety[i][k]==1:
                label.append(k)
                count+=1
        if count>1:
            G.add_node(i, value=14)
        else:
            G.add_node(i, value=label[0])
        for j in range(i+1,node_num):
            kk = 0
            k=0
            for pp in label:
                if datasety[j][pp] == 1:
                    kk += 1
                    k=pp
            if kk > 1:
                G.add_node(j,value=14)
                node_A=i
                node_B=j
                G.add_edge(node_A,node_B)
            elif kk==1:
                G.add_node(j, value=k)
                node_A = i
                node_B = j
                G.add_edge(node_A, node_B)
             #end for j
        #end for if
    #end for i
    return G

def label_Graph4(datasetx,datasety):
    #调整不同标签值作为判定是否连边的依据
    # 无权重
    G = nx.Graph()
    labels_num = datasety.shape[1]
    node_num = datasetx.shape[0]
    for i in range(node_num):
        label = []
        for k in range(labels_num):
            if datasety[i][k] == 1:
                label.append(k)
        for j in range(i + 1, node_num):
            count = 0
            for k in label:
                if datasety[j][k] == 1:
                    count += 1
            if count > 2:
                node_A = i
                node_B = j
                G.add_edge(node_A, node_B)
        # end for j
    # end for i
    return G




def saveCominformationToFile(information, filename):
    nodes_of_community_c = []  # 保存社团中的节点，每个元素是一个节点字符串

    file = open(filename, 'w')

    for c in range(len(information)):
        str_nodes = ""
        for j in information[c]:
            str_nodes += str(j) + " "
        str_nodes += "\n"
        nodes_of_community_c.append(str_nodes)
    # end for

    file.writelines(nodes_of_community_c)
    file.close()

def test_shao(filename,num):
    #测试每个社区生成文件所缺少的点
    list1 = []
    with open(filename, 'r') as f:
        for line in f.readlines():  # 读取全部行
            items = line.strip('\r\n').strip().split(' ')
            items_new = [x for x in items if x != ' ' and int(x) not in list1]
            for i in items_new:
                list1.append(int(i))
    less=[]
    count=0
    for i in range(num):
        if i not in list1:
            less.append(i)
            count+=1
    return num-count
# global G1
# G1=nx.Graph()
# G2=nx.Graph()
if __name__=="__main__":
    ####################################读数据######################################
    datasetx1 = sio.loadmat('data/yeast/yeast_train_x.mat')
    datasetx = datasetx1['x']
    datasety1 = sio.loadmat('data/yeast/yeast_train_y.mat')
    datasety = datasety1['y']

    ####################################考虑对称权重的图预测过程###################################################
    G = label_Graph2(datasetx, datasety)#修改label_Graph2
    nodenumbers = G.number_of_nodes()
    print(G.number_of_nodes())  # 确定有没有点没有标签

    com_num = []
    count = 0
    nx.write_gml(G, "result/duichen/yeast1/a_G_yeast1.gml")
    test_slpa2.saveGraphToEdgeFile(G, "result/duichen/yeast1/a_G_yeast_edge1.txt")
    for T in range(100, 40, -10):
        for i in range(5, 55, 5):
            com_nummid = []
            com_nummid.append(T)
            com_nummid.append(i)
            print("this is the :", i)
            r = i / 100
            communities, commnum = test_slpa2.find_community(G, T, r)
            print("community number is:", commnum)
            com_nummid.append(commnum)
            for c in communities.keys():
                print(str(c) + "-->" + str(sorted(communities[c])))
            o = {}
            overlapping_node = 0
            for node_i in G.nodes():
                o[node_i] = 0
                for c in communities.keys():
                    if node_i in communities[c]:
                        o[node_i] += 1
                if o[node_i] > 1:
                    overlapping_node += 1
            print("重叠节点个数：", overlapping_node)
            com_nummid.append(overlapping_node)
            filename = "result/duichen/yeast1/" + "communities_" + "yeast_%d" % T + "_r_0%d" % i + ".txt"
            test_slpa.saveCommunitiesToFile(communities, filename)
            less=test_shao(filename, 1500)
            print("the nodes in the all community:", less)
            com_nummid.append(less)
            com_num.append(com_nummid)
    filename1 = "result/duichen/yeast1/" + "a_communities" + ".txt"
    saveCominformationToFile(com_num, filename1)



    '''
    ####################################不同k（count）值的的预测过程################################
    G=label_Graph4(datasetx,datasety)
    nodenumbers=G.number_of_nodes()
    print(G.number_of_nodes())#确定有没有点没有标签

    com_num = []
    count = 0
    nx.write_gml(G,"result/k=3/yeast/yeast2/a_G_yeast2.gml")
    test_slpa.saveGraphToEdgeFile(G,"result/k=3/yeast/yeast2/a_G_yeast_edge2.txt")
    for T in range(100,90,-10):
        for i in range(5,55,5):
            com_nummid = []
            com_nummid.append(T)
            com_nummid.append(i)
            print("this is the :",i)
            r=i/100
            communities,commnum = test_slpa.find_community(G, T, r)
            print("community number is:",commnum)
            com_nummid.append(commnum)
            for c in communities.keys():
                print(str(c)+"-->"+str(sorted(communities[c])))
            o = {}
            overlapping_node = 0
            for node_i in G.nodes():
                o[node_i] = 0
                for c in communities.keys():
                    if node_i in communities[c]:
                        o[node_i] += 1
                if o[node_i] > 1:
                    overlapping_node += 1
            print("重叠节点个数：", overlapping_node)
            com_nummid.append(overlapping_node)
            com_num.append(com_nummid)
            filename = "result/k=3/yeast/yeast2/" + "communities_" + "yeast_%d" % T + "_r_0%d" % i + ".txt"
            test_slpa.saveCommunitiesToFile(communities, filename)
            print("the nodes in the all community:",test_shao(filename,1500))
    filename1 = "result/k=3/yeast/yeast2/" + "a_communities" + ".txt"
    saveCominformationToFile(com_num, filename1)
    '''

    '''
    ####################################考虑权重的图预测过程###################################################
    com_num=[]
    count=0
    del G
    gc.collect()
    G=label_Graph2(datasetx, datasety)
    nx.write_gml(G, "result/multi_label/mediamill/G_mill2.gml")
    test_slpa2.saveGraphToEdgeFile(G, "result/multi_label/mediamill/Gmill_edge2.txt")
    for T in range(100, 600, 100):
        for i in range(5, 50, 5):
            com_nummid = []
            com_nummid.append(T)
            com_nummid.append(i)
            print("this is the :",i)
            r = i / 100
            communities, commnum = test_slpa2.find_community(G, T, r)
            print("community number is:", commnum)
            com_nummid.append(commnum)
            for c in communities.keys():
                print(str(c) + "-->" + str(sorted(communities[c])))
            o = {}
            overlapping_node = 0
            for node_i in G.nodes():
                o[node_i] = 0
                for c in communities.keys():
                    if node_i in communities[c]:
                        o[node_i] += 1
                if o[node_i] > 1:
                    overlapping_node += 1
            print("重叠节点个数：", overlapping_node)
            com_nummid.append(overlapping_node)
            com_num.append(com_nummid)

            filename = "result/multi_label/mediamill/mediamill2/" + "communities_" + "mediamill_%d" % T + "_r_0%d" % i + ".txt"
            test_slpa2.saveCommunitiesToFile(communities, filename)
    filename1 = "result/multi_label/mediamill/mediamill2/" + "a_communities"+ ".txt"
    saveCominformationToFile(com_num,filename1)
    '''


    '''
    #############################用比较少的点画一个小一点的图##############################################
    # datasetx1 = sio.loadmat('data/yeast_train_x.mat')
    # datasetx = datasetx1['x']
    # datasety1 = sio.loadmat('data/yeast_train_y.mat')
    # datasety = datasety1['y']
    # G = label_Graph3(datasetx, datasety)
    # nx.write_gml(G,"result/multi_label/G_80test2.gml")

    #test_slpa.saveGraphToEdgeFile(G,"result/multi_label/G_80edge.txt")
    # for T in range(100, 90, -10):
    #     for i in range(20, 50, 5):
    #         print("this is the :", i)
    #         r = i / 100
    #         communities, commnum = test_slpa.find_community(G, T, r)
    #         print("community number is:", commnum)
    #         for c in communities.keys():
    #             print(str(c) + "-->" + str(sorted(communities[c])))
    #         o = {}
    #         overlapping_node = 0
    #         for node_i in G.nodes():
    #             o[node_i] = 0
    #             for c in communities.keys():
    #                 if node_i in communities[c]:
    #                     o[node_i] += 1
    #             if o[node_i] > 1:
    #                 overlapping_node += 1
    #         print("重叠节点个数：", overlapping_node)
    #
    #         filename = "result/multi_label/yeast_test2/" + "communities_" + "yeast_%d" % T + "_r_0%d" % i + ".txt"
    #         test_slpa.saveCommunitiesToFile(communities, filename)
    '''

    print('a')

