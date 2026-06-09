"""
Optimised params_by_cluster — paste this into the basket notebook cell.

Parameters were found via grid search over:
  min_support  : [0.01, 0.02, 0.03, 0.05, 0.08, 0.10, 0.15, 0.20, 0.25, 0.30]
  min_threshold: [1.0, 1.1, 1.2, 1.5]   (lift threshold)

Scoring: avg_lift*3 + avg_confidence*2 + rule-count bonus (target 10-30 rules)

NOTE: Key renamed "Average customers" -> "Average customer"
      to match the actual label in ci_clustered.csv.
"""

params_by_cluster = {
    "Average customer": {
        "min_support": 0.05,
        "min_threshold": 1.0,
        "min_confidence": 0.10
    },
    "Bargain hunters": {
        "min_support": 0.03,
        "min_threshold": 1.0,
        "min_confidence": 0.10
    },
    "Big families (big spenders)": {
        "min_support": 0.01,
        "min_threshold": 1.5,
        "min_confidence": 0.10
    },
    "Clean and healthy": {
        "min_support": 0.01,
        "min_threshold": 1.0,
        "min_confidence": 0.10
    },
    "Gamers": {
        "min_support": 0.08,
        "min_threshold": 1.5,
        "min_confidence": 0.10
    },
    "Karens": {
        "min_support": 0.15,
        "min_threshold": 1.5,
        "min_confidence": 0.10
    },
    "Loyal big spenders": {
        "min_support": 0.02,
        "min_threshold": 1.0,
        "min_confidence": 0.10
    },
    "Tech enthusiasts": {
        "min_support": 0.03,
        "min_threshold": 1.5,
        "min_confidence": 0.10
    },
    "Vegans": {
        "min_support": 0.05,
        "min_threshold": 1.0,
        "min_confidence": 0.10
    },
}
