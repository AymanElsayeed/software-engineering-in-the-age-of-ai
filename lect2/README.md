# Lecture 2 - Few-Shot and Chain-of-Thought (CoT)

This folder contains an experiment that compares how different prompting styles and different models answer Python-learning tasks.

## Goal of `lect2`

1. Define a Python task/prompt.
2. Run it with two prompting methods:
   - Few-shot
   - Chain-of-Thought (CoT)
3. Compare outputs from two models:
   - Claude
   - GPT

## Folder Structure

- `README.md`  
  This file. Explains what each file/folder in `lect2` means.

- `taks.md`  
  Base assignment/prompt template used in this lecture.

- `task-c.md`  
  Claude's answer for the main task.

- `task-g.md`  
  GPT's answer for the main task.

- `few-shot/`  
  Files related to the few-shot method:
  - `few-shot.md` - few-shot prompt draft and response notes.
  - `few-shot-c.md` - Claude few-shot output.
  - `few-shot-g.md` - GPT few-shot output.

- `cot/`  
  Files related to Chain-of-Thought method:
  - `Cot.md` - CoT prompt and instructions flow.
  - `Cot-c.md` - Claude CoT output.
  - `Cot-g.md` - GPT CoT output.

- `comparison/`  
  Side-by-side evaluation files:
  - `comparison-fs.md` - comparison of few-shot outputs (`few-shot-c.md` vs `few-shot-g.md`).
  - `comparison-cot.md` - comparison of CoT outputs (`Cot-c.md` vs `Cot-g.md`).

- `loopOverTuples.py`  
  A Python example file generated from one of the prompting tasks.

## File Name Conventions

- `-c` = Claude output
- `-g` = GPT output
- `few-shot` = Few-shot prompting method
- `cot` / `Cot` = Chain-of-Thought prompting method
- `comparison-*` = comparison/evaluation documents

## How To Read This Folder (Recommended Order)

1. Read `taks.md` to understand the original task.
2. Read model outputs:
   - `task-c.md`, `task-g.md`
   - `few-shot/few-shot-c.md`, `few-shot/few-shot-g.md`
   - `cot/Cot-c.md`, `cot/Cot-g.md`
3. Read comparisons:
   - `comparison/comparison-fs.md`
   - `comparison/comparison-cot.md`