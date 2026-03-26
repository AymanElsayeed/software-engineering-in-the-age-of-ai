# Mapping AI Patterns to SWE Principles

| AI Pattern | Matching SWE Principle | How this pattern supports the principle |
|---|---|---|
| Direct Prompting Strategy | Maintainability & Readability | Starts with a simple baseline that is easy to understand, debug, and improve later. |
| The Role of Evaluations (Evals) | Testability & Automation | Adds repeatable checks for non-deterministic outputs, similar to automated tests. |
| Scoring and Judging Metrics | Reliability & Fault Tolerance | Defines quality thresholds so bad outputs are detected before they affect users. |
| Embeddings as Data Representation | Modularity & Separation of Concerns | Separates semantic search/data representation from text generation logic. |
| Retrieval Augmented Generation (RAG) | Open/Closed (SOLID - O) | Extends model knowledge with external context without modifying model weights. |
| Hybrid Retriever Techniques | Scalability | Combines methods to keep retrieval quality high as data size and query variety grow. |
| Query Rewriting Patterns | Single Responsibility Principle (SRP) | Assigns one focused job to a dedicated step: improving query quality before retrieval. |
| Reranker Implementation | Loose Coupling & High Cohesion | Keeps ranking as an isolated, focused component between retrieval and generation. |
| Guardrail Implementation | Reliability & Fault Tolerance | Adds safety filters that prevent harmful or invalid input/output from propagating. |
| Fine-Tuning for Specialized Domains | Dependency Inversion (SOLID - D) | Application behavior depends on abstract model interfaces, so backend models can be specialized/replaced. |
| The Hierarchy of Optimization | DRY | Reuses lower-cost improvements first (prompting/evals/RAG) before expensive retraining. |
| Realistic RAG Pipelines | Continuous Integration / Continuous Delivery | Encourages a clear, stage-based pipeline that can be versioned, tested, and deployed continuously. |
| Lifecycle Management and Evolution | Maintainability & Readability | Promotes continuous monitoring and iterative updates so the system stays understandable and sustainable over time. |
