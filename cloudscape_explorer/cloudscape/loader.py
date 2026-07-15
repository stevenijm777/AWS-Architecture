import os
import networkx as nx
import csv


class Study:
    def __init__(self, nx_graph):
        self.nx_graph = nx_graph

    def get_functional_goals(self):
        return self.nx_graph.graph.get("categories", "").split(",")

    def use_for_analysis(self):
        return self.nx_graph.graph["graph_usable"]

    def get_all_nodes_services(self):
        return [v["service"] for k, v in self.nx_graph.nodes(data=True)]

    def select_nodes(self, sel_fn):
        return [k for k, v in self.nx_graph.nodes(data=True) if sel_fn(v)]

    def get_inbound_nodes_for_svc(self, svc, data_only=True):
        svc_nodes = self.select_nodes(lambda v: v["service"] == svc)
        edges = self.nx_graph.in_edges(svc_nodes, True)  # includes duplicates
        if data_only:
            edges = [x for x in edges if x[2]["type"] == "data"]
        src_nodes = [x[0] for x in edges]
        return [self.nx_graph.nodes[x] for x in src_nodes]

    def get_outbound_nodes_for_svc(self, svc, data_only=True):
        svc_nodes = self.select_nodes(lambda v: v["service"] == svc)
        edges = self.nx_graph.out_edges(svc_nodes, True)  # includes duplicates
        if data_only:
            edges = [x for x in edges if x[2]["type"] == "data"]
        tgt_nodes = [x[1] for x in edges]
        return [self.nx_graph.nodes[x] for x in tgt_nodes]

    def iterate_flows(self):
        edges = self.nx_graph.edges(data=True)
        grouped = {}
        for edge in edges:
            flow_id = edge[2]["flow_id"]
            minimal_edge = (edge[0], edge[1])
            grouped.setdefault(flow_id, []).append(minimal_edge)
        return list(grouped.values())


def load_studies(dir):
    studies = []
    for filename in os.listdir(dir):
        if not filename.endswith(".graphml"):
            continue
        path = os.path.join(dir, filename)
        studies.append(Study(nx.read_graphml(path)))
    return studies


def extract_svc_info(fname):
    with open(fname, "r") as f:
        reader = csv.DictReader(f)
        svc_info = {row["name"]: row for row in reader}
    for v in svc_info.values():
        v["is_aws"] = {"True": True, "False": False}[v["is_aws"]]

    return svc_info
