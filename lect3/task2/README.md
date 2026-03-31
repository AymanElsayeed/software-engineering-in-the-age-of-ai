# Task 2
⸻
•	Read (15 minutes): Design an architecture for a “smart support system powered by AI for enterprise customers.”
•	Assignment: Include in your design the following components:

1.	A semantic cache mechanism.
2.	Working with 2 different AI models using the Adapter pattern.
3.	A team of at least 2 agents using a MAS (Multi-Agent System) approach: one for handling issues + one for solutions.
4.	Access of the system to enterprise knowledge using RAG (Retrieval-Augmented Generation).
5.	A HITL (Human-in-the-Loop) team where human customer service representatives validate the system’s actions.

⸻


Desing an architicture of Support System AI based.

Use RAG as follow:

- Symantic caching system
  - Saving cost
   by privide an answer if we have seen this problem before
  - Sustanbility
    if for any reasons we did not get answe back from AI API, we can send the request again to the same API or different one
- Adapter using two AI agents using the pattern Adatper
  - Fallback
    if one agent/API does not response, we can use the second one.
- use MAS(Multi Agent System ) one agent for anslysis the issue and one for suggesting solution
  - Agent A: Analyisis the problem
    - Act like Gard
    - Reterive the relevant context
  - Agent B: Given the analyised problem, provide possible solutions
- HITL - human in the loop

