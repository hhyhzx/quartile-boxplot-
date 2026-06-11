"""
人教版八年级数学下册 — 四分位数与箱线图（箱体图）动画演示
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 示例数据（某班一次数学测验成绩，共 15 名同学）
# ============================================================
data = np.array([62, 68, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92, 95, 96, 98])
data_sorted = np.sort(data)
n = len(data)

q1 = np.percentile(data, 25)
q2 = np.percentile(data, 50)
q3 = np.percentile(data, 75)
vmin = data_sorted[0]
vmax = data_sorted[-1]
iqr = q3 - q1

def clamp(v):
    return max(0.0, min(1.0, v))

# ============================================================
# Figure 1: 四分位数概念演示 + 箱线图构建动画
# ============================================================
fig1, (ax_data, ax_box) = plt.subplots(2, 1, figsize=(8, 5.5), gridspec_kw={'height_ratios': [1.2, 1]})
fig1.patch.set_facecolor('#FEFEFE')

# --- 数据轴 ---
ax_data.set_xlim(-0.5, n + 0.5)
ax_data.set_ylim(55, 105)
ax_data.set_yticks(data_sorted)
ax_data.set_xticks([])
ax_data.set_ylabel('成绩（分）', fontsize=13)
ax_data.set_title('数据从小到大排列，找四分位数', fontsize=16, fontweight='bold', color='#1D3557')
ax_data.grid(axis='y', alpha=0.3)
for spine in ax_data.spines.values():
    spine.set_visible(False)
ax_data.axhline(0, color='black', lw=0.5)

scat = ax_data.scatter(range(n), data_sorted, s=120, c='#457B9D', zorder=5, ec='white', lw=1)
for i, val in enumerate(data_sorted):
    ax_data.text(i, val + 1.5, str(val), ha='center', fontsize=9, color='#333333')

Q1_COLOR = '#E63946'
Q2_COLOR = '#1D3557'
Q3_COLOR = '#2A9D8F'
BOX_COLOR = '#457B9D'
MEDIAN_COLOR = '#1D3557'

idx_q1 = 3.5
idx_q2 = 7
idx_q3 = 10.5

vline_q1 = ax_data.axvline(x=idx_q1, color=Q1_COLOR, lw=2, ls='--', alpha=0, ymin=0, ymax=0.85)
vline_q2 = ax_data.axvline(x=idx_q2, color=Q2_COLOR, lw=2.5, ls='--', alpha=0, ymin=0, ymax=0.85)
vline_q3 = ax_data.axvline(x=idx_q3, color=Q3_COLOR, lw=2, ls='--', alpha=0, ymin=0, ymax=0.85)

text_q1 = ax_data.text(idx_q1, 103, '', fontsize=11, color=Q1_COLOR, ha='center', fontweight='bold')
text_q2 = ax_data.text(idx_q2, 103, '', fontsize=11, color=Q2_COLOR, ha='center', fontweight='bold')
text_q3 = ax_data.text(idx_q3, 103, '', fontsize=11, color=Q3_COLOR, ha='center', fontweight='bold')

rect_low = mpatches.Rectangle((-0.5, 55), idx_q1 + 0.5, 50, alpha=0, facecolor='#FFE5E5', zorder=0)
rect_mid1 = mpatches.Rectangle((idx_q1, 55), idx_q2 - idx_q1, 50, alpha=0, facecolor='#E5F0FF', zorder=0)
rect_mid2 = mpatches.Rectangle((idx_q2, 55), idx_q3 - idx_q2, 50, alpha=0, facecolor='#E5FFF0', zorder=0)
rect_high = mpatches.Rectangle((idx_q3, 55), n - 0.5 - idx_q3, 50, alpha=0, facecolor='#FFF5E5', zorder=0)
ax_data.add_patch(rect_low)
ax_data.add_patch(rect_mid1)
ax_data.add_patch(rect_mid2)
ax_data.add_patch(rect_high)

label_low = ax_data.text((idx_q1 - 0.5) / 2, 59, '', fontsize=10, ha='center', color=Q1_COLOR, alpha=0)
label_mid1 = ax_data.text((idx_q1 + idx_q2) / 2, 59, '', fontsize=10, ha='center', color=Q2_COLOR, alpha=0)
label_mid2 = ax_data.text((idx_q2 + idx_q3) / 2, 59, '', fontsize=10, ha='center', color=Q2_COLOR, alpha=0)
label_high = ax_data.text((idx_q3 + n - 0.5) / 2, 59, '', fontsize=10, ha='center', color=Q3_COLOR, alpha=0)

# --- 箱线图轴 ---
ax_box.set_xlim(55, 105)
ax_box.set_ylim(-0.5, 1.5)
ax_box.set_xticks(np.arange(55, 106, 5))
ax_box.set_xlabel('成绩（分）', fontsize=13)
ax_box.set_title('箱线图（箱体图 / 盒须图）', fontsize=16, fontweight='bold', color='#1D3557')
ax_box.grid(axis='x', alpha=0.3)
for spine in ax_box.spines.values():
    spine.set_visible(False)

box_x = [q1, q1, q3, q3]
box_y = [-0.25, 0.25, 0.25, -0.25]
box_patch = mpatches.Polygon(list(zip(box_x, box_y)), closed=True,
                              facecolor='#A8DADC', edgecolor=BOX_COLOR, lw=2.5, alpha=0)
ax_box.add_patch(box_patch)

median_line = ax_box.axvline(x=q2, ymin=0.44, ymax=0.56, color=MEDIAN_COLOR, lw=3, alpha=0)

whisker_low = ax_box.plot([vmin, q1], [0, 0], color=BOX_COLOR, lw=2, alpha=0)[0]
whisker_high = ax_box.plot([q3, vmax], [0, 0], color=BOX_COLOR, lw=2, alpha=0)[0]
cap_low = ax_box.plot([vmin, vmin], [-0.12, 0.12], color=BOX_COLOR, lw=2, alpha=0)[0]
cap_high = ax_box.plot([vmax, vmax], [-0.12, 0.12], color=BOX_COLOR, lw=2, alpha=0)[0]

annot_min = ax_box.text(vmin, -0.45, '', fontsize=10, ha='center', color='#333333', alpha=0)
annot_q1 = ax_box.text(q1, -0.45, '', fontsize=10, ha='center', color=Q1_COLOR, fontweight='bold', alpha=0)
annot_q2 = ax_box.text(q2, 0.4, '', fontsize=10, ha='center', color=MEDIAN_COLOR, fontweight='bold', alpha=0)
annot_q3 = ax_box.text(q3, -0.45, '', fontsize=10, ha='center', color=Q3_COLOR, fontweight='bold', alpha=0)
annot_max = ax_box.text(vmax, -0.45, '', fontsize=10, ha='center', color='#333333', alpha=0)
subtitle = ax_box.text(80, 1.2, '', fontsize=12, ha='center', color='#666666', alpha=0)

# ============================================================
# 动画帧
# ============================================================
total_frames = 90

def animate(frame):
    t = frame / total_frames

    # ---- 阶段 0: 展示数据 (0 ~ 0.1) ----
    if t <= 0.1:
        pass

    # ---- 阶段 1: Q1 (0.10 ~ 0.25) ----
    if 0.10 < t <= 0.25:
        p = clamp((t - 0.10) / 0.15)
        vline_q1.set_alpha(p)
        text_q1.set_text(f'Q1 = {q1:.0f}')
        text_q1.set_alpha(p)
        rect_low.set_alpha(p * 0.25)
        rect_mid1.set_alpha(p * 0.15)
        if p > 0.6:
            pp = clamp((p - 0.6) / 0.4)
            label_low.set_text('前 25%')
            label_low.set_alpha(pp)

    if t > 0.25:
        vline_q1.set_alpha(1.0)
        text_q1.set_text(f'Q1 = {q1:.0f}')
        text_q1.set_alpha(1.0)
        rect_low.set_alpha(0.25)
        rect_mid1.set_alpha(0.15)
        label_low.set_text('前 25%')
        label_low.set_alpha(1.0)

    # ---- 阶段 2: Q2 (0.25 ~ 0.40) ----
    if 0.25 < t <= 0.40:
        p = clamp((t - 0.25) / 0.15)
        vline_q2.set_alpha(p)
        text_q2.set_text(f'Q2 = {q2:.0f}（中位数）')
        text_q2.set_alpha(p)
        rect_mid1.set_alpha(0.15 + p * 0.1)
        rect_mid2.set_alpha(p * 0.15)
        if p > 0.6:
            pp = clamp((p - 0.6) / 0.4)
            label_mid1.set_text('25%~50%')
            label_mid1.set_alpha(pp)

    if t > 0.40:
        vline_q2.set_alpha(1.0)
        text_q2.set_text(f'Q2 = {q2:.0f}（中位数）')
        text_q2.set_alpha(1.0)
        rect_mid1.set_alpha(0.25)
        rect_mid2.set_alpha(0.15)
        label_mid1.set_text('25%~50%')
        label_mid1.set_alpha(1.0)

    # ---- 阶段 3: Q3 (0.40 ~ 0.55) ----
    if 0.40 < t <= 0.55:
        p = clamp((t - 0.40) / 0.15)
        vline_q3.set_alpha(p)
        text_q3.set_text(f'Q3 = {q3:.0f}')
        text_q3.set_alpha(p)
        rect_mid2.set_alpha(0.15 + p * 0.1)
        rect_high.set_alpha(p * 0.15)
        if p > 0.6:
            pp = clamp((p - 0.6) / 0.4)
            label_mid2.set_text('50%~75%')
            label_mid2.set_alpha(pp)
            label_high.set_text('后 25%')
            label_high.set_alpha(pp)

    if t > 0.55:
        vline_q3.set_alpha(1.0)
        text_q3.set_text(f'Q3 = {q3:.0f}')
        text_q3.set_alpha(1.0)
        rect_mid2.set_alpha(0.25)
        rect_high.set_alpha(0.15)
        label_mid2.set_text('50%~75%')
        label_mid2.set_alpha(1.0)
        label_high.set_text('后 25%')
        label_high.set_alpha(1.0)

    # ---- 阶段 4: 最小/最大值 (0.55 ~ 0.65) ----
    if 0.55 < t <= 0.65:
        p = clamp((t - 0.55) / 0.10)
        subtitle.set_text('Step 1: 画出最小值和最大值（两条须的端点）')
        subtitle.set_alpha(p)
        cap_low.set_alpha(p)
        cap_high.set_alpha(p)
        annot_min.set_text(f'最小值={vmin}')
        annot_min.set_alpha(p)
        annot_max.set_text(f'最大值={vmax}')
        annot_max.set_alpha(p)

    if t > 0.65:
        cap_low.set_alpha(1.0)
        cap_high.set_alpha(1.0)
        annot_min.set_text(f'最小值={vmin}')
        annot_min.set_alpha(1.0)
        annot_max.set_text(f'最大值={vmax}')
        annot_max.set_alpha(1.0)

    # ---- 阶段 5: 箱体 (0.65 ~ 0.75) ----
    if 0.65 < t <= 0.75:
        p = clamp((t - 0.65) / 0.10)
        subtitle.set_text('Step 2: 从 Q1 到 Q3 画一个矩形（箱体）')
        box_patch.set_alpha(p)
        annot_q1.set_text(f'Q1={q1:.0f}')
        annot_q1.set_alpha(p)
        annot_q3.set_text(f'Q3={q3:.0f}')
        annot_q3.set_alpha(p)

    if t > 0.75:
        box_patch.set_alpha(0.7)
        annot_q1.set_text(f'Q1={q1:.0f}')
        annot_q1.set_alpha(1.0)
        annot_q3.set_text(f'Q3={q3:.0f}')
        annot_q3.set_alpha(1.0)

    # ---- 阶段 6: 中位线 (0.75 ~ 0.85) ----
    if 0.75 < t <= 0.85:
        p = clamp((t - 0.75) / 0.10)
        subtitle.set_text('Step 3: 在箱体内画中位数线（Q2）')
        median_line.set_alpha(p)
        annot_q2.set_text(f'中位数={q2:.0f}')
        annot_q2.set_alpha(p)

    if t > 0.85:
        median_line.set_alpha(1.0)
        annot_q2.set_text(f'中位数={q2:.0f}')
        annot_q2.set_alpha(1.0)

    # ---- 阶段 7: 须 (0.85 ~ 0.95) ----
    if 0.85 < t <= 0.95:
        p = clamp((t - 0.85) / 0.10)
        subtitle.set_text('Step 4: 从箱体向两端画"须"（连线到最小值和最大值）')
        whisker_low.set_alpha(p)
        whisker_high.set_alpha(p)

    if t > 0.95:
        whisker_low.set_alpha(1.0)
        whisker_high.set_alpha(1.0)

    # ---- 阶段 8: 完成 (0.95 ~ 1.0) ----
    if t > 0.95:
        p = clamp((t - 0.95) / 0.05)
        subtitle.set_text(f'箱线图完成！IQR = Q3 - Q1 = {iqr:.0f}（四分位距）')
        subtitle.set_alpha(p)

    if t >= 1.0:
        subtitle.set_text(f'箱线图完成！IQR = Q3 - Q1 = {iqr:.0f}（四分位距）')
        subtitle.set_alpha(1.0)

    return []

# ============================================================
# 生成动画
# ============================================================
ani = animation.FuncAnimation(
    fig1, animate, frames=total_frames, interval=60, blit=False, repeat=True
)

# ============================================================
# Figure 2: 多组数据对比箱线图
# ============================================================
fig2, ax = plt.subplots(figsize=(14, 6))
fig2.patch.set_facecolor('#FEFEFE')

np.random.seed(42)
groups = {
    '八(1)班': np.random.normal(78, 8, 40).clip(40, 100),
    '八(2)班': np.random.normal(72, 12, 40).clip(40, 100),
    '八(3)班': np.random.normal(82, 6, 40).clip(40, 100),
    '八(4)班': np.random.normal(75, 10, 40).clip(40, 100),
}

group_names = list(groups.keys())
group_data = [groups[name] for name in group_names]

bp = ax.boxplot(group_data, tick_labels=group_names, patch_artist=True,
                widths=0.5, showmeans=True,
                meanprops=dict(marker='D', markerfacecolor='#E63946', markersize=8, markeredgecolor='white'),
                medianprops=dict(color='#1D3557', lw=3),
                whiskerprops=dict(color='#457B9D', lw=1.8),
                capprops=dict(color='#457B9D', lw=1.8),
                boxprops=dict(lw=1.8))

colors = ['#A8DADC', '#F4A261', '#2A9D8F', '#E9C46A']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)

ax.set_ylabel('成绩（分）', fontsize=14)
ax.set_title('各班数学成绩箱线图对比', fontsize=18, fontweight='bold', color='#1D3557')
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(35, 105)

legend_elements = [
    mpatches.Patch(facecolor='#A8DADC', alpha=0.7, label='箱体 (Q1~Q3)'),
    plt.Line2D([0], [0], color='#1D3557', lw=3, label='中位数 (Q2)'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#E63946',
               markersize=8, label='平均数', lw=0),
    plt.Line2D([0], [0], color='#457B9D', lw=1.8, label='须 (min~max)'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.9)

for i, (name, d) in enumerate(zip(group_names, group_data)):
    q1v = np.percentile(d, 25)
    q2v = np.percentile(d, 50)
    q3v = np.percentile(d, 75)
    ax.annotate(f'Q1={q1v:.1f}\nQ2={q2v:.1f}\nQ3={q3v:.1f}',
                xy=(i + 1, q3v + 1), fontsize=8, ha='center', color='#333333',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()

# ============================================================
# Figure 3: 四分位数计算详解图
# ============================================================
fig3, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(13, 8), gridspec_kw={'height_ratios': [1, 0.7]})
fig3.patch.set_facecolor('#FEFEFE')

ax_top.set_xlim(-0.5, n + 0.5)
ax_top.set_ylim(55, 105)
ax_top.set_title('四分位数计算方法（n=15，奇数个数据）', fontsize=16, fontweight='bold', color='#1D3557')
for spine in ax_top.spines.values():
    spine.set_visible(False)
ax_top.grid(axis='y', alpha=0.2)
ax_top.set_xticks([])

for i, val in enumerate(data_sorted):
    ax_top.plot(i, val, 'o', ms=16, color='#457B9D', zorder=5, markeredgecolor='white', markeredgewidth=1.5)
    ax_top.text(i, val - 4, str(val), ha='center', fontsize=9, color='#333')

for i in range(n):
    ax_top.text(i, 57, f'第{i+1}个', ha='center', fontsize=8, color='#999999')

# Q2: 第 (n+1)/2 = 第 8 个, index 7
ax_top.axvline(x=7, ymin=0.58, ymax=0.95, color=Q2_COLOR, lw=2.5, ls='--')
ax_top.text(7, 100, f'Q2: 第{(n+1)//2}个 = 第8个\n    值 = {data_sorted[7]}', ha='center', fontsize=11,
            color=Q2_COLOR, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor=Q2_COLOR))

# Q1: 前半段 (第1~7个) 的中位数 -> 第4个, index 3
ax_top.axvline(x=3, ymin=0.58, ymax=0.95, color=Q1_COLOR, lw=2, ls='--')
ax_top.text(3, 104, f'Q1: 前7个的中位数\n    = 第4个 = {data_sorted[3]}', ha='center', fontsize=11,
            color=Q1_COLOR, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor=Q1_COLOR))

# Q3: 后半段 (第9~15个)的中位数 -> 第12个, index 11
ax_top.axvline(x=11, ymin=0.58, ymax=0.95, color=Q3_COLOR, lw=2, ls='--')
ax_top.text(11, 104, f'Q3: 后7个的中位数\n    = 第12个 = {data_sorted[11]}', ha='center', fontsize=11,
            color=Q3_COLOR, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor=Q3_COLOR))

# 高亮三个关键数据点
ax_top.plot(7, data_sorted[7], 's', ms=20, color=Q2_COLOR, zorder=6, markeredgecolor='white', markeredgewidth=2)
ax_top.plot(3, data_sorted[3], 'D', ms=18, color=Q1_COLOR, zorder=6, markeredgecolor='white', markeredgewidth=2)
ax_top.plot(11, data_sorted[11], 'D', ms=18, color=Q3_COLOR, zorder=6, markeredgecolor='white', markeredgewidth=2)

# --- 下部: 公式和文字说明 ---
ax_bot.axis('off')
ax_bot.set_xlim(0, 10)
ax_bot.set_ylim(0, 4)

formulas = [
    ('第 1 步：排序', '将数据从小到大排列'),
    ('第 2 步：找中位数 Q2', 'Q2 = 第 (n+1)/2 个数据 (n为奇数)\nQ2 = 中间两个数的平均数 (n为偶数)'),
    ('第 3 步：找 Q1 和 Q3', 'Q1 = 前半段数据的中位数\nQ3 = 后半段数据的中位数'),
    ('第 4 步：五数概括', f'最小值={vmin}  Q1={q1:.0f}  Q2={q2:.0f}  Q3={q3:.0f}  最大值={vmax}'),
    ('四分位距 IQR', f'IQR = Q3 - Q1 = {q3:.0f} - {q1:.0f} = {iqr:.0f}'),
]

for i, (title, content) in enumerate(formulas):
    y = 3.5 - i * 0.75
    ax_bot.text(0.2, y, title, fontsize=12, fontweight='bold', color='#1D3557', va='top')
    ax_bot.text(3.5, y, content, fontsize=11, color='#444444', va='top')
    if i < 4:
        ax_bot.axhline(y=y - 0.25, xmin=0.02, xmax=0.98, color='#E0E0E0', lw=0.5)

plt.tight_layout()

# ============================================================
# 保存
# ============================================================
base = 'E:/maths_work'
fig1.savefig(f'{base}/quartile_boxplot_anim_frame.png', dpi=150, bbox_inches='tight')
fig2.savefig(f'{base}/quartile_multi_boxplot.png', dpi=150, bbox_inches='tight')
fig3.savefig(f'{base}/quartile_calculation.png', dpi=150, bbox_inches='tight')

# 保存动画为 GIF
ani.save(f'{base}/quartile_animation.gif', writer='pillow', fps=10, dpi=72)
print('Done! Output files:')
print('  quartile_animation.gif')
print('  quartile_boxplot_anim_frame.png')
print('  quartile_multi_boxplot.png')
print('  quartile_calculation.png')

plt.show()
