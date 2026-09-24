Owner: Zhixuan Li
Status: In progress
Layout: stage-review

Query and Retrieval — Member B. This section develops a seven-category failure taxonomy, compares evidence from 22 studies, and explains the conditional relationship between retrieval failures and hallucination.

## 5.1 Stage Role and Boundary

Query and retrieval determine which external evidence is available to a retrieval-augmented generation (RAG) system. Within a literature review of hallucination, the purpose of this section is to explain how failures in obtaining that evidence create conditions for unsupported, misleading or incorrectly attributed answers. Retrieval quality is therefore examined as a potential cause of downstream failure, not as a substitute for measuring hallucination itself.

Lewis et al. (2020) establish the combination of parametric generation with non-parametric retrieval. Subsequent research shows why access to a retriever does not guarantee that the material returned will answer the intended question. The system may misinterpret the request, rewrite it incorrectly, fail to match suitable documents, omit necessary evidence or select passages that are individually relevant but collectively incomplete. Iterative retrieval adds the possibility that an incorrect intermediate result changes the target of later searches.

The input to this stage is the user’s information need, any relevant conversation history and a searchable index. Its output is a selected set of evidence, ideally with identifiable sources, passed to context construction. This review includes query interpretation and reformulation, candidate retrieval, relevance scoring, reranking, evidence selection and decisions to search again. It treats source availability, source correctness and destructive chunking as upstream concerns; compression, prompt arrangement and truncation after evidence selection belong to context construction. Reasoning, faithful use of evidence, abstention and citation generation are downstream behaviours. Iterative systems can revisit retrieval during generation, so these boundaries are functional rather than a strictly one-way sequence.

This boundary matters for diagnosis. A necessary fact may be absent from the corpus, removed when the index was built, missed by candidate retrieval, excluded by selection, lost during prompt construction or ignored by the generator. The same final answer can arise from these different pathways. Ru et al. (2024) and Leung et al. (2026) support component-level investigation rather than inferring the failed stage solely from an incorrect response.

Section 5.2 defines seven failure categories and their boundaries. Section 5.3 compares the research supporting those categories, including methods, selected results, diagnostic measures and mitigation limits. Section 5.4 connects the retrieval stage to hallucination manifestations; Section 5.5 gives the resulting assessment and research priorities. The corpus contains 22 studies, including all 11 additions to the earlier literature set. Bibliographic records and accessible primary papers were checked for the preceding review on 24 September 2026; this revision reorganises and synthesises that evidence. It is a focused critical review, not an exhaustive systematic review or a report of new experiments.

## 5.2 Major Failure Mechanisms

The seven categories provide an operational taxonomy for examining where and how retrieval fails. They are not mutually exclusive labels at one uniform causal level: query–document mismatch describes a mechanism, missing evidence describes a retrieval outcome, and multi-hop failure describes a dependency problem that can amplify other mechanisms. An incident can receive more than one label, provided the analysis records their relationship. The examples below are explanatory illustrations, not additional experimental findings.

### 5.2.1 Ambiguous or Incomplete Queries

This category concerns an information need whose entity, relation, time period or other necessary constraint has not been resolved before retrieval. A conversational question such as “Did it improve after that change?” may be meaningful to the user but insufficient for a retriever unless the system identifies what “it” and “that change” refer to. Ambiguity in the user’s wording is an input condition; the system failure is proceeding with an unjustified interpretation or failing to recover context that was available.

RQ-RAG distinguishes disambiguation from rewriting and decomposition (Chan et al., 2024). UTRAG highlights the dependence of conversational retrieval on selecting appropriate history (Zhou and Lin, 2026). Together they support treating recovery of the information need as a distinct problem. However, model-generated clarification is not equivalent to clarification supplied by the user: several interpretations may remain plausible even after a fluent standalone question has been produced.

The diagnostic question is whether the query used for search contains the intended referents and constraints. If the correct interpretation cannot be established, explicit clarification or preservation of alternative interpretations is a reasonable design response, rather than silently committing to one. These are implications of the taxonomy, not a claim that every reviewed method evaluates interactive clarification. The category ends where a sufficiently specified request becomes the input to a transformation; errors introduced by that transformation belong to Section 5.2.2.

### 5.2.2 Query Reformulation Problems

Reformulation failure occurs when rewriting, expansion, decomposition or history incorporation changes the information need in a way that harms evidence acquisition. A rewrite can remove a negation, replace an exact entity with a broader category, drop a date restriction or insert an unsupported premise. Unlike unresolved ambiguity, the problem can occur even when the original request was clear.

Ma et al. (2023), Wang et al. (2025) and Cao et al. (2026) optimise reformulation using different feedback signals. Their interventions make query transformation a controllable component, but improvement in an aggregate retrieval or answer score does not establish that every constraint has been preserved. Agreement among candidate rewrites likewise does not rule out a shared incorrect assumption. HyDE adds an important qualification: a generated hypothetical document is a search representation, so inaccurate intermediate details are not automatically hallucinations in the final answer (Gao et al., 2023).

Diagnosis requires comparing the original request, the reformulated query and the evidence subsequently returned. The relevant failure is semantic drift or harmful expansion, not merely wording change. Retaining the original query for comparison, checking critical constraints and examining whether generated assumptions redirect search are appropriate safeguards to evaluate. The distinction from Section 5.2.3 is that a faithful reformulation can still be poorly matched to its retriever.

### 5.2.3 Query–Document Mismatch

Here the intended information need is sufficiently specified, but the representation or scoring mechanism fails to connect it to suitable indexed material. Vocabulary differences, representation choices and retriever-specific preferences can affect matching. The defining question is whether an alternative expression or retrieval mechanism can recover relevant evidence without changing what is being asked.

HyDE changes the representation used for dense retrieval; DVCQR produces separate rewrites aligned with sparse and dense retrievers (Gao et al., 2023; Li et al., 2026). Goyal et al. (2026) examine a related but different concern: sensitivity to document features that should not determine relevance. Retriever compatibility and resistance to bias must therefore be distinguished. A query can fit a scoring model well while remaining vulnerable to that model’s undesirable preferences.

A useful diagnosis holds the information need and corpus fixed while comparing representations, retrievers and controlled document changes. The available evidence supports retriever-aware reformulation in tested settings, not a universal claim that one representation must fail across all retrievers. Mismatch may cause the missing-evidence outcome in Section 5.2.4, but the outcome alone does not establish mismatch as its cause.

### 5.2.4 Missing Relevant Evidence

This category applies when evidence required to answer the question exists in the searchable index but does not enter the candidate set. Finding a relevant document is insufficient if the answer-bearing page, passage or relation is missing. For a comparison question, retrieving evidence about only one of the compared entities leaves an information requirement unmet even if all returned passages are topically relevant.

Kobeissi and Langlais (2026) examine this distinction across document, page and chunk retrieval in financial question answering. RAGChecker’s claim recall provides a complementary way to ask how much of the reference answer is supported by retrieved material (Ru et al., 2024). These studies motivate evaluating coverage at the granularity needed to justify the answer, rather than relying on document-level relevance alone.

The analyst should first establish that the evidence was available in the index. If it was absent from the source or damaged by chunking, the primary problem is upstream. If it entered the candidate set but was later excluded, the relevant selection failure belongs to Section 5.2.6. Candidate expansion or further search can address missed evidence, but simply increasing the number of results may add redundancy without recovering the absent fact. Reference annotations also require scrutiny because incomplete labels can miss valid alternative evidence.

### 5.2.5 Irrelevant Retrieved Passages

This category concerns material admitted to the retrieved evidence that does not help answer the intended question. A passage can share the correct topic while concerning the wrong entity, period or applicable condition. Such passages consume a limited evidence budget and may distract the generator or invite transfer of a fact to an inappropriate setting. Irrelevance is relative to the question; it is not equivalent to factual falsity.

RGB examines noise robustness separately from information integration, negative rejection and counterfactual robustness (Chen et al., 2024). RAGChecker distinguishes context precision from claim recall, while DRUID questions whether synthetic evidence conditions adequately represent naturally retrieved material (Ru et al., 2024; Hagström et al., 2025). These distinctions caution against treating every low-precision result as equally harmful or every apparently relevant passage as safe to use.

Diagnosis should inspect both what was included and whether it affected the answer. Filtering may remove distractors, but aggressive filtering can also discard weak-looking bridge evidence needed for a multi-hop answer. The failure category records unwanted evidence inclusion; identifying ranking as its cause requires a separate comparison with the available candidates. Contradictory sources are not automatically irrelevant: they may be directly relevant and require downstream conflict handling rather than deletion.

### 5.2.6 Ranking and Evidence Selection Failures

Ranking and selection fail when the available candidates contain necessary evidence but the ordering, cutoff or set-selection decision does not preserve it for generation. A scoring model may place an answer-bearing passage below the cutoff. Alternatively, the top-ranked passages may repeat the same fact while omitting a complementary fact already present in the pool.

SetR explicitly treats passage selection as a joint decision over information requirements (Lee et al., 2025). Ammann et al. (2025) distinguish question decomposition, reranking and their combination. These approaches show why candidate acquisition and selection should not be collapsed into a single label. They also motivate examining the final set rather than only the first relevant result’s position.

The diagnostic comparison is between candidate coverage and selected-set coverage under a stated budget. If the needed passage never entered the pool, reranking alone cannot repair the problem. If it was selected but subsequently removed during compression or prompt truncation, the failure lies at the next stage. Reranking and complementary selection are therefore appropriate mitigation targets only after the location of the loss has been established.

### 5.2.7 Multi-Hop Retrieval Failures

Multi-hop retrieval fails when the system does not obtain and preserve the connected evidence required across several information needs. A later query may omit a bridge entity, use an incorrect intermediate answer or retrieve one branch of a comparison while neglecting another. The distinctive mechanism is failure to maintain dependencies, rather than merely conducting more than one search.

MultiHop-RAG supplies questions and supporting evidence for assessing this problem (Tang and Yang, 2024). ChainRAG examines missing entities in later subquestions, and Q-DREAM combines decomposition with dependency optimisation and dynamic retrieval (Zhu et al., 2025; Ye et al., 2025). Their results support analysing how intermediate results shape later searches. FLARE addresses repeated retrieval during generation, but repeated retrieval and multi-hop reasoning are not synonymous (Jiang et al., 2023).

A useful record includes each subquestion, its evidence, the intermediate entity or claim passed forward and the stopping decision. This makes it possible to distinguish an incomplete chain from a wrong but internally coherent one. Dependency-aware reformulation and further retrieval can help, but extra rounds also create opportunities to propagate an earlier mistake. This category can coexist with query drift, mismatch or selection failure; it identifies how such errors become linked across steps.

## 5.3 Comparison of Existing Literature

The comparisons below examine what each research design can establish about the failure categories, how proposed detection or mitigation methods differ, and where their evidence stops. Results are interpreted within their original experimental settings. The four-part structure separates reported findings from this review’s analysis and current judgement.

### 5.3.1 Query Reformulation and Supervision

#### Paper comparison

Ma et al. (2023) make the search query an adaptable component between a user request and frozen retrieval and reading modules. Their Rewrite-Retrieve-Read framework trains a small rewriter using feedback from the reader, with improvements on open-domain and multiple-choice question answering. Chan et al. (2024), in RQ-RAG, instead teach explicit rewriting, decomposition and disambiguation. Their distinction matters: resolving an omitted referent, separating several evidence requirements and choosing an interpretation are different operations, although each changes the text submitted for retrieval.

Wang et al. (2025) and Cao et al. (2026) ask what should supervise that change. MaFeRw combines feedback associated with query–gold-document similarity, retrieval ranking and answer ROUGE, as well as rewrite ROUGE against manual rewrites. Its implementation therefore contains four reward components, rather than only the three aspects emphasised in the abstract. MSPA-CQR constructs preferences from consistency across candidate rewrites, retrieved passages and generated responses, then uses prefix-guided preference optimisation. MaFeRw relies on labelled reference information for its rewards; MSPA-CQR reduces this dependence through self-consistency. These are different supervision assumptions, not interchangeable forms of downstream feedback.

Zhou and Lin (2026) add a deployment-oriented perspective through UTRAG. Their SemEval system combines history-aware rewriting with a LoRA-adapted generator. It reports retrieval nDCG@5 of 0.4855 in Subtask A and discusses cumulative history-selection and query-formulation errors as conversations lengthen. Its end-to-end results concern a combined system, so they cannot all be attributed to rewriting alone.

#### Analysis

The shared problem is loss of the intended retrieval target. A fluent standalone question can still discard a date restriction, resolve a pronoun to the wrong entity or import a mistaken assumption from conversation history. The relevant test is therefore whether the reformulation preserves the information need while making its missing context explicit. Readability is useful but does not establish this property.

The papers also expose a supervision dilemma. Final-answer rewards connect rewriting to its practical purpose, but they can be sparse and depend on the reader’s existing knowledge. More local rewards provide additional guidance, yet query similarity and ranking remain proxies for evidential support. Self-consistency removes some annotation requirements but introduces another assumption: frequently repeated interpretations are more useful. Several candidates can agree on the same incorrect referent. This is a limitation of consistency as evidence of truth, not a demonstrated failure rate of MSPA-CQR.

A useful comparison is therefore not “which rewriter has the highest score?” but “which requirement does the training signal protect?” Rewrite supervision can protect explicitness, retrieval supervision can favour discoverability, and answer supervision can favour task performance. None alone guarantees preservation of all user constraints. The synthesis suggests evaluating those constraints separately, particularly negation, time, entity identity and the relation being requested. This proposed diagnostic would distinguish a retrieval-compatible paraphrase from a rewrite that succeeds by answering a different question.

#### Current conclusion

Query reformulation should be assessed as a constrained transformation of the information need. The evidence supports its usefulness, but not an unconditional rule that every question should be expanded or rewritten. A defensible claim is that task-aware feedback can improve performance in the tested pipelines; demonstrating fewer hallucinations additionally requires evidence-level or claim-level evaluation of the resulting answers.

#### Evidence reviewed

Ma et al. (2023): reader-guided query adaptation and downstream QA experiments. Chan et al. (2024): explicit refinement operations and single-hop and multi-hop evaluation. Wang et al. (2025): reward construction, training stability and conversational RAG results. Cao et al. (2026): preference construction, retrieval experiments, ablations and Appendix G.10 answer evaluation, which uses ROUGE and BERTScore rather than a direct hallucination measure. Zhou and Lin (2026): shared-task results and analysis of multi-turn drift. These studies support different parts of the mechanism; their scores do not form a common comparative leaderboard.


### 5.3.2 Retriever Alignment and Bias

#### Paper comparison

Gao et al. (2023) address zero-shot dense retrieval with Hypothetical Document Embeddings (HyDE). A language model generates a hypothetical relevant document; an encoder uses it to locate real corpus documents. The generated text is a retrieval representation, not verified evidence. HyDE improves over the unsupervised Contriever baseline across the reported tasks and languages, supporting the value of changing the representation used for matching.

Li et al. (2026) make retriever dependence explicit in DVCQR. A single generation produces a sparse-oriented rewrite with distinctive lexical anchors and a dense-oriented rewrite carrying semantic constraints. Stage-wise reinforcement learning aligns these views with their respective retrievers. In Table 1, using the same Qwen2.5-3B backbone as ConvSearch-R1, TopiOCQA MRR rises from 35.2 to 37.4 under BM25 and from 51.4 to 52.5 under ANCE. These are gains of 2.2 and 1.1 points on the paper’s reported scale, not hallucination reductions. Results also include QReCC and cross-dataset CAsT evaluation, with exceptions to uniform improvement.

Goyal et al. (2026) examine a different question: whether rewriting reduces sensitivity to document features that should not drive retrieval. Across five enhancement methods and six retrievers, their controlled bias study reports approximately 54% aggregate bias reduction for simple rewriting. However, compounded adversarial conditions reveal weaker robustness. Their analysis distinguishes reduced normalised bias scores from reduced correlation with bias-inducing features; the two need not coincide.

#### Analysis

DVCQR and Goyal et al. should not be read as contradictory. A representation can be better aligned with a scoring system and still exploit, or remain vulnerable to, undesirable scoring behaviour. Alignment asks whether the query works with the retriever. Bias evaluation asks whether ranking changes for inappropriate reasons. An improvement in one objective does not establish an improvement in the other.

HyDE further shows why generated falsehoods need to be located precisely in the pipeline. A hypothetical passage may include inaccurate details and still act as a useful search representation. It becomes a different reliability problem if those details are treated as source evidence or steer retrieval away from the intended entity. Thus, the existence of invented intermediate text does not by itself demonstrate a hallucinated final answer, while retrieval gains do not prove the intermediate representation harmless.

The scope of the bias evidence also matters. Goyal et al. use controlled document pairs and do not establish the prevalence of each bias in naturally occurring RAG traffic. Their limitations exclude generalisation to sparse and hybrid retrieval without further testing. Likewise, DVCQR’s BM25 and ANCE experiments justify retriever-aware design in those settings, not the impossibility of a useful unified rewrite for every future retriever.

These comparisons refine the diagnosis of query–document mismatch. Some failures concern missing language or entity information; others concern the geometry or feature preferences of the matching model. Repeatedly rewriting a semantically adequate query may therefore target the wrong component. A stronger diagnostic would hold the information need constant while varying query form, retriever and controlled document features, then inspect which evidence changes.

#### Current conclusion

Query quality is conditional on the retrieval mechanism. The literature supports separating semantic fidelity, retriever compatibility and robustness to spurious document features. Query-side interventions can improve retrieval, but some document-encoding vulnerabilities are unlikely to disappear through rewriting alone. A faithful query that retrieves poorly therefore warrants inspection of the scoring mechanism as well as the query text.

#### Evidence reviewed

Gao et al. (2023): HyDE’s generation–encoding–retrieval design and zero-shot retrieval evaluation. Li et al. (2026): Tables 1–3, retriever-specific outputs and staged alignment. Goyal et al. (2026): controlled bias measures, adversarial evaluation, feature-score analysis and stated scope limitations. These are primarily retrieval-mechanism studies; none of the numerical results quoted here measures the rate of unsupported final claims.


### 5.3.3 Evidence Coverage and Diagnostic Granularity

#### Paper comparison

Ru et al. (2024) provide a useful diagnostic distinction in RAGChecker. Claim recall measures the proportion of reference-answer claims supported by retrieved chunks. Context precision measures the proportion of retrieved chunks that support at least one reference claim. The units differ deliberately: a chunk may count as relevant while containing substantial irrelevant material. High context precision therefore does not mean that every sentence in the context is useful.

Kobeissi and Langlais (2026) examine a related failure hidden by document-level evaluation. On a 150-question FinanceBench subset, they compare retrieval at document, page and chunk levels and use oracle conditions to estimate remaining headroom. Retrieving the correct financial filing can still miss the particular page or passage needed for the answer. Their page-then-chunk approach uses a fine-tuned page scorer; document-separated cross-validation is reported to reduce leakage. This is valuable domain-specific evidence, though its scale and financial setting constrain generalisation.

Leung et al. (2026) distinguish chunking, retrieval, reranking and generation errors in a practical taxonomy. Their treatment of overchunking shows why a fragment lacking its referent or qualifying information should not automatically be labelled a search failure. Conversely, intact evidence in the index that is absent from the candidate pool is a retrieval problem. The taxonomy allows errors to co-occur rather than forcing every response into a single mutually exclusive cause.

#### Analysis

These papers challenge a loose use of “missing relevant evidence.” At least three states must be separated: the source never contained the information; the indexed representation failed to preserve it; or an adequate representation existed but the retrieval process did not return it. Only the third clearly belongs to search under the boundary of this review. A fourth state arises when retrieval returns the evidence but subsequent selection removes it, which is considered in Section 5.2.6.

Granularity changes the apparent success of a system. Document recall may reward retrieving the right report even if a crucial numerical value lies hundreds of pages away. Passage recall is more informative, but a passage containing a target term may omit the reporting year, unit or comparison baseline. A claim-level measure can identify some of these omissions, provided the reference answer specifies them. Reference incompleteness, however, can make legitimate alternative evidence appear irrelevant or leave required reasoning facts unevaluated.

Coverage and precision also describe different failure costs. Low coverage leaves an answer requirement unsupported. Low precision consumes context budget and may introduce distractions, but its downstream effect depends on whether the reader can ignore them. It follows that increasing the number of returned chunks is not a complete repair strategy. Additional chunks must contribute missing information rather than repeat material already found. The practical quantity of interest is the marginal evidential contribution of another retrieval result.

A concrete diagnostic follows from this synthesis: inspect evidence survival at successive boundaries. Was the required fact in the source, preserved in an indexed unit, returned among candidates, selected for generation and retained in the actual prompt? Comparing these states is more informative than deciding retrospectively that a wrong answer “must have had bad retrieval.” It also allows oracle experiments to target the boundary where information was lost.

#### Current conclusion

Retrieval coverage should be evaluated at the granularity required to justify the answer. Correct-document retrieval is insufficient evidence of successful grounding, and context precision is not equivalent to semantic cleanliness. The strongest supported diagnosis combines coverage measurements with inspection of where required facts disappear. The financial study supplies a specific instance of this problem rather than a universal estimate of its frequency.

#### Evidence reviewed

Ru et al. (2024): Section 3.3.2 metric definitions and component-level evaluation. Kobeissi and Langlais (2026): multi-granularity experiments, oracle analysis and page scorer evaluation. Leung et al. (2026): stage-specific taxonomy and examples of fragmented evidence. Together these sources support distinguishing unavailable, damaged and unretrieved evidence, while leaving corpus quality and index construction as adjacent causes rather than absorbing them into retrieval.


### 5.3.4 Ranking and Evidence Set Selection

#### Paper comparison

Lee et al. (2025) formulate passage selection as a set-level problem in SetR. The model identifies a question’s information requirements and selects passages that jointly address them. In Table 2 on MultiHopRAG, SetR with chain-of-thought and information requirement identification obtains Prec@5 of 0.2268 and Recall@5 of 0.3669, compared with 0.1799 and 0.3601 for RankGPT using GPT-4o. However, its MRR@10 is lower: 0.5742 versus 0.6358. The paper also reports end-to-end QA gains and controlled comparisons sharing the backbone, training data and teacher supervision. The evidence supports a distinction between ranking quality and set utility, not universal superiority on every retrieval metric.

Ammann et al. (2025) broaden the candidate pool through question decomposition and then rerank it. Their MultiHop-RAG results give MRR@10 of 0.464 for naive RAG, 0.498 for decomposition alone, 0.574 for reranking alone and 0.635 for the combination. The approximately 36.9% relative increase calculated from the displayed rounded endpoints is close to the abstract’s 36.7%; the absolute increase is 0.171. The reranking-only comparison shows that attributing the full gain to decomposition would be incorrect.

SetR changes how candidates are selected; Ammann et al. change both candidate acquisition and subsequent prioritisation. Neither intervention should be interpreted as a generic demonstration that more passages produce better evidence.

#### Analysis

Ranking and set selection optimise related but non-identical objects. A ranking can place a highly relevant passage first and still fill the remaining positions with duplicates. A set can have slightly weaker individual rankings while covering all facts required for a comparison. For example, an illustrative question asking which of two organisations changed its policy first requires a date for each organisation. Several strong passages about one organisation cannot substitute for the missing date of the other. This is an analytical example, not a benchmark observation.

Set selection remains bounded by the candidate pool. If a necessary fact is absent, reordering or selecting existing passages cannot recover it. This separates two remedies that are often conflated: search again to improve candidate coverage, or select better to preserve complementarity already present. A selector that identifies an unmet information requirement could supply a targeted follow-up query, but that proposed combination is not an experimentally established result of SetR alone.

The apparent disagreement between SetR’s MRR and precision results is therefore informative. MRR rewards the rank of the first relevant result; it does not certify that every requirement is supported. Precision and recall improve the diagnosis but still depend on which passages count as gold evidence. None directly proves logical sufficiency when the answer requires relationships, temporal constraints or arithmetic across documents.

Ammann et al. also illustrate the importance of component controls. Their combined pipeline improves over either module alone, but the improvement over naive RAG includes two interventions. Comparing only the best system with the weakest baseline would conceal their relative contributions. Their retained original query and merged retrieval pool also differ from replacing the question with one rewritten query. These design choices change both coverage and noise.

#### Current conclusion

A retrieval stage should deliver an evidence set that covers the question’s distinct requirements within its budget. Ranking remains useful, but rank-based metrics should be supplemented by coverage, redundancy and set-sufficiency assessment. Candidate-pool failure and selection failure require different remedies; a well-designed selector cannot compensate for evidence it never receives.

#### Evidence reviewed

Lee et al. (2025): set-selection formulation, retrieval Table 2, end-to-end evaluation and matched-setting ablations. Ammann et al. (2025): pipeline design and Table 1 decomposition/reranking controls. Numerical comparisons are within each paper; they are not cross-paper rankings because retrieval configurations, generators and evaluation protocols differ.


### 5.3.5 Multi-Hop Dependencies and Iterative Retrieval

#### Paper comparison

Tang and Yang (2024) introduce MultiHop-RAG with a news-based knowledge base, multi-hop questions, reference answers and supporting evidence. Their separate retrieval and answer experiments expose difficulty in collecting and using multiple evidence pieces. This establishes a benchmarked problem, whereas intervention papers test specific ways of addressing it.

Zhu et al. (2025) identify a narrower mechanism in ChainRAG: decomposition can omit key entities needed in later subquestions. Their progressive rewriting completes those entities using earlier results. In the controlled retrieval analysis, second-subquestion Recall@2 on MuSiQue rises from 40.91% to 58.81% after entity completion. The authors match chunk size for this comparison, which helps distinguish rewriting effects from sentence-versus-chunk granularity. The full system additionally uses a sentence graph, so its end-to-end gains cannot be assigned solely to entity completion.

Ye et al. (2025) combine question decomposition, dependency optimisation and dynamic passage retrieval in Q-DREAM. Their 2WikiMQA ablation is particularly instructive: F1 is 62.1 for the full method, 56.5 without the dynamic retrieval module, 38.1 without both dependency optimisation and dynamic retrieval, and 44.7 with all three modules removed. Unassisted decomposition can therefore underperform direct retrieval within this setup. The method addresses dependency specification and semantic matching together.

Jiang et al. (2023) use a different retrieval schedule in FLARE. Predicted upcoming sentences guide searches, and low-confidence tokens trigger retrieval and regeneration. This targets information needs emerging during long-form generation rather than requiring all subquestions to be known in advance. Chan et al. (2024) similarly broaden refinement beyond a fixed initial query, but their learned refinement operations should not be equated with FLARE’s confidence-based retrieval trigger.

#### Analysis

Multi-hop retrieval introduces a state-dependence problem. After the first search, later queries may depend on an entity or fact that was previously unknown. A wrong intermediate answer can redirect the search to a plausible but irrelevant branch. The final evidence set may then look coherent while supporting the wrong trajectory. Conversely, independently decomposing every subquestion before identifying the bridge entity may leave later searches underspecified.

ChainRAG and Q-DREAM provide complementary evidence for this diagnosis. The former tests restoration of missing entity information; the latter shows that decomposition without dependency handling can be harmful. The implication is not that decomposition is inherently unreliable, but that an intervention must preserve the links between information requirements. Counting subquestions or retrieval calls does not measure whether those links are correct.

There is also a distinction between multi-hop and iterative retrieval. A comparison question can require multiple independent facts retrieved in parallel. A bridge question may require a sequential update. FLARE can retrieve repeatedly even for long-form tasks without an explicit multi-hop question. These systems share a need to manage evolving information requirements, but they should not be combined into a single claim that additional retrieval rounds always help.

Ammann et al. (2025) provide a caution about answer-level evaluation: on HotpotQA, the combined pipeline improves answer F1 from 31.3 to 35.0, but its reported supporting-fact F1 is 11.2, below reranking alone at 12.9. Better answer scores therefore need not indicate uniform improvement in evidence identification. Their analysis also shows subquestion counts largely following the prompt’s budget rather than gold evidence counts. Decomposition output length is consequently weak evidence of reasoning completeness.

A useful future comparison would track the identity and provenance of each intermediate fact, measure complete-chain recovery and distinguish stopping because the evidence is sufficient from stopping because a fixed budget is exhausted. These are evaluation proposals arising from the review, not results already demonstrated across the papers.

#### Current conclusion

Multi-hop reliability depends on maintaining correct dependencies across searches. Evidence supports entity completion and dependency-aware refinement, while also showing that decomposition can fail without them. The relevant object is the retrieval trajectory and its accumulated support, not simply the quality of each isolated search or the final answer score.

#### Evidence reviewed

Tang and Yang (2024): multi-hop benchmark and separate retrieval/generation experiments. Zhu et al. (2025): Section 4.4 and Table 2 entity-completion analysis. Ye et al. (2025): Table 2 ablations and dynamic retrieval design. Jiang et al. (2023): FLARE’s retrieval trigger and long-form task evaluation. Chan et al. (2024): learned refinement operations. Ammann et al. (2025): HotpotQA Table 2 and decomposition-budget analysis. These settings establish related mechanisms rather than a controlled comparison of all six systems.


### 5.3.6 Evaluation of Evidence Sufficiency and Hallucination

#### Paper comparison

Lewis et al. (2020) establish the foundational combination of parametric generation and non-parametric retrieval, reporting gains on knowledge-intensive tasks. That result motivates external grounding but does not imply that retrieved evidence is sufficient or that generated claims faithfully use it. Niu et al. (2024) make the remaining output problem observable through RAGTruth, with nearly 18,000 generated responses and manual case-level and word-level hallucination annotations. Its focus is unsupported or contradictory output relative to supplied material, not causal identification of which earlier component failed.

Chen et al. (2024) use RGB to separate noise robustness, negative rejection, information integration and counterfactual robustness. Their English and Chinese testbeds show that the ability to tolerate some irrelevant material does not imply reliable rejection when evidence is inadequate or reliable treatment of false information. Joren et al. (2025) instead stratify performance by whether context contains enough information to answer. The tested stronger models generally perform well with sufficient context but often answer incorrectly when it is insufficient; weaker models can fail even with sufficient context. Sufficiency-guided selective generation improves correctness among answered cases, a quantity that must be interpreted alongside response coverage.

Hagström et al. (2025) question the realism of context-utilisation evaluation itself. DRUID uses real retrieved evidence for claim verification and compares it with synthetic settings. The study finds that artificial context characteristics can inflate utilisation estimates. Thus, controlled perturbations and naturally retrieved contexts answer different questions about robustness and practical behaviour.

#### Analysis

Three properties must remain separate: whether the evidence contains enough information, whether the answer is supported by that evidence, and whether the answer is factually correct. An answer can be correct from the model’s memory yet unsupported by the provided context. It can faithfully repeat an incorrect source. It can also be wrong despite sufficient correct evidence because of reasoning or extraction failure. Collapsing these outcomes into one accuracy or hallucination label loses the distinction the review is trying to explain.

Sufficiency is more demanding than relevance, but insufficient context does not identify a unique upstream cause. The fact may be absent from the corpus, lost during chunking, missed in search, removed by reranking or omitted during context construction. Joren et al.’s distinction should therefore be used to diagnose the evidence–generation boundary, not automatically relabel all insufficient contexts as retriever failures.

RAGChecker and Leung et al. offer complementary ways to investigate this boundary. The former measures retrieval and generation properties separately; the latter seeks stage and error-type attribution. Leung et al.’s automatic classification still disagrees with human labels, as shown in its stage agreement matrix. A taxonomy is therefore an operational diagnostic aid rather than ground truth about causality. Pipeline traces and controlled interventions are needed when several plausible causes coexist.

DRUID adds an external-validity constraint: the frequency and combinations of misleading, incomplete and difficult evidence in real retrieval may differ from a synthetic stress test. Controlled experiments isolate mechanisms; natural retrieval studies test whether those mechanisms explain realistic outcomes. A persuasive review needs both without treating their numerical results as directly comparable.

#### Current conclusion

Retrieval failure and hallucination are related but distinct. Query and retrieval interventions can improve the availability of supporting evidence; whether that evidence yields a grounded answer additionally depends on context preservation, evidence utilisation and abstention. “Better retrieval is necessary” is too absolute for every individual response, since a model can answer correctly from memory or safely decline. For tasks requiring externally justified answers, however, access to adequate evidence remains a central requirement.

#### Evidence reviewed

Lewis et al. (2020): foundational retrieval-conditioned generation. Niu et al. (2024): RAGTruth’s annotation target and naturally generated outputs. Chen et al. (2024): RGB’s four capability testbeds. Joren et al. (2025): sufficiency-stratified errors and selective generation. Hagström et al. (2025): real-versus-synthetic context comparison. Ru et al. (2024) and Leung et al. (2026): complementary component diagnostics. These sources support cross-stage distinctions more strongly than they support any universal numerical mapping from recall gains to hallucination reduction.


## 5.4 Cross-Stage Effects and Hallucination Manifestations

The taxonomy describes failures in obtaining evidence. Hallucination describes properties of the resulting response, so a causal account must also explain what happens between these two points. The following pathways are a synthesis of the reviewed mechanisms and evaluation studies, not observed frequencies or mutually exclusive outcome classes.

### 5.4.1 From Missing Evidence to Unsupported Completion

An unresolved query, matching failure or incomplete retrieval chain may leave the context without a necessary fact. The generator can then decline to answer, give a qualified partial answer or fill the gap using parametric knowledge or an unsupported inference. Only the latter behaviours can produce the unsupported-completion pathway; evidence absence does not force hallucination.

Joren et al. (2025) show why evidence sufficiency should be assessed separately from response correctness. RGB tests whether a system rejects questions it cannot answer from the supplied information, while RAGTruth annotates unsupported or contradictory output (Chen et al., 2024; Niu et al., 2024). Together these studies support evaluating the evidence deficit and the response to that deficit as two distinct events. A factually correct answer recalled from model memory may still lack the external justification required by the task.

### 5.4.2 From Distractors to Misleading or Incorrectly Attributed Claims

A passage about the wrong entity or period may be used as though it answered the original question. In this pathway, the retrieved text need not be false: the error is applying it outside its supported scope. Query drift and irrelevant-passage inclusion can create this opportunity, while the generator’s evidence use determines whether it becomes an incorrect assertion.

An associated attribution risk arises when a retrieved source is attached to a claim it does not support. Retrieval can supply unsuitable material, but citation selection and placement occur downstream. The reviewed retrieval studies do not establish a citation-specific error rate, so this pathway should be treated as a mechanism to investigate rather than a quantitatively demonstrated effect. Likewise, disagreement between two relevant sources belongs to cross-source conflict handling; discarding one as “irrelevant” without analysis could hide the real problem.

### 5.4.3 From Partial Evidence to Incomplete or Contradictory Synthesis

Ranking and selection may retain individually plausible passages while omitting qualifications or a necessary complementary fact. A generator may then produce an overgeneralised conclusion, infer a comparison from only one side or combine intermediate claims whose dependencies were never established. SetR and the multi-hop studies explain why single-passage relevance is not sufficient for these tasks, while RGB and RAGChecker provide ways to examine integration and output support.

The handoff to context construction must nevertheless be checked. If the selected evidence was complete but compression removed a qualification, the primary loss occurred after retrieval. If sufficient evidence reached the prompt but the answer contradicted it, the remaining failure concerns utilisation or reasoning. Assigning every such error to retrieval would erase the stage boundaries that make mitigation actionable.

### 5.4.4 Conditions for Attributing a Hallucination Reduction to Retrieval

A persuasive evaluation should hold the question, corpus, generator and relevant budgets comparable, record evidence before and after selection, and measure supported and unsupported answer claims. It should report evidence sufficiency alongside response correctness, contradictions, abstention and the proportion of questions answered. Otherwise, fewer erroneous answers may reflect reduced willingness to answer rather than better evidence acquisition.

DRUID strengthens the case for including naturally retrieved evidence alongside controlled perturbations (Hagström et al., 2025). Controlled experiments help isolate a mechanism; realistic retrieval tests whether it remains important when incomplete, distracting and misleading material coexist. Leung et al. (2026) further show why automatic stage attribution should be treated as a diagnostic aid rather than unquestionable causal ground truth. These requirements are this review’s proposed evaluation standard, not a claim that all 22 papers already meet it.

## 5.5 Section Conclusion

Query and retrieval contribute to hallucination risk by changing what information is searched for, what evidence is recovered and what evidence survives selection. The seven categories distinguish unresolved information needs, harmful transformations, representation mismatch, missing candidates, unwanted passages, defective ranking or selection, and dependency failures across searches. Their relationships should remain explicit: one mechanism can produce several outcomes, and several mechanisms can contribute to one failed response.

The reviewed literature supports targeted mitigation more strongly than a general claim that “better retrieval eliminates hallucination.” Query refinement can improve expression and retriever compatibility; candidate expansion can increase coverage; reranking and set selection can preserve useful evidence; dependency-aware retrieval can repair incomplete search trajectories. Each remedy has a boundary. Rewriting cannot retrieve facts absent from the corpus, selection cannot recover candidates it never receives, and sufficient context cannot guarantee faithful generation.

The strongest grounds for these conclusions are component comparisons and diagnostic distinctions. SetR’s differing precision and MRR results show that retrieval metrics can prefer different systems. Ammann et al.’s controls separate decomposition from reranking, while ChainRAG and Q-DREAM expose the importance of intermediate entities and dependency handling. RAGTruth, RGB, RAGChecker, Sufficient Context, DRUID and Leung et al.’s taxonomy constrain what can be inferred about output reliability from those retrieval gains. Because the tasks, corpora, models and evaluation protocols differ, the reported scores should not be combined into a cross-paper leaderboard or pooled effect size.

Three open questions follow. First, can systems identify which information requirements remain unsupported before generation, while distinguishing corpus absence from retrieval and selection failures? Second, which retrieval interventions reduce unsupported or contradictory claims when the generator, retrieval budget and answering coverage are held comparable? Third, how well do these findings transfer to naturally occurring queries with ambiguous entities, temporal constraints and multi-hop dependencies in high-stakes domains?

The financial retrieval study provides a domain-specific example of why the right document is not enough, but its limited evaluation does not establish readiness for financial, clinical or legal deployment. Such applications need domain-specific evidence of coverage, applicability, provenance and appropriate refusal, together with review procedures proportionate to the consequences of error. This is a research implication of the stage analysis, not a deployment claim made on behalf of the reviewed papers.

The resulting position is that query and retrieval quality should be judged by whether the system obtains a collectively adequate evidence set for the intended question. Demonstrating reduced hallucination additionally requires showing that the downstream answer stays within what that evidence supports.

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
