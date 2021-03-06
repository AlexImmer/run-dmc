from process import processed_data, split_data_at_id
from dmc.ensemble import ECEnsemble
from dmc.classifiers import Forest
from dmc.classifiers import TensorFlowNeuralNetwork as TensorNetwork
from dmc.classifiers import NaiveBayes as Bayes
from dmc.transformation import scale_features as scaler


trits = ['articleID', 'customerID', 'productGroup']

""" Train on 70%, Test on 30% and save test set """

data = processed_data(load_full=True)
data = data[~data.returnQuantity.isnull()]
train, test = split_data_at_id(data, 1527394)

# allocate Memory
del data

params = {
    # article, customer, productGroup
    'uuu': {'sample': 100000, 'scaler': scaler, 'classifier': TensorNetwork},
    'uuk': {'sample': 100000, 'scaler': scaler, 'classifier': TensorNetwork},
    'uku': {'sample': 500000, 'scaler': None, 'classifier': Forest},
    'ukk': {'sample': 500000, 'scaler': None, 'classifier': Forest},
    'kuk': {'sample': 100000, 'scaler': scaler, 'classifier': TensorNetwork},
    'kkk': {'sample': 500000, 'scaler': None, 'classifier': Forest}
}

for p in params:
    params[p]['ignore_features'] = None

# use bayes for the zero-split
params['uku']['classifier'] = Bayes

ensemble = ECEnsemble(train, test, params, trits)
print('transform for test')
ensemble.transform()
print('classify for test')
ensemble.classify(dump_results=True, dump_name='trestest-ensemble')
