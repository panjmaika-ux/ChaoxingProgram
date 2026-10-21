import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------------- 页面基础设置 ----------------------
st.set_page_config(page_title="二阶系统仿真", layout="wide")

# 【修改点1】替换标题，控制字体大小，不再用st.title()大标题
st.markdown("# Streamlit交互式仿真工具")
st.markdown("二阶系统传递函数：$G(s)=\\dfrac{\\omega_n^2}{s^2+2\\zeta\\omega_n s+\\omega_n^2}$")

# 初始化session_state，保存多条曲线
if "curve_list" not in st.session_state:
    st.session_state["curve_list"] = []

# ---------------------- 参数滑块区域 ----------------------
col1, col2 = st.columns(2)
with col1:
    zeta = st.slider("阻尼比 ζ", min_value=0.0, max_value=1.8, value=0.707, step=0.01)
with col2:
    wn = st.slider("自然振荡频率 ωₙ (rad/s)", min_value=0.2, max_value=3.0, value=1.0, step=0.1)

# ---------------------- 计算阶跃响应 ----------------------
t = np.linspace(0, 12, 1000)
# 二阶系统单位阶跃响应
if zeta < 1:
    wd = wn * np.sqrt(1 - zeta**2)
    y_out = 1 - np.exp(-zeta * wn * t) * (np.cos(wd * t) + (zeta / np.sqrt(1 - zeta**2)) * np.sin(wd * t))
elif zeta == 1:
    y_out = 1 - (1 + wn * t) * np.exp(-wn * t)
else:
    s1 = -wn * zeta + wn * np.sqrt(zeta**2 - 1)
    s2 = -wn * zeta - wn * np.sqrt(zeta**2 - 1)
    y_out = 1 + (s2/(s1-s2))*np.exp(s1*t) + (s1/(s2-s1))*np.exp(s2*t)

# 计算极点
p1 = -zeta * wn + 1j * wn * np.sqrt(max(1-zeta**2,0))
p2 = -zeta * wn - 1j * wn * np.sqrt(max(1-zeta**2,0))

# ---------------------- 绘图（两张图统一尺寸，关键修改） ----------------------
# 【修改点2】统一画布figsize，两张图尺寸一致，缩小画面
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

# 图1：单位阶跃响应 Unit Step Response
ax1.plot(t, y_out, "r", label=f"current: ζ={zeta:.3f}, ωₙ={wn:.2f}")
# 绘制历史保存曲线
for (wn_save, zeta_save, t_save, y_save, color) in st.session_state["curve_list"]:
    ax1.plot(t_save, y_save, color=color, label=f"ζ={zeta_save:.3f},ωₙ={wn_save:.2f}")
ax1.set_title("Unit Step Response")
ax1.set_xlabel("t / s")
ax1.set_ylabel("y(t)")
ax1.grid(True)
ax1.legend(fontsize=8)
ax1.set_xlim(0,12)

# 图2：S-plane Pole Map
# 绘制单位圆(ωn圆)
theta_circle = np.linspace(0, np.pi*2, 200)
ax2.plot(wn*np.cos(theta_circle), wn*np.sin(theta_circle), "k--", lw=1, label="$\\omega_n$ circle")
ax2.plot(np.real(p1), np.imag(p1), "rx", markersize=10)
ax2.plot(np.real(p2), np.imag(p2), "rx", markersize=10)
# 绘制历史保存极点
for (wn_save, zeta_save, t_save, y_save, color) in st.session_state["curve_list"]:
    p1s = -zeta_save*wn_save + 1j*wn_save*np.sqrt(max(1-zeta_save**2,0))
    p2s = -zeta_save*wn_save - 1j*wn_save*np.sqrt(max(1-zeta_save**2,0))
    ax2.plot(np.real(p1s), np.imag(p1s), marker="x", c=color, markersize=9)
    ax2.plot(np.real(p2s), np.imag(p2s), marker="x", c=color, markersize=9)
ax2.set_title("S-plane Pole Map")
ax2.set_xlabel("σ")
ax2.set_ylabel("jω")
ax2.grid(True)
ax2.axhline(y=0, color="k", lw=0.8)
ax2.axvline(x=0, color="k", lw=0.8)
ax2.legend(fontsize=8)

plt.tight_layout()
st.pyplot(fig)

# ---------------------- 极点信息展示 ----------------------
st.subheader("系统极点信息")
st.write(f"极点1：{p1:.3f}")
st.write(f"极点2：{p2:.3f}")

# ---------------------- 保存 / 清空按钮（完全保留原有逻辑） ----------------------
# 准备配色，新增曲线自动分配颜色
color_list = ["#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd", "#8c564b"]
c1, c2 = st.columns(2)
with c1:
    if st.button("保存本组曲线，用于叠加对比"):
        pick_color = color_list[len(st.session_state["curve_list"]) % len(color_list)]
        st.session_state["curve_list"].append((wn, zeta, t, y_out, pick_color))
        st.success(f"已保存：ζ={zeta:.3f}，ωₙ={wn:.2f}")
with c2:
    if st.button("清空叠加曲线列表"):
        st.session_state["curve_list"].clear()
        st.info("已清空叠加曲线")

# ---------------------- 课堂探究任务（保留原文） ----------------------
st.markdown("### 📝操作说明")
st.markdown("""
> 1. 请拖动滑块改变参数值；
> 2. 每设置一组参数点击【保存本组曲线，用于叠加对比】按钮，可观察不同参数对应阶跃响应曲线及极点分布；
> 3. 同一参数对应曲线和极点颜色一致。
> 4. s平面圆半径跟随ωₙ同步缩放。
""")
