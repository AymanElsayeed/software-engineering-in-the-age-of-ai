# Methodological Limitation

Based on the provided sources, here are the specific methodological limitations identified for each study:

### **Pearce et al. (Security Focus)**

- **CodeQL Tool Limitations:** The study relied heavily on GitHub’s CodeQL, which has difficulty identifying vulnerabilities that require context outside the specific code file. It also has a limited ability to derive memory boundaries (like array lengths), which can lead to "fail-safe" errors where code is marked vulnerable when it might not be.
- **Subjectivity of Manual Marking:** For domains not supported by CodeQL (such as the hardware description language Verilog), the authors had to mark code manually. This introduces the "human element," meaning results for these sections may be debatable.
- **Artificiality of Scenarios:** The "CWE scenarios" used were handcrafted and artificial, designed specifically to target known weaknesses. Consequently, they do not fully reflect the complexity, messiness, and large amount of context found in real-world software development.
- **Limited Statistical Scope:** Due to the manual nature of requesting results from the Copilot interface at the time of the study, the number of samples collected for each scenario was limited, making it difficult to make definitive claims on statistical significance.

### **Dakhel et al. (Functional/Efficiency Focus)**

- **Academic vs. Professional Tasks:** The study used fundamental algorithmic problems and university course assignments as its benchmark. These tasks are not necessarily representative of the typical, complex programming tasks performed by professional developers in an industrial environment.
- **Student Baseline Proxy:** The "human" comparison group consisted of students. While used as a proxy for junior developers, they may not accurately represent the skills or behaviors of the broader population of professional programmers.
- **Lack of Qualitative Insight:** The research focused almost exclusively on quantitative metrics (such as Cyclomatic Complexity and AST similarity). It did not capture qualitative aspects, such as how humans actually interact with the tool or their subjective experience using it.
- **Prompt Sensitivity:** The study found that Copilot often failed to understand natural language requirements (e.g., "older people at the front") but succeeded when using technical terms (e.g., "descending order"). This suggests the results are highly dependent on the researchers' specific "prompt engineering" rather than the AI's general capability.

### **Limitations Common to Both Studies**

- **"Black Box" Nature:** Because Copilot is closed-source and proprietary, neither study could analyze the model's internal logic or training data.
- **Non-Reproducibility:** Copilot is non-deterministic, meaning it can generate different answers for the same prompt at different times. Furthermore, because the model is continuously updated on remote servers, the results obtained during these studies may not be reproducible in the future.



## How might the limitations you listed affect the generalization of the studies  findings ?

The methodological limitations of these studies suggest that their findings may not fully represent the risks and benefits of using AI-generated code within a large-scale **organizational development environment**.

The following points explain how these limitations affect the **generalization** of their findings:

- **Underestimating Complexity:** Both studies used relatively small, isolated code snippets or academic assignments. In a professional organization, code is "considerably messier" and relies on vast amounts of context across multiple files. Limitations in static analysis tools like **CodeQL** to reason over this broader context mean that **security vulnerabilities or functional bugs requiring inter-file logic might be missed**, potentially under-reporting the risks in complex enterprise systems.
- **The "Student" Proxy vs. Professional Teams:** Dakhel et al. used students as a baseline for comparison. While students are a proxy for junior developers, they do not reflect the **collaborative workflows, peer review standards, or domain expertise** found in professional teams. Findings regarding the "repairing cost" of AI bugs might be overly optimistic when applied to complex industrial logic that students do not typically encounter.
- **Tool Evolution and Non-Reproducibility:** Because Copilot is a "black box" that is continuously updated on remote servers, the findings represent a **frozen snapshot in time**. An organization using a newer version of the tool might experience different error rates or security profiles than those documented, making it difficult for companies to use these studies as a permanent "gauge" for necessary scrutiny.
- **Prompt Sensitivity in Specialized Domains:** The studies found that findings were highly dependent on how a prompt was engineered—for example, changing "older people at the front" to "descending order" drastically improved correctness. In an organization with specialized domains (like the Verilog hardware examples), a developer’s **lack of experience in "AI prompting"** could lead to much higher failure rates than the studies suggest.
- **Static vs. Dynamic Risk:** Pearce et al. focused on "mechanical" implementation bugs caught by static analysis. However, many dangerous organizational vulnerabilities are **architectural** or require information beyond the source code (e.g., how the application interacts with the server), which these studies explicitly excluded.

