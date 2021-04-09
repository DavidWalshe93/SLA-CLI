import pandas as pd
import yaml
import json
from pprint import pprint
from collections import OrderedDict

# Load schema to map.
with open(r"db_schema.yml") as fh:
    data = yaml.safe_load(fh)

sorted_datasets = sorted(data["datasets"])

order_dict = OrderedDict()
order_dict.update({"datasets": OrderedDict()})
order_dict.update({"abbrev": data["abbrev"]})

# Format the dataset names.
for dataset in sorted_datasets:
    dataset_new = (dataset.lower()
                   .replace(" ", "_")
                   .replace("-", "_")
                   .replace("(", "")
                   .replace(")", "")
                   .replace("/", "")
                   .replace("\\", "")
                   .replace("__", "_")
                   .replace("__", "_"))
    order_dict["datasets"].update({dataset_new: data["datasets"][dataset]})

# Write out the json database file.
with open("../src/sla_cli/db/db.json", "w") as fh:
    json.dump(order_dict, fh, indent=4)
