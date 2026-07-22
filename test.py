import keras

model = keras.models.load_model("app/trained_model/best_fashion_model.keras")

print("Model loaded successfully!")
model.summary()