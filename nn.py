from pybrain.tools.shortcuts import buildNetwork


inputs = 2 # inputs are epoch and station
hidden_nodes = 2
outputs = 6 # outputs are a crowdedness level for each train wagon

net = buildNetwork(inputs, hidden_nodes, outputs)