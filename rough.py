# balance 2 connection is needed
import random
import pandas as pd 
import pickle
user_data=pd.read_csv("data/musae_git_target.csv")
edge_data=pd.read_csv("data/musae_git_edges.csv")

selected_nodes=pickle.load(open("data/selected_nodes.pkl","rb"))
selected_nodes.drop(["index"],axis=1,inplace=True)
selected_nodes["id"]=selected_nodes["id"].astype("int")
selected_nodes["ml_target"]=selected_nodes["id"].apply(lambda idx : user_data.iloc[idx]["ml_target"])

selected_nodes_ids=list(selected_nodes["id"])
edge_index=[[],[]]
nodes_parsed=[]
def generate_graph(dev_id,nodes_needed):
    neighbour_dev_ids=edge_data.loc[edge_data["id_1"]==dev_id]["id_2"].values
    still_needed=0
    for neighbour_dev in neighbour_dev_ids:
        if len(set([item for sublist in edge_index for item in sublist]))>=10:
            break
        else:
            if dev_id in selected_nodes_ids and neighbour_dev in selected_nodes_ids:
                edge_index[0].append(dev_id),edge_index[1].append(neighbour_dev)
                still_needed+=1
            else:
                pass
                
    nodes_parsed.append(dev_id)
    nodes=set([item for sublist in edge_index for item in sublist])
    if len(nodes)>=nodes_needed:
        return edge_index
    else:
        dev_id = list(set(nodes) - set(nodes_parsed))[0]
        nodes_needed-=still_needed+1 #why plus 1 because of the current node 
        return generate_graph(dev_id,nodes_needed)




result=generate_graph(36141,10)
print(result)
nodes=set([item for sublist in result for item in sublist])
print(len(nodes))



### Visualization

dev_name=user_data.loc[user_data["id"]==dev_id]["name"].values[0]
print("Developer's Name :",dev_name)
Graph=nx.Graph()
for source,dest in zip(result[0],result[1]):
    src_name,dest_name=user_data.loc[user_data["id"]==source]["name"].values[0],user_data.loc[user_data["id"]==dest]["name"].values[0]
    src_domain,dest_domain=user_data.loc[user_data["id"]==source]["ml_target"].values[0],user_data.loc[user_data["id"]==dest]["ml_target"].values[0]
    if src_domain==1:
        src_domain="ML_dev"
    else:
        src_domain="web_dev"
    if dest_domain==1:
        dest_domain="ML_dev"
    else:
        dest_domain="web_dev"
    src,dest=src_name+"_"+src_domain,dest_name+"_"+dest_domain
    Graph.add_edge(src,dest)
nx.draw(Graph,with_labels=True)
