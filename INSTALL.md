# 安装说明 · 乙女老公.skill

本文说明如何在 **Claude Code**、**OpenClaw**、**Cursor** 中安装与验证本仓库。

仓库地址（占位）：`https://github.com/Daim7/otome-husband-skill.git`

---

## Claude Code

### 方式一：安装到当前项目

```bash
# 在 git 仓库根目录执行
mkdir -p .claude/skills
git clone https://github.com/Daim7/otome-husband-skill.git .claude/skills/otome-husband-skill
```

### 方式二：安装到全局

```bash
git clone https://github.com/Daim7/otome-husband-skill.git ~/.claude/skills/otome-husband-skill
```

### 安装依赖（推荐）

```bash
cd .claude/skills/otome-husband-skill
pip install -r requirements.txt
```

依赖说明：

- `requests` — HTTP 请求（后续扩展采集、API 时使用）
- `pypinyin` — 中文名转拼音生成 slug（可选；未安装时需手动指定 `--slug`）

---

## OpenClaw

### 克隆到工作区

```bash
git clone https://github.com/Daim7/otome-husband-skill.git ~/.openclaw/workspace/skills/otome-husband-skill
```

### 配置文件示例

在 `~/.openclaw/config.yaml` 中注册 Skill（路径请按本机实际修改）：

```yaml
skills:
  - name: otome-husband-skill
    path: ~/.openclaw/workspace/skills/otome-husband-skill
    description: "乙女老公.skill — 让纸片人老公走进日常互动"
    triggers:
      - "/otome-husband"
      - "乙女老公"
      - "老公 skill"
    tools:
      - Read
      - Write
      - Edit
      - Bash
```

安装依赖：

```bash
pip install -r ~/.openclaw/workspace/skills/otome-husband-skill/requirements.txt
```

---

## Cursor

1. 克隆仓库到本地：

   ```bash
   git clone https://github.com/Daim7/otome-husband-skill.git
   ```

2. 在 Cursor 中打开该目录（或把本仓库作为子文件夹加入工作区）。
3. 根目录或 `husbands/{slug}/` 下的 `SKILL.md` 可被识别为 Agent Skill（取决于你的 Cursor 规则与技能扫描路径）。

---

## 验证安装

### 1. 命令行工具

在项目根目录执行：

```bash
python tools/skill_writer.py --action list --base-dir ./husbands
```

若已包含示例老公 `example_lingxiao`，应能看到列表输出；若为全新克隆且已删除示例外目录，可能显示「暂无已创建的老公 Skill」，均属正常。

再测创建流程（可选）：

```bash
python tools/skill_writer.py --action create --slug demo --name "测试" --base-dir ./husbands
```

（可按需删除 `husbands/demo/` 测试目录。）

### 2. 版本管理器

```bash
python tools/version_manager.py --action list --slug example_lingxiao --base-dir ./husbands
```

尚未执行过 `update` 时，可能提示暂无历史版本，说明路径与 slug 正确即可。

### 3. 在 AI 客户端中验证

在 Claude Code / OpenClaw 中触发你在 `config.yaml` 或项目规则里配置的指令（例如「乙女老公」「创建老公 skill」等）。若助手能按 `SKILL.md` 的流程引导你录入原型、甜度与人设，即表示加载成功。

---

## 其他编辑器

本项目遵循常见的 Agent Skill 目录约定；凡支持自定义技能路径的工具，将本仓库目录注册为技能根路径即可。
