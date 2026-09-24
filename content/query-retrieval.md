Owner: Zhixuan Li
Status: In progress
Layout: stage-review

**Main finding:** Query and retrieval failures can lead to hallucination by **directing evidence towards the wrong interpretation, leaving essential facts unsupported, or carrying misleading information into subsequent reasoning**. Hallucination emerges when the generator treats these flawed evidence conditions as sufficient grounds for a claim.

**Reviewed corpus: 25 papers.** The synthesis separates upstream failure evidence, downstream output experiments, and diagnostic studies. Retrieval failure is a contributing cause, not a guarantee of hallucination.

## 4.1 Stage Role and Boundary

This stage translates an information need into searches and selects evidence for generation. Its causal role is to determine **which entities, conditions and facts the answer can be grounded in**.

RAGTruth identifies unsupported or contradictory output [23]; RAGChecker and Leung et al. distinguish pipeline errors [24, 25]. These are different levels of analysis: a missing passage is a retrieval failure; inventing the missing fact is an output failure. A valid answer to another interpretation may be unhelpful without being hallucinated.

**Boundary:** evidence absent from the source/index belongs upstream; evidence lost during context construction belongs downstream. Repeating a false source can be factually wrong while faithful to that source. The pathways below therefore distinguish evidence acquisition from how the generator uses it.

## 4.2 Major Failure Mechanisms

The seven mechanisms can overlap. Missing evidence describes an outcome; mismatch, ranking and broken dependencies can explain how it arose. False premises are treated explicitly within query validity, rather than conflated with ambiguity.

### 4.2.1 Ambiguous or Incomplete Queries

**Paper comparison.** CondAmbigQA studies missing conditions; AmbigDocs examines same-name entities; Tree of Clarifications explores alternative interpretations [3–5]. Qin et al. address a different problem: false premises [6].

**Analysis.** An unspecified entity or time period lets the system silently choose an interpretation. Retrieved documents can then support the wrong target, or supply attributes from different entities that the generator merges. A false premise instead presupposes an event or relation that may not exist.

**Current conclusion.** The hallucination pathway is **unverified interpretation → misapplied or merged evidence → unsupported attribution**. Ambiguity alone is not hallucination; the decisive error is presenting an unjustified assumption or fabricated combination as fact.

**Evidence reviewed.** Conditional-answer evaluation [3]; entity-merging output categories [4]; clarification interventions [5]; premise verification [6]. Watson et al. provide observational query-risk evidence, not a RAG causal experiment [1].

### 4.2.2 Query Reformulation Problems

**Paper comparison.** Abe et al. examine expansion failures on unfamiliar and ambiguous queries; Goyal et al. test rewriting under retriever biases; RaDIO studies queries formed during generation [2, 7, 22].

**Analysis.** Expansion can add an incorrect detail or privilege a popular interpretation. The resulting search may retrieve convincing evidence for the rewritten question while failing to support the original one. In iterative retrieval, a query that misses the current information gap can leave that gap unresolved.

**Current conclusion.** Reformulation can introduce **semantic drift before evidence is collected**. A downstream answer becomes unsupported when it treats the altered assumption as established. The cited retrieval gains or losses do not themselves measure this final transition.

**Evidence reviewed.** Expansion comparisons across retrievers [2]; controlled bias tests [7]; query/trigger component experiments [22].

### 4.2.3 Query–Document Mismatch

**Paper comparison.** Abe et al. show query-dependent retrieval failures; Goyal et al. examine sensitivity to document features; AmbigDocs isolates confusion between same-name entities [2, 7, 4].

**Analysis.** Matching can favour surface similarity or a familiar entity over the relation actually requested. Evidence can appear relevant while referring to another person, period or condition. If generation ignores this scope difference, a real fact is attributed to the wrong target.

**Current conclusion.** Mismatch can produce **plausible but wrongly attributed answers**, not merely empty results. These studies support particular forms of misalignment; they do not establish that every vocabulary or embedding mismatch produces hallucination.

**Evidence reviewed.** Retrieval comparisons [2, 7]; entity-level output analysis [4]. AmbigDocs mainly supplies gold documents, so its reader errors cannot all be assigned to the retriever.

### 4.2.4 Missing Relevant Evidence

**Paper comparison.** Park and Lee manipulate imperfect retrieval; RGB tests rejection when evidence cannot answer; Sufficient Context separates sufficient from insufficient contexts [8, 9, 13]. DRUID tests context utilisation under more realistic retrieved evidence [14].

**Analysis.** A missing supporting fact leaves a claim ungrounded. The model may supply a plausible completion from prior knowledge or pattern matching, producing a fluent answer whose certainty exceeds the evidence. Alternatively, it may correctly refuse or answer only the supported part.

**Current conclusion.** The causal pathway requires two conditions: **an evidence gap and a decision to answer beyond it**. Absence of evidence alone is insufficient to explain hallucination.

**Evidence reviewed.** Unanswerable-context output categories [8, 9]; sufficiency-stratified responses [13]; naturally retrieved context evaluation [14].

### 4.2.5 Irrelevant Retrieved Passages

**Paper comparison.** Yoran et al. examine retrieval-induced errors; Cuconasu et al. distinguish distracting from random documents; Hong et al. test counterfactual noise [10–12].

**Analysis.** A passage sharing entities or topic words can supply an attractive but inapplicable answer. The generator may copy its entity or relation into the response. This differs from arbitrary noise: random material sometimes improves accuracy in Cuconasu et al.'s settings, so irrelevance is not uniformly harmful.

**Current conclusion.** The risk depends on **how distractors compete with or impersonate supporting evidence**, not simply their number. False source content also implicates source quality and downstream trust, not query formulation alone.

**Evidence reviewed.** Retrieval/no-retrieval comparisons and selected-case error analysis [10]; controlled noise types [11]; misleading-context experiments [12].

### 4.2.6 Ranking and Evidence Selection Failures

**Paper comparison.** SetR examines complementary evidence selection; MultiHop-RAG tests questions requiring multiple facts; RAGChecker separates claim coverage from context quality [16, 17, 24].

**Analysis.** Ranking individually relevant passages can repeatedly select the same fact while omitting a necessary qualifier or comparison value. The evidence appears abundant but is incomplete. A generator can then generalise beyond a supported condition or invent the missing relationship.

**Current conclusion.** Ranking contributes through **selective omission and misleading evidence composition**. This differs from candidate-generation failure: useful evidence may exist among candidates but never reach the selected set.

**Evidence reviewed.** Set-selection comparisons [16]; multi-evidence retrieval evaluation [17]; diagnostic metrics [24]. These establish coverage problems more directly than final hallucination causation.

### 4.2.7 Multi-Hop Retrieval Failures

**Paper comparison.** ChainRAG addresses lost intermediate entities; Q-DREAM examines decomposition and dependencies; MARCH combines ambiguity with multi-hop inference [18–20]. HopRefusalBench tests unanswerable chains and hallucinated completion [21].

**Analysis.** An incorrect or missing bridge entity changes the next query. Later searches may retrieve internally consistent evidence about the wrong path, reinforcing the initial mistake. When a required hop cannot be supported, continued answering may fabricate the missing connection.

**Current conclusion.** Multi-hop hallucination can arise through **error propagation or unsupported chain completion**. Additional retrieval does not necessarily repair a path already redirected by a mistaken intermediate assumption.

**Evidence reviewed.** Entity-completion and dependency ablations [18, 19]; ambiguity/clarification evaluation [20]; refusal and search-trajectory analysis [21]. The last is a 2026 preprint.

## 4.3 Comparison of Existing Literature

#### Paper comparison

| Evidence approach | Representative studies | What it establishes—and what it does not |
|---|---|---|
| Query variation and reformulation | Watson; Abe; Goyal [1, 2, 7] | Query-associated risk and retrieval drift; not a complete query-to-hallucination causal estimate. |
| Ambiguity and premise analysis | CondAmbigQA; AmbigDocs; Qin; MARCH [3, 4, 6, 20] | Missing conditions, entity fusion and invalid assumptions are distinct mechanisms; alternative valid answers are not automatically hallucinations. |
| Manipulated retrieval/context | Park and Lee; RGB; Yoran; Cuconasu; Hong [8–12] | Stronger evidence about responses to particular evidence defects; synthetic settings do not establish real-world prevalence. |
| Sufficiency and realistic context | Sufficient Context; DRUID; FaithEval [13–15] | Whether evidence permits an answer and how models respond; insufficient context does not identify which upstream component failed. |
| Selection and multi-hop controls | SetR; MultiHop-RAG; ChainRAG; Q-DREAM; HopRefusalBench [16–19, 21] | Missing complementary facts and broken dependencies; most answer-score gains are not claim-level hallucination measurements. |

#### Analysis

**The studies measure different links in the causal chain.** An expansion experiment can show why relevant evidence disappears without observing hallucination. An unanswerable-context experiment can show unsupported answering without explaining why retrieval missed the evidence. Their findings are complementary, but cannot be pooled into a common “hallucination reduction” ranking.

Two comparisons constrain the interpretation. AmbigDocs observes entity confusion even with supplied gold documents, showing that query ambiguity also affects evidence use. Cuconasu et al.'s noise results challenge any blanket claim that more irrelevant passages cause more hallucination. The explanation must specify the document's misleading content and the model's response to it.

#### Current conclusion

The strongest synthesis connects **a demonstrated upstream defect with an independently observed output behaviour**, while marking the connection as synthesis where no single experiment isolates the whole pathway. Controlled failures explain mechanisms; naturally retrieved contexts test their practical relevance.

#### Evidence reviewed

All 25 papers inform the section. Tree of Clarifications [5] and RaDIO [22] provide intervention evidence; RAGTruth, RAGChecker and Leung et al. [23–25] ground output definitions and stage attribution. The corpus is a targeted, question-led selection, not an exhaustive systematic review.

## 4.4 Cross-Stage Effects and Hallucination Manifestations

| Upstream failure | Evidence reaching generation | Possible hallucination manifestation |
|---|---|---|
| Ambiguity or reformulation drift | Material for the wrong entity or condition | Wrong attribution or fusion of different entities' facts |
| False premise | No valid support for the assumed event/relation | Fabricated explanation that accepts the premise |
| Missing evidence or poor selection | Partial support with a crucial fact absent | Unsupported completion or overgeneralisation |
| Misleading passage | Plausible but inapplicable/false content | Incorrect claim adopted from retrieved material |
| Broken multi-hop dependency | Wrong bridge or incomplete chain | Invented connection or propagated intermediate error |

**Analysis and current conclusion.** These pathways combine evidence defects with generator behaviour: accepting assumptions, confusing scope, trusting misleading content or filling gaps. Safe refusal can interrupt them. Conversely, sufficient evidence can still be misused. FaithEval and RAGTruth also require a distinction between factual error and unfaithfulness to supplied context [15, 23].

**Evidence reviewed.** The comparison draws on entity/premise studies [4, 6], imperfect-context experiments [8–15], multi-hop analysis [18–21] and stage diagnostics [24, 25]. If the selected evidence was sufficient but later compressed incorrectly, the primary loss belongs to context construction rather than retrieval.

## 4.5 Section Conclusion

**Query and retrieval failures contribute to hallucination by changing what the answer appears to be supported by.** Three recurring pathways emerge:

- **Wrong target:** ambiguity, false assumptions or reformulation drift lead the system to answer about the wrong entity, condition or relation.
- **Missing support:** retrieval and selection omit a necessary fact; the generator fills the gap instead of limiting its claim.
- **Error propagation:** misleading passages or incorrect bridge entities enter later reasoning and become part of a coherent-looking but unsupported answer.

The central causal judgement is therefore **flawed evidence acquisition interacting with unsupported inference**. Query defects are neither harmless wording issues nor sufficient causes by themselves. Their consequences depend on whether the generator recognises uncertainty, preserves entity boundaries and stops when a claim lacks support.

**Open evidence gap:** relatively few studies trace a controlled query defect through retrieved passages to manually verified hallucinated claims. This limits estimates of how often each mechanism causes hallucination, even when the mechanism itself is well motivated. In high-stakes settings, a key question is which missing conditions or intermediate facts most often turn apparently supported answers into false claims.

## References

The 25-paper corpus below uses numbered citations. Publication years follow the published version where available; HopRefusalBench is a preprint.

1. **Watson et al. (2026).** [What Makes a Good Query? Measuring the Impact of Human-Confusing Linguistic Features on LLM Performance](https://aclanthology.org/2026.findings-eacl.251/). Findings of EACL 2026.
2. **Abe et al. (2025).** [LLM-based Query Expansion Fails for Unfamiliar and Ambiguous Queries](https://arxiv.org/abs/2505.12694). SIGIR 2025.
3. **Li et al. (2025).** [CondAmbigQA: A Benchmark and Dataset for Conditional Ambiguous Question Answering](https://aclanthology.org/2025.emnlp-main.115/). EMNLP 2025.
4. **Lee et al. (2024).** [AmbigDocs: Reasoning across Documents on Different Entities under the Same Name](https://arxiv.org/abs/2404.12447). COLM 2024.
5. **Kim et al. (2023).** [Tree of Clarifications: Answering Ambiguous Questions with Retrieval-Augmented Large Language Models](https://aclanthology.org/2023.emnlp-main.63/). EMNLP 2023.
6. **Qin et al. (2026).** [Don’t Let It Hallucinate: Premise Verification via Retrieval-Augmented Logical Reasoning](https://arxiv.org/abs/2504.06438). TMLR 2026 (initial preprint 2025).
7. **Goyal et al. (2026).** [Masking or Mitigating? Deconstructing the Impact of Query Rewriting on Retriever Biases in RAG](https://aclanthology.org/2026.findings-acl.414/). Findings of ACL 2026.
8. **Park and Lee (2024).** [Toward Robust RALMs: Revealing the Impact of Imperfect Retrieval on Retrieval-Augmented Language Models](https://aclanthology.org/2024.tacl-1.91/). TACL 2024.
9. **Chen et al. (2024).** [Benchmarking Large Language Models in Retrieval-Augmented Generation (RGB)](https://ojs.aaai.org/index.php/AAAI/article/view/29728). AAAI 2024.
10. **Yoran et al. (2024).** [Making Retrieval-Augmented Language Models Robust to Irrelevant Context](https://arxiv.org/abs/2310.01558). ICLR 2024.
11. **Cuconasu et al. (2024).** [The Power of Noise: Redefining Retrieval for RAG Systems](https://arxiv.org/abs/2401.14887). SIGIR 2024.
12. **Hong et al. (2024).** [Why So Gullible? Enhancing the Robustness of Retrieval-Augmented Models against Counterfactual Noise](https://aclanthology.org/2024.findings-naacl.159/). Findings of NAACL 2024.
13. **Joren et al. (2025).** [Sufficient Context: A New Lens on Retrieval Augmented Generation Systems](https://arxiv.org/abs/2411.06037). ICLR 2025.
14. **Hagström et al. (2025).** [A Reality Check on Context Utilisation for Retrieval-Augmented Generation (DRUID)](https://aclanthology.org/2025.acl-long.968/). ACL 2025.
15. **Ming et al. (2025).** [FaithEval: Can Your Language Model Stay Faithful to Context, Even If “The Moon is Made of Marshmallows”](https://arxiv.org/abs/2410.03727). ICLR 2025 (initial preprint 2024).
16. **Lee et al. (2025).** [Shifting from Ranking to Set Selection for Retrieval Augmented Generation (SetR)](https://aclanthology.org/2025.acl-long.861/). ACL 2025.
17. **Tang and Yang (2024).** [MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries](https://arxiv.org/abs/2401.15391). COLM 2024.
18. **Zhu et al. (2025).** [Mitigating Lost-in-Retrieval Problems in Retrieval Augmented Multi-Hop Question Answering (ChainRAG)](https://aclanthology.org/2025.acl-long.1089/). ACL 2025.
19. **Ye et al. (2025).** [Optimizing Question Semantic Space for Dynamic Retrieval-Augmented Multi-hop Question Answering (Q-DREAM)](https://aclanthology.org/2025.acl-long.871/). ACL 2025.
20. **Park et al. (2026).** [MARCH: Evaluating the Intersection of Ambiguity Interpretation and Multi-hop Inference](https://aclanthology.org/2026.findings-acl.1352/). Findings of ACL 2026.
21. **Xie et al. (2026).** [HopRefusalBench: Diagnosing Refusal Failures in Search-Augmented Agents for Multi-Hop Reasoning](https://arxiv.org/abs/2608.01358). arXiv preprint, August 2026.
22. **Zhu et al. (2025).** [RaDIO: Real-Time Hallucination Detection with Contextual Index Optimized Query Formulation for Dynamic Retrieval Augmented Generation](https://ojs.aaai.org/index.php/AAAI/article/view/34809). AAAI 2025.
23. **Niu et al. (2024).** [RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models](https://aclanthology.org/2024.acl-long.585/). ACL 2024.
24. **Ru et al. (2024).** [RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation](https://arxiv.org/abs/2408.08067). NeurIPS 2024, Datasets and Benchmarks.
25. **Leung et al. (2026).** [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://aclanthology.org/2026.eacl-long.147/). EACL 2026.
