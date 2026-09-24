# RAG Hallucination Taxonomy

An interactive research atlas for exploring our team's work on hallucination in retrieval-augmented generation (RAG).

**[Open the research website](https://sierrali3888.github.io/rag-hallucination-taxonomy/)**

The homepage displays a connected mind map: one central topic branches into six research directions, then into each contributor’s headings. Expand nodes with +, zoom, or drag to explore. Select a node to read its content below on the same page. Subcategories, evidence, comparisons, analysis, and conclusions are left for each contributor to develop. Empty sections are placeholders, not completed findings.

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

1. Open your research page on the website and select **Edit this research on GitHub**, or open your content file from the table above and click the pencil icon. Sign in to your GitHub account if prompted.
2. Check the `Owner:` line and update `Status:` as appropriate: `Not started`, `In progress`, or `Ready for review`. Keep both lines and the blank line after them.
3. Replace the “To be completed…” prompts with your research. The eight template sections are a starting point. Add or edit `##`, `###`, and `####` headings to create branches automatically; ordinary paragraphs update node content. Empty template sections remain hidden from the map. Direction 4 instead follows the supplied report: seven chapter headings, each containing Paper comparison, Analysis, Current conclusion, and Evidence reviewed, followed by a separate References section.
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

Direction 4 uses `Layout: report` in its metadata. Its `##` chapter headings and `###` subsection headings generate the expandable branch navigation directly. Preserve the report headings when editing this file.

### Automatic mind-map branches

Each contributor edits only their own file in `content/`:

- `## Heading` creates a branch below your research direction.
- `### Heading` creates a child branch; `#### Heading` creates the next level.
- Paragraphs, lists, and tables beneath a heading become that node’s research content.
- Empty default placeholders do not create branches. Add content or a child heading to make the section appear.
- Save or merge into `main`; the automatic deployment rebuilds the diagram from the latest files.

For example (illustrative headings only):

```markdown
## Your research topic

A concise overview of this topic.

### Paper comparison

Your comparison of the reviewed papers.

### Analysis

Your synthesis and supporting evidence.
```

Direction 4 retains the exact chapter and subsection headings of Zhixuan Li’s report. Other contributors may organise their own headings. Keep `Owner:` and `Status:` at the top of each file, followed by a blank line. Images can be stored in `assets/` and linked using `assets/filename`.

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
scripts/build.py            Generates seven static pages from Markdown
scripts/check.py            Checks local links, anchors, and required sections
.github/workflows/pages.yml  Pull request checks and automatic deployment
requirements.txt            Pinned build dependency
```

Research content is maintained as trusted repository source. Markdown supports HTML, so review contributions before merging. Visitors browse a read-only website; contributors edit through GitHub.
