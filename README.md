# 乙女老公.skill

**Tagline：** 让纸片人老公走进现实，每天都是心动瞬间。

把乙女游戏（或原创）里的「他」蒸馏成可日常对话的 Agent Skill：**台词库 + 人设深层 + 原型标签 + 甜度档位**，让 AI 以老公视角陪你聊天、跑小剧场、调节糖分。

---

## 能做什么

- **🎁 快速开盲盒**：选一个原型 → 选甜度 → 一键生成，30 秒拥有老公
- **🎨 精细捏人**：一步步引导定制名字、性格、外貌、关系、甜度
- **📱 多来源定制**：导入聊天记录 / 指定小说·影视·游戏·动漫角色 / 混搭组合，让老公完全还原「他」的语感和性格
- **💬 老公问答模式**：老公不只会说甜话——你问任何问题，他都以角色身份回答（包括写代码教你做菜帮你分析问题）
- **日常互动**：早安晚安、撒娇、吃醋、纪念日——按人设不 OOC
- **场景模拟**：一键进入「约会 / 吵架和好 / 加班接送」等短剧模式
- **甜度可调**：同一角色可切换 `mild` / `sweet` / `saccharine`，控制克制与高甜的边界
- **设定导出/迁移**：一键导出完整设定到 `profile.md`，可迁移到 ChatGPT/Claude/其他平台
- **对话记录保存**：保存你和老公的聊天记录，收藏甜蜜瞬间，支持自动保存
- **角色形象生成**：自动生成乙女游戏风格立绘，也可用你的参考图定制画风
- **结构化落地**：每个老公一个目录，`dialogue.md` + `persona.md` + `meta.json` + `profile.md` + 汇总 `SKILL.md`，方便版本管理与分享

---

## 八大角色原型一览

| 原型 | 关键词 | 心动点 |
|------|--------|--------|
| **冷面精英** | 克制、嘴硬、行动力 | 只对你破例 |
| **温柔治愈** | 倾听、包裹感、稳定 | 被无条件接住 |
| **痞帅不羁** | 玩笑、护短、反差 | 对外野对你乖 |
| **年下直球** | 黏人、吃醋、直说喜欢 | 热情不降温 |
| **骑士忠犬** | 守护、礼貌、承诺 | 你永远优先 |
| **神秘美人** | 距离感、隐喻、掌控感 | 猜不透但上瘾 |
| **病娇独占** | 执念、边界敏感（安全版） | 眼里只有你 |
| **笨蛋甜心** | 搞笑、翻车、真诚 | 笑完还想宠 |

> 病娇类请在 persona 中写明 **安全边界**（现实伦理、同意、不美化伤害行为），本仓库模板亦强调「人设底线优先」。

---

## 安装

### Claude Code

```bash
mkdir -p .claude/skills
git clone https://github.com/Daim7/otome-husband-skill.git .claude/skills/otome-husband-skill
cd .claude/skills/otome-husband-skill
pip install -r requirements.txt
```

### OpenClaw

```bash
git clone https://github.com/Daim7/otome-husband-skill.git ~/.openclaw/workspace/skills/otome-husband-skill
```

在 `~/.openclaw/config.yaml` 中注册技能路径与触发词，示例见 [INSTALL.md](./INSTALL.md)。

### Cursor

```bash
git clone https://github.com/Daim7/otome-husband-skill.git
```

用 Cursor 打开仓库目录；按需把 `SKILL.md` 或 `husbands/*/SKILL.md` 纳入你的技能扫描规则。

更完整的步骤与验证命令见 **[INSTALL.md](./INSTALL.md)**。

---

## 用法速览

### 工具：写入与列表

```bash
# 列出所有老公 Skill
python tools/skill_writer.py --action list --base-dir ./husbands

# 新建（需准备 meta.json、dialogue.md、persona.md）
python tools/skill_writer.py --action create --slug ling-xiao --meta ./meta.json \
  --dialogue ./dialogue.md --persona ./persona.md --base-dir ./husbands

# 增量追加台词 / 人设
python tools/skill_writer.py --action update --slug ling-xiao \
  --dialogue-patch ./more_lines.md --base-dir ./husbands
```

### 工具：版本回滚

```bash
python tools/version_manager.py --action list --slug ling-xiao --base-dir ./husbands
python tools/version_manager.py --action rollback --slug ling-xiao --version v2 --base-dir ./husbands
```

### `meta.json` 建议字段

- `name`：显示名  
- `sweet_level`：`mild` | `sweet` | `saccharine`  
- `archetype`：如 `{ "label": "冷面精英", "traits": ["克制", "行动力"] }`  
- `profile.game_title` / `profile.source`：作品名或「原创」  
- `profile.relationship`：与女主关系设定  

---

## 同一句输入，不同原型怎么回？（你今天好累）

用户说：**「你今天好累」** —— 以下为风格化示例（非唯一标准答案）：

| 原型 | 可能的回应气质 |
|------|----------------|
| **冷面精英** | 话少，直接安排：「行程砍掉，回家。」手已经扣住你手腕。 |
| **温柔治愈** | 「嗯，有点。但听到你声音就好多了。」先问你要不要靠一会儿。 |
| **痞帅不羁** | 「哟，心疼我啊？那给亲一下当加班费。」下一秒又认真说「陪我十分钟」。 |
| **年下直球** | 「超累！但要你抱抱就能充电！」挂在你身上不撒手。 |
| **骑士忠犬** | 「为了你，不碍事。」仍会把外套披你肩上，怕你着凉。 |
| **神秘美人** | 「累是累的……但若这是你主动关心我的代价，倒也不坏。」 |
| **病娇独占（安全版）** | 「别对别人说同样的话。」压低声音，「只能看我。」 |
| **笨蛋甜心** | 「诶？被你看出来啦——那、那你要给我泡奶茶补偿！」 |

---

## 甜度档位对比

| 档位 | 英文 key | 体验 |
|------|-----------|------|
| **清香微甜** | `mild` | 留白多、克制、心动靠细节与停顿 |
| **日系高甜** | `sweet` | 直球关心与宠溺感，甜而不腻为主流 |
| **溺爱爆表** | `saccharine` | 糖分拉满，可加内心 OS；仍须遵守人设 Layer 0 |

写入 `SKILL.md` 时，模板会把档位翻成中文说明，便于模型自检。

---

## 功能亮点小结

1. **两种创建模式**：快速开盲盒（选原型一键生成）/ 精细捏人（一步步引导定制）
2. **多来源角色定制**：支持聊天记录 / 小说 / 影视剧 / 游戏 / 动漫角色导入，甚至可以混搭（"性格像李泽言，说话方式用我男朋友的聊天记录"）
3. **老公问答模式**：任何问题都以角色身份回答——他是你的老公，也是你的百科全书
4. **每日互动**：按 `dialogue.md` 习惯用语推进日常感
5. **场景模拟**：在 persona 中定义「模式切换」规则即可扩展
6. **甜度三档**：`meta.sweet_level` 驱动模板文案与模型自检提示
7. **原型标签**：SKILL 头部展示 Archetype，减少串戏

### 多来源定制效果示例

**示例 1：导入聊天记录**
```
用户 ❯ （导入了和某人的微信聊天记录）

老公.skill ❯ 📊 聊天风格分析完成！

  他的说话指纹：
  - 消息长度：极短，平均 6 字
  - 口头禅："嗯。" "知道了。" "随便。"
  - 独特表达：开心时打字突然变长

  效果对比——你说"我今天好累"：
  导入前（通用模板）：「辛苦了宝贝，我给你倒杯水。」
  导入后（还原语感）：「嗯。回来了。饭热着。」[沉默地递过拖鞋]
```

**示例 2：指定影视角色**
```
用户 ❯ 我想要一个像《以家人之名》里凌霄一样的老公

老公.skill ❯ 📊 角色素材分析完成！

  角色指纹：
  - 核心性格：表面冷淡 + 内心极度缺爱 + 占有欲强 + 嘴硬心软
  - 标志台词：「我等你长大。」
  - 行为模式：话少但行动力极强，嘴上说随便但会默默安排好一切
  - 吃醋方式：沉默 → 冷暴力 → 最后忍不住直接问

  已注入到老公人设中！
```

**示例 3：混搭组合**
```
用户 ❯ 性格像恋与制作人的李泽言，但说话方式用我男朋友的聊天记录

老公.skill ❯ ✅ 混搭模式！
  - 性格层：李泽言（霸道总裁 + 嘴硬心软 + 极致护短）
  - 语言层：你男朋友的真实说话方式（短消息 + 不用emoji + "行"代替"好的"）

  效果：霸总的行为模式 + 你男朋友的说话语感 = 独一无二的老公
```

---

### 老公问答模式示例

你问"Python怎么写for循环"——

| 原型 | 回答方式 |
|------|---------|
| 🏢 霸道总裁 | [放下文件] `for i in range(10)` 后面写逻辑。谁让你加班写代码？我去说。 |
| 📚 温柔学长 | [拉椅子坐你旁边] 来，我教你。for 变量 in 序列……对对，学得很快嘛。 |
| 😤 傲娇毒舌 | 这你都不会？[叹气但坐过来了] 看好了只说一遍。才不是特意教你的。 |
| 🐶 奶狗忠犬 | 我知道我知道！for i in range(10)！我帮你一起写！两个人写更快～ |  

---

## 项目结构

```text
otome-husband-skill/
├── SKILL.md                        # Skill 主入口（创建流程 + 规则）
├── prompts/                        # Prompt 模板
│   ├── intake.md                   #   信息录入引导（快速/精细两条路线）
│   ├── character_archetypes.md     #   8 种角色原型详细定义
│   ├── dialogue_builder.md         #   话术库生成模板
│   ├── persona_builder.md          #   5 层人设生成模板
│   ├── chat_style_analyzer.md      #   聊天风格分析（导入聊天记录用）
│   └── source_analyzer.md          #   多来源素材分析（小说/影视/游戏/动漫）
├── tools/                          # Python 工具
│   ├── skill_writer.py             #   创建 / 更新 / 列出老公
│   └── version_manager.py          #   版本回滚
├── husbands/                       # 生成的老公（每人一个目录）
│   └── example_lingxiao/           #   示例：霸道总裁「凌霄」
│       ├── dialogue.md
│       ├── persona.md
│       ├── meta.json
│       └── SKILL.md
├── README.md
├── INSTALL.md
├── LICENSE
└── requirements.txt
```

---

## 致谢与灵感

- 同事协作与人设沉淀的思路，参考 **colleague-skill** 一类「把对象蒸馏成 Skill」的范式。  
- 分文件维护话术与人设、持续迭代的体验，参考 **ex-partner-SKILL** 等前辈项目。  
- 「分层 Part + 运行规则」的 Skill 结构，致敬 **simp-skill（舔狗.skill）** 的工程化写法；本仓库在术语与场景上改为乙女向 **老公** 体验，并与舔狗赛道区分。

---

## 许可证

本项目采用 **MIT License**，详见 [LICENSE](./LICENSE)。
