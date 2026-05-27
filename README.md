# Chatbot-Based Medical History Taking Using Qwen3

This repository contains the chatbot implementation code used for the study:

**Evaluation of Prompt Design and Internal Reasoning in Chatbot-Based Medical History Taking**

The chatbot was developed to conduct simulated preconsultation medical history-taking interviews using Qwen3-14B through an Ollama backend. The system was used to generate chatbot–simulated patient transcripts for evaluating how prompt design and internal reasoning configuration affect checklist-based information coverage.

## Study Overview

The study evaluated four LLM chatbot configurations in a 2×2 factorial design:

| Configuration | Prompt Type | Reasoning Mode |
|---|---|---|
| DT | Detailed prompt | Thinking mode |
| DN | Detailed prompt | Non-thinking mode |
| MT | Minimal prompt | Thinking mode |
| MN | Minimal prompt | Non-thinking mode |

These four configurations were compared with a rule-based choice-based chatbot baseline.

The chatbot was evaluated using standardized primary care cases and simulated patient interactions. Transcript coverage was assessed using case-specific checklists inspired by Objective Structured Clinical Examination (OSCE) frameworks.

## Repository Contents

This repository includes the chatbot implementation code used for the study.

Raw chatbot–simulated patient transcripts, case scripts, and detailed checklist items are not included because they may contain participant-generated wording and case-specific details derived from copyrighted source materials.

The prompts used in the study are provided in the manuscript supplementary materials.

## Environment

The system was implemented using:

- Python 3.13.3
- Streamlit 1.44.1
- LangChain Core 0.3.51
- LangChain Ollama 0.3.1
- Ollama backend
- Qwen3-14B model

## Installation

Create and activate a conda environment:

```bash
conda create -n chatbot_qwen_paper python=3.13.3
conda activate chatbot_qwen_paper
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Ollama Setup
Install Ollama separately, then pull the Qwen3-14B model:
```bash
ollama pull qwen3:14b
```

## Running the Chatbot
Start the Streamlit application:
```bash
streamlit run app.py
```

##  Notes on Reproducibility
The repository is intended to document the chatbot implementation used for transcript generation. The study-specific case materials, full transcripts, and checklist items are not publicly shared due to privacy and copyright considerations.

## Data Availability
The chatbot implementation code is available in this repository. The case-level coverage dataset used for statistical analysis may be made available from the corresponding author upon reasonable request. Full chatbot–simulated patient transcripts, case scripts, and detailed checklist items are not publicly shared because they may contain participant-generated wording and case-specific details derived from copyrighted source materials.

## Citation
If you use or refer to this repository, please cite the associated manuscript once available.