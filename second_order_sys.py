import matplotlib.pyplot as plt
# ==========解决云平台中文方块乱码 新增开始==========
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示方框
# ==========解决云平台中文方块乱码 新增结束==========

import streamlit as st
import numpy as np
import control as ct


import streamlit as st
import control as ct
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="二阶系统时域探究", layout="wide")
st.title("二阶系统仿真探究：s平面极点与阶跃响应联动")
st.markdown(r"闭环传递函数：$G(s)=\dfrac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}$")

# 会话状态：保存多条叠加曲线 (wn, zeta, t, y)
if "curve_list" not in st.session_state:
    st.session_state["curve_list"] = []

# ==========两个可调节参数滑块==========
col_slider1, col_slider2 = st.columns(2)
with col_slider1:
    zeta = st.slider("阻尼比 ζ", min_value=0.0, max_value=2.0, step=0.05, value=0.707)
with col_slider2:
    wn = st.slider("自然振荡频率 ωₙ (rad/s)", min_value=0.5, max_value=3.0, step=0.1, value=1.0)

# 构建二阶系统
num = [wn ** 2]
den = [1, 2 * zeta * wn, wn ** 2]
sys = ct.TransferFunction(num, den)

# 阶跃响应，时间范围根据ωn自适应
t_end = 12 / wn
t, y = ct.step_response(sys, T=np.linspace(0, t_end, 1000))
poles = sys.poles()

col1, col2 = st.columns(2)

with col1:
    st.subheader("单位阶跃响应")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(t, y, label=f"$\zeta$={zeta:.3f}, $\omega_n$={wn:.2f}", linewidth=1.5)
    # 绘制已经保存的叠加曲线
    for w_save, z_save, t_save, y_save in st.session_state["curve_list"]:
        ax1.plot(t_save, y_save, label=f"$\zeta$={z_save:.3f}, $\omega_n$={w_save:.2f}", linestyle="--")
    ax1.set_xlabel("t / s")
    ax1.set_ylabel("c(t)")
    ax1.grid(True)
    ax1.legend(fontsize="x-small")
    ax1.set_title("阶跃响应")
    st.pyplot(fig1)

with col2:
    st.subheader("s平面极点分布")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    # 圆半径跟随当前ωn实时变化
    theta = np.linspace(0, 2 * np.pi, 200)
    ax2.plot(wn * np.cos(theta), wn * np.sin(theta), "k--", alpha=0.5, label=r"半径$\omega_n$")
    ax2.axhline(0, color="k", lw=1)
    ax2.axvline(0, color="k", lw=1)
    ax2.scatter(np.real(poles), np.imag(poles), marker="x", s=80, c="red", label="闭环极点")
    ax2.set_xlabel(r"$\sigma$ (实轴)")
    ax2.set_ylabel(r"$j\omega$ (虚轴)")
    ax2.set_aspect("equal")
    ax2.grid(True)
    ax2.legend()
    ax2.set_title("s平面极点")
    st.pyplot(fig2)

# 保存 / 清空按钮
c1, c2 = st.columns(2)
with c1:
    if st.button("保存本组曲线，用于叠加对比"):
        st.session_state["curve_list"].append((wn, zeta, t, y))
        st.success(f"已保存：ζ={zeta:.3f}，ωₙ={wn:.2f}")
with c2:
    if st.button("清空叠加曲线列表"):
        st.session_state["curve_list"].clear()
        st.info("已清空叠加曲线")

st.markdown("### 📝课堂探究任务")
st.markdown("""
**任务A（固定 ωₙ=1 rad/s）**
依次设置 ζ = 0、0.3、0.707、1、1.5，每设置一组点击【保存本组曲线】，观察阻尼比对响应与极点的影响。

**任务B（固定 ζ=0.707）**
依次设置 ωₙ =1、2、3 rad/s，保存曲线，观察自然振荡频率如何改变系统响应快慢。

> 观察要点：
> 1. ζ主要影响超调量（平稳性）；
> 2. ωₙ主要改变响应速度，不改变超调大小；
> 3. s平面圆半径跟随ωₙ同步缩放。
""")
