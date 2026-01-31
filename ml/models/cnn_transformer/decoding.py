import torch
import math
from collections import defaultdict


def ctc_greedy_decode(logits, idx_to_token, blank_idx=0):
    preds = torch.argmax(logits, dim=2)  # [T, B]
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
# CTC Prefix Beam Search (KEY UPGRADE)
# --------------------------------------------------
def ctc_beam_search_decode(
    logits,
    idx_to_token,
    beam_width=5,
    blank_idx=0
):
    """
    logits: (T, B, C) log-probabilities
    Returns best decoded string per batch item
    """

    T, B, C = logits.size()
    results = []

    for b in range(B):
        log_probs = logits[:, b, :]  # (T, C)

        beams = {(): 0.0}  # prefix -> log prob

        for t in range(T):
            new_beams = defaultdict(lambda: -math.inf)

            for prefix, score in beams.items():
                for c in range(C):
                    p = log_probs[t, c].item()
                    if c == blank_idx:
                        new_beams[prefix] = max(
                            new_beams[prefix],
                            score + p
                        )
                    else:
                        new_prefix = prefix + (c,)
                        new_beams[new_prefix] = max(
                            new_beams[new_prefix],
                            score + p
                        )

            # keep top beams
            beams = dict(
                sorted(new_beams.items(), key=lambda x: x[1], reverse=True)
                [:beam_width]
            )

        # choose best beam
        best_prefix = max(beams.items(), key=lambda x: x[1])[0]

        # collapse repeats + remove blanks
        decoded = []
        prev = None
        for token in best_prefix:
            if token != blank_idx and token != prev and token in idx_to_token:
                decoded.append(idx_to_token[token])
            prev = token

        results.append("".join(decoded))

    return results
