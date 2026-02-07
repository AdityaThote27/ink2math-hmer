# Ink2Math – Handwritten Mathematical Expression Recognition (HMER)

Ink2Math is an end-to-end **Handwritten Mathematical Expression Recognition (HMER)** system that converts handwritten mathematical expressions from images into evaluated numerical results.

The project implements a **segmentation-first pipeline**, combining classical computer vision techniques with deep learning and symbolic computation. Given a handwritten image, the system preprocesses the input, segments individual symbols, performs hybrid symbol recognition (CNN-based digit recognition + rule-based operator detection), constructs a valid mathematical expression, and evaluates it using SymPy.

### Key Features
- End-to-end pipeline: image → expression → result
- OpenCV-based preprocessing and symbol segmentation
- CNN-based digit recognition (reusing a trained MNIST-style model)
- Rule-based detection of arithmetic operators (`+`, `-`, `*`)
- Syntax post-processing to ensure valid mathematical expressions
- Symbolic evaluation using SymPy
- Modular, research-oriented architecture designed for extensibility

### Current Status
This repository contains **HMER v1**, a stable and working prototype focused on pipeline correctness rather than recognition accuracy. Operator detection and expression validation are handled heuristically, while accuracy improvements and advanced models (e.g., Transformers, expression trees) are planned as future enhancements.

### Future Work
- Operator confidence scoring and improved heuristics
- Support for additional operators (division, parentheses)
- Expression tree (AST)–based parsing
- Unified multi-class symbol recognition
- Dataset expansion beyond MNIST
- Research paper and performance evaluation

This project is intended for research, experimentation, and learning in the areas of computer vision, deep learning, and symbolic mathematics.
