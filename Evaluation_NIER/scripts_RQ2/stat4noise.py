## ChatGPT suggestion.
# The Jensen–Shannon divergence computation used in our evaluation was 
# generated with an AI-based code generation tool (ChatGPT 5.2, 11 Feb 2025). 
# The implementation was manually reviewed, tested, and validated by the authors 
# prior to use in the experimental pipeline.
import math
from typing import Dict, Iterable, List, Sequence, Tuple, Union, Optional

Counts = Union[Dict[str, int], Sequence[int]]

def _to_prob_vector(
    counts: Counts,
    outcomes: Optional[Sequence[str]] = None
) -> Tuple[List[float], List[str]]:
    """
    Convert counts to a probability vector over a fixed outcome ordering.
    - If counts is a dict, outcomes must be provided OR inferred as sorted keys.
    - If counts is a list/tuple, outcomes (if given) is only for labeling.
    Returns (probabilities, outcome_list).
    """

    if isinstance(counts, dict):
        if outcomes is None:
            outcomes = sorted(counts.keys())
        vec = [int(counts.get(o, 0)) for o in outcomes]
        labels = list(outcomes)
    else:
        vec = [int(x) for x in counts]
        labels = list(outcomes) if outcomes is not None else [str(i) for i in range(len(vec))]

    total = sum(vec)
    if total <= 0:
        raise ValueError("Total counts must be > 0.")
    probs = [v / total for v in vec]
    return probs, labels

def js_divergence(
    counts_p: Counts,
    counts_q: Counts,
    outcomes: Optional[Sequence[str]] = None,
    base: float = 2.0
) -> float:
    """
    Jensen–Shannon divergence between two discrete distributions given as counts.
    - Symmetric, bounded in [0, log_base(2)] when base is the log base.
      For base=2, JS in [0, 1].
    - Handles zeros naturally (0 * log(0/.) treated as 0).
    """

    P, labels_p = _to_prob_vector(counts_p, outcomes=outcomes)
    print(P)
    Q, labels_q = _to_prob_vector(counts_q, outcomes=outcomes if outcomes is not None else labels_p)
    print(Q)

    if len(P) != len(Q):
        raise ValueError("Distributions must have the same number of outcomes.")

    M = [(p + q) / 2.0 for p, q in zip(P, Q)]

    def kl(a: List[float], b: List[float]) -> float:
        s = 0.0
        for ai, bi in zip(a, b):
            if ai == 0.0:
                continue
            # bi should never be 0 when ai>0 because bi is M or another prob vector.
            s += ai * math.log(ai / bi, base)
        return s

    return 0.5 * kl(P, M) + 0.5 * kl(Q, M)

def js_similarity(
    counts_p: Counts,
    counts_q: Counts,
    outcomes: Optional[Sequence[str]] = None,
    base: float = 2.0
) -> float:
    """
    Convert JS divergence to a similarity in [0, 1] (for base=2).
    Similarity = 1 - JS.
    """
    js = js_divergence(counts_p, counts_q, outcomes=outcomes, base=base)
    # For base=2, JS is in [0, 1]. For other bases, max is log_base(2).
    js_max = math.log(2.0, base)
    return 1.0 - (js / js_max)

# ---- Example using your 2-qubit outcomes ----
outcomes = ['00', '01', '10', '11']

A1 = [4940, 2498, 1, 2561]
A2 = [4887, 2634, 0, 2479]

B1 = [10, 0, 0, 0]
B2 = [0, 1, 0, 9]

C1 = [80, 1, 1, 18]
C2 = [80, 20, 0, 0]

print("..")
print("JS(A1,A2) =", js_divergence(A1, A2, outcomes=outcomes, base=2))
print("Sim(A1,A2) =", js_similarity(A1, A2, outcomes=outcomes, base=2))
print(" ")
print("JS(B1,B2) =", js_divergence(B1, B2, outcomes=outcomes, base=2))
print("Sim(B1,B2) =", js_similarity(B1, B2, outcomes=outcomes, base=2))
print(" ")
print("JS(C1,C2) =", js_divergence(C1, C2, outcomes=outcomes, base=2))
print("Sim(C1,C2) =", js_similarity(C1, C2, outcomes=outcomes, base=2))
