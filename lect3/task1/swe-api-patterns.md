# Mapping AI Patterns to SWE Principles


| AI Pattern                           | Matching SWE Principle                | How this pattern supports the principle                                               |
| ------------------------------------ | ------------------------------------- | ------------------------------------------------------------------------------------- |
| Direct Prompting                     | Maintainability & Readability         | Gives a clear baseline design that is easy to understand before adding complexity.    |
| Evals                                | Testability & Automation              | Introduces systematic, repeatable quality checks for non-deterministic behavior.      |
| Embeddings                           | Modularity & Separation of Concerns   | Isolates semantic representation/retrieval logic from generation logic.               |
| Retrieval Augmented Generation (RAG) | Open/Closed (SOLID - O)               | Extends model behavior with external knowledge without changing core model internals. |
| Hybrid Retriever                     | Scalability                           | Keeps retrieval robust as data volume and query diversity increase.                   |
| Query Rewriting                      | Single Responsibility Principle (SRP) | Assigns one focused component to improve query quality before retrieval.              |
| Reranker                             | Loose Coupling & High Cohesion        | Adds a dedicated relevance-ranking step that stays focused and decoupled.             |
| Guardrails                           | Reliability & Fault Tolerance         | Adds protective checks on input/output to reduce unsafe or invalid system behavior.   |
| Fine Tuning                          | Maintainability & Readability         | Used after simpler options, it targets domain behavior explicitly and predictably.    |


