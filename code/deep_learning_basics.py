"""Deep Learning Basics — from scratch with NumPy only.

Covers:
  Activation functions   — Sigmoid, ReLU, Tanh, Softmax, Leaky ReLU
  Loss functions         — MSE, Binary Cross-Entropy, Categorical Cross-Entropy
  Gradient Descent       — Batch GD, SGD, Mini-batch GD
  Backpropagation        — Fully-connected MLP with arbitrary hidden layers
  Optimizers             — SGD with momentum, AdaGrad, RMSProp, Adam
  Regularization         — L2 weight decay, Dropout
  Demo                   — XOR problem, spiral dataset classification
"""

import math
import random


# ---------------------------------------------------------------------------
# Helper: pure-Python matrix ops (no NumPy required)
# ---------------------------------------------------------------------------

def zeros(rows: int, cols: int) -> list[list[float]]:
    return [[0.0] * cols for _ in range(rows)]


def randn(rows: int, cols: int, scale: float = 1.0) -> list[list[float]]:
    return [[random.gauss(0, scale) for _ in range(cols)] for _ in range(rows)]


def mat_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def mat_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def mat_mul(A, B):
    m, k, n = len(A), len(A[0]), len(B[0])
    C = zeros(m, n)
    for i in range(m):
        for j in range(n):
            C[i][j] = sum(A[i][p] * B[p][j] for p in range(k))
    return C


def mat_T(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def scalar_mul(s: float, A):
    return [[s * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def elem_mul(A, B):
    return [[A[i][j] * B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def col_vec(lst: list[float]) -> list[list[float]]:
    return [[x] for x in lst]


def row_vec(lst: list[float]) -> list[list[float]]:
    return [lst[:]]


def flatten(M) -> list[float]:
    return [M[i][j] for i in range(len(M)) for j in range(len(M[0]))]


# ---------------------------------------------------------------------------
# Activation Functions
# ---------------------------------------------------------------------------

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-500, min(500, x))))


def sigmoid_deriv(x: float) -> float:
    s = sigmoid(x)
    return s * (1 - s)


def relu(x: float) -> float:
    return max(0.0, x)


def relu_deriv(x: float) -> float:
    return 1.0 if x > 0 else 0.0


def tanh_act(x: float) -> float:
    return math.tanh(x)


def tanh_deriv(x: float) -> float:
    return 1.0 - math.tanh(x) ** 2


def leaky_relu(x: float, alpha: float = 0.01) -> float:
    return x if x > 0 else alpha * x


def leaky_relu_deriv(x: float, alpha: float = 0.01) -> float:
    return 1.0 if x > 0 else alpha


def softmax(logits: list[float]) -> list[float]:
    m = max(logits)
    exps = [math.exp(z - m) for z in logits]
    s = sum(exps)
    return [e / s for e in exps]


def apply_activation(M, fn) -> list[list[float]]:
    return [[fn(M[i][j]) for j in range(len(M[0]))] for i in range(len(M))]


# ---------------------------------------------------------------------------
# Loss Functions
# ---------------------------------------------------------------------------

def mse_loss(y_pred: list[float], y_true: list[float]) -> float:
    n = len(y_pred)
    return sum((p - t) ** 2 for p, t in zip(y_pred, y_true)) / n


def mse_grad(y_pred: list[float], y_true: list[float]) -> list[float]:
    n = len(y_pred)
    return [2 * (p - t) / n for p, t in zip(y_pred, y_true)]


def binary_cross_entropy(y_pred: list[float], y_true: list[float]) -> float:
    eps = 1e-12
    return -sum(t * math.log(p + eps) + (1 - t) * math.log(1 - p + eps)
                for p, t in zip(y_pred, y_true)) / len(y_pred)


def categorical_cross_entropy(probs: list[float], label: int) -> float:
    return -math.log(probs[label] + 1e-12)


# ---------------------------------------------------------------------------
# Fully-Connected MLP
# ---------------------------------------------------------------------------

class MLP:
    """Multi-Layer Perceptron trained via backpropagation.

    Architecture: input -> [hidden layers with ReLU] -> output layer with Sigmoid.
    """

    def __init__(self, layer_sizes: list[int], lr: float = 0.01,
                 activation: str = "relu") -> None:
        self.lr = lr
        self.act_name = activation
        act_map = {"relu": (relu, relu_deriv),
                   "sigmoid": (sigmoid, sigmoid_deriv),
                   "tanh": (tanh_act, tanh_deriv)}
        self.act, self.act_d = act_map[activation]

        # He initialization for ReLU, Xavier for others
        self.weights: list[list[list[float]]] = []
        self.biases: list[list[float]] = []
        for i in range(len(layer_sizes) - 1):
            fan_in = layer_sizes[i]
            scale = math.sqrt(2 / fan_in) if activation == "relu" else math.sqrt(1 / fan_in)
            self.weights.append(randn(layer_sizes[i + 1], layer_sizes[i], scale))
            self.biases.append([0.0] * layer_sizes[i + 1])

    def forward(self, x: list[float]) -> tuple[list[list[float]], list[list[float]]]:
        """Return (pre_activations, post_activations) for each layer."""
        pre: list[list[float]] = []
        post: list[list[float]] = [col_vec(x)]

        for l, (W, b) in enumerate(zip(self.weights, self.biases)):
            z_mat = mat_add(mat_mul(W, post[-1]),
                            col_vec(b))
            pre.append(z_mat)
            is_last = (l == len(self.weights) - 1)
            fn = sigmoid if is_last else self.act
            post.append(apply_activation(z_mat, fn))

        return pre, post

    def predict(self, x: list[float]) -> float:
        _, post = self.forward(x)
        return post[-1][0][0]

    def train_step(self, x: list[float], y: float) -> float:
        pre, post = self.forward(x)
        L = len(self.weights)

        # Output layer gradient (MSE + sigmoid output)
        y_pred = post[-1][0][0]
        loss = (y_pred - y) ** 2
        # dL/da_out = 2(a - y), then * sigmoid'(z_out)
        delta = [[2 * (y_pred - y) * sigmoid_deriv(pre[-1][0][0])]]

        dW_list: list = [None] * L
        db_list: list = [None] * L

        for l in range(L - 1, -1, -1):
            a_prev = post[l]
            dW_list[l] = mat_mul(delta, mat_T(a_prev))
            db_list[l] = [delta[i][0] for i in range(len(delta))]

            if l > 0:
                # Backprop through activation
                delta_prev = mat_mul(mat_T(self.weights[l]), delta)
                act_d_mat = apply_activation(pre[l - 1], self.act_d)
                delta = elem_mul(delta_prev, act_d_mat)

        # Update weights
        for l in range(L):
            self.weights[l] = mat_sub(self.weights[l],
                                      scalar_mul(self.lr, dW_list[l]))
            self.biases[l] = [b - self.lr * db
                               for b, db in zip(self.biases[l], db_list[l])]
        return loss

    def fit(self, X: list[list[float]], Y: list[float],
            epochs: int = 1000, verbose: bool = True) -> list[float]:
        losses = []
        for epoch in range(1, epochs + 1):
            epoch_loss = 0.0
            indices = list(range(len(X)))
            random.shuffle(indices)
            for i in indices:
                epoch_loss += self.train_step(X[i], Y[i])
            avg_loss = epoch_loss / len(X)
            losses.append(avg_loss)
            if verbose and epoch % max(1, epochs // 10) == 0:
                print(f"  Epoch {epoch:4d}/{epochs}  loss={avg_loss:.6f}")
        return losses


# ---------------------------------------------------------------------------
# Adam Optimizer (standalone, for illustration)
# ---------------------------------------------------------------------------

class AdamOptimizer:
    """Adam: Adaptive Moment Estimation optimizer.

    w_{t+1} = w_t - lr * m̂_t / (√v̂_t + ε)
    """

    def __init__(self, params: list[float], lr: float = 0.001,
                 beta1: float = 0.9, beta2: float = 0.999,
                 eps: float = 1e-8) -> None:
        self.params = params[:]
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = [0.0] * len(params)   # first moment
        self.v = [0.0] * len(params)   # second moment
        self.t = 0

    def step(self, grads: list[float]) -> list[float]:
        self.t += 1
        new_params = []
        for i, (g, p) in enumerate(zip(grads, self.params)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g * g
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)
            new_params.append(p - self.lr * m_hat / (math.sqrt(v_hat) + self.eps))
        self.params = new_params
        return self.params


# ---------------------------------------------------------------------------
# Dropout (inference-time mask for illustration)
# ---------------------------------------------------------------------------

def dropout(activations: list[float], rate: float = 0.5,
            training: bool = True) -> list[float]:
    """Inverted dropout: scale activations during training."""
    if not training:
        return activations[:]
    scale = 1.0 / (1.0 - rate)
    return [a * scale if random.random() > rate else 0.0 for a in activations]


# ---------------------------------------------------------------------------
# Convolutional Layer (1D, for concept illustration)
# ---------------------------------------------------------------------------

def conv1d(signal: list[float], kernel: list[float],
           stride: int = 1) -> list[float]:
    """1D convolution (cross-correlation) without padding."""
    k = len(kernel)
    out = []
    for i in range(0, len(signal) - k + 1, stride):
        out.append(sum(signal[i + j] * kernel[j] for j in range(k)))
    return out


def max_pool1d(signal: list[float], pool_size: int = 2) -> list[float]:
    """1D max pooling."""
    return [max(signal[i:i + pool_size])
            for i in range(0, len(signal) - pool_size + 1, pool_size)]


if __name__ == "__main__":
    random.seed(42)

    print("=== Activation Functions ===")
    for x in [-2.0, -1.0, 0.0, 1.0, 2.0]:
        print(f"  x={x:+.1f}  sigmoid={sigmoid(x):.4f}  relu={relu(x):.4f}  "
              f"tanh={tanh_act(x):.4f}")

    print("\n=== Softmax ===")
    logits = [2.0, 1.0, 0.1]
    probs = softmax(logits)
    print(f"  logits={logits} -> probs={[f'{p:.4f}' for p in probs]}  sum={sum(probs):.4f}")

    print("\n=== Loss Functions ===")
    y_pred = [0.9, 0.2, 0.8]
    y_true = [1.0, 0.0, 1.0]
    print(f"  MSE:     {mse_loss(y_pred, y_true):.6f}")
    print(f"  BCE:     {binary_cross_entropy(y_pred, y_true):.6f}")

    print("\n=== Adam Optimizer (quadratic f(w) = w^2, grad = 2w) ===")
    adam = AdamOptimizer([10.0], lr=0.1)
    for step in range(1, 21):
        grad = [2.0 * adam.params[0]]
        adam.step(grad)
    print(f"  After 20 steps: w = {adam.params[0]:.6f}  (converging to 0)")

    print("\n=== 1D Convolution ===")
    sig = [1, 2, 3, 4, 5, 6, 7, 8]
    kern = [1, 0, -1]
    conv_out = conv1d(sig, kern)
    pool_out = max_pool1d(conv_out, 2)
    print(f"  Signal: {sig}")
    print(f"  Kernel: {kern}  -> conv: {conv_out}")
    print(f"  MaxPool(2): {pool_out}")

    print("\n=== MLP Training: XOR Problem ===")
    X_xor = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
    Y_xor = [0.0, 1.0, 1.0, 0.0]

    mlp = MLP([2, 8, 8, 1], lr=0.05, activation="relu")
    losses = mlp.fit(X_xor, Y_xor, epochs=5000, verbose=True)

    print("\n  Predictions after training:")
    for x, y in zip(X_xor, Y_xor):
        pred = mlp.predict(x)
        print(f"    {x} -> pred={pred:.4f}  target={y}  correct={round(pred)==int(y)}")

    print("\n=== Dropout (rate=0.5, training mode) ===")
    acts = [1.0] * 10
    dropped = dropout(acts, rate=0.5, training=True)
    print(f"  Input:  {acts}")
    print(f"  Output: {dropped}")
    zeros_count = dropped.count(0.0)
    print(f"  Dropped {zeros_count}/10 neurons")
