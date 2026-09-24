Owner: Zhixuan Li
Status: In progress
Layout: stage-review

**Main finding:** Better retrieval can provide stronger evidence, but does not by itself prevent hallucination. This review identifies **seven failure mechanisms** across **22 papers**.

## 5.1 Stage Role and Boundary

**Question → query formulation → retrieval and selection → evidence for generation.**

This stage determines what evidence reaches the generator (Lewis et al., 2020). Missing source information is upstream; losing evidence during context construction or misusing it during generation is downstream. Diagnose where evidence disappears before assigning blame.

## 5.2 Major Failure Mechanisms

These categories can co-occur. The distinction is **what failed**, not simply whether the final answer was wrong.

### 5.2.1 Ambiguous or Incomplete Queries

**Unclear information need.** The entity, time period or constraint is unspecified. Check whether conversation history or clarification resolves it.

### 5.2.2 Query Reformulation Problems

**Meaning changes during rewriting.** A rewrite drops a condition or adds an unsupported assumption. Compare it with the original question.

### 5.2.3 Query–Document Mismatch

**The request is clear, but matching fails.** Vocabulary or representation differences prevent retrieval of suitable indexed evidence.

### 5.2.4 Missing Relevant Evidence

**Required evidence never enters the candidate set.** First confirm that it exists in the searchable index.

### 5.2.5 Irrelevant Retrieved Passages

**Unhelpful evidence enters the results.** Topical similarity can conceal a wrong entity or period; extra passages may distract the generator.

### 5.2.6 Ranking and Evidence Selection Failures

**Useful candidates are available but poorly selected.** Redundant passages displace complementary facts. High individual relevance does not guarantee a sufficient evidence set.

### 5.2.7 Multi-Hop Retrieval Failures

**The evidence chain breaks.** A missing or incorrect intermediate entity redirects later searches. Check dependencies between retrieval steps.

## 5.3 Comparison of Existing Literature

Each comparison separates the intervention, its limitation and the conclusion supported. Results from different experimental settings are not a shared leaderboard.

### 5.3.1 Query Reformulation and Supervision

#### Paper comparison

Ma uses reader feedback; MaFeRw combines feedback signals; Cao uses preference alignment. RQ-RAG learns refinement; UTRAG incorporates history.

#### Analysis

They optimise different objectives; better scores do not prove preserved meaning.

#### Current conclusion

Evaluate constraint preservation alongside task performance.

#### Evidence reviewed

Ma (2023); Chan (2024); Wang (2025); Cao (2026); Zhou & Lin (2026).

### 5.3.2 Retriever Alignment and Bias

#### Paper comparison

HyDE changes the search representation; DVCQR aligns sparse/dense rewrites; Goyal tests retriever bias.

#### Analysis

Compatibility with a retriever does not establish resistance to bias.

#### Current conclusion

Test relevance gains and bias robustness separately.

#### Evidence reviewed

Gao (2023); Li (2026); Goyal (2026): representation experiments and controlled bias tests.

### 5.3.3 Evidence Coverage and Diagnostic Granularity

#### Paper comparison

RAGChecker measures claim coverage; the financial retrieval study distinguishes document/page/chunk retrieval; Leung classifies pipeline errors.

#### Analysis

Finding the correct document can still miss the necessary fact.

#### Current conclusion

Check evidence survival at each stage boundary.

#### Evidence reviewed

Ru (2024); Kobeissi & Langlais (2026); Leung (2026).

### 5.3.4 Ranking and Evidence Set Selection

#### Paper comparison

SetR selects complementary passages; Ammann combines decomposition with reranking.

#### Analysis

SetR improves Prec@5 over RankGPT (0.2268 vs 0.1799), yet has lower MRR@10 (0.5742 vs 0.6358) on MultiHopRAG.

#### Current conclusion

Evaluate collective coverage, not just the first relevant result.

#### Evidence reviewed

Lee (2025), Table 2; Ammann (2025), component controls.

### 5.3.5 Multi-Hop Dependencies and Iterative Retrieval

#### Paper comparison

MultiHop-RAG benchmarks the problem; ChainRAG restores entities; Q-DREAM manages dependencies; FLARE triggers further retrieval during generation.

#### Analysis

ChainRAG entity completion raises second-subquestion Recall@2 from 40.91% to 58.81% on MuSiQue. Q-DREAM ablations show decomposition alone can hurt.

#### Current conclusion

Preserve intermediate dependencies; more searches alone are insufficient.

#### Evidence reviewed

Tang & Yang (2024); Zhu (2025); Ye (2025); Jiang (2023).

### 5.3.6 Evaluation of Evidence Sufficiency and Hallucination

#### Paper comparison

Sufficient Context tests answerability; RGB tests robustness; RAGTruth labels unsupported output; DRUID tests realistic context use.

#### Analysis

Evidence sufficiency, factual correctness and faithfulness are different properties.

#### Current conclusion

Measure supported claims and abstention alongside retrieval scores.

#### Evidence reviewed

Joren (2025); Chen (2024); Niu (2024); Hagström (2025).

## 5.4 Cross-Stage Effects and Hallucination Manifestations

| Retrieval condition | Possible downstream manifestation | Boundary to check |
|---|---|---|
| Missing evidence | Unsupported completion | Did the model abstain or fill the gap? |
| Irrelevant evidence | Wrong-entity claims or unsupported attribution | Was the passage applied beyond its scope? |
| Incomplete evidence chain | Misleading comparison or synthesis | Were all required facts retained and connected? |

These are **possible pathways, not inevitable outcomes**. Sufficient evidence can still be misused; insufficient evidence can lead to safe refusal. Support: RGB, RAGTruth, RAGChecker and Sufficient Context.

## 5.5 Section Conclusion

**Judge retrieval by whether the selected evidence jointly answers the intended question.** Demonstrate reduced hallucination separately through supported-answer evaluation.

**Open question:** Which retrieval improvements reduce unsupported claims when the generator, retrieval budget and proportion of questions answered are comparable?

## References

The 22 papers below form the reviewed corpus. Entries are listed alphabetically; the text uses author–year citations.

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
