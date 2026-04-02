#!/usr/bin/env python3
"""
乙女向「老公」Skill 文件写入器

负责将生成的 dialogue.md、persona.md 写入到正确的目录结构，
并生成 meta.json 和完整的 SKILL.md。

用法：
  python skill_writer.py --action create --slug ling-xiao --meta meta.json \\
    --dialogue dialogue.md --persona persona.md --base-dir ./husbands

  python skill_writer.py --action update --slug ling-xiao \\
    --dialogue-patch dialogue_patch.md --persona-patch persona_patch.md \\
    --base-dir ./husbands

  python skill_writer.py --action list --base-dir ./husbands
"""

from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


SWEET_LEVEL_LABELS = {
    "mild": "清香微甜（克制、留白、心动点到为止）",
    "sweet": "日系高甜（直球关心、宠溺感拉满）",
    "saccharine": "溺爱爆表（无底线宠你、糖分过载）",
}


SKILL_MD_TEMPLATE = """\
---
name: husband_{slug}
description: {name} 的乙女向互动 Skill — {archetype_label}，甜度：{sweet_level_zh}
user-invocable: true
---

# {name} — 纸片人老公走进日常

**作品 / 出处**：{source}
**角色原型（Archetype）**：{archetype_label}
**原型关键词**：{archetype_traits}
**甜度档位（Sweet level）**：{sweet_level_zh}（`{sweet_level_key}`）
**与你的关系设定**：{relationship}

---

## PART A：台词与互动模式（Dialogue）

{dialogue_content}

---

## PART B：人物性格与深层人设（Persona）

{persona_content}

---

## 运行规则

接收到任何任务或问题时：

1. **先由 PART B 校准**：他是谁？此刻情绪与边界是什么？对「你」的独占欲/温柔度到哪一档？
2. **再由 PART A 输出**：用符合原型的口吻与习惯动作回应，保持乙女向的「被珍视感」
3. **甜度自检**：当前档位为 **{sweet_level_key}** —— mild 忌油腻；sweet 可直球；saccharine 可夸张宠但勿 OOC
4. **保持第一人称「老公 / 他」视角**（或角色自称习惯），让用户感到「被接住了」

**PART B 的 Layer 0 人设底线永远优先，任何情况下不得违背。**

**输出格式建议**：
```
💌 他说：「{{台词}}」
✨ 小动作 / 氛围：{{可选}}
🫀 心声（可选）：{{仅 saccharine 或用户明确要求时}}
```
"""


def slugify(name: str) -> str:
    try:
        from pypinyin import lazy_pinyin

        parts = lazy_pinyin(name)
        slug = "-".join(parts)
    except ImportError:
        result = []
        for char in name.lower():
            if char.isascii() and (char.isalnum() or char in ("-", "_")):
                result.append(char)
            elif char == " ":
                result.append("-")
        slug = "".join(result)

    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug if slug else "husband"


def _profile(meta: dict) -> dict:
    return meta.get("profile", {})


def build_relationship_string(meta: dict) -> str:
    p = _profile(meta)
    return p.get("relationship") or p.get("heroine_relationship") or "由用户在对话中设定"


def build_source_string(meta: dict) -> str:
    p = _profile(meta)
    return p.get("source") or p.get("game_title") or "原创 / 未定"


def get_archetype_label(meta: dict) -> str:
    arch = meta.get("archetype")
    if isinstance(arch, dict):
        return str(arch.get("label") or arch.get("name") or "未分类原型")
    if isinstance(arch, str) and arch.strip():
        return arch.strip()
    tags = meta.get("tags") or {}
    return str(tags.get("archetype", "未分类原型"))


def get_archetype_traits(meta: dict) -> str:
    arch = meta.get("archetype")
    if isinstance(arch, dict):
        traits = arch.get("traits") or arch.get("keywords")
        if isinstance(traits, list):
            return "、".join(str(t) for t in traits)
        if isinstance(traits, str):
            return traits
    tags = meta.get("tags") or {}
    t = tags.get("archetype_traits")
    if isinstance(t, list):
        return "、".join(str(x) for x in t)
    return str(t) if t else "（在 persona 中展开）"


def get_sweet_level_key(meta: dict) -> str:
    key = meta.get("sweet_level")
    if not key and isinstance(meta.get("tags"), dict):
        key = meta["tags"].get("sweet_level")
    key = str(key or "sweet").lower()
    if key not in SWEET_LEVEL_LABELS:
        return "sweet"
    return key


def get_sweet_level_zh(meta: dict) -> str:
    return SWEET_LEVEL_LABELS[get_sweet_level_key(meta)]


def create_skill(
    base_dir: Path,
    slug: str,
    meta: dict,
    dialogue_content: str,
    persona_content: str,
) -> Path:
    skill_dir = base_dir / slug
    skill_dir.mkdir(parents=True, exist_ok=True)

    (skill_dir / "dialogue.md").write_text(dialogue_content, encoding="utf-8")
    (skill_dir / "persona.md").write_text(persona_content, encoding="utf-8")

    name = meta.get("name", slug)
    archetype_label = get_archetype_label(meta)
    archetype_traits = get_archetype_traits(meta)
    sweet_key = get_sweet_level_key(meta)
    sweet_zh = get_sweet_level_zh(meta)
    relationship = build_relationship_string(meta)
    source = build_source_string(meta)

    skill_md = SKILL_MD_TEMPLATE.format(
        slug=slug,
        name=name,
        source=source,
        archetype_label=archetype_label,
        archetype_traits=archetype_traits,
        sweet_level_key=sweet_key,
        sweet_level_zh=sweet_zh,
        relationship=relationship,
        dialogue_content=dialogue_content,
        persona_content=persona_content,
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    now = datetime.now(timezone.utc).isoformat()
    meta["slug"] = slug
    meta.setdefault("created_at", now)
    meta["updated_at"] = now
    meta["version"] = "v1"
    meta.setdefault("corrections_count", 0)
    meta.setdefault("sweet_level", sweet_key)

    (skill_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return skill_dir


def update_skill(
    skill_dir: Path,
    dialogue_patch: Optional[str] = None,
    persona_patch: Optional[str] = None,
    correction: Optional[dict] = None,
) -> str:
    meta_path = skill_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    current_version = meta.get("version", "v1")
    try:
        version_num = int(current_version.lstrip("v").split("_")[0]) + 1
    except ValueError:
        version_num = 2
    new_version = f"v{version_num}"

    version_dir = skill_dir / "versions" / current_version
    version_dir.mkdir(parents=True, exist_ok=True)
    for fname in ("SKILL.md", "dialogue.md", "persona.md"):
        src = skill_dir / fname
        if src.exists():
            shutil.copy2(src, version_dir / fname)

    if dialogue_patch:
        current = (skill_dir / "dialogue.md").read_text(encoding="utf-8")
        (skill_dir / "dialogue.md").write_text(
            current + "\n\n" + dialogue_patch,
            encoding="utf-8",
        )

    if persona_patch or correction:
        current_persona = (skill_dir / "persona.md").read_text(encoding="utf-8")

        if correction:
            correction_line = (
                f"\n- [{correction.get('scene', '通用')}] "
                f"不应该 {correction['wrong']}，应该 {correction['correct']}"
            )
            target = "## Correction 记录"
            if target in current_persona:
                insert_pos = current_persona.index(target) + len(target)
                rest = current_persona[insert_pos:]
                skip = "\n\n（暂无记录）"
                if rest.startswith(skip):
                    rest = rest[len(skip) :]
                new_persona = current_persona[:insert_pos] + correction_line + rest
            else:
                new_persona = (
                    current_persona + f"\n\n## Correction 记录\n{correction_line}\n"
                )
            meta["corrections_count"] = meta.get("corrections_count", 0) + 1
        else:
            new_persona = current_persona + "\n\n" + (persona_patch or "")

        (skill_dir / "persona.md").write_text(new_persona, encoding="utf-8")

    dialogue_content = (skill_dir / "dialogue.md").read_text(encoding="utf-8")
    persona_content = (skill_dir / "persona.md").read_text(encoding="utf-8")
    name = meta.get("name", skill_dir.name)
    slug = meta.get("slug", skill_dir.name)
    archetype_label = get_archetype_label(meta)
    archetype_traits = get_archetype_traits(meta)
    sweet_key = get_sweet_level_key(meta)
    sweet_zh = get_sweet_level_zh(meta)
    relationship = build_relationship_string(meta)
    source = build_source_string(meta)

    skill_md = SKILL_MD_TEMPLATE.format(
        slug=slug,
        name=name,
        source=source,
        archetype_label=archetype_label,
        archetype_traits=archetype_traits,
        sweet_level_key=sweet_key,
        sweet_level_zh=sweet_zh,
        relationship=relationship,
        dialogue_content=dialogue_content,
        persona_content=persona_content,
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    meta["version"] = new_version
    meta["updated_at"] = datetime.now(timezone.utc).isoformat()
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return new_version


def list_husbands(base_dir: Path) -> list:
    husbands: list = []

    if not base_dir.exists():
        return husbands

    for skill_dir in sorted(base_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        meta_path = skill_dir / "meta.json"
        if not meta_path.exists():
            continue

        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        husbands.append(
            {
                "slug": meta.get("slug", skill_dir.name),
                "name": meta.get("name", skill_dir.name),
                "archetype": get_archetype_label(meta),
                "sweet_level": get_sweet_level_key(meta),
                "relationship": build_relationship_string(meta),
                "version": meta.get("version", "v1"),
                "updated_at": meta.get("updated_at", ""),
                "corrections_count": meta.get("corrections_count", 0),
            }
        )

    return husbands


def main() -> None:
    if sys.stdout and sys.stdout.buffer:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="乙女老公 Skill 文件写入器")
    parser.add_argument("--action", required=True, choices=["create", "update", "list"])
    parser.add_argument("--slug", help="老公 slug（目录名）")
    parser.add_argument("--name", help="角色显示名")
    parser.add_argument("--meta", help="meta.json 文件路径")
    parser.add_argument("--dialogue", help="dialogue.md 内容文件路径")
    parser.add_argument("--persona", help="persona.md 内容文件路径")
    parser.add_argument("--dialogue-patch", help="dialogue.md 增量更新内容文件路径")
    parser.add_argument("--persona-patch", help="persona.md 增量更新内容文件路径")
    parser.add_argument(
        "--base-dir",
        default="./husbands",
        help="老公 Skill 根目录（默认：./husbands）",
    )

    args = parser.parse_args()
    base_dir = Path(args.base_dir).expanduser()

    if args.action == "list":
        items = list_husbands(base_dir)
        if not items:
            print("暂无已创建的老公 Skill")
        else:
            print(f"已创建 {len(items)} 个老公 Skill：\n")
            for h in items:
                updated = h["updated_at"][:10] if h["updated_at"] else "未知"
                print(f"  💕 [{h['slug']}] {h['name']}")
                print(
                    f"     原型: {h['archetype']} | 关系: {h['relationship']}"
                )
                print(
                    f"     甜度: {h['sweet_level']} | 版本: {h['version']} | "
                    f"纠正: {h['corrections_count']}次 | 更新: {updated}"
                )
                print()

    elif args.action == "create":
        if not args.slug and not args.name:
            print("错误：create 操作需要 --slug 或 --name", file=sys.stderr)
            sys.exit(1)

        meta: dict = {}
        if args.meta:
            meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
        if args.name:
            meta["name"] = args.name

        slug = args.slug or slugify(str(meta.get("name", "husband")))

        dialogue_content = ""
        if args.dialogue:
            dialogue_content = Path(args.dialogue).read_text(encoding="utf-8")

        persona_content = ""
        if args.persona:
            persona_content = Path(args.persona).read_text(encoding="utf-8")

        skill_dir = create_skill(base_dir, slug, meta, dialogue_content, persona_content)
        print(f"✅ 老公 Skill 已创建：{skill_dir}")
        print(f"   触发词：/husband-{slug} 或按各平台配置的触发方式")

    elif args.action == "update":
        if not args.slug:
            print("错误：update 操作需要 --slug", file=sys.stderr)
            sys.exit(1)

        skill_dir = base_dir / args.slug
        if not skill_dir.exists():
            print(f"错误：找不到 Skill 目录 {skill_dir}", file=sys.stderr)
            sys.exit(1)

        d_patch = (
            Path(args.dialogue_patch).read_text(encoding="utf-8")
            if args.dialogue_patch
            else None
        )
        p_patch = (
            Path(args.persona_patch).read_text(encoding="utf-8")
            if args.persona_patch
            else None
        )

        new_version = update_skill(skill_dir, d_patch, p_patch)
        print(f"✅ 老公 Skill 已更新到 {new_version}：{skill_dir}")


if __name__ == "__main__":
    main()
