# RAG Hallucination Taxonomy

An interactive research atlas for exploring our team's work on hallucination in retrieval-augmented generation (RAG).

**[Open the research website](https://sierrali3888.github.io/rag-hallucination-taxonomy/)**

The homepage displays a connected mind map: one central topic branches into six research directions, then into each contributor’s headings. Select a direction to expand its branches, then select a chapter or research note. One direction is expanded at a time; its content appears in the reading panel beside the map. Short map labels keep the diagram readable, while the reading panel preserves the full source headings. Use All directions to return to the overview, or zoom and drag to explore. Subcategories, evidence, comparisons, analysis, and conclusions are left for each contributor to develop. Empty sections are placeholders, not completed findings.

## Team responsibilities

| Direction | Research area | Contributor | Content file |
| --- | --- | --- | --- |
| 1 | Conflict Hallucination |  | [conflict-hallucination.md](content/conflict-hallucination.md) |
| 2 | Unsupported / Baseless Hallucination |  | [unsupported-baseless-hallucination.md](content/unsupported-baseless-hallucination.md) |
| 3 | Knowledge Source & Indexing | Peiqi Guo | [knowledge-source-indexing.md](content/knowledge-source-indexing.md) |
| 4 | Query & Retrieval | Zhixuan Li | [query-retrieval.md](content/query-retrieval.md) |
| 5 | Post-Retrieval / Context Construction | Xuefeng Lu | [post-retrieval-context-construction.md](content/post-retrieval-context-construction.md) |
| 6 | Generation & Knowledge Utilisation | Yanzhang Xie | [generation-knowledge-utilisation.md](content/generation-knowledge-utilisation.md) |

The six branches organise team responsibilities. Their placement does not imply a causal sequence or a final classification. The contributor fields for Directions 1 and 2 are intentionally blank.

## How to contribute without writing code

1. Open your research page on the website and select **Edit on GitHub**, or open your content file from the table above and click the pencil icon. Sign in to your GitHub account if prompted.
2. Check the `Owner:` line and update `Status:` as appropriate: `Not started`, `In progress`, or `Ready for review`. Keep both lines and the blank line after them.
3. Replace the “To be completed…” prompts with your research. The eight template sections are a starting point. Add or edit `##`, `###`, and `####` headings to create branches automatically; ordinary paragraphs update node content. Empty template sections remain hidden from the map. Direction 4 follows the agreed Section 4 structure: five main sections, seven failure mechanisms under Section 4.2, and a separate References section. Each mechanism branches into Paper comparison, Analysis, Current conclusion, and Evidence reviewed.
4. Select **Commit changes…**, describe your contribution, and choose **Create a new branch for this commit and start a pull request**. Ask a teammate to review the proposed changes.
5. After the checks pass and the pull request is merged into `main`, GitHub automatically updates the website. Allow a few minutes, then refresh your research page.

Edit your assigned file to reduce conflicts. Each file's `Owner:` value is displayed on both the homepage and its research page, so contributors do not need to edit frontend code to update their names.

### Research outcome template

The blank contributor templates contain these eight sections:

- Overview / Definition
- Subcategories or Failure Modes
- Evidence Reviewed
- Cross-paper Comparison
- Analysis / Synthesis
- Current Conclusion
- Detection & Mitigation, if applicable
- References

Direction 4 uses `Layout: stage-review` in its metadata. Preserve its agreed Section 4 headings and seven failure mechanisms. The `####` research-note headings under each mechanism create another clickable level. Other contributors can develop their own heading structure from the blank templates.

### Automatic mind-map branches

Each contributor edits only their own file in `content/`. No frontend or diagram configuration changes are needed.

| What you write | What appears on the website |
| --- | --- |
| `## Topic` | A branch below your assigned research direction |
| `### Subtopic` | A child of the preceding `##` topic |
| `#### Paper comparison` | A child of the preceding `###` subtopic |
| `##### Detail` / `###### Further detail` | Further nested branches |
| Paragraphs, bullet lists, tables, or citations | Content in the selected node's reading panel |
| `**Bold text**` | Emphasis within the content, not a new branch |

Put each heading on its own line, with a space after the `#` characters and a blank line before the content. Use successive heading levels to express parent–child relationships. A new heading creates a branch even before you add its body text. Untouched template sections containing only “To be completed…” stay hidden; replacing that prompt with your content makes the section appear.

Copy this example into your assigned file and replace the illustrative text:

```markdown
## Your research topic

A concise overview of this topic.

### Your failure mechanism

A concise definition of this mechanism.

#### Paper comparison

Your comparison of the reviewed papers.

#### Analysis

Your synthesis and supporting evidence.

#### Current conclusion

Your current conclusion and remaining uncertainty.

#### Evidence reviewed

The studies supporting this mechanism, with citation numbers.

## References

1. Author. Paper title. Year. Link.
```

This creates **your direction → research topic → failure mechanism → four research-note branches**, plus a separate References branch. Click a node with **+** to expand its children; click it again to collapse. Selecting a node opens its text in the right-hand panel. New branches appear after the change reaches `main` and the **Validate and deploy GitHub Pages** workflow succeeds. A saved draft or an unmerged pull request does not update the live website.

If a branch is missing, check that its title uses a heading marker rather than bold text, expand its parent, and check the latest deployment under **Actions**. Refresh the website after deployment.

Keep `Owner:` and `Status:` at the top of each file, followed by a blank line; preserve `Layout:` if present. Images can be stored in `assets/` and linked using `assets/filename`.

## Giving teammates editing access

The repository owner can invite teammates through **Settings → Collaborators → Add people**. Each teammate needs a GitHub account and must accept the invitation before editing the repository.

Collaborators have write access to the repository as a whole; the assignment table is a team agreement, not a restriction on individual files. Review changes before merging them into `main`.

## GitHub Pages deployment

This project is deployed at:

https://sierrali3888.github.io/rag-hallucination-taxonomy/

The workflow in `.github/workflows/pages.yml` builds and checks pull requests. Successful builds on `main` are deployed to GitHub Pages. Deployment also generates the GitHub editing links for the current repository.

For a new copy of this project:

1. Create a GitHub repository with `main` as the default branch.
2. Put this project's source files at the repository root, including `.github/workflows/pages.yml`. Do not upload `.venv/` or the generated `dist/` directory.
3. Under **Settings → Pages → Build and deployment → Source**, select **GitHub Actions**.
4. Under **Actions**, select **Validate and deploy GitHub Pages** and choose **Run workflow**, or push a change to `main`.
5. Find the published URL in the deployment result or **Settings → Pages**.

Repository and Pages availability depend on the account plan and organisation policies. See GitHub's [custom Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Local preview for maintainers

Requires Python 3.12 or newer:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/check.py
python -m http.server 8765 --directory dist
```

Open `http://localhost:8765`. After editing Markdown, run the build again and refresh the page. You can also open the generated `dist/index.html` directly in a browser. The published site requires no database or runtime dependencies, and relative links support project-based GitHub Pages URLs.

## Project structure

```text
content/                    Six contributor files and the research direction list
assets/style.css            Shared presentation styles
assets/workbench.css        Mind-map and reading-panel styles
assets/home.js              Branch expansion and reading interaction
scripts/home.py             Builds the map from contributor headings
scripts/build.py            Generates seven static pages from Markdown
scripts/check.py            Checks local links, anchors, and required sections
.github/workflows/pages.yml  Pull request checks and automatic deployment
requirements.txt            Pinned build dependency
```

Research content is maintained as trusted repository source. Markdown supports HTML, so review contributions before merging. Visitors browse a read-only website; contributors edit through GitHub.
