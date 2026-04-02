#!/usr/bin/env python3
"""
OpenClaw 10分钟极速上手技能 V2
优化点：
1. 第二关增加更多个性化信息收集
2. 第三关提供双选项（示例复制/模板自定义）
3. 进阶三完善安装指引，增加故障排除
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ============ 配置 ============
DATA_DIR = os.path.expanduser("~/.openclaw/skills/quickstart/data")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")
TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# ============ 任务数据加载 ============
def load_tasks() -> Dict:
    """加载任务配置"""
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# ============ 进度管理 ============
def load_progress() -> Dict:
    """加载用户进度，首次使用返回默认结构"""
    if not os.path.exists(PROGRESS_FILE):
        default_progress = {
            "intro_completed": False,
            "intro_current": 0,  # 当前进行到的入门任务索引
            "intro_done": [],    # 已完成的入门任务ID列表
            "advanced_unlocked": False,
            "advanced_current": None,  # 当前选择的进阶关卡
            "advanced_done": [],
            "reminder_enabled": True,  # 是否开启提醒
            "started_at": None,
            "last_active": None,
            "intro3_choice": None  # 记录第三关的选择 A/B
        }
        save_progress(default_progress)
        return default_progress
    
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_progress(progress: Dict):
    """保存用户进度"""
    progress["last_active"] = datetime.now().isoformat()
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def reset_progress():
    """重置所有进度"""
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
    return load_progress()

# ============ 消息生成器 ============
def format_task_card(task: Dict, is_intro: bool, progress: Dict) -> str:
    """格式化任务卡片，简洁可直接复制"""
    level_type = "入门关卡" if is_intro else "进阶关卡"
    total = 3 if is_intro else 4
    current_num = progress["intro_current"] + 1 if is_intro else (progress["advanced_current"] or 0) + 1
    
    tips_str = ""
    if task.get("tips"):
        tips_str = "\n💡 **小贴士**：\n" + "\n".join([f"• {tip}" for tip in task["tips"][:2]])
    
    follow_up = ""
    if task.get("follow_up"):
        follow_up = f"\n\n✅ **完成后测试**：{task['follow_up']}"
    
    # 特殊处理第二关（增加详细设置指南）
    if task.get("setup_guide"):
        setup_section = f"""\n\n---\n\n### 📝 个人信息收集清单\n\n复制以下内容，填写后发送给龙虾：\n```\n{task['setup_guide']}\n```\n"""
    else:
        setup_section = ""
    
    # 特殊处理第三关（双选项）
    if task.get("options") and task["id"] == "intro_3":
        options_str = ""
        for opt in task["options"]:
            options_str += f"\n\n**{opt['name']}**\n"
            if opt.get("template_guide"):
                options_str += f"\n{opt['template_guide']}\n"
            if opt.get("action"):
                options_str += f"\n📋 **执行指令**：\n```\n{opt['action']}\n```\n"
            if opt.get("note"):
                options_str += f"\n💡 *{opt['note']}*"
        
        action_section = f"""\n---\n\n### 🎯 选择你的学习方式{options_str}"""
    else:
        action_section = f"""\n---\n\n### 📋 执行指令（直接复制）\n```\n{task['action']}\n```"""
    
    return f"""# 🎯 {task['title']}

**⏱️ 预计耗时**：{task['duration']} | **进度**：{current_num}/{total}

**📝 任务说明**：{task['description']}
{setup_section}{action_section}

---

**✅ 完成标准**：{task['checkpoint']}{follow_up}{tips_str}

---

**下一步**：完成任务后发送 **「完成」**，我将为你解锁下一关 🚀
"""

def format_welcome() -> str:
    """欢迎消息"""
    return """# 🦞 欢迎来到 OpenClaw 10分钟极速上手！

我将带你完成 **3个入门关卡**，只需 **10分钟**，你就能：
- ✅ 让龙虾正常回复你的消息
- ✅ 配置专属人格，让龙虾深入了解你  
- ✅ 掌握精准提问，效果提升10倍

**🎁 完成后解锁**：4个进阶关卡自由选择

---

**常用指令**：
- 发送 **「开始」** - 开始第一关
- 发送 **「完成」** - 标记当前任务完成，进入下一关
- 发送 **「进度」** - 查看当前进度
- 发送 **「跳过」** - 跳过当前任务（不推荐）

---

准备好开始了吗？发送 **「开始」** 🚀
"""

def format_intro_complete() -> str:
    """入门完成庆祝消息"""
    return """# 🎉 恭喜你完成入门三关！

你已经掌握了 OpenClaw 的核心使用方法：
- ✅ 第一关：成功和龙虾对话
- ✅ 第二关：配置了专属人格（更详细的信息收集）
- ✅ 第三关：学会了精准提问（双选项灵活学习）

---

## 🚀 现在解锁进阶关卡（自由选择）

| 关卡 | 主题 | 预计耗时 |
|:---|:---|:---:|
| 进阶一 | 模仿实战案例 | 5分钟 |
| 进阶二 | 完成第一件真实工作 | 5-10分钟 |
| 进阶三 | 安装第一个Skill（含完整故障排除） | 5-8分钟 |
| 进阶四 | 建立知识库 | 5-10分钟 |

---

**发送「进阶」选择你想学习的关卡** 🎯

💡 **提示**：入门任务已全部完成，每日提醒已自动关闭。如需重新开启提醒，发送「开启提醒」。
"""

def format_advanced_menu(tasks: List[Dict]) -> str:
    """进阶关卡选择菜单"""
    options = []
    for i, task in enumerate(tasks, 1):
        options.append(f"{i}. **{task['title']}** - {task['duration']}")
    
    options_str = "\n".join(options)
    
    return f"""# 📚 进阶关卡选择

请发送数字 **1-4** 选择你想学习的关卡：

{options_str}

---

💡 **推荐**：如果是第一次，建议从「进阶三：安装Skill」开始，解锁龙虾的完整能力！

发送 **「进度」** 可随时查看完成情况 ✅
"""

def format_progress(progress: Dict, tasks: Dict) -> str:
    """格式化进度展示"""
    intro_tasks = tasks["intro"]
    advanced_tasks = tasks["advanced"]
    
    # 入门进度
    intro_done_count = len(progress["intro_done"])
    intro_total = len(intro_tasks)
    intro_status = "✅ 已完成" if progress["intro_completed"] else f"⏳ 进行中 ({intro_done_count}/{intro_total})"
    
    # 进阶进度
    adv_done_count = len(progress["advanced_done"])
    adv_status = f"已解锁，完成 {adv_done_count}/4" if progress["advanced_unlocked"] else "🔒 未解锁"
    
    current_task = ""
    if not progress["intro_completed"] and progress["intro_current"] < intro_total:
        current = intro_tasks[progress["intro_current"]]
        current_task = f"\n📍 **当前任务**：{current['title']}"
    elif progress["advanced_unlocked"] and progress["advanced_current"] is not None:
        current = advanced_tasks[progress["advanced_current"]]
        current_task = f"\n📍 **当前任务**：{current['title']}"
    
    return f"""# 📊 你的学习进度

**入门关卡**：{intro_status}
**进阶关卡**：{adv_status}{current_task}

---

**快捷指令**：
- 「开始」- 开始/继续入门任务
- 「进阶」- 选择进阶关卡（入门完成后）
- 「完成」- 标记当前任务完成
- 「重置」- 重新开始（谨慎使用）
"""

def format_reminder(progress: Dict) -> Optional[str]:
    """每日提醒消息"""
    intro_tasks = load_tasks()["intro"]
    current_idx = progress["intro_current"]
    
    if current_idx >= len(intro_tasks):
        return None  # 入门已完成，不需要提醒
    
    current_task = intro_tasks[current_idx]
    
    return f"""# ⏰ 每日学习提醒

你好！你正在学习 OpenClaw 入门课程，目前进度：**{current_idx}/3**

📍 **当前待完成任务**：{current_task['title']}

**快速继续**：
发送 **「继续」** 查看完整任务，或发送 **「进度」** 查看详情。

💡 每天只需10分钟，3天掌握AI提效技能！
"""

# ============ 核心处理逻辑 ============
def handle_start(progress: Dict, tasks: Dict) -> str:
    """处理开始/继续命令"""
    if progress["intro_completed"]:
        return format_intro_complete()
    
    intro_tasks = tasks["intro"]
    current_idx = progress["intro_current"]
    
    # 如果还没开始
    if progress["started_at"] is None:
        progress["started_at"] = datetime.now().isoformat()
        save_progress(progress)
    
    # 如果入门已完成但未标记
    if current_idx >= len(intro_tasks):
        progress["intro_completed"] = True
        progress["reminder_enabled"] = False
        save_progress(progress)
        return format_intro_complete()
    
    current_task = intro_tasks[current_idx]
    return format_task_card(current_task, True, progress)

def handle_done(progress: Dict, tasks: Dict) -> str:
    """处理完成任务"""
    if progress["intro_completed"] and progress["advanced_current"] is None:
        return "🎉 你已完成了入门关卡！发送「进阶」选择进阶关卡继续学习。"
    
    # 处理入门任务
    if not progress["intro_completed"]:
        intro_tasks = tasks["intro"]
        current_idx = progress["intro_current"]
        
        if current_idx >= len(intro_tasks):
            progress["intro_completed"] = True
            progress["reminder_enabled"] = False  # 关闭提醒
            save_progress(progress)
            return format_intro_complete()
        
        current_task = intro_tasks[current_idx]
        task_id = current_task["id"]
        
        # 标记完成
        if task_id not in progress["intro_done"]:
            progress["intro_done"].append(task_id)
        
        # 进入下一关
        progress["intro_current"] = current_idx + 1
        
        # 检查是否入门全部完成
        if progress["intro_current"] >= len(intro_tasks):
            progress["intro_completed"] = True
            progress["reminder_enabled"] = False
            save_progress(progress)
            return format_intro_complete()
        
        save_progress(progress)
        
        # 返回下一关任务
        next_task = intro_tasks[progress["intro_current"]]
        return f"✅ 太棒了！上一关已完成。\n\n" + format_task_card(next_task, True, progress)
    
    # 处理进阶任务
    else:
        advanced_tasks = tasks["advanced"]
        current_idx = progress["advanced_current"]
        
        if current_idx is None or current_idx >= len(advanced_tasks):
            return "🎉 当前没有进行中的进阶任务。发送「进阶」选择新的关卡。"
        
        current_task = advanced_tasks[current_idx]
        task_id = current_task["id"]
        
        if task_id not in progress["advanced_done"]:
            progress["advanced_done"].append(task_id)
        
        progress["advanced_current"] = None  # 进阶任务一次性的，完成后需要重新选择
        save_progress(progress)
        
        return f"""# ✅ 进阶任务完成！

你已完成：**{current_task['title']}**

---

**发送「进阶」继续学习其他关卡**，或随时发送「进度」查看完成情况。

💡 **建议**：趁热打铁，尝试用这个技能完成一个真实工作任务！
"""

def handle_advanced(progress: Dict, tasks: Dict, choice: Optional[int] = None) -> str:
    """处理进阶关卡选择"""
    if not progress["intro_completed"]:
        return "🔒 请先完成入门三关！发送「开始」继续入门任务。"
    
    advanced_tasks = tasks["advanced"]
    
    # 如果没有指定选择，显示菜单
    if choice is None:
        return format_advanced_menu(advanced_tasks)
    
    # 验证选择
    if choice < 1 or choice > len(advanced_tasks):
        return f"❌ 无效选择，请发送 1-{len(advanced_tasks)} 之间的数字。"
    
    # 设置当前进阶任务
    progress["advanced_current"] = choice - 1
    save_progress(progress)
    
    selected_task = advanced_tasks[choice - 1]
    
    # 构建进阶任务展示
    content = f"# 📚 {selected_task['title']}\n\n"
    content += f"**预计耗时**：{selected_task['duration']}\n\n"
    content += f"**任务说明**：{selected_task['description']}\n\n---\n\n"
    
    # 进阶三特殊处理（完整安装指南）
    if selected_task["id"] == "adv_3" and "install_guide" in selected_task:
        guide = selected_task["install_guide"]
        content += "### 📖 完整安装指南（按步骤执行）\n\n"
        content += f"{guide['pre_check']}\n\n---\n\n"
        content += f"{guide['step1']}\n\n---\n\n"
        content += f"{guide['step2']}\n\n---\n\n"
        content += f"{guide['step3']}\n\n---\n\n"
        content += f"{guide['step4']}\n\n---\n\n"
        content += f"{guide['troubleshooting']}\n\n---\n\n"
    
    # 如果有选项（进阶一、二有多个选择）
    elif "options" in selected_task:
        content += "### 🎯 选择一个案例执行：\n\n"
        for i, option in enumerate(selected_task["options"], 1):
            content += f"**选项{i}：{option['name']}**\n"
            content += f"```\n{option['action']}\n```\n\n"
        content += "---\n\n"
    
    # 如果有推荐（进阶三，当没有install_guide时显示）
    elif "recommendations" in selected_task and "install_guide" not in selected_task:
        content += "### 🛠️ 推荐安装的技能：\n\n"
        for rec in selected_task["recommendations"]:
            content += f"• **{rec['name']}** - {rec['desc']}\n"
        content += f"\n**执行指令**：```\n{selected_task['action']}\n```\n\n---\n\n"
    
    # 通用执行指令
    elif "action" in selected_task and "options" not in selected_task and "recommendations" not in selected_task:
        content += f"### 📋 执行指令：\n```\n{selected_task['action']}\n```\n\n---\n\n"
    
    # 提示
    if selected_task.get("tips"):
        content += "💡 **提示**：\n" + "\n".join([f"• {tip}" for tip in selected_task["tips"]]) + "\n\n---\n\n"
    
    content += "完成任务后发送 **「完成」** ✅"
    
    return content

def handle_skip(progress: Dict, tasks: Dict) -> str:
    """处理跳过任务"""
    if not progress["intro_completed"]:
        intro_tasks = tasks["intro"]
        current_idx = progress["intro_current"]
        
        if current_idx >= len(intro_tasks):
            return "入门任务已全部完成！"
        
        progress["intro_current"] = current_idx + 1
        save_progress(progress)
        
        # 检查是否全部完成
        if progress["intro_current"] >= len(intro_tasks):
            progress["intro_completed"] = True
            progress["reminder_enabled"] = False
            save_progress(progress)
            return format_intro_complete()
        
        next_task = intro_tasks[progress["intro_current"]]
        return f"⏭️ 已跳过当前任务。\n\n" + format_task_card(next_task, True, progress)
    
    return "进阶任务无法跳过，请完成后再继续。"

def handle_heartbeat() -> Optional[str]:
    """处理每日定时提醒"""
    progress = load_progress()
    
    # 如果入门已完成或提醒已关闭，不发送
    if progress["intro_completed"] or not progress["reminder_enabled"]:
        return None
    
    # 检查是否刚开始（24小时内不提醒）
    if progress.get("started_at"):
        started = datetime.fromisoformat(progress["started_at"])
        if (datetime.now() - started).days < 1:
            return None
    
    return format_reminder(progress)

# ============ 主入口 ============
def main():
    """主入口函数"""
    import sys
    
    # 获取输入
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:]).strip().lower()
    else:
        user_input = ""
    
    # 加载数据
    tasks = load_tasks()
    progress = load_progress()
    
    # 特殊处理heartbeat
    if user_input == "__heartbeat__":
        result = handle_heartbeat()
        if result:
            print(result)
        return
    
    # 命令路由
    response = ""
    
    if not user_input or user_input in ["开始", "start", "继续", "resume"]:
        response = handle_start(progress, tasks)
    
    elif user_input in ["完成", "done", "ok", "好了"]:
        response = handle_done(progress, tasks)
    
    elif user_input in ["进阶", "advanced"]:
        response = handle_advanced(progress, tasks)
    
    elif user_input.isdigit() and progress.get("intro_completed"):
        # 进阶关卡选择
        response = handle_advanced(progress, tasks, int(user_input))
    
    elif user_input in ["进度", "progress", "状态", "status"]:
        response = format_progress(progress, tasks)
    
    elif user_input in ["跳过", "skip", "next"]:
        response = handle_skip(progress, tasks)
    
    elif user_input in ["重置", "reset", "重新开始"]:
        progress = reset_progress()
        response = "🔄 进度已重置。发送「开始」重新开始学习！"
    
    elif user_input in ["帮助", "help", "?"]:
        response = """# 🦞 快速上手指令

**入门阶段**：
- 「开始」- 开始入门任务
- 「完成」- 标记任务完成，进入下一关
- 「跳过」- 跳过当前任务（不推荐）

**进阶阶段**（入门完成后）：
- 「进阶」- 查看进阶关卡菜单
- 发送数字 1-4 - 选择对应进阶关卡

**其他**：
- 「进度」- 查看当前进度
- 「重置」- 重新开始（谨慎使用）
"""
    
    else:
        response = """🤔 没听懂呢～

常用指令：
- 「开始」- 开始入门任务
- 「完成」- 标记当前任务完成  
- 「进阶」- 选择进阶关卡
- 「进度」- 查看进度

发送「帮助」查看完整指令列表。"""
    
    print(response)

if __name__ == "__main__":
    main()
