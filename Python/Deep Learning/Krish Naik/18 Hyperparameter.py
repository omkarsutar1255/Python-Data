# todo: Artificial Neural Network

# todo: Part 1 - Data Preprocessing

# todo: Importing the libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
# todo: Perform Hyperparameter Optimization
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
# todo: Keras libraries for model building
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
# todo: Evaluation of model
from sklearn.metrics import confusion_matrix, accuracy_score

# todo: Importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:, 3:13]
y = dataset.iloc[:, 13]

# todo: Create dummy variables
geography = pd.get_dummies(X["Geography"], drop_first=True)
gender = pd.get_dummies(X['Gender'], drop_first=True)

# todo: Concatenate the Data Frames
X = pd.concat([X, geography, gender], axis=1)

# todo: Drop Unnecessary columns
X = X.drop(['Geography', 'Gender'], axis=1)

# todo: Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# todo: Feature Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


def create_model(layers, activation):
    model = Sequential()
    for i, nodes in enumerate(layers):
        if i == 0:
            model.add(Dense(nodes, input_dim=X_train.shape[1]))
            model.add(Activation(activation))
            model.add(Dropout(0.3))
        else:
            model.add(Dense(nodes))
            model.add(Activation(activation))
            model.add(Dropout(0.3))

    model.add(Dense(units=1, kernel_initializer='glorot_uniform',
                    activation='sigmoid'))  # Note: no activation beyond this point

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


model = KerasClassifier(build_fn=create_model, verbose=0)

layers = [(20,), (40, 20), (45, 30, 15)]
activations = ['sigmoid', 'relu']
param_grid = dict(layers=layers, activation=activations, batch_size=[128, 256], epochs=[30])
grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=5)

grid_result = grid.fit(X_train, y_train)

# todo: Model Best Result
print(grid_result.best_score_, grid_result.best_params_)

# todo: Part 3 - Making the predictions and evaluating the model

# todo: 1)Predicting the Test set results
y_pred = grid.predict(X_test)
y_pred = (y_pred > 0.5)

# todo: 2)Making the Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

# todo: 2)Calculate the Accuracy
score = accuracy_score(y_pred, y_test)
print(score)