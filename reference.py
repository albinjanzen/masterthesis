import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import matplotlib.pyplot as plt

# Load the dataset from CSV file
df = pd.read_csv('data/Structured/all_data.csv')

df = df.dropna(axis=1, how='all')
df.drop(['Summa gas/Diesel'], axis=1, inplace=True)

df = df.fillna(method='ffill')
df = df.fillna(method='bfill')
for e in df.columns:
    if df[e].nunique() == 1:
        df = df.drop(e, axis=1)
  
first_column = df.pop('SE1')
df.insert(1, 'SE1', first_column)
df.drop(['Date'], axis=1, inplace=True)

df = df.iloc[:,0:2]
print(df.head(10))


n_features = df.shape[1]

# Normalize the features using MinMaxScaler
scaler = MinMaxScaler()
df[df.columns[1:]] = scaler.fit_transform(df[df.columns[1:]])

# Define the sequence length for the LSTM model
sequence_length = 10

# Split the dataset into training and testing sets
train_size = int(len(df) * 0.7)
train_df = df[:train_size]
test_df = df[train_size:]

# Create sequences of input and output for the LSTM model
def create_sequences(df, sequence_length):
    X = []
    y = []
    for i in range(len(df) - sequence_length):
        X.append(df.iloc[i:i+sequence_length, 0])
        y.append(df.iloc[i+sequence_length, 0])
    return np.array(X), np.array(y)


X_train, y_train = create_sequences(train_df, sequence_length)
X_test, y_test = create_sequences(test_df, sequence_length)
print(X_train.shape)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

plt.plot(X_train[0,:,0])
plt.plot(y_train[0])
plt.show()

# Define the model architecture
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(64, input_shape=(sequence_length, 1)),
    tf.keras.layers.Dense(1)
])

# Compile the model with mean squared error loss and Adam optimizer
model.compile(optimizer='adam', loss='mse')

# Train the model on the training set
model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1)

# Evaluate the model on the test set
loss = model.evaluate(X_test, y_test, verbose=0)
print('Test loss:', loss)

# Make predictions on new data
new_data = pd.read_csv('new_data.csv', index_col=0)
new_data[new_data.columns[1:]] = scaler.transform(new_data[new_data.columns[1:]])
X_new = np.array([new_data.iloc[i:i+sequence_length, 1:].values for i in range(len(new_data) - sequence_length)])
y_pred = model.predict(X_new)

# Print the predicted prices
print(y_pred)
