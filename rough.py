# balance 2 connection is needed
import random
import pandas as pd 
edge_data=pd.read_csv("data/musae_git_edges.csv")

edge_index=[[],[]]
nodes_parsed=[]
def generate_graph(dev_id,nodes_needed):
    neighbour_dev_ids=edge_data.loc[edge_data["id_1"]==dev_id]["id_2"].values
    for neighbour_dev in neighbour_dev_ids:
        if len(nodes=set([item for sublist in edge_index for item in sublist]))>=10:
            break
        else:
            edge_index[0].append(dev_id),edge_index[1].append(neighbour_dev)
    nodes_parsed.append(dev_id)
    nodes=set([item for sublist in edge_index for item in sublist])
    if len(nodes)>=nodes_needed:
        return edge_index
    else:
        dev_id = random.choice(list(set(nodes) - set(nodes_parsed)))
        nodes_needed-=len(neighbour_dev_ids)+1 #why plus 1 because of the current node 
        return generate_graph(dev_id,nodes_needed)
print(generate_graph(1,10))
# edge_index