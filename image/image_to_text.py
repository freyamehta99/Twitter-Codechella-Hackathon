import tensorflow as tf


import collections
import random
import re
import numpy as np
import os
import time
import json
from glob import glob
from PIL import Image
import pickle

from tqdm import tqdm

saved_tokenizer_path = "./saved_models/tokenizer.json"
saved_model_path = "./saved_models/checkpoints"


class BahdanauAttention(tf.keras.Model):
    def __init__(self, units):
        super(BahdanauAttention, self).__init__()
        self.W1 = tf.keras.layers.Dense(units)
        self.W2 = tf.keras.layers.Dense(units)
        self.V = tf.keras.layers.Dense(1)

    def call(self, features, hidden):
        # features(CNN_encoder output) shape == (batch_size, 64, embedding_dim)

        # hidden shape == (batch_size, hidden_size)
        # hidden_with_time_axis shape == (batch_size, 1, hidden_size)
        hidden_with_time_axis = tf.expand_dims(hidden, 1)

        # attention_hidden_layer shape == (batch_size, 64, units)
        attention_hidden_layer = tf.nn.tanh(
            self.W1(features) + self.W2(hidden_with_time_axis)
        )

        # score shape == (batch_size, 64, 1)
        # This gives you an unnormalized score for each image feature.
        score = self.V(attention_hidden_layer)

        # attention_weights shape == (batch_size, 64, 1)
        attention_weights = tf.nn.softmax(score, axis=1)

        # context_vector shape after sum == (batch_size, hidden_size)
        context_vector = attention_weights * features
        context_vector = tf.reduce_sum(context_vector, axis=1)

        return context_vector, attention_weights


class CNN_Encoder(tf.keras.Model):
    # Since you have already extracted the features and dumped it using pickle
    # This encoder passes those features through a Fully connected layer
    def __init__(self, embedding_dim):
        super(CNN_Encoder, self).__init__()
        # shape after fc == (batch_size, 64, embedding_dim)
        self.fc = tf.keras.layers.Dense(embedding_dim)

    def call(self, x):
        x = self.fc(x)
        x = tf.nn.relu(x)
        return x


class RNN_Decoder(tf.keras.Model):
    def __init__(self, embedding_dim, units, vocab_size):
        super(RNN_Decoder, self).__init__()
        self.units = units

        self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
        self.gru = tf.keras.layers.GRU(
            self.units,
            return_sequences=True,
            return_state=True,
            recurrent_initializer="glorot_uniform",
        )
        self.fc1 = tf.keras.layers.Dense(self.units)
        self.fc2 = tf.keras.layers.Dense(vocab_size)

        self.attention = BahdanauAttention(self.units)

    def call(self, x, features, hidden):
        # defining attention as a separate model
        context_vector, attention_weights = self.attention(features, hidden)

        # x shape after passing through embedding == (batch_size, 1, embedding_dim)
        x = self.embedding(x)

        # x shape after concatenation == (batch_size, 1, embedding_dim + hidden_size)
        x = tf.concat(values=[tf.expand_dims(context_vector, 1), x], axis=-1)

        # passing the concatenated vector to the GRU
        output, state = self.gru(x)

        # shape == (batch_size, max_length, hidden_size)
        x = self.fc1(output)

        # x shape == (batch_size * max_length, hidden_size)
        x = tf.reshape(x, (-1, x.shape[2]))

        # output shape == (batch_size * max_length, vocab)
        x = self.fc2(x)

        return x, state, attention_weights

    def reset_state(self, batch_size):
        return tf.zeros((batch_size, self.units))


class Img2txt:
    def __init__(self, max_length=55, embedding_dim=256, units=512, vocab_size=5001):
        
        self.max_length = max_length

        self.encoder = CNN_Encoder(embedding_dim)
        self.decoder = RNN_Decoder(embedding_dim, units, vocab_size)
        self.optimizer = tf.keras.optimizers.Adam()
        self._restore_saved_model(saved_model_path)

        self.image_features_extract_model = self._init_feature_extractor()

        with open(saved_tokenizer_path, "r") as tokenizer_json_file:
            tokenizer_json = tokenizer_json_file.read()
        self.tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_json)

    def _restore_saved_model(self, saved_model_path):
        ckpt = tf.train.Checkpoint(
            encoder=self.encoder, decoder=self.decoder, optimizer=self.optimizer
        )
        ckpt_manager = tf.train.CheckpointManager(ckpt, saved_model_path, max_to_keep=5)
        ckpt.restore(ckpt_manager.latest_checkpoint)

    def _init_feature_extractor(self):
        image_model = tf.keras.applications.InceptionV3(
            include_top=False, weights="imagenet"
        )
        new_input = image_model.input
        hidden_layer = image_model.layers[-1].output
        return tf.keras.Model(new_input, hidden_layer)

    def _load_image(self, image_path):
        img = tf.io.read_file(image_path)
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, (299, 299))
        img = tf.keras.applications.inception_v3.preprocess_input(img)
        return img, image_path

    def predict(self, image_url):
        image_name = image_url.split("/")[-1]
        image = tf.keras.utils.get_file("image" + image_name, origin=image_url)

        hidden = self.decoder.reset_state(batch_size=1)

        temp_input = tf.expand_dims(self._load_image(image)[0], 0)
        img_tensor_val = self.image_features_extract_model(temp_input)
        img_tensor_val = tf.reshape(
            img_tensor_val, (img_tensor_val.shape[0], -1, img_tensor_val.shape[3])
        )

        features = self.encoder(img_tensor_val)

        dec_input = tf.expand_dims([self.tokenizer.word_index["<start>"]], 0)
        result = []

        for _ in range(self.max_length):
            predictions, hidden, _ = self.decoder(dec_input, features, hidden)
            predicted_id = tf.random.categorical(predictions, 1)[0][0].numpy()
            result.append(self.tokenizer.index_word[predicted_id])

            if self.tokenizer.index_word[predicted_id] == "<end>":
                return " ".join(result[:-1]).replace(" <unk>", "")

            dec_input = tf.expand_dims([predicted_id], 0)

        return " ".join(result[:-1])


i2t = Img2txt()

def predict(url):
    return i2t.predict(url)

