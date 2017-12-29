from pythonds.dcs.a_priori import APriori
from pythonds.dcs.mcb import MCB
# Example of a dcs techniques
from pythonds.dcs.ola import OLA
from pythonds.des.des_p import DESP
from pythonds.des.knora_u import KNORAU
from sklearn.calibration import CalibratedClassifierCV
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import BaggingClassifier
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split

# Example of a des techniques
from pythonds.des.knora_e import KNORAE

if __name__ == "__main__":

    # Generate a classification dataset
    data = load_breast_cancer()
    X = data.data
    y = data.target
    # split the data into training and test data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    # Split the data into training and DSEL for DS techniques
    X_train, X_dsel, y_train, y_dsel = train_test_split(X_train, y_train, test_size=0.5)
    # Considering a pool composed of 10 base classifiers
    # Calibrating Perceptrons to estimate probabilities
    model = CalibratedClassifierCV(Perceptron())
    # Train a pool of 100 classifiers
    pool_classifiers = BaggingClassifier(model, n_estimators=10)
    pool_classifiers.fit(X_train, y_train)

    # Initialize the DS techniques
    knorau = KNORAU(pool_classifiers)
    kne = KNORAE(pool_classifiers)
    desp = DESP(pool_classifiers)
    ola = OLA(pool_classifiers)
    mcb = MCB(pool_classifiers)
    apriori = APriori(pool_classifiers)

    # Fit the des techniques
    knorau.fit(X_dsel, y_dsel)
    kne.fit(X_dsel, y_dsel)
    desp.fit(X_dsel, y_dsel)

    # Fit the dcs techniques
    ola.fit(X_dsel, y_dsel)
    mcb.fit(X_dsel, y_dsel)
    apriori.fit(X_dsel, y_dsel)

    # Calculate classification accuracy of each technique
    print('Classification accuracy Bagging: ', pool_classifiers.score(X_test, y_test))
    print('Classification accuracy KNORA-Union: ', knorau.score(X_test, y_test))
    print('Classification accuracy KNORA-Eliminate: ', kne.score(X_test, y_test))
    print('Classification accuracy DESP: ', desp.score(X_test, y_test))
    print('Classification accuracy OLA: ', ola.score(X_test, y_test))
    print('Classification accuracy A priori: ', apriori.score(X_test, y_test))




