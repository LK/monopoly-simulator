import tensorflow as tf
import numpy as np

STATE_DIM = 1000

# Initialize in/out variables
x = tf.placeholder(tf.float32, shape=[None, 3])
y_ = tf.placeholder(tf.float32, shape=[None, 1])


# Create model
def linear(name, in_, in_size, out_size):
    with tf.name_scope(name):
        W = tf.get_variable(
            "W",
            shape=[in_size, out_size],
            initializer=tf.contrib.layers.xavier_initializer(),
        )
        b = tf.get_variable(
            "b", shape=[out_size], initializer=tf.constant_initializer(0.1)
        )
        return tf.matmul(in_, W) + b


def relu(name, in_, in_size, out_size):
    return tf.nn.relu(linear(name, in_, in_size, out_size))


error = tf.reduce_mean(tf.square(y - y_))
train_step = tf.train.AdamOptimizer(1e-2).minimize(error)

sess = tf.Session()
sess.run(tf.initialize_all_variables())
for i in range(20000):
    batch = np.random.rand(10, 3).astype(np.float32)
    sess.run(
        train_step,
        feed_dict={x: batch, y_: np.expand_dims(batch.sum(axis=1), axis=1) * 10 - 54},
    )
    if i % 1000 == 0:
        print(
            sess.run(
                error,
                feed_dict={
                    x: batch,
                    y_: np.expand_dims(batch.sum(axis=1), axis=1) * 10 - 54,
                },
            )
        )
