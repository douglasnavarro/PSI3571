from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from datetime import datetime
from pybrain.supervised.trainers import BackpropTrainer


def parse_data(row):
    station, date, crowd_level = row.split(',')

    date = datetime.strptime(date, '%Y-%m-%dT%H:%M')
    year = date.year
    dayofmonth = date.day
    month = date.month
    dayofweek = date.weekday()
    hour = date.hour
    minute = date.minute

    crowd_level = tuple(crowd_level.split(' '))

    return (int(station), year, month, dayofmonth, dayofweek, hour, minute), crowd_level

inputs = 7 # inputs are station, year, month, day of month, day of week, hour and minute
hidden_nodes = 4
outputs = 6 # outputs are a crowdedness level for each train wagon

net = buildNetwork(inputs, hidden_nodes, outputs)
print(net)

ds = SupervisedDataSet(7, 6)
print("\nParsing data from file to SupervisedDataset...")
with open('fake_data.txt', 'r') as f:
    for row in f:
        row = row.replace('\n', '')
        inpt, target = parse_data(row)
        ds.addSample(inpt, target)
print("Dataset populated with " + str(len(ds)) + " samples")

trainer = BackpropTrainer(net, ds)
print(trainer.trainUntilConvergence(verbose = True))

for mod in net.modules:
    print("Module:", mod.name)
    if mod.paramdim > 0:
        print("--parameters:", mod.params)
    for conn in net.connections[mod]:
        print("-connection to", conn.outmod.name)
        if conn.paramdim > 0:
             print("- parameters", conn.params)
    if hasattr(net, "recurrentConns"):
        print("Recurrent connections")
        for conn in net.recurrentConns:
            print("-", conn.inmod.name, " to", conn.outmod.name)
            if conn.paramdim > 0:
                print("- parameters", conn.params)

