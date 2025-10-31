"""
Power User深度行为分析和Reach Out策略设计

目标：
1. 识别power user的关键行为特征
2. 理解他们为什么没有转化
3. 从目标倒推设计reach out问题框架
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

# 读取数据
non_creators = pd.read_csv('/Users/hancezhang/Claude code exp/product_op/data/latest_results/non_creator_engagement.csv')
all_users = pd.read_csv('/Users/hancezhang/Claude code exp/product_op/data/latest_results/marketing_bot_users.csv')

# 转换时间列
non_creators['first_interaction'] = pd.to_datetime(non_creators['first_interaction'])
non_creators['last_interaction'] = pd.to_datetime(non_creators['last_interaction'])

print("=" * 80)
print("POWER USER深度行为分析")
print("=" * 80)
print()

# ============================================================================
# 第一部分：Power User行为模式识别
# ============================================================================

print("📊 第一部分：POWER USER行为模式深度分析")
print("-" * 80)
print()

# 1. 定义Power User分层
print("1️⃣ Power User分层定义")
print()

# 超级用户（25+ msgs）
super_users = non_creators[non_creators['total_messages'] >= 25].copy()
# 高参与用户（6-24 msgs）
high_engagement = non_creators[(non_creators['total_messages'] >= 6) &
                               (non_creators['total_messages'] < 25)].copy()
# 低参与用户（1-5 msgs）
low_engagement = non_creators[non_creators['total_messages'] < 6].copy()

print(f"超级用户（25+ msgs）: {len(super_users)} 位")
print(f"高参与用户（6-24 msgs）: {len(high_engagement)} 位")
print(f"低参与用户（1-5 msgs）: {len(low_engagement)} 位")
print()

# 2. 超级用户行为特征分析
print("2️⃣ 超级用户（Top 10）行为特征")
print()

top_10 = super_users.nlargest(10, 'total_messages')

for idx, user in top_10.iterrows():
    print(f"User {user['user_id']}:")
    print(f"  • 消息数: {user['total_messages']}")
    print(f"  • Bot数量: {user['bots_used']}")
    print(f"  • 参与时长: {user['engagement_hours']:.1f} 小时")
    print(f"  • 活跃天数: {user['active_days']} 天")

    # 计算参与强度指标
    msgs_per_day = user['total_messages'] / max(user['active_days'], 1)
    msgs_per_hour = user['total_messages'] / max(user['engagement_hours'], 1) if user['engagement_hours'] > 0 else 0

    print(f"  • 每天消息数: {msgs_per_day:.1f}")
    if msgs_per_hour > 0:
        print(f"  • 每小时消息数: {msgs_per_hour:.1f}")

    # 使用时间跨度
    time_span = (user['last_interaction'] - user['first_interaction']).days
    print(f"  • 时间跨度: {time_span} 天")

    # 判断使用模式
    if user['active_days'] == 1:
        pattern = "🔥 单日爆发型"
    elif user['active_days'] >= 5:
        pattern = "📈 长期粘性型"
    else:
        pattern = "🎯 短期集中型"

    print(f"  • 使用模式: {pattern}")
    print()

# 3. 行为模式聚类分析
print("3️⃣ 行为模式聚类")
print()

# 单日爆发型
burst_users = non_creators[
    (non_creators['total_messages'] >= 20) &
    (non_creators['active_days'] == 1)
]

# 长期粘性型
sticky_users = non_creators[
    (non_creators['total_messages'] >= 20) &
    (non_creators['active_days'] >= 5)
]

# 短期集中型
focused_users = non_creators[
    (non_creators['total_messages'] >= 20) &
    (non_creators['active_days'] > 1) &
    (non_creators['active_days'] < 5)
]

# 多Bot探索型
explorer_users = non_creators[
    (non_creators['bots_used'] >= 2)
]

print(f"🔥 单日爆发型（20+ msgs, 1天）: {len(burst_users)} 位")
print(f"   特征：短时间高强度使用，可能有紧急需求")
print(f"   代表：User {burst_users.nlargest(1, 'total_messages')['user_id'].values[0] if len(burst_users) > 0 else 'N/A'}")
print()

print(f"📈 长期粘性型（20+ msgs, 5+天）: {len(sticky_users)} 位")
print(f"   特征：长期持续使用，形成习惯")
print(f"   代表：User {sticky_users.nlargest(1, 'total_messages')['user_id'].values[0] if len(sticky_users) > 0 else 'N/A'}")
print()

print(f"🎯 短期集中型（20+ msgs, 2-4天）: {len(focused_users)} 位")
print(f"   特征：短期内高频使用，可能项目驱动")
print(f"   代表：User {focused_users.nlargest(1, 'total_messages')['user_id'].values[0] if len(focused_users) > 0 else 'N/A'}")
print()

print(f"🔍 多Bot探索型（2+ bots）: {len(explorer_users)} 位")
print(f"   特征：尝试多个工具，对生态有认知")
if len(explorer_users) > 0:
    print(f"   代表：User {explorer_users.nlargest(1, 'total_messages')['user_id'].values[0]}")
print()

# 4. 关键洞察：为什么他们没有转化？
print("4️⃣ 关键洞察：Power Users为什么没有转化？")
print()

insights = {
    "认知差距假设": {
        "证据": [
            f"{len(super_users)} 位超级用户（25+ msgs）全部未转化",
            f"User 39120797 发送了131条消息但未创建bot",
            f"只有 {len(explorer_users)} 位用户尝试了2+个bot，说明对生态认知有限",
            "报告指出：营销bot没有提到ShellAgent"
        ],
        "可信度": "90%",
        "验证方法": "直接询问是否知道可以创建bot"
    },

    "需求已满足假设": {
        "证据": [
            f"平均每小时消息数较高，说明效率可接受",
            f"{len(burst_users)} 位单日爆发型用户，完成任务即离开",
            "Hook Generator 覆盖82.9%用户，可能已满足基本需求"
        ],
        "可信度": "60%",
        "验证方法": "询问当前bot的局限性和未满足需求"
    },

    "创建门槛过高假设": {
        "证据": [
            "需要BotFather token（技术门槛）",
            "需要等待10分钟（耐心门槛）",
            "Remix功能0%使用率（摩擦太大）"
        ],
        "可信度": "70%",
        "验证方法": "询问是否愿意投入时间创建"
    },

    "价值主张不清晰假设": {
        "证据": [
            "用户不理解为什么要创建自己的bot",
            "当前bot已够用，缺少定制化动机",
            "没有看到其他创作者的成功案例"
        ],
        "可信度": "65%",
        "验证方法": "询问对定制化bot的理解和兴趣"
    }
}

for hypothesis, details in insights.items():
    print(f"💡 {hypothesis}")
    print(f"   可信度: {details['可信度']}")
    print(f"   证据:")
    for evidence in details['证据']:
        print(f"     - {evidence}")
    print(f"   验证方法: {details['验证方法']}")
    print()

# ============================================================================
# 第二部分：从目标倒推Reach Out策略
# ============================================================================

print("=" * 80)
print("🎯 第二部分：从目标倒推REACH OUT策略")
print("=" * 80)
print()

print("1️⃣ 核心目标设定")
print()

goals = {
    "主目标": {
        "描述": "将power users转化为bot创建者",
        "成功指标": "5-7位新创建者（转化率7-10%）",
        "时间框架": "30天"
    },

    "次要目标": {
        "描述": "理解未转化的根本原因",
        "成功指标": "获得42位高参与度用户的转化障碍清单",
        "时间框架": "14天"
    },

    "第三目标": {
        "描述": "建立用户关系，为长期转化铺路",
        "成功指标": "20+位用户回复，建立沟通渠道",
        "时间框架": "7天"
    }
}

for goal_type, details in goals.items():
    print(f"{goal_type}: {details['描述']}")
    print(f"  成功指标: {details['成功指标']}")
    print(f"  时间框架: {details['时间框架']}")
    print()

print("2️⃣ 目标倒推问题设计框架")
print()

question_framework = {
    "开场破冰": {
        "目标": "建立连接，展示关注",
        "问题类型": "观察型 + 感谢型",
        "预期回复率": "60-70%"
    },

    "需求探索": {
        "目标": "理解当前需求和痛点",
        "问题类型": "开放式 + 场景化",
        "预期回复率": "40-50%"
    },

    "认知检查": {
        "目标": "验证'认知差距'假设",
        "问题类型": "Yes/No + 解释",
        "预期回复率": "30-40%"
    },

    "障碍识别": {
        "目标": "发现转化的具体障碍",
        "问题类型": "选择题 + 开放",
        "预期回复率": "25-35%"
    },

    "价值展示": {
        "目标": "教育定制化bot的价值",
        "问题类型": "案例 + 对比",
        "预期回复率": "20-30%"
    },

    "软性CTA": {
        "目标": "引导试用Playground",
        "问题类型": "邀请型 + 低承诺",
        "预期回复率": "15-25%"
    }
}

for stage, details in question_framework.items():
    print(f"阶段：{stage}")
    print(f"  目标: {details['目标']}")
    print(f"  问题类型: {details['问题类型']}")
    print(f"  预期回复率: {details['预期回复率']}")
    print()

# ============================================================================
# 第三部分：用户分层Reach Out策略
# ============================================================================

print("=" * 80)
print("📋 第三部分：用户分层REACH OUT策略")
print("=" * 80)
print()

print("Tier 1: 超级VIP用户（Top 3） - 个性化深度访谈")
print("-" * 80)
print()

tier1_users = top_10.head(3)
for idx, user in tier1_users.iterrows():
    print(f"User {user['user_id']} ({user['total_messages']} msgs)")
    print(f"  策略: 1对1深度访谈（30-45分钟）")
    print(f"  触达方式: Telegram私信 + 可选视频通话")
    print(f"  激励: $50 Amazon礼品卡 / 终身Pro账户")
    print(f"  预期产出: 深度需求洞察 + 50%转化概率")
    print()

print("Tier 2: 高价值用户（Top 4-10） - 结构化问卷")
print("-" * 80)
print()
tier2_users = top_10.iloc[3:10]
print(f"7位用户: {', '.join([str(u) for u in tier2_users['user_id'].values])}")
print(f"  策略: 结构化问卷（10-15分钟）")
print(f"  触达方式: Telegram私信 + Google Form")
print(f"  激励: 提前体验新功能 / $20礼品卡")
print(f"  预期产出: 量化数据 + 30%转化概率")
print()

print("Tier 3: 高参与用户（11-42） - 快速调研")
print("-" * 80)
print()
tier3_users = high_engagement[~high_engagement['user_id'].isin(top_10['user_id'])]
print(f"{len(tier3_users)} 位用户")
print(f"  策略: 3-5个快速问题")
print(f"  触达方式: Telegram私信")
print(f"  激励: 感谢信 + 社区认可")
print(f"  预期产出: 趋势验证 + 10%转化概率")
print()

# ============================================================================
# 输出分析结果
# ============================================================================

# 保存超级用户列表
output_data = {
    'super_users': super_users.to_dict('records'),
    'behavior_patterns': {
        'burst': burst_users['user_id'].tolist(),
        'sticky': sticky_users['user_id'].tolist(),
        'focused': focused_users['user_id'].tolist(),
        'explorer': explorer_users['user_id'].tolist()
    },
    'tier1_users': tier1_users['user_id'].tolist(),
    'tier2_users': tier2_users['user_id'].tolist(),
    'insights': insights,
    'goals': goals,
    'question_framework': question_framework
}

# 保存为JSON
output_file = '/Users/hancezhang/Claude code exp/product_op/data/latest_results/power_user_analysis.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)

print(f"✅ 分析结果已保存到: {output_file}")
print()

# 保存CSV格式的超级用户列表
super_users_output = super_users.copy()
super_users_output['tier'] = super_users_output['user_id'].apply(
    lambda x: 'Tier 1' if x in tier1_users['user_id'].values
    else ('Tier 2' if x in tier2_users['user_id'].values
    else 'Tier 3')
)

csv_file = '/Users/hancezhang/Claude code exp/product_op/data/latest_results/power_users_reach_out_list.csv'
super_users_output.to_csv(csv_file, index=False)
print(f"✅ Power Users列表已保存到: {csv_file}")
print()

print("=" * 80)
print("分析完成！")
print("=" * 80)
