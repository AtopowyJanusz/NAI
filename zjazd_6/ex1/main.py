"""
Autorzy: Maciej Dzieciuch, Patrycja Bednarka
Źródło: https://www.tensorflow.org/tutorials/customization/custom_training_walkthrough
http://archive.ics.uci.edu/ml/datasets/MAGIC+Gamma+Telescope

Zadanie: Wykorzystanie sieci neuronowych do określenia symulacji rejestracji
wysokoenergetycznych cząstek gamma w atmosferycznym teleskopie Czerenkowa
"""
import matplotlib.pyplot as plt
import tensorflow as tf

"""
Przypisanie pliku .csv z danymi do uczenia
"""
train_file_path = 'magic-gamma-telescope.csv'

"""
Określenie nazw kolumn dla danych wejściowych
"""
column_names = ['length', 'width', 'size', 'conc', 'conc1', 'asym',
                'M3Long', 'M3Trans', 'alpha', 'dist', 'class']

"""
Feature names określa wszystkie kolumny oprócz ostatniej
Label określa wartości z ostatniej kolumny
"""
feature_names = column_names[:-1]
label_name = column_names[-1]
class_names = ['Signal', 'Background']

batch_size = 32

"""
Funkcja do sparsowania danych odpowiedniego formatu w naszym przypadku .csv
"""
train_dataset = tf.data.experimental.make_csv_dataset(
    train_file_path,
    batch_size,
    column_names=column_names,
    label_name=label_name,
    num_epochs=1)

"""
Funkcja pobierająca wartości z listy tensorów i tworzy połączony tensor w określonym wymiarze
"""


def pack_features_vector(features, labels):
    features = tf.stack(list(features.values()), axis=1)
    return features, labels


"""
Spakowanie wszystkich danych do zbioru danych treningowych
"""
train_dataset = train_dataset.map(pack_features_vector)
features, labels = next(iter(train_dataset))

"""
Pobieranie listy instancji warstw
"""
model = tf.keras.Sequential([
    tf.keras.layers.Dense(200, activation=tf.nn.relu, input_shape=(10,)),  # input shape required
    tf.keras.layers.Dense(200, activation=tf.nn.relu),
    tf.keras.layers.Dense(2)
])

predictions = model(features)
tf.nn.softmax(predictions[:5])
print("Prediction: {}".format(tf.argmax(predictions, axis=1)))
print("    Labels: {}".format(labels))

"""
Obliczanie straty za pomocą funkcji SparseCategoricalCrossentropy, która
pobiera przewidywania prawdopodobieństwa klasy modelu oraz etykietę i zwraca
średnią stratę dla wszystkich przykładów
"""
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)


def loss(model, x, y, training):
    # training=training is needed only if there are layers with different
    # behavior during training versus inference (e.g. Dropout).
    y_ = model(x, training=training)

    return loss_object(y_true=y, y_pred=y_)


l = loss(model, features, labels, training=False)
print("Loss test: {}".format(l))

"""
Obliczanie gradientów do optymalizacji modelu
"""


def grad(model, inputs, targets):
    with tf.GradientTape() as tape:
        loss_value = loss(model, inputs, targets, training=True)
    return loss_value, tape.gradient(loss_value, model.trainable_variables)


"""
Użycie algorytmu optymalizującego
"""
optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

loss_value, grads = grad(model, features, labels)

print("Step: {}, Initial Loss: {}".format(optimizer.iterations.numpy(),
                                          loss_value.numpy()))

optimizer.apply_gradients(zip(grads, model.trainable_variables))

print("Step: {}, Loss: {}".format(optimizer.iterations.numpy(),
                                  loss(model, features, labels, training=True).numpy()))

train_loss_results = []
train_accuracy_results = []

num_epochs = 50

"""
Pętla treningowa która przekazuje przykłady z zestawu danych do modelu
"""
for epoch in range(num_epochs):
    epoch_loss_avg = tf.keras.metrics.Mean()
    epoch_accuracy = tf.keras.metrics.SparseCategoricalAccuracy()

    # Training loop - using batches of 32
    for x, y in train_dataset:
        # Optimize the model
        loss_value, grads = grad(model, x, y)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        # Track progress
        epoch_loss_avg.update_state(loss_value)  # Add current batch loss
        epoch_accuracy.update_state(y, model(x, training=True))

    # End epoch
    train_loss_results.append(epoch_loss_avg.result())
    train_accuracy_results.append(epoch_accuracy.result())

    if epoch % 50 == 0:
        print("Epoch {:03d}: Loss: {:.3f}, Accuracy: {:.3%}".format(epoch,
                                                                    epoch_loss_avg.result(),
                                                                    epoch_accuracy.result()))
fig, axes = plt.subplots(2, sharex=True, figsize=(12, 8))
fig.suptitle('Training Metrics')

axes[0].set_ylabel("Loss", fontsize=14)
axes[0].plot(train_loss_results)

axes[1].set_ylabel("Accuracy", fontsize=14)
axes[1].set_xlabel("Epoch", fontsize=14)
axes[1].plot(train_accuracy_results)
plt.show()

test_dataset = tf.data.experimental.make_csv_dataset(
    train_file_path,
    batch_size,
    column_names=column_names,
    label_name=label_name,
    num_epochs=1,
    shuffle=False)

test_dataset = test_dataset.map(pack_features_vector)

test_accuracy = tf.keras.metrics.Accuracy()
i = 0

for (x, y) in test_dataset:
    i = i + 1
    logits = model(x, training=False)
    prediction = tf.argmax(logits, axis=1, output_type=tf.int32)
    test_accuracy(prediction, y)
    if (i <= 10):
        print(prediction)

print("Test set accuracy: {:.3%}".format(test_accuracy.result()))
