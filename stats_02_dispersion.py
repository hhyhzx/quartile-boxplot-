"""
人教版八年级数学下册 第二十四章 — 数据的离散程度 动画演示
涵盖: 离差、离差平方和、方差、标准差
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def clamp(v):
    return max(0.0, min(1.0, v))

BASE = 'E:/maths_work'

# Two datasets with same mean but different spread
data_a = np.array([72, 74, 76, 78, 80, 82, 84, 86, 88, 90])
data_b = np.array([60, 65, 70, 75, 80, 85, 90, 95, 100, 80])
mean_a = np.mean(data_a)
mean_b = np.mean(data_b)
var_a = np.var(data_a)
var_b = np.var(data_b)
q_a = np.sum((data_a - mean_a)**2)
q_b = np.sum((data_b - mean_b)**2)

# ============================================================
# Figure 1: 离差 动画 — 从"平衡点"看偏差
# ============================================================
fig1, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(10, 6.5), gridspec_kw={'height_ratios': [1, 0.7]})
fig1.patch.set_facecolor('#FEFEFE')

ax_top.set_xlim(-0.5, len(data_a) + 0.5)
ax_top.set_ylim(55, 100)
ax_top.set_xticks(range(len(data_a)))
ax_top.set_xticklabels([f'#{i+1}' for i in range(len(data_a))], fontsize=9)
ax_top.set_ylabel('成绩（分）', fontsize=12)
ax_top.set_title('离差：每个数据到平均数的"距离"', fontsize=16, fontweight='bold', color='#1D3557')
for spine in ax_top.spines.values():
    spine.set_visible(False)
ax_top.grid(axis='y', alpha=0.2)

# Mean line
mean_line = ax_top.axhline(y=mean_a, color='#E63946', lw=2, ls='--', alpha=0, zorder=3)

# Data points
data_points = []
for i, val in enumerate(data_a):
    pt, = ax_top.plot(i, val, 'o', ms=18, color='#457B9D', zorder=5, markeredgecolor='white', markeredgewidth=2)
    data_points.append(pt)

# Deviation lines (vertical)
dev_lines = []
dev_texts = []
for i, val in enumerate(data_a):
    dev = val - mean_a
    l, = ax_top.plot([i, i], [mean_a, val], '-', lw=2.5, alpha=0, zorder=2,
                     color='#E63946' if dev < 0 else '#2A9D8F')
    dev_lines.append(l)
    t = ax_top.text(i + 0.25, (mean_a + val) / 2, '', fontsize=9, alpha=0, fontweight='bold')
    dev_texts.append((t, dev))

# Sum display
ax_bot.set_xlim(0, 10)
ax_bot.set_ylim(0, 5)
ax_bot.axis('off')
sum_title = ax_bot.text(5, 4.5, '', fontsize=14, ha='center', fontweight='bold', color='#1D3557', alpha=0)
sum_detail = ax_bot.text(5, 3.2, '', fontsize=10, ha='center', color='#333333', alpha=0)
sum_note = ax_bot.text(5, 2, '', fontsize=11, ha='center', color='#666666', alpha=0)
q_formula = ax_bot.text(5, 1, '', fontsize=13, ha='center', color='#E63946', fontweight='bold', alpha=0)

def animate_dispersion(frame):
    t = frame / 100
    if t > 1.0:
        t = 1.0

    # Phase 1: mean line (0~0.2)
    if t <= 0.2:
        mean_line.set_alpha(t / 0.2)
    else:
        mean_line.set_alpha(1.0)

    # Phase 2: deviations (0.2~0.6)
    if 0.2 < t <= 0.6:
        p = clamp((t - 0.2) / 0.4)
        for l in dev_lines:
            l.set_alpha(p)
        for txt, dev in dev_texts:
            txt.set_text(f'{dev:+.1f}')
            txt.set_alpha(p)
        sum_title.set_text(f'离差平方和 Q = Σ(x_i - x)^2 = {q_a:.1f}')
        sum_title.set_alpha(p)

    if t > 0.6:
        for l in dev_lines:
            l.set_alpha(1.0)
        for txt, dev in dev_texts:
            txt.set_text(f'{dev:+.1f}')
            txt.set_alpha(1.0)
        sum_title.set_text(f'离差平方和 Q = Σ(x_i - x)^2 = {q_a:.1f}')
        sum_title.set_alpha(1.0)

    # Phase 3: formula (0.6~0.85)
    if 0.6 < t <= 0.85:
        p = clamp((t - 0.6) / 0.25)
        parts = ' + '.join([f'({data_a[i]:.0f}-{mean_a:.0f})^2' for i in range(5)])
        sum_detail.set_text(f'= {parts}\n  + ... = {q_a:.1f}')
        sum_detail.set_alpha(p)
        sum_note.set_text('离差平方相加，避免正负抵消')
        sum_note.set_alpha(p)

    if t > 0.85:
        sum_detail.set_text(f'= {q_a:.1f}')
        sum_detail.set_alpha(1.0)
        sum_note.set_text('离差平方相加，避免正负抵消')
        sum_note.set_alpha(1.0)

    # Phase 4: variance (0.85~1.0)
    if 0.85 < t <= 1.0:
        p = clamp((t - 0.85) / 0.15)
        q_formula.set_text(f'方差 s^2 = Q / n = {q_a:.1f} / {len(data_a)} = {var_a:.1f}\n标准差 s = sqrt(s^2) = {np.sqrt(var_a):.1f}')
        q_formula.set_alpha(p)

    if t >= 1.0:
        q_formula.set_text(f'方差 s^2 = Q / n = {q_a:.1f} / {len(data_a)} = {var_a:.1f}\n标准差 s = sqrt(s^2) = {np.sqrt(var_a):.1f}')
        q_formula.set_alpha(1.0)

    return []

ani1 = animation.FuncAnimation(fig1, animate_dispersion, frames=100, interval=60, blit=False, repeat=True)
ani1.save(f'{BASE}/stats_dispersion_animation.gif', writer='pillow', fps=10, dpi=72)
fig1.savefig(f'{BASE}/stats_dispersion_frame.png', dpi=150, bbox_inches='tight')
plt.close()
print('Figure 1 (Dispersion) done')

# ============================================================
# Figure 2: 两组数据对比 — 平均数相同，方差不同
# ============================================================
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
fig2.patch.set_facecolor('#FEFEFE')

for ax, d, label, color in [(ax1, data_a, 'A班', '#457B9D'), (ax2, data_b, 'B班', '#F4A261')]:
    m = np.mean(d)
    v = np.var(d)
    sd = np.std(d)
    ax.set_xlim(55, 105)
    ax.set_ylim(-0.5, 3.5)
    ax.set_title(f'{label}: 平均数={m:.1f}, 方差={v:.1f}, 标准差={sd:.1f}',
                 fontsize=14, fontweight='bold', color=color)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis='x', alpha=0.2)
    ax.set_yticks([])

    for vv in d:
        ax.plot(vv, 0.5 + np.random.uniform(-0.2, 0.2), 'o', ms=14, color=color, zorder=3,
                markeredgecolor='white', markeredgewidth=1.5)

    ax.axvline(x=m, color='#E63946', lw=3, ls='-', zorder=5)

    # Show range
    ax.annotate('', xy=(m - sd, 2.5), xytext=(m + sd, 2.5),
                arrowprops=dict(arrowstyle='<->', color='#1D3557', lw=2.5))
    ax.text(m, 2.9, f'1个标准差范围 = {sd:.1f}', ha='center', fontsize=11, color='#1D3557', fontweight='bold')
    ax.text(m, 2.2, f'方差 s^2 = {v:.1f}', ha='center', fontsize=11, color='#E63946')

plt.suptitle('平均数相同 (80分)，看方差区分"整齐"还是"参差不齐"', fontsize=15, fontweight='bold', color='#1D3557', y=1.01)
plt.tight_layout()
fig2.savefig(f'{BASE}/stats_variance_compare.png', dpi=150, bbox_inches='tight')
plt.close()
print('Figure 2 (Variance Compare) done')

# ============================================================
# Figure 3: 离差平方和计算全过程 (静态详解)
# ============================================================
fig3, ax = plt.subplots(figsize=(14, 8))
fig3.patch.set_facecolor('#FEFEFE')
ax.set_xlim(0, 10)
ax.set_ylim(0, 9)
ax.axis('off')

# Data
d_example = np.array([2, 4, 4, 6, 9])
m_example = np.mean(d_example)

ax.text(5, 8.5, '离差 → 离差平方和 → 方差：完整计算流程', fontsize=18, ha='center',
        fontweight='bold', color='#1D3557')

# Table
col_headers = ['数据 x_i', '离差 x_i - x', '(离差)^2']
col_x = [2, 4.5, 7.5]
row_y = [7.3, 6.5, 5.7, 4.9, 4.1]

# Header
for j, (hdr, cx) in enumerate(zip(col_headers, col_x)):
    ax.text(cx, 7.8, hdr, ha='center', fontsize=12, fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1D3557'))

for i, v in enumerate(d_example):
    dev = v - m_example
    sq = dev ** 2
    row = [str(v), f'{dev:+.1f}', f'{sq:.1f}']
    for j, (txt, cx) in enumerate(zip(row, col_x)):
        bg = '#FFF8F0' if i % 2 == 0 else 'white'
        ax.text(cx, row_y[i], txt, ha='center', fontsize=12, fontweight='bold' if j == 0 else 'normal',
                color='#333' if j == 0 else ('#E63946' if j == 2 else '#457B9D'),
                bbox=dict(boxstyle='round,pad=0.2', facecolor=bg, edgecolor='#DDD'))

# Sum row
ax.text(col_x[0], 3.4, f'和 = {np.sum(d_example)}', ha='center', fontsize=13, fontweight='bold', color='#1D3557')
ax.text(col_x[1], 3.4, '和 = 0（正负抵消！）', ha='center', fontsize=12, color='#E63946', fontweight='bold')
q_val = np.sum((d_example - m_example)**2)
ax.text(col_x[2], 3.4, f'Q = {q_val:.1f}', ha='center', fontsize=13, fontweight='bold', color='#2A9D8F')

# Highlight box
from matplotlib.patches import FancyBboxPatch
box = FancyBboxPatch((6.5, 3.0), 2.5, 1.0, boxstyle="round,pad=0.1", facecolor='#E5FFF0',
                      edgecolor='#2A9D8F', lw=2.5)
ax.add_patch(box)

# Bottom formulas
ax.text(5, 2.2, f'离差平方和 Q = Σ(x_i - x)^2 = {q_val:.1f}', fontsize=15, ha='center',
        fontweight='bold', color='#1D3557',
        bbox=dict(boxstyle='round', facecolor='#E5F0FF', alpha=0.8, edgecolor='#457B9D'))
ax.text(5, 1.3, f'方差 s^2 = Q / n = {q_val:.1f} / {len(d_example)} = {np.var(d_example):.1f}',
        fontsize=15, ha='center', fontweight='bold', color='#E63946',
        bbox=dict(boxstyle='round', facecolor='#FFE5E5', alpha=0.8, edgecolor='#E63946'))
ax.text(5, 0.5, f'标准差 s = √(s^2) = √({np.var(d_example):.1f}) = {np.std(d_example):.2f}',
        fontsize=14, ha='center', color='#333')

plt.tight_layout()
fig3.savefig(f'{BASE}/stats_deviation_calc.png', dpi=150, bbox_inches='tight')
plt.close()
print('Figure 3 (Calculation) done')

print('\n=== 离散程度: All 3 figures done ===')
