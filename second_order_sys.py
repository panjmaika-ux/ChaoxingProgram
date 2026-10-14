import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import control as ct

# ===================== 绘图全局配置（解决负号、数学公式乱码）=====================
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'

# 初始化session_state，存储多条对比曲线
if "curve_list" not in st.session_state:
    st.session_state["curve_list"] = []

# ===================== Streamlit页面中文UI（网页界面，不会乱码）=====================
st.set_page_config(page_title="二阶系统仿真探究", layout="wide")
st.title("二阶系统仿真探究：s平面极点与阶跃响应联动")

st.latex(r"G(s)=\frac{\omega_n^2}{s^2 + 2\zeta\omega_n s+\omega_n^2}")

col1, col2 = st.columns(2)
with col1:
    zeta = st.slider("阻尼比 $\\zeta$", min_value=0.01, max_value=1.2, value=0.707, step=0.01)
with col2:
    wn = st.slider("自然振荡频率 $\\omega_n$(rad/s)", min_value=0.2, max_value=3.0, value=1.0, step=0.05)

# 构造二阶系统传递函数
num = [wn ** 2]
den = [1, 2 * zeta * wn, wn ** 2]
sys = ct.TransferFunction(num, den)

# 计算阶跃响应
t = np.linspace(0, 12, 1000)
t_out, y_out = ct.step_response(sys, T=t)

# 求极点
poles = sys.poles()

# ======================== 绘图：Unit Step Response 单位阶跃响应 ========================
fig1, ax1 = plt.subplots(figsize=(8, 6))
# 当前滑块对应的曲线
ax1.plot(t_out, y_out, label=f"$\zeta$={zeta:.3f}, $\omega_n$={wn:.2f}", linewidth=2)
# 绘制已经保存的叠加对比曲线
for (wn_s, zeta_s, t_s, y_s) in st.session_state["curve_list"]:
    ax1.plot(t_s, y_s, alpha=0.6, label=f"saved:$\zeta$={zeta_s:.2f},$\omega_n$={wn_s:.2f}")

ax1.set_title("Unit Step Response")
ax1.set_xlabel("$t$ / s")
ax1.set_ylabel("$c(t)$")
ax1.grid(True)
ax1.legend(loc="upper right")
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 1.15)

# ======================== 绘图：S‑plane Pole Map s平面极点分布 ========================
fig2, ax2 = plt.subplots(figsize=(8, 6))
# 画等阻尼圆
theta = np.linspace(0, 2 * np.pi, 200)
xc = wn * np.cos(theta)
yc = wn * np.sin(theta)
ax2.plot(xc, yc, "k--", alpha=0.6, label=r"$\omega_n$ circle")

# 绘制极点
ax2.scatter(np.real(poles), np.imag(poles), marker="x", color="red", s=120, linewidth=2)

ax2.set_title("S‑plane Pole Map")
ax2.set_xlabel("$\\sigma$")
ax2.set_ylabel("$j\\omega$")
ax2.grid(True)
ax2.axhline(0, color="k", lw=1)
ax2.axvline(0, color="k", lw=1)
ax2.legend(loc="lower right")
ax2.set_aspect("equal")

# 双列并排展示两张图
col_a, col_b = st.columns(2)
with col_a:
    st.pyplot(fig1)
with col_b:
    st.pyplot(fig2)

# ============ 输出系统极点信息（网页中文，无乱码）============
st.subheader("系统极点信息")
pole_text = ""
for idx, p in enumerate(poles):
    pole_text += f"极点{idx+1}: {p:.3f}\n"
st.code(pole_text)

# ===================== 保存 / 清空按钮（原样保留你的逻辑） =====================
c1, c2 = st.columns(2)
with c1:
    if st.button("保存本组曲线，用于叠加对比"):
        st.session_state["curve_list"].append((wn, zeta, t_out, y_out))
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
