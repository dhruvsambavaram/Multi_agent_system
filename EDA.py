"""
EDA.py

Exploratory Data Analysis for the Iris dataset using NumPy and Matplotlib.
"""

import sys
import numpy as np
import matplotlib

# Use the Agg backend so the script runs in non-interactive / headless environments
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_iris():
    """Load the Iris dataset. Attempts sklearn first, falls back to a
    deterministic simulated dataset if sklearn is unavailable."""
    try:
        from sklearn.datasets import load_iris
        data = load_iris(as_frame=True)
        X = data["data"].to_numpy()
        y = data["target"].to_numpy()
        feature_names = list(data["data"].columns)
        target_names = list(data["target_names"])
        print(f"Iris dataset loaded via sklearn: {X.shape[0]} samples, "
              f"{X.shape[1]} features")
    except NotImplementedError:
        # as_frame=True may fail depending on sklearn version; try without
        from sklearn.datasets import load_iris
        data = load_iris()
        X = data["data"]
        y = data["target"]
        feature_names = list(data["feature_names"])
        target_names = list(data["target_names"])
        print(f"Iris dataset loaded via sklearn: {X.shape[0]} samples, "
              f"{X.shape[1]} features")
    except ImportError:
        # Fallback: deterministic simulated Iris-like data
        print("sklearn not available – using simulated Iris-like data")
        rng = np.random.default_rng(42)
        cluster_means = np.array([
            [5.84, 3.05, 4.39, 1.43],   # setosa
            [5.94, 2.77, 4.26, 1.326],  # versicolor
            [6.59, 2.97, 5.55, 2.026],  # virginica
        ])
        cluster_covs = np.stack([
            np.diag([0.19, 0.09, 0.19, 0.124]),
            np.diag([0.26, 0.10, 0.22, 0.108]),
            np.diag([0.40, 0.11, 0.42, 0.119]),
        ])
        X = np.vstack([
            rng.multivariate_normal(cluster_means[i], cluster_covs[i], size=50)
            for i in range(3)
        ])
        X = np.clip(X, 0.1, None)
        y = np.repeat([0, 1, 2], 50)
        feature_names = ["sepal length", "sepal width", "petal length", "petal width"]
        target_names = ["setosa", "versicolor", "virginica"]
    return X, y, feature_names, target_names


def main():
    X, y, feature_names, target_names = load_iris()

    # --- NumPy statistical measures ---
    feature_means = np.mean(X, axis=0)
    print("\nPer-feature means:")
    for name, mean_val in zip(feature_names, feature_means):
        print(f"  {name:>15s}: {mean_val:.4f}")

    per_class_means = np.array([np.mean(X[y == c], axis=0) for c in range(len(target_names))])
    print("\nPer-class means:")
    for cls, mean_row in zip(target_names, per_class_means):
        print(f"  {cls:>10s}: {np.round(mean_row, 4).tolist()}")

    # --- Matplotlib distribution plot ---
    fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=False)
    axes = axes.ravel()

    for idx, feat_idx in enumerate(range(X.shape[1])):
        ax = axes[idx]
        for c in range(len(target_names)):
            ax.hist(X[y == c, feat_idx], bins=15, alpha=0.5, label=target_names[c])
        ax.set_xlabel(feature_names[feat_idx])
        ax.set_ylabel("Frequency")
        ax.set_title(f"Distribution: {feature_names[feat_idx]}")
        ax.legend()

    fig.suptitle("Iris Dataset – Feature Distributions", fontsize=14)
    fig.tight_layout()
    plt.savefig("iris_eda.png", dpi=150, bbox_inches="tight")
    print("\nPlot saved to 'iris_eda.png'")


if __name__ == "__main__":
    main()
