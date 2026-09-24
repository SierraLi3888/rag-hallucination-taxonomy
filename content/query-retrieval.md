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

The six comparisons below explain **what the studies change, what their evidence establishes, and where the conclusion stops**. Numerical results are compared within each paper’s setting, not across incompatible benchmarks.

### 5.3.1 Query Reformulation and Supervision

#### Paper comparison

Ma et al. (2023) train rewriting through reader feedback; RQ-RAG explicitly learns rewriting, decomposition and disambiguation. MaFeRw combines reference-based rewrite, retrieval and answer signals, whereas Cao et al. (2026) construct preferences from self-consistency. UTRAG incorporates conversation history alongside generator adaptation.

#### Analysis

**The central difference is what the supervision protects.** Reader feedback rewards useful answers, but a knowledgeable reader may compensate for a poor query. Retrieval rewards favour discoverability, but do not guarantee that the original entity, date or negation survives. Self-consistency reduces dependence on reference labels, yet several rewrites can share the same mistaken interpretation.

This explains why fluent rewriting and improved answer scores are insufficient evidence of faithful reformulation. UTRAG also changes the generator, so its full-system gains cannot be assigned to rewriting alone. The relevant comparison needs both component controls and inspection of which question constraints are preserved.

#### Current conclusion

Treat rewriting as a **constrained transformation of the information need**. The evidence supports task-aware refinement in tested pipelines; it does not support rewriting every query unconditionally. Evaluate semantic preservation alongside retrieval and answer quality, particularly for ambiguous conversation history.

#### Evidence reviewed

Ma (2023): reader feedback; Chan (2024): refinement operations; Wang (2025): reward design; Cao (2026): preference construction and ablations; Zhou & Lin (2026): multi-turn system analysis.

### 5.3.2 Retriever Alignment and Bias

#### Paper comparison

HyDE generates a hypothetical document as a dense-search representation. DVCQR produces separate sparse- and dense-oriented rewrites. Goyal et al. instead test sensitivity to document features that should not determine relevance. DVCQR raises TopiOCQA MRR from 35.2 to 37.4 with BM25 and from 51.4 to 52.5 with ANCE against its matched-backbone comparator.

#### Analysis

**Retriever alignment and resistance to bias are separate objectives.** A rewrite may improve compatibility with a scoring model while remaining vulnerable to its undesirable preferences. DVCQR’s ranking gains therefore do not answer Goyal’s robustness question. Conversely, lower bias scores do not establish complete evidence coverage.

HyDE adds a boundary distinction: its hypothetical text is a search aid, not verified evidence. Inaccurate intermediate details must be assessed by whether they misdirect retrieval; they should not automatically be counted as hallucinations in the final answer.

#### Current conclusion

Use retriever-aware representations where supported, while testing bias separately. None of these retrieval gains directly measures unsupported final claims. The defensible conclusion concerns **better evidence matching under specified conditions**, not a general reduction in hallucination.

#### Evidence reviewed

Gao (2023): generation–encoding design; Li (2026): Table 1 and retriever-specific evaluation; Goyal (2026): controlled bias and adversarial tests.

### 5.3.3 Evidence Coverage and Diagnostic Granularity

#### Paper comparison

RAGChecker distinguishes claim recall from context precision. Kobeissi and Langlais compare document, page and chunk retrieval in financial QA. Leung et al. distinguish errors across chunking, retrieval, reranking and generation. Together, they examine coverage at different levels rather than proposing interchangeable metrics.

#### Analysis

**Retrieving the right document is weaker than retrieving the required evidence.** A financial report can be relevant while the retrieved passage omits the year, unit or comparison value. RAGChecker’s context precision also counts a chunk as relevant when it supports at least one reference claim; this does not mean every sentence is useful.

Diagnosis must separate evidence absent from the source, damaged during indexing, missed by search and removed during selection. Increasing the number of passages only addresses some of these failures and can add redundancy. Reference-answer incompleteness can also make legitimate alternative evidence appear irrelevant.

#### Current conclusion

Assess coverage at the granularity needed to justify the answer, and **locate the first boundary where required information is lost**. Combine metrics with evidence inspection. The financial study illustrates this problem in one domain; it does not establish its prevalence across all RAG systems.

#### Evidence reviewed

Ru (2024): diagnostic metric definitions; Kobeissi & Langlais (2026): granularity and oracle comparisons; Leung (2026): stage attribution and agreement analysis.

### 5.3.4 Ranking and Evidence Set Selection

#### Paper comparison

SetR selects passages that jointly meet information requirements; Ammann et al. expand candidates through decomposition and then rerank. On MultiHopRAG, SetR improves Prec@5 over RankGPT (0.2268 vs 0.1799), yet has lower MRR@10 (0.5742 vs 0.6358). Ammann’s MRR@10 rises from 0.464 for naive RAG to 0.574 with reranking alone and 0.635 with decomposition plus reranking.

#### Analysis

**The metrics reward different properties.** MRR rewards the position of the first relevant result; it does not certify coverage of every information requirement. SetR’s contrasting results therefore support evaluating complementary evidence, rather than declaring one method uniformly superior.

Ammann’s component controls also change the interpretation: the full gain cannot be attributed to decomposition when reranking alone produces substantial improvement. Candidate acquisition and selection require separate diagnoses. A selector cannot recover a necessary fact that never entered its candidate pool.

#### Current conclusion

Evaluate **coverage and redundancy of the selected set**, alongside ranking metrics. Search again when evidence is missing; improve selection when useful candidates are already available. Set-level retrieval metrics remain proxies until the resulting answer is checked for support.

#### Evidence reviewed

Lee (2025): Table 2 and matched-setting ablations; Ammann (2025): Table 1 decomposition and reranking controls. Scores are interpreted within each study.

### 5.3.5 Multi-Hop Dependencies and Iterative Retrieval

#### Paper comparison

MultiHop-RAG benchmarks multi-evidence questions. ChainRAG restores entities omitted from later subquestions; Q-DREAM combines decomposition, dependency optimisation and dynamic retrieval. FLARE instead triggers searches during generation. ChainRAG entity completion raises second-subquestion Recall@2 from 40.91% to 58.81% on MuSiQue under a matched chunk-size comparison.

#### Analysis

**Decomposition only helps if the links between subquestions remain correct.** In Q-DREAM’s 2WikiMQA ablation, retaining decomposition without dependency optimisation or dynamic retrieval gives F1 of 38.1, below 44.7 with all three modules removed. This is evidence against unassisted decomposition in that setup, not against decomposition universally.

An incorrect intermediate entity can redirect later searches, producing a coherent-looking but wrong evidence chain. FLARE addresses emerging information needs during generation, so repeated retrieval should not be equated with multi-hop dependency resolution. More calls do not establish a more complete chain.

#### Current conclusion

Track the intermediate fact passed between searches and whether each dependency is supported. Evaluate **complete-chain recovery**, not only final-answer scores or the number of retrieval rounds. ChainRAG’s full-system gains also include its sentence graph and cannot all be assigned to entity completion.

#### Evidence reviewed

Tang & Yang (2024): benchmark; Zhu (2025): Section 4.4 and Table 2; Ye (2025): Table 2 ablations; Jiang (2023): retrieval-trigger design.

### 5.3.6 Evaluation of Evidence Sufficiency and Hallucination

#### Paper comparison

Sufficient Context separates contexts by whether they contain enough information to answer. RGB tests noise robustness, rejection and integration; RAGTruth labels unsupported or contradictory output. DRUID compares real retrieved evidence with synthetic context settings and questions inflated estimates of context utilisation.

#### Analysis

**Sufficiency, correctness and faithfulness must remain distinct.** An answer can be correct from model memory but unsupported by the supplied evidence. It can faithfully repeat a false source, or misuse sufficient correct evidence. A single answer-accuracy score conceals these differences.

Selective answering creates another confound: fewer wrong answers may reflect more refusals rather than better retrieval. DRUID further limits generalisation from artificial contexts to naturally retrieved material. Controlled experiments isolate mechanisms; realistic retrieval evaluates whether those mechanisms explain practical failures.

#### Current conclusion

Report evidence sufficiency, supported-answer quality and the proportion of questions answered together. Attribute hallucination reduction to retrieval only with comparable generators and budgets, plus evidence that output support improved. **Better retrieval is an intermediate achievement, not proof of faithful generation.**

#### Evidence reviewed

Joren (2025): sufficiency-stratified evaluation; Chen (2024): RGB capability tests; Niu (2024): RAGTruth annotations; Hagström (2025): real-versus-synthetic context comparison.

## 5.4 Cross-Stage Effects and Hallucination Manifestations

| Retrieval condition | Possible downstream manifestation | Boundary to check |
|---|---|---|
| Missing evidence | Unsupported completion | Did the model abstain or fill the gap? |
| Irrelevant evidence | Wrong-entity claims or unsupported attribution | Was the passage applied beyond its scope? |
| Incomplete evidence chain | Misleading comparison or synthesis | Were all required facts retained and connected? |

These are **possible pathways, not inevitable outcomes**. Sufficient evidence can still be misused; insufficient evidence can lead to safe refusal. Support: RGB, RAGTruth, RAGChecker and Sufficient Context.

**Attribution rule:** If selected evidence was complete but context compression removed a qualification, the primary loss is downstream of retrieval. If sufficient evidence reached the prompt but the answer contradicts it, investigate evidence use or reasoning. This prevents the taxonomy from assigning every wrong answer to the retriever.

## 5.5 Section Conclusion

**The main finding is that retrieval should be judged by collective evidence sufficiency for the intended question.** The review supports three connected judgements:

- **Preserve the target.** Query refinement can improve retrieval, but gains are difficult to interpret when the rewrite changes the entity, constraint or relation being asked about.
- **Recover and retain complementary support.** Coverage, ranking and set selection solve different problems. The SetR metric contrast and Ammann component controls show why a single retrieval score cannot explain all improvements.
- **Verify the downstream claim.** ChainRAG and Q-DREAM explain how evidence chains improve; Sufficient Context, RGB, RAGTruth and DRUID show why this still does not establish fewer unsupported answers.

The contribution of this taxonomy is to connect each failure to a diagnostic decision: clarify the request, repair its representation, search for missing facts, select complementary candidates or verify intermediate dependencies. These remedies are not interchangeable, and several failures can coexist.

**The main evidence gap is causal attribution.** Many studies demonstrate retrieval or answer-score gains; fewer directly isolate whether a retrieval intervention reduces unsupported claims while keeping the generator, budget and answering coverage comparable. Cross-paper scores should therefore not be pooled into a common ranking.

**Next research questions:** Can systems identify unmet evidence requirements before generation? Can they distinguish missing candidates from poor selection? Do the resulting improvements survive naturally occurring ambiguity and multi-hop dependencies in high-stakes domains?

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
