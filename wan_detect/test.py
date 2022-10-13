import json

with open('config.json','r') as f:
    config = json.load(f)
config['Interval'] = 3
with open('config.json','w') as f:
    f.write(json.dumps(config))
