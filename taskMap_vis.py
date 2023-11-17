import utils 
import sys
import networkx as nx
from pyvis.network import Network

data_file = 'data.xml'
data_root = utils.getRoot(data_file)

map_file = 'map.xml'
map_root = utils.getRoot(map_file)

map_list = []
"""
    map_list = list of mapping 
    mapping = (task, node)
"""
for bind in map_root.findall('bind'):
    task = bind.find('task').get('value')
    node = bind.find('node').get('value')
    map_list.append((int(task), int(node)))

tasks_list = []
"""
    tasks_list = list of tasks
    task = [id, requirement, generate]
"""
for tasks in data_root.findall('tasks'):
    for task in tasks:
        single_task = []
        requirement_dict = {} 
        task_id = task.attrib['id']
        single_task.append(task_id)
        for requirement in task.findall(".//requires/requirement"): 
            type_value = requirement.find('type').get('value')
            source_value = requirement.find('source').get('value')
            count_min = requirement.find('count').get('min')
            requirement_dict['type'] = type_value
            requirement_dict['source'] = source_value
            requirement_dict['count_min'] = count_min

        single_task.append(requirement_dict)
            
        destination_dict = {} 
        for destination in task.findall(".//generates/possibility/destinations/destination"): 
            count = destination.find('count').get('min')
            type = destination.find('type').get('value')
            dest = destination.find('task').get('value')
            destination_dict['count'] = count 
            destination_dict['type'] = type 
            destination_dict['dest'] = dest 
        
        single_task.append(destination_dict)
        tasks_list.append(single_task)

print("\n--- Results ---")

print("\nRequire + Generate Info")
for task in tasks_list:
    print(task)

print("\nMapping")
print(map_list)


print("\nStarting Serious Business")

net = Network(notebook=True, directed=True)

for bind in map_list:
    task = bind[0]
    node = bind[1]

    net.add_node(node)
    net.nodes[node]["id"] = task





# for i in range(len(map_list)):
#     for task in tasks_list:
#         node_id = net.nodes[i]['id']
#         if node_id == int(task[0]):
#             """Checking Generate"""
#             if len(task[2]) != 0:

#                 print("Generate is not empty")
#                 net.add_edge(node_id, int(task[2]['dest']), label="G", 
#                                                           count=task[2]['count'], 
#                                                           type=task[2]['type'])

#             """Checking Require"""
#             if len(task[1]) != 0:
#                 print("Require is not Empty")
#                 net.add_edge(node_id, int(task[1]['source']),  label="R", 
#                                                             count=task[1]['count_min'], 
#                                                             type=task[1]['type'])



# # print(G.edges(data=True))
# # utils.getNodeAttributes(G)
# utils.visMultiDiGraph(net)