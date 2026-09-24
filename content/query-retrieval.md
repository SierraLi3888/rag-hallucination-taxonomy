Owner: Zhixuan Li
Status: In progress

## Overview / Definition

**Progress:** Reviewed 22 papers and developed a provisional account of how query and retrieval failures affect the evidence available to a RAG system. This is a focused critical literature review, not a new experimental study.

**Key finding:** Better retrieval scores do not, by themselves, demonstrate fewer hallucinations. Evidence availability, collective sufficiency, and faithful generation require separate evaluation.

**Scope:** Query interpretation and reformulation, matching, candidate retrieval, reranking, evidence selection, and subsequent retrieval decisions. Corpus absence and destructive chunking are upstream issues; context compression and arrangement follow selection.

## Subcategories or Failure Modes

The following five mechanisms are provisional categories derived from the review.

### Query intent drift

Rewriting or disambiguation can change the entity, time constraint, or relation being requested. Fluency and agreement between rewrites do not establish fidelity to the original question. [2, 3, 15, 19, 21](#references)

### Query–retriever mismatch

A faithful query may work poorly with a particular retriever. Sparse and dense retrieval favour different representations; improved compatibility does not guarantee robustness to spurious document features. [5, 6, 14](#references)

### Incomplete evidence coverage

Retrieving the correct document can still miss the answer-bearing passage or qualifying information. Diagnosis must distinguish facts absent from the corpus, damaged during indexing, and missed by retrieval. [10, 12, 17](#references)

### Redundant or insufficient evidence selection

Individually relevant passages can repeat the same fact while leaving another requirement unsupported. Reranking cannot recover evidence that never entered the candidate pool. [1, 11](#references)

### Broken multi-hop dependencies

Missing bridge entities or incorrect intermediate facts can redirect later searches. Decomposition needs to preserve dependencies; more subquestions or retrieval rounds do not establish complete support. [8, 18, 20, 22](#references)

## Evidence Reviewed

The corpus combines query-rewriting methods, retrieval and selection interventions, multi-hop benchmarks, and diagnostic studies. The review compared mechanisms, supervision assumptions, component ablations, and evaluation measures.

**Illustrative result:** ChainRAG reports second-subquestion Recall@2 on MuSiQue rising from 40.91% to 58.81% after entity completion in its controlled analysis. This measures retrieval recovery, not a reduction in hallucinations. [22](#references)

**Evidence boundary:** Results come from different tasks, corpora, models, and retrieval budgets. They are not a shared leaderboard, and no pooled effect size is estimated. RAGTruth, RGB, DRUID, and Sufficient Context help distinguish retrieval performance from downstream support, correctness, and context use. [4, 7, 9, 16](#references)

## Cross-paper Comparison

| Comparison | Finding from the reviewed studies | Implication |
| --- | --- | --- |
| DVCQR and retriever-bias analysis [6, 14] | Retriever-specific rewriting improves matching in tested settings; bias robustness remains a separate objective. | Evaluate fidelity, compatibility, and robustness separately. |
| RAGChecker and financial QA diagnostics [10, 17] | Correct-document retrieval can conceal missing answer-bearing facts. | Inspect evidence at the granularity needed to justify the answer. |
| SetR and decomposition plus reranking [1, 11] | SetR improves some coverage measures while trailing a comparator on MRR; decomposition and reranking make distinct contributions. | Separate candidate acquisition, rank quality, and set sufficiency. |
| ChainRAG and Q-DREAM [20, 22] | Entity completion improves retrieval; Q-DREAM's ablations show that decomposition without dependency handling can hurt performance. | Trace intermediate entities and dependencies across searches. |

## Analysis / Synthesis

The review's main contribution is a diagnostic sequence: **preserve the question → recover the required facts → select complementary evidence → assess support for the answer.**

Failures should be located where evidence is lost, rather than inferred solely from an incorrect answer. Relevant distinctions are:

- **Ranking versus coverage:** A highly ranked relevant passage may leave other requirements unmet.
- **Coverage versus sufficiency:** Retrieved facts must jointly support the requested answer.
- **Support versus correctness:** An answer may be correct from model memory yet unsupported by the supplied context, or faithfully repeat an incorrect source.

## Current Conclusion

Query and retrieval interventions address specific upstream evidence failures. Their effect on hallucination must be demonstrated separately through unsupported-claim and contradiction evaluation, alongside the proportion of questions answered when abstention is allowed.

**Next research priority:** Compare interventions on the same questions, corpus, generator, and budget; trace evidence before and after selection; and test naturally retrieved failures alongside controlled perturbations. These are proposed next steps, not completed experiments.

## Detection & Mitigation

| Failure to diagnose | Candidate response | Remaining limitation |
| --- | --- | --- |
| Intent drift or matching failure | Audit entity, time, negation, and relation constraints; test retriever-aware rewriting. | Fluent or self-consistent rewrites can still be wrong. |
| Missing or redundant evidence | Inspect claim coverage and evidence survival; use targeted retrieval and complementary set selection. | Selection cannot recover facts absent from its candidates. |
| Broken retrieval dependencies | Track intermediate fact provenance; use entity completion and dependency-aware refinement. | An early mistake can propagate to later searches. |
| Insufficient support for an answer | Assess context sufficiency and use clarification or abstention where appropriate. | Report correctness together with answer coverage. |

## References

The 22 papers below form the reviewed corpus. Numbers correspond to citations above; bibliographic details follow the progress report.

1. **Ammann et al. (2025).** [Question Decomposition for Retrieval-Augmented Generation](https://aclanthology.org/2025.acl-srw.32/). ACL Student Research Workshop.
2. **Cao et al. (2026).** [Multi-Faceted Self-Consistent Preference Alignment for Query Rewriting in Conversational Search](https://aclanthology.org/2026.findings-acl.638/). Findings of ACL.
3. **Chan et al. (2024).** [RQ-RAG: Learning to Refine Queries for Retrieval Augmented Generation](https://arxiv.org/abs/2404.00610). COLM. arXiv:2404.00610.
4. **Chen et al. (2024).** [Benchmarking Large Language Models in Retrieval-Augmented Generation](https://doi.org/10.1609/aaai.v38i16.29728). Proceedings of the AAAI Conference on Artificial Intelligence.
5. **Gao et al. (2023).** [Precise Zero-Shot Dense Retrieval without Relevance Labels](https://aclanthology.org/2023.acl-long.99/). ACL.
6. **Goyal et al. (2026).** [Masking or Mitigating? Deconstructing the Impact of Query Rewriting on Retriever Biases in RAG](https://aclanthology.org/2026.findings-acl.414/). Findings of ACL.
7. **Hagström et al. (2025).** [A Reality Check on Context Utilisation for Retrieval-Augmented Generation](https://aclanthology.org/2025.acl-long.968/). ACL.
8. **Jiang et al. (2023).** [Active Retrieval Augmented Generation](https://aclanthology.org/2023.emnlp-main.495/). EMNLP.
9. **Joren et al. (2025).** [Sufficient Context: A New Lens on Retrieval Augmented Generation Systems](https://arxiv.org/abs/2411.06037). ICLR. arXiv:2411.06037.
10. **Kobeissi & Langlais (2026).** [Decomposing Retrieval Failures in RAG for Long-Document Financial Question Answering](https://arxiv.org/abs/2602.17981). arXiv preprint.
11. **Lee et al. (2025).** [Shifting from Ranking to Set Selection for Retrieval Augmented Generation](https://aclanthology.org/2025.acl-long.861/). ACL.
12. **Leung et al. (2026).** [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://aclanthology.org/2026.eacl-long.147/). EACL.
13. **Lewis et al. (2020).** [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401). Advances in Neural Information Processing Systems.
14. **Li et al. (2026).** [DVCQR: Dual-View Conversational Query Rewriting with Stage-wise Reinforcement Learning](https://aclanthology.org/2026.acl-long.1054/). ACL.
15. **Ma et al. (2023).** [Query Rewriting in Retrieval-Augmented Large Language Models](https://aclanthology.org/2023.emnlp-main.322/). EMNLP.
16. **Niu et al. (2024).** [RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models](https://aclanthology.org/2024.acl-long.585/). ACL.
17. **Ru et al. (2024).** [RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation](https://arxiv.org/abs/2408.08067). Advances in Neural Information Processing Systems.
18. **Tang & Yang (2024).** [MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries](https://arxiv.org/abs/2401.15391). COLM. arXiv:2401.15391.
19. **Wang et al. (2025).** [MaFeRw: Query Rewriting with Multi-Aspect Feedbacks for Retrieval-Augmented Large Language Models](https://doi.org/10.1609/aaai.v39i24.34732). Proceedings of the AAAI Conference on Artificial Intelligence.
20. **Ye et al. (2025).** [Optimizing Question Semantic Space for Dynamic Retrieval-Augmented Multi-hop Question Answering](https://aclanthology.org/2025.acl-long.871/). ACL.
21. **Zhou & Lin (2026).** [UTRAG at SemEval-2026 Task 8: History-Aware Query Rewriting and LoRA-Finetuned Generation for Multi-Turn RAG](https://aclanthology.org/2026.semeval-1.237/). SemEval.
22. **Zhu et al. (2025).** [Mitigating Lost-in-Retrieval Problems in Retrieval Augmented Multi-Hop Question Answering](https://aclanthology.org/2025.acl-long.1089/). ACL.
