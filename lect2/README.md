# Lecture 2 - Few-Shot and Chain-of-Thought (CoT)

This folder documents a small experiment: how different prompting methods and models answer Python learning tasks.

## What You Will Find Here

- A base task prompt.
- Two prompting styles:
  - Few-shot
  - Chain-of-Thought (CoT)
- Responses from two models:
  - Claude
  - GPT
- Comparison notes between model outputs.

## Folder Map

### Root (`lect2/`)

- `README.md`  
  This guide. Explains the purpose of each file/folder in `lect2`.

- [`doc.md`](./doc.md)  
  Early prompt draft / notes used while preparing the exercise.

- [`task/`](./task/)  
  Baseline task prompt and direct model outputs.
  - [`task/README.md`](./task/README.md): base task prompt text.
  - [`task/task-c.md`](./task/task-c.md): Claude response for the baseline task.
  - [`task/task-g.md`](./task/task-g.md): GPT response for the baseline task.

- [`few-shot/`](./few-shot/)  
  Few-shot version of the same learning goal.
  - [`few-shot/README.md`](./few-shot/README.md): few-shot prompt.
  - [`few-shot/few-shot-c.md`](./few-shot/few-shot-c.md): Claude few-shot response.
  - [`few-shot/few-shot-g.md`](./few-shot/few-shot-g.md): GPT few-shot response.

- [`cot/`](./cot/)  
  Chain-of-Thought version of the same learning goal.
  - [`cot/README.md`](./cot/README.md): CoT prompt/instructions.
  - [`cot/Cot-c.md`](./cot/Cot-c.md): Claude CoT response.
  - [`cot/Cot-g.md`](./cot/Cot-g.md): GPT CoT response.

- [`comparison/`](./comparison/)  
  Side-by-side comparison files.
  - [`comparison/comparison-task.md`](./comparison/comparison-task.md): compare baseline task outputs (`task-c.md` vs `task-g.md`).
  - [`comparison/comparison-fs.md`](./comparison/comparison-fs.md): compare few-shot outputs (`few-shot-c.md` vs `few-shot-g.md`).
  - [`comparison/comparison-cot.md`](./comparison/comparison-cot.md): compare CoT outputs (`Cot-c.md` vs `Cot-g.md`).

- [`api/`](./api/)  
  Optional API-based experiment area.
  - [`api/README.md`](./api/README.md): API contract/requirements.
  - `api/exp.ipynb`: notebook for API experiments.
  - `api/tickets.csv`: sample support tickets input data.

## File Name Conventions

- `-c` = Claude output.
- `-g` = GPT output.
- `few-shot-*` = files for few-shot prompting.
- `Cot-*` = files for Chain-of-Thought prompting.
- `comparison-*` = evaluation/comparison notes.

## Suggested Reading Order

1. Read the base prompt: [`task/README.md`](./task/README.md).
2. Read baseline outputs: `task/task-c.md`, `task/task-g.md`.
3. Read few-shot prompt and outputs in `few-shot/`.
4. Read CoT prompt and outputs in `cot/`.
5. Read the comparison files in `comparison/`.

This order makes it easy to understand the task first, then see how method and model change the quality of results.