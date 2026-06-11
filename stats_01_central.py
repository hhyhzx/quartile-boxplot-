"""
人教版八年级数学下册 第二十四章 — 数据的集中趋势 动画演示
涵盖: 算术平均数、加权平均数、中位数、众数
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
data = np.array([62, 68, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92, 95, 96, 98])
data_sort = np.sort(data)
n = len(data)
mean_val = np.mean(data)
median_val = np.median(data)
# mode: find most frequent (no repeats here, use the value near center)
from scipy import stats as sp_stats
mode_result = sp_stats.mode(data, keepdims=True)
mode_val = mode_result.mode[0]

# ============================================================
# Figure 1: 算术平均数动画 (平衡天平)
# ============================================================
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), gridspec_kw={'height_ratios': [1.2, 1]})
fig1.patch.set_facecolor('#FEFEFE')

ax1.set_xlim(55, 105)
ax1.set_ylim(-2, 12)
ax1.set_title('算术平均数 — 数据的"平衡点"', fontsize=16, fontweight='bold', color='#1D3557')
ax1.set_xlabel('成绩（分）', fontsize=12)
ax1.set_yticks([])
for spine in ax1.spines.values():
    spine.set_visible(False)
ax1.grid(axis='x', alpha=0.3)

# Data points on number line
dots = []
for val in data_sort:
    d, = ax1.plot(val, 0.5 + np.random.uniform(-0.3, 0.3), 'o', ms=12, color='#457B9D',
                  zorder=5, markeredgecolor='white', markeredgewidth=1.2)
    dots.append(d)

# Mean indicator (animated)
mean_arrow = ax1.annotate('', xy=(mean_val, 0), xytext=(mean_val, 3),
                          arrowprops=dict(arrowstyle='->', color='#E63946', lw=3), alpha=0)
mean_text = ax1.text(mean_val, 3.5, '', fontsize=13, color='#E63946', ha='center', fontweight='bold', alpha=0)

# 天平效果 — 左右两边的虚线连接
left_connectors = []
right_connectors = []
for val in data_sort:
    if val < mean_val:
        l, = ax1.plot([val, mean_val], [2.2, 2.8], 'r-', lw=0.8, alpha=0, zorder=1)
        left_connectors.append(l)
    elif val > mean_val:
        r, = ax1.plot([mean_val, val], [2.2, 2.8], 'b-', lw=0.8, alpha=0, zorder=1)
        right_connectors.append(r)

# Deviation labels
dev_labels = []
for i, val in enumerate(data_sort):
    dev = val - mean_val
    if abs(dev) > 2:
        t = ax1.text(val, 1.8, '', fontsize=7, ha='center', alpha=0, zorder=3)
        dev_labels.append((t, dev))

# Bottom axis: avg formula buildup
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 6)
ax2.axis('off')
formula_text = ax2.text(50, 3, '', fontsize=14, ha='center', va='center', alpha=0)
step_text = ax2.text(50, 1.5, '', fontsize=12, ha='center', color='#666666', alpha=0)

def animate_central(frame):
    t = frame / 120

    # Phase 1: show data (0~0.2)
    # Phase 2: animate mean calculation (0.2~0.5)
    if 0.2 < t <= 0.5:
        p = clamp((t - 0.2) / 0.3)
        mean_arrow.set_alpha(p)
        mean_text.set_text(f'平均数 = {mean_val:.1f}')
        mean_text.set_alpha(p)
        for l in left_connectors:
            l.set_alpha(p * 0.4)
        for r in right_connectors:
            r.set_alpha(p * 0.4)

    if t > 0.5:
        mean_arrow.set_alpha(1.0)
        mean_text.set_text(f'平均数 = {mean_val:.1f}')
        mean_text.set_alpha(1.0)
        for l in left_connectors:
            l.set_alpha(0.4)
        for r in right_connectors:
            r.set_alpha(0.4)

    # Phase 3: show deviations (0.5~0.7)
    if 0.5 < t <= 0.7:
        p = clamp((t - 0.5) / 0.2)
        for lbl, dev in dev_labels:
            lbl.set_text(f'{dev:+.1f}')
            lbl.set_alpha(p)

    if t > 0.7:
        for lbl, dev in dev_labels:
            lbl.set_text(f'{dev:+.1f}')
            lbl.set_alpha(1.0)

    # Phase 4: formula (0.7~1.0)
    if 0.7 < t <= 1.0:
        p = clamp((t - 0.7) / 0.3)
        formula_text.set_text(f'x = ({ " + ".join(str(v) for v in data_sort[:5]) }\n   + ... + {data_sort[-1]}) / {n} = {mean_val:.1f}')
        formula_text.set_alpha(p)
        step_text.set_text('所有数据之和 / 数据个数 → 数据的"重心"')
        step_text.set_alpha(p)

    return []

ani1 = animation.FuncAnimation(fig1, animate_central, frames=120, interval=50, blit=False, repeat=True)
ani1.save(f'{BASE}/stats_mean_animation.gif', writer='pillow', fps=10, dpi=72)
fig1.savefig(f'{BASE}/stats_mean_frame.png', dpi=150, bbox_inches='tight')
plt.close()
print('Figure 1 (Mean) done')

# ============================================================
# Figure 2: 中位数 vs 平均数 vs 众数 对比
# ============================================================
fig2, axes = plt.subplots(1, 3, figsize=(15, 5))
fig2.patch.set_facecolor('#FEFEFE')
titles = ['中位数 (Median)', '众数 (Mode)', '平均数 (Mean)']
colors_m = ['#2A9D8F', '#E9C46A', '#E63946']

for ax, title, color in zip(axes, titles, colors_m):
    ax.set_xlim(55, 105)
    ax.set_ylim(-0.5, 2.5)
    ax.set_title(title, fontsize=14, fontweight='bold', color=color)
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis='x', alpha=0.2)

    for val in data_sort:
        ax.plot(val, 0.8, 'o', ms=14, color='#457B9D', zorder=3, markeredgecolor='white', markeredgewidth=1)

# Median
axes[0].axvline(x=median_val, color=colors_m[0], lw=3, ls='-', zorder=5)
axes[0].text(median_val, 2.1, f'中位数 = {median_val:.0f}', ha='center', fontsize=13,
             color=colors_m[0], fontweight='bold')
axes[0].text(median_val, 1.6, '第8个（中间位置）', ha='center', fontsize=10, color='#666')

# Mode
axes[1].axvline(x=mode_val, color=colors_m[1], lw=3, ls='-', zorder=5)
axes[1].text(mode_val, 2.1, f'众数 = {mode_val:.0f}', ha='center', fontsize=13,
             color=colors_m[1], fontweight='bold')
axes[1].text(mode_val, 1.6, '出现次数最多', ha='center', fontsize=10, color='#666')

# Mean
axes[2].axvline(x=mean_val, color=colors_m[2], lw=3, ls='-', zorder=5)
axes[2].text(mean_val, 2.1, f'平均数 = {mean_val:.1f}', ha='center', fontsize=13,
             color=colors_m[2], fontweight='bold')
axes[2].text(mean_val, 1.6, f'总和/n = {mean_val:.1f}', ha='center', fontsize=10, color='#666')

plt.suptitle('三种集中趋势度量对比 （同一组数据: 15人成绩）', fontsize=16, fontweight='bold', color='#1D3557', y=1.01)
plt.tight_layout()
fig2.savefig(f'{BASE}/stats_compare_three.png', dpi=150, bbox_inches='tight')
plt.close()
print('Figure 2 (Compare) done')

# ============================================================
# Figure 3: 加权平均数 (期末总评)
# ============================================================
fig3, ax = plt.subplots(figsize=(10, 6))
fig3.patch.set_facecolor('#FEFEFE')

categories = ['平时作业', '课堂表现', '期中考试', '期末考试']
scores = [88, 92, 78, 85]
weights = [0.15, 0.15, 0.30, 0.40]
weighted_sum = sum(s * w for s, w in zip(scores, weights))
simple_avg = np.mean(scores)

x = np.arange(len(categories))
width = 0.35

bars1 = ax.bar(x - width/2, scores, width, color='#A8DADC', edgecolor='#457B9D', lw=1.5, label=f'原始分数 (简单平均={simple_avg:.1f})')
bars2 = ax.bar(x + width/2, [s * w for s, w in zip(scores, weights)], width,
               color='#F4A261', edgecolor='#E76F51', lw=1.5, alpha=0.85,
               label=f'加权分数 (加权平均={weighted_sum:.1f})')

for i, (s, w) in enumerate(zip(scores, weights)):
    ax.text(i - width/2, s + 0.5, str(s), ha='center', fontsize=11, fontweight='bold')
    ax.text(i + width/2, s * w + 0.3, f'{s*w:.1f}', ha='center', fontsize=11, fontweight='bold', color='#E76F51')
    ax.text(i, -3, f'权重 {w:.0%}', ha='center', fontsize=10, color='#1D3557', fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12)
ax.set_ylabel('分数', fontsize=13)
ax.set_title('加权平均数 vs 简单平均数\n（期末总评 = 各项分数 × 对应权重之和）', fontsize=16, fontweight='bold', color='#1D3557')
ax.legend(fontsize=11, loc='upper right')
ax.set_ylim(0, 100)
ax.grid(axis='y', alpha=0.2)
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
fig3.savefig(f'{BASE}/stats_weighted_mean.png', dpi=150, bbox_inches='tight')
plt.close()
print('Figure 3 (Weighted Mean) done')

# ============================================================
# Figure 4: 平均数受极端值影响 (鲁棒性对比)
# ============================================================
fig4, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(14, 5.5))
fig4.patch.set_facecolor('#FEFEFE')

# Normal data
data_normal = np.array([68, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92])
# With outlier
data_outlier = np.array([68, 70, 72, 75, 78, 80, 82, 85, 88, 90, 25])

for ax, d, title in [(ax_a, data_normal, '无极端值'), (ax_b, data_outlier, '有一个极端值 (25分)')]:
    m = np.mean(d)
    med = np.median(d)
    ax.set_xlim(20, 105)
    ax.set_ylim(-2, 4)
    ax.set_title(title, fontsize=14, fontweight='bold', color='#1D3557')
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis='x', alpha=0.2)

    for v in d:
        ax.plot(v, 1.5, 'o', ms=16, color='#457B9D', zorder=3, markeredgecolor='white', markeredgewidth=1.5)

    ax.axvline(x=m, color='#E63946', lw=3, ls='-', zorder=5, label=f'平均数 = {m:.1f}')
    ax.axvline(x=med, color='#2A9D8F', lw=3, ls='--', zorder=5, label=f'中位数 = {med:.1f}')
    ax.legend(fontsize=12, loc='upper left')

plt.suptitle('平均数 vs 中位数：谁更"稳健"？', fontsize=16, fontweight='bold', color='#1D3557', y=1.01)
plt.tight_layout()
fig4.savefig(f'{BASE}/stats_robustness.png', dpi=150, bbox_inches='tight')
plt.close()
print('Figure 4 (Robustness) done')

print('\n=== 集中趋势: All 4 figures done ===')
