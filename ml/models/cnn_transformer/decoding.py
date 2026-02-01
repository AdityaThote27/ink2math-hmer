import torch
import math
from collections import defaultdict


# --------------------------------------------------
# Greedy CTC Decode (baseline)
# --------------------------------------------------
def ctc_greedy_decode(logits, idx_to_token, blank_idx=0):
    """
    logits: (T, B, C) log-probabilities
    """
    preds = torch.argmax(logits, dim=2)  # (T, B)
    decoded_sequences = []

    for b in range(preds.size(1)):
        prev = None
        out = []
        for t in range(preds.size(0)):
            token = preds[t, b].item()
            if token != blank_idx and token != prev and token in idx_to_token:
                out.append(idx_to_token[token])
            prev = token
        decoded_sequences.append("".join(out))

    return decoded_sequences


# --------------------------------------------------
# CTC Beam Search Decode (LENGTH-AWARE)
# --------------------------------------------------
def ctc_beam_search_decode(
    logits,
    idx_to_token,
    beam_width=5,
    blank_idx=0,
    length_bonus=0.15
):
    """
    logits: (T, B, C) log-probabilities
    Returns best decoded string per batch item
    """

    T, B, C = logits.size()
    results = []

    for b in range(B):
        log_probs = logits[:, b, :]  # (T, C)

        # prefix (tuple of token ids) -> score
        beams = {(): 0.0}

        for t in range(T):
            new_beams = defaultdict(lambda: -math.inf)

            for prefix, score in beams.items():
                for c in range(C):
                    p = log_probs[t, c].item()

                    # Blank token: no length bonus
                    if c == blank_idx:
                        new_beams[prefix] = max(
                            new_beams[prefix],
                            score + p
                        )
                    else:
                        # Non-blank token: reward sequence extension
                        new_prefix = prefix + (c,)
                        new_beams[new_prefix] = max(
                            new_beams[new_prefix],
                            score + p + length_bonus
                        )

            # Keep top-K beams
            beams = dict(
                sorted(
                    new_beams.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:beam_width]
            )

        # Best scoring prefix
        # Prefer non-empty sequences if scores are close
        best_prefix = max(
            beams.items(),
            key=lambda x: (len(x[0]) > 0, x[1])
        )[0]


        # Collapse repeats and remove blanks
        decoded = []
        prev = None
        for token in best_prefix:
            if token != blank_idx and token != prev and token in idx_to_token:
                decoded.append(idx_to_token[token])
            prev = token

        results.append("".join(decoded))

    return results
