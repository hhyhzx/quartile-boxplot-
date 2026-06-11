"""
人教版八年级数学下册 第二十四章 — 数据分组与频数分布 动画演示
涵盖: 组距分组、频率分布表、直方图、分组原则
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

# 模拟50人成绩数据
np.random.seed(42)
scores = np.concatenate([
    np.random.normal(65, 7, 10),
    np.random.normal(75, 5, 15),
    np.random.normal(82, 4, 15),
    np.random.normal(90, 5, 10),
]).clip(40, 100).astype(int)
scores.sort()

n = len(scores)
score_min = scores.min()
score_max = scores.max()

# ============================================================
# Figure 1: 分组过程动画 — 原始散点 → 分组 → 频数表 → 直方图
# ============================================================
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [0.55, 0.45]})
fig1.patch.set_facecolor('#FEFEFE')

ax1.set_xlim(35, 105)
ax1.set_ylim(-0.5, 5.5)
ax1.set_title('数据分组：从原始散点到直方图', fontsize=16, fontweight='bold', color='#1D3557')
for spine in ax1.spines.values():
    spine.set_visible(False)
ax1.set_yticks([])
ax1.grid(axis='x', alpha=0.2)

# Scatter original data
scatter = ax1.scatter(scores, np.random.uniform(1.5, 3.5, n), s=25, c='#457B9D', alpha=0.7, zorder=3)

# Group boundaries and histogram
bins = [40, 50, 60, 70, 80, 90, 100]
bin_centers = [(bins[i] + bins[i+1]) / 2 for i in range(len(bins) - 1)]
hist_counts, _ = np.histogram(scores, bins=bins)

# Histogram bars (animated)
bars = []
bar_rects = []
for i, (cnt, left, right) in enumerate(zip(hist_counts, bins[:-1], bins[1:])):
    bar, = ax1.plot([], [], '-', lw=0, alpha=0)
    bars.append(bar)
    rect = mpatches.Rectangle((left, 4), right - left, 0, alpha=0, facecolor='#A8DADC',
                               edgecolor='#457B9D', lw=1.5, zorder=2)
    ax1.add_patch(rect)
    bar_rects.append(rect)

# Bin labels
bin_labels = []
for left, right in zip(bins[:-1], bins[1:]):
    t = ax1.text((left + right) / 2, 4.8, '', ha='center', fontsize=9, alpha=0, color='#666')
    bin_labels.append(t)

# Frequency labels
freq_labels = []
for i, cnt in enumerate(hist_counts):
    t = ax1.text((bins[i] + bins[i+1]) / 2, 4.3, '', ha='center', fontsize=11, alpha=0,
                 fontweight='bold', color='#1D3557')
    freq_labels.append(t)

# Bottom table area
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 4)
ax2.axis('off')
table_title = ax2.text(5, 3.5, '', ha='center', fontsize=13, fontweight='bold', color='#1D3557', alpha=0)
table_content = ax2.text(5, 2.2, '', ha='center', fontsize=10, color='#333', alpha=0)
group_principle = ax2.text(5, 0.8, '', ha='center', fontsize=11, color='#E63946', alpha=0, fontweight='bold')

def animate_grouping(frame):
    t = frame / 90
    if t > 1.0:
        t = 1.0

    # Phase 1: show bin boundaries (0~0.3)
    if t <= 0.3:
        p = t / 0.3
        for lbl in bin_labels:
            lbl.set_text(f'{bins[bin_labels.index(lbl)]}~{bins[bin_labels.index(lbl)+1]}')
            lbl.set_alpha(p)
        table_title.set_text('Step 1: 确定组距和组数')
        table_title.set_alpha(p)
        table_content.set_text(f'数据范围: {score_min}~{score_max},  组距 = 10分,  组数 = 6')
        table_content.set_alpha(p)

    if t > 0.3:
        for lbl in bin_labels:
            lbl.set_alpha(1.0)
        table_title.set_text('Step 1: 确定组距和组数')
        table_title.set_alpha(1.0)
        table_content.set_text(f'数据范围: {score_min}~{score_max},  组距 = 10分,  组数 = 6')
        table_content.set_alpha(1.0)

    # Phase 2: count frequencies, animate bars (0.3~0.7)
    if 0.3 < t <= 0.7:
        p = clamp((t - 0.3) / 0.4)
        table_title.set_text('Step 2: 统计每组频数（数一数每组有几个数据）')
        for i, (rect, cnt) in enumerate(zip(bar_rects, hist_counts)):
            target_h = cnt / max(hist_counts) * 1.2
            rect.set_height(target_h * p)
            rect.set_alpha(0.7 * p)

    if 0.5 < t <= 0.7:
        p2 = clamp((t - 0.5) / 0.2)
        for i, (lbl, cnt) in enumerate(zip(freq_labels, hist_counts)):
            lbl.set_text(f'{cnt}人')
            lbl.set_alpha(p2)

    if t > 0.7:
        for rect, cnt in zip(bar_rects, hist_counts):
            target_h = cnt / max(hist_counts) * 1.2
            rect.set_height(target_h)
            rect.set_alpha(0.7)
        for lbl, cnt in zip(freq_labels, hist_counts):
            lbl.set_text(f'{cnt}人')
            lbl.set_alpha(1.0)

    # Phase 3: principle (0.7~1.0)
    if 0.7 < t <= 1.0:
        p = clamp((t - 0.7) / 0.3)
        table_title.set_text('Step 3: 验证分组原则')
        table_title.set_alpha(1.0)
        group_principle.set_text('分组原则: 组内差异尽可能小, 组间差异尽可能大\n(同一组的分数相近, 不同组的分数明显不同)')
        group_principle.set_alpha(p)

    return []

ani1 = animation.FuncAnimation(fig1, animate_grouping, frames=90, interval=60, blit=False, repeat=True)
ani1.save(f'{BASE}/stats_grouping_animation.gif', writer='pillow', fps=10, dpi=72)
fig1.savefig(f'{BASE}/stats_grouping_frame.png', dpi=150, bbox_inches='tight')
plt.close()
print('Figure 1 (Grouping Animation) done')

# ============================================================
# Figure 2: 完整频率分布表 + 直方图 (静态)
# ============================================================
fig2, (ax_tab, ax_bar) = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={'width_ratios': [0.6, 1]})
fig2.patch.set_facecolor('#FEFEFE')

# --- Table ---
ax_tab.set_xlim(0, 10)
ax_tab.set_ylim(0, 10)
ax_tab.axis('off')
ax_tab.set_title('频数/频率分布表', fontsize=15, fontweight='bold', color='#1D3557')

col_headers = ['组别\n(分数段)', '频数\n(人数)', '频率\n(频数/n)', '累计频数']
col_x_t = [1.5, 4, 6.5, 8.8]
start_y = 8.3
row_h = 0.95

# Header row
for hdr, cx in zip(col_headers, col_x_t):
    ax_tab.text(cx, start_y + 0.2, hdr, ha='center', fontsize=10, fontweight='bold', color='white',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#1D3557'))

cumul = 0
for i, (cnt, left, right) in enumerate(zip(hist_counts, bins[:-1], bins[1:])):
    y = start_y - (i + 1) * row_h
    cumul += cnt
    freq = cnt / n
    row_data = [f'{left}~{right}', str(cnt), f'{freq:.2f} ({freq:.0%})', str(cumul)]
    bg = '#FFF8F0' if i % 2 == 0 else 'white'
    for txt, cx in zip(row_data, col_x_t):
        ax_tab.text(cx, y, txt, ha='center', fontsize=11,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor=bg, edgecolor='#DDD'))

# Total row
y_total = start_y - len(hist_counts) * row_h - row_h
ax_tab.text(col_x_t[0], y_total, '合计', ha='center', fontsize=11, fontweight='bold')
ax_tab.text(col_x_t[1], y_total, str(n), ha='center', fontsize=11, fontweight='bold')
ax_tab.text(col_x_t[2], y_total, '1.00 (100%)', ha='center', fontsize=11, fontweight='bold')
ax_tab.text(col_x_t[3], y_total, str(n), ha='center', fontsize=11, fontweight='bold')

# --- Histogram ---
ax_bar.bar(bin_centers, hist_counts, width=9, color='#A8DADC', edgecolor='#457B9D', lw=2, alpha=0.8, zorder=3)
# Frequency polygon overlay
freq_mid = np.array(bin_centers)
freq_vals = np.array(hist_counts)
ax_bar.plot(freq_mid, freq_vals, 'o-', color='#E63946', lw=2.5, ms=10, zorder=5, label='频数折线')

for mid, cnt in zip(bin_centers, hist_counts):
    ax_bar.text(mid, cnt + 0.3, str(cnt), ha='center', fontsize=12, fontweight='bold', color='#1D3557')

ax_bar.set_xticks(bins)
ax_bar.set_xlabel('分数段', fontsize=13)
ax_bar.set_ylabel('频数（人数）', fontsize=13)
ax_bar.set_title('成绩分布直方图 (n=50)', fontsize=15, fontweight='bold', color='#1D3557')
ax_bar.legend(fontsize=11)
ax_bar.grid(axis='y', alpha=0.2)
for spine in ax_bar.spines.values():
    spine.set_visible(False)

plt.tight_layout()
fig2.savefig(f'{BASE}/stats_histogram.png', dpi=150, bbox_inches='tight')
plt.close()
print('Figure 2 (Histogram + Table) done')

# ============================================================
# Figure 3: 分组原则 — 组距过大 vs 过小 vs 合适
# ============================================================
fig3, axes = plt.subplots(1, 3, figsize=(16, 5))
fig3.patch.set_facecolor('#FEFEFE')

bins_options = [
    ([40, 60, 80, 100], "组距过大 (20分/组)\n信息丢失, 太粗糙"),
    ([40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100], "组距过小 (5分/组)\n太琐碎, 看不出规律"),
    ([40, 50, 60, 70, 80, 90, 100], "组距合适 (10分/组)\n既能看出分布形态,\n又不丢失细节"),
]

for ax, (bns, label) in zip(axes, bins_options):
    cnts, _ = np.histogram(scores, bins=bns)
    centers = [(bns[i] + bns[i+1]) / 2 for i in range(len(bns) - 1)]
    widths = [(bns[i+1] - bns[i]) * 0.9 for i in range(len(bns) - 1)]

    bars = ax.bar(centers, cnts, width=widths, color='#A8DADC', edgecolor='#457B9D', lw=1.5, alpha=0.8)
    ax.set_xticks(bns)
    ax.set_xlim(35, 105)
    ax.set_title(label, fontsize=12, color='#1D3557')
    ax.grid(axis='y', alpha=0.2)
    for spine in ax.spines.values():
        spine.set_visible(False)

plt.suptitle('分组原则：组距的选择影响数据呈现效果', fontsize=16, fontweight='bold', color='#1D3557', y=1.02)
plt.tight_layout()
fig3.savefig(f'{BASE}/stats_grouping_bins.png', dpi=150, bbox_inches='tight')
plt.close()
print('Figure 3 (Bins Compare) done')

print('\n=== 数据分组: All 3 figures done ===')
