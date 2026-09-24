# RAG Hallucination Taxonomy

面向老师浏览的交互式研究成果网站。主页只有六个研究方向，每个方向进入独立成果页；全部研究内容从成员 Markdown 文件生成。**没有预设任何细分类别、文献、分析或结论。**

## 六人分工

| 成员 | 研究方向 | 只需编辑 |
| --- | --- | --- |
| 1 | Conflict Hallucination | [conflict-hallucination.md](content/conflict-hallucination.md) |
| 2 | Unsupported / Baseless Hallucination | [unsupported-baseless-hallucination.md](content/unsupported-baseless-hallucination.md) |
| 3 | Knowledge Source & Indexing | [knowledge-source-indexing.md](content/knowledge-source-indexing.md) |
| 4 | Query & Retrieval | [query-retrieval.md](content/query-retrieval.md) |
| 5 | Post-Retrieval / Context Construction | [post-retrieval-context-construction.md](content/post-retrieval-context-construction.md) |
| 6 | Generation & Knowledge Utilisation | [generation-knowledge-utilisation.md](content/generation-knowledge-utilisation.md) |

Member 1–6 是占位编号，不代表已经确认的姓名。六个分支用于组织分工，不代表因果顺序或已定稿的分类体系。

## 组员怎样填写

打开自己的文件，点击 GitHub 编辑按钮：

1. 顶部 `Owner:` 填姓名；`Status:` 按实际情况写 `Not started`、`In progress` 或 `Ready for review`。请保留这两行及后面的空行。
2. 替换各节的 “To be completed…” 提示。八个 `##` 标题保持原样和顺序；正文自由填写。
3. 在 `Subcategories or Failure Modes` 下用 `###` 添加自己研究得出的子类别，用 `####` 添加下一层。网站会自动生成可点击的分支导航，点击后定位到相应内容。不要把其他七节的普通小标题误当作 taxonomy 节点。
4. 支持普通 Markdown：段落、列表、链接、引用、表格、代码块和图片。图片放到 `assets/` 并使用 `assets/文件名` 链接。
5. 创建自己的分支，如 `member-4/research-update`，提交 Pull Request。检查通过后由组内负责人合并到 `main`，网站自动更新。多人分别编辑自己的文件可以减少冲突。

八个统一区域：Overview / Definition；Subcategories or Failure Modes；Evidence Reviewed；Cross-paper Comparison；Analysis / Synthesis；Current Conclusion；Detection & Mitigation（如适用）；References。

下方仅说明 Markdown 用法，不会出现在网站中；请用自己的研究内容替换：

```markdown
### 组员自行确定的子类别标题

在这里写定义、证据、分析与结论，并链接参考文献。

#### 组员自行确定的更细节点

在这里补充相应研究成果。
```

## 首次部署到 GitHub Pages

1. 新建 GitHub 仓库，默认分支为 `main`。将**本目录内的文件**作为仓库根目录上传，必须包含隐藏的 `.github/workflows/pages.yml`，不要上传 `.venv/` 或 `dist/`。
2. 仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
3. 在 **Actions** 启用工作流，选择 `Validate and deploy GitHub Pages` → `Run workflow`。以后向 `main` 合并内容即可自动构建发布。
4. 成功后的 Pages 地址在部署结果或 Settings → Pages 中显示。常见形式为 `https://用户名.github.io/仓库名/`。
5. 在仓库 Settings → Collaborators 中邀请其他五位成员（由仓库拥有者操作）。可设置 `main` 保护规则，要求 Pull Request 和构建检查。

仓库和 Pages 的可见性、可用性取决于 GitHub 账户计划及组织策略。不要将空模板显示为已完成研究。

部署遵循 [GitHub 官方自定义 Pages 工作流说明](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。PR 只构建和检查，不发布；`main` 的成功构建才部署。工作流自动设置对应 GitHub 编辑链接。

## 本地预览（负责人使用）

需要 Python 3.12 或更新版本：

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/check.py
python -m http.server 8765 --directory dist
```

打开 `http://localhost:8765`。修改 Markdown 后再次运行构建并刷新页面。生成后的 `dist/index.html` 也可以直接在浏览器中打开；网站没有运行时依赖，不需要数据库。部署使用相对路径，兼容带仓库名的 Pages 地址。

## 项目结构

```text
content/                  六个成员文件 + 六个主方向清单
assets/style.css          共用样式（组员无需修改）
scripts/build.py          Markdown → 七个静态页面
scripts/check.py          链接、锚点和模板完整性检查
.github/workflows/pages.yml  PR 检查 + main 自动部署
requirements.txt          固定构建依赖
```

所有成员内容属于受信任的仓库源码。Markdown 支持 HTML，因此只合并经过审阅的贡献。网站为老师提供只读浏览；编辑通过 GitHub 完成，无网页内账号或保存功能。
