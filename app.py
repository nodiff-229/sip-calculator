import streamlit as st

st.set_page_config(page_title="基金定投计算器", page_icon="📈", layout="wide")

st.title("📈 基金定投计算器")
st.markdown("---")

# 预设基金列表
FUNDS = [
    "南方纳斯达克 100 指数发起 I",
    "博时标普 500 联接 E",
    "广发中证 A500ETF 联接 A",
    "易方达中证红利 ETF 联接发起式 A",
    "易方达恒生科技 ETF 联接 A",
]

# 侧边栏输入
st.sidebar.header("💰 投资设置")
monthly_amount = st.sidebar.number_input(
    "每月定投总金额 (元)",
    min_value=0.0,
    value=5000.0,
    step=100.0,
)

st.sidebar.markdown("---")
st.sidebar.header("📊 基金组合比例")

# 为每个基金创建比例输入
allocations = {}
for fund in FUNDS:
    short_name = fund.split(" ")[0][:4]
    allocations[fund] = st.sidebar.number_input(
        f"{short_name}...",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=1.0,
    )

# 计算总比例
total_allocation = sum(allocations.values())

# 显示总比例并验证
if total_allocation != 100:
    st.error(f"⚠️ 当前比例总和为 {total_allocation:.1f}%，请调整为 100%")
else:
    st.success("✅ 组合比例正确 (100%)")

# 计算结果
if monthly_amount > 0 and total_allocation == 100:
    st.markdown("## 📋 定投计划详情")
    
    # 创建结果数据
    results = []
    for fund in FUNDS:
        monthly = monthly_amount * (allocations[fund] / 100)
        weekly = monthly / 4
        results.append({
            "基金名称": fund,
            "比例": f"{allocations[fund]:.1f}%",
            "每月定投 (元)": f"{monthly:.2f}",
            "每周定投 (元)": f"{weekly:.2f}",
        })
    
    # 显示表格
    st.dataframe(results, use_container_width=True, hide_index=True)
    
    # 显示汇总
    col1, col2 = st.columns(2)
    with col1:
        st.metric("每月总投资", f"¥{monthly_amount:.2f}")
    with col2:
        st.metric("每周总投资", f"¥{monthly_amount/4:.2f}")
    
    # 投资提示
    st.markdown("---")
    st.markdown("### 💡 定投提示")
    st.info("""
    - **定投日建议**: 每月发工资后 1-3 天
    - **周投分配**: 可将周投金额分为 4 次，每周固定日期买入
    - **长期持有**: 建议持有周期 3-5 年以上
    - **动态再平衡**: 每半年检查一次比例，偏离超过 5% 时调整
    """)

# 页脚
st.markdown("---")
st.caption("💡 投资有风险，入市需谨慎。本工具仅供参考，不构成投资建议。")
