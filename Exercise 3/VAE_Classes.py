import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


class Sampling(layers.Layer):
    def call(self, inputs):
        """ Sample z from Gaussian distribution using z_mean and z_log_var.

        Args:
          inputs: z_mean (float), z_log_var (float) 

        Returns: Sample from Gaussian distribution
          
        """
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dimension = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dimension))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

    
class VAE(keras.Model):
    def __init__(self, encoder, decoder,is_image=True, **kwargs):
        """ Initialize variational autoencoder.

        Args:
          encoder: keras.Model
          decoder: keras.Model
          is_image: bool
          
        """
        super(VAE, self).__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        self.is_image = is_image
        self.total_loss_tracker = keras.metrics.Mean(name="total_loss")
        self.reconstruction_loss_tracker = keras.metrics.Mean(
            name="reconstruction_loss"
        )
        self.kl_loss_tracker = keras.metrics.Mean(name="kl_loss")
    
    @property
    def metrics(self):
        """ Define network metrics.
        
        Returns:
            kl_loss: float
            reconstruction_loss: float
            total_loss: float
          
        """
        return [
            self.total_loss_tracker,
            self.reconstruction_loss_tracker,
            self.kl_loss_tracker,
        ]

    def train_step(self, data):
        """ Training step.
        
        Args:
            data: numpy.ndarray
           
        Returns:
            kl_loss: float
            reconstruction_loss: float
            total_loss: float
          
        """
        with tf.GradientTape() as tape:
            z_mean, z_log_var, z = self.encoder(data)
            reconstruction = self.decoder(z)
            if self.is_image:
                reconstruction_loss = tf.reduce_mean(
                    tf.reduce_sum(
                        keras.losses.binary_crossentropy(data, reconstruction), axis=(1, 2)
                    )
                )
            else:
                reconstruction_loss = tf.reduce_mean(tf.reduce_sum(tf.square(data - reconstruction)))
            kl_loss = -0.5 * (1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
            kl_loss = tf.reduce_mean(tf.reduce_sum(kl_loss, axis=1))
            total_loss = reconstruction_loss + kl_loss
        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))
        self.total_loss_tracker.update_state(total_loss)
        self.reconstruction_loss_tracker.update_state(reconstruction_loss)
        self.kl_loss_tracker.update_state(kl_loss)
        return {
            "loss": self.total_loss_tracker.result(),
            "reconstruction_loss": self.reconstruction_loss_tracker.result(),
            "kl_loss": self.kl_loss_tracker.result(),
        }