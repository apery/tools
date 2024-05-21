import json
import sys

all_flows = {}

with open(sys.argv[1], "r") as data:
    for line in data:
        d = json.loads(line)
        
        # ignore replies
        if "reply" in d["flow"]:
            if d["flow"]["reply"] == True:
                continue
        
        source = d["flow"]["source"]
        
        source_namespace = "unknown"
        if "namespace" in source:
            source_namespace = source["namespace"]
        if source_namespace not in all_flows:
            all_flows[source_namespace] = {}
        dic_source_namespace = all_flows[source_namespace]

        source_labels = "unknown"
        if "labels" in source:
            source_labels = str(frozenset(source["labels"]))
        if source_labels not in dic_source_namespace:
            dic_source_namespace[source_labels] = {}
        dic_source_labels = dic_source_namespace[source_labels]

        destination = d["flow"]["destination"]
        
        destination_namespace = "unknown"
        if "namespace" in destination:
            destination_namespace = destination["namespace"]
        if destination_namespace not in dic_source_labels:
            dic_source_labels[destination_namespace] = {}
        dic_destination_namespace = dic_source_labels[destination_namespace]
            
        destination_labels = "unknown"
        if "labels" in destination:
            destination_labels = str(frozenset(destination["labels"]))
        if destination_labels not in dic_destination_namespace:
           dic_destination_namespace[destination_labels] = {}
        dic_destination_labels = dic_destination_namespace[destination_labels]

        l4 = d["flow"]["l4"]

        for proto in l4:
            if proto not in dic_destination_labels:
                dic_destination_labels[proto] = {}
            dic_proto = dic_destination_labels[proto]

            destination_port = "unknown"
            if "destination_port" in l4[proto]:
                destination_port = l4[proto]["destination_port"]

            if destination_port not in dic_proto:
                dic_proto[destination_port] = {}

print("{source_namespace};{source_labels};{destination_namespace};{destination_labels};{proto};{destination_port};")
for source_namespace in all_flows:
    dic_source_namespace = all_flows[source_namespace]
    for source_labels in dic_source_namespace:
        dic_destination_namespace = dic_source_namespace[source_labels]
        for destination_namespace in dic_destination_namespace:
            dic_destination_labels = dic_destination_namespace[destination_namespace]
            for destination_labels in dic_destination_labels:
                dic_proto = dic_destination_labels[destination_labels]
                for proto in dic_proto:
                    dic_destination_ports = dic_proto[proto]
                    for destination_port in dic_destination_ports:
                        print(f"{source_namespace};{source_labels};{destination_namespace};{destination_labels};{proto};{destination_port};")

