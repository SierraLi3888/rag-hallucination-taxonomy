Owner: Zhixuan Li
Status: In progress
Layout: report

A critical review of 22 papers on query and retrieval failures in RAG, covering query reformulation, matching, evidence coverage, selection, and multi-hop dependencies. The review distinguishes improvements in retrieval from evidence of reduced hallucination.

## 1 Representing the information need without changing the question

### Paper comparison

Ma et al. introduce reader-guided rewriting; RQ-RAG separates rewriting, decomposition, and disambiguation. MaFeRw uses labelled feedback, whereas MSPA-CQR uses self-consistency. UTRAG combines history-aware rewriting with generator adaptation, limiting attribution to rewriting alone. [2, 3, 15, 19, 21](#references)

### Analysis

A fluent rewrite can still lose an entity, date, negation, or requested relation. Retrieval and answer rewards protect different objectives; agreement between candidate rewrites does not establish truth.

### Current conclusion

Reformulation should preserve the information need while improving retrievability. Its usefulness is supported in tested pipelines, but indiscriminate rewriting is not justified.

### Evidence reviewed

Rewriting objectives, supervision assumptions, conversational drift, ablations, and downstream QA evaluation across the five studies above.

## 2 Matching query representations to retrievers and their biases

### Paper comparison

HyDE uses generated hypothetical documents as search representations. DVCQR aligns separate rewrites with sparse and dense retrievers. Goyal et al. assess whether rewriting reduces sensitivity to inappropriate document features. [5, 6, 14](#references)

### Analysis

Retriever compatibility and bias robustness are distinct. A hypothetical passage may aid search despite inaccurate details; treating it as verified evidence creates a different reliability problem.

### Current conclusion

Query quality depends on the retrieval mechanism. Evaluate semantic fidelity, retriever compatibility, and robustness separately; rewriting alone may not repair document-encoding vulnerabilities.

### Evidence reviewed

HyDE retrieval experiments; DVCQR retriever-specific results; controlled bias measures and adversarial tests, with their stated scope limitations.

## 3 Finding the required evidence at the right granularity

### Paper comparison

RAGChecker distinguishes claim recall from context precision. Kobeissi and Langlais show that retrieving the correct financial document can still miss the answer-bearing page or chunk. Leung et al. separate chunking, retrieval, and later-stage errors. [10, 12, 17](#references)

### Analysis

Trace whether a required fact existed in the source, survived indexing, entered the candidate pool, and reached the prompt. Document-level relevance does not establish answer-level coverage.

### Current conclusion

Evaluate coverage at the granularity required to justify the answer. Distinguish unavailable, damaged, and unretrieved evidence before assigning a cause.

### Evidence reviewed

RAGChecker metric definitions; FinanceBench multi-granularity and oracle experiments; stage-specific error examples.

## 4 Selecting complementary evidence rather than redundant relevance

### Paper comparison

SetR selects passages jointly: on MultiHopRAG, its reported Prec@5 exceeds RankGPT’s (0.2268 versus 0.1799), while MRR@10 is lower (0.5742 versus 0.6358). Ammann et al. separate decomposition, reranking, and their combination. [1, 11](#references)

### Analysis

A highly relevant passage may be followed by duplicates that leave other requirements unanswered. Candidate acquisition and complementary selection are different problems; a selector cannot recover missing candidates.

### Current conclusion

Supplement ranking metrics with coverage, redundancy, and set-sufficiency assessment. More passages do not necessarily provide more useful evidence.

### Evidence reviewed

SetR set-selection experiments and matched controls; decomposition and reranking component comparisons.

## 5 Preserving dependencies through multi hop and iterative retrieval

### Paper comparison

MultiHop-RAG benchmarks evidence collection across hops. ChainRAG’s entity completion raises second-subquestion Recall@2 from 40.91% to 58.81% in its MuSiQue analysis. Q-DREAM shows decomposition can hurt without dependency handling; FLARE retrieves as generation develops. [8, 18, 20, 22](#references)

### Analysis

Later searches depend on intermediate entities and facts. An early error can redirect the entire trajectory. Parallel evidence collection, sequential bridge reasoning, and repeated retrieval are related but distinct.

### Current conclusion

Multi-hop reliability requires preserving dependencies and accumulated support. Counting subquestions or retrieval calls does not measure completeness.

### Evidence reviewed

Benchmark evidence labels, entity-completion controls, dependency ablations, retrieval-trigger design, and supporting-fact evaluation. [1, 3, 8, 18, 20, 22](#references)

## 6 Distinguishing insufficient evidence from downstream hallucination

### Paper comparison

RAGTruth annotates unsupported or contradictory spans; RGB tests noise, rejection, integration, and counterfactual robustness. Sufficient Context separates answerability from utilisation. DRUID finds that synthetic evidence can inflate context-utilisation estimates. [4, 7, 9, 16](#references)

### Analysis

Evidence sufficiency, answer support, and factual correctness are different properties. Insufficient context has several possible upstream causes; sufficient evidence can still be misused. Selective generation must be evaluated alongside answer coverage.

### Current conclusion

Retrieval failures and hallucinations are related but distinct. Grounded answers also depend on context preservation, faithful utilisation, and appropriate abstention.

### Evidence reviewed

Foundational RAG, hallucination annotations, capability benchmarks, sufficiency-stratified errors, and component diagnostics. [4, 7, 9, 12, 13, 16, 17](#references)

## 7 Overall assessment and research priorities

### Paper comparison

The corpus studies different intervention targets and outcomes: query text, matching, candidates, selected sets, retrieval trajectories, and response policy. Retrieval metrics, QA scores, and unsupported-claim measures are not interchangeable.

### Analysis

Four questions organise the synthesis: Does the representation preserve the question? Are the required facts retrieved? Does the selected set jointly support the answer? Is that support used faithfully? Priorities are matched comparisons, evidence traces, claim-level evaluation, and naturally retrieved failure cases.

### Current conclusion

Retrieval improvements reduce specific upstream evidence failures; hallucination reduction requires separate downstream evaluation. Reliable grounding depends on collectively adequate evidence and generation constrained by that evidence.

### Evidence reviewed

All 22 references below, triangulated across methods, benchmarks, and diagnostic studies. Heterogeneous settings preclude a pooled effect estimate.

## References

The 22 papers below form the reviewed corpus. Numbers correspond to citations above.

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
