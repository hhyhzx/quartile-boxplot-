"""
为四大统计概念生成带中文语音讲解的 MP4 视频
使用 edge-tts (微软免费TTS) + moviepy
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import numpy as np
import asyncio
import edge_tts
import os, sys, tempfile, shutil

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

BASE = 'E:/maths_work'
VOICE = 'zh-CN-XiaoxiaoNeural'  # 晓晓 - 女声，清晰自然
FPS = 8  # frames per second for video
DPI = 100

def clamp(v):
    return max(0.0, min(1.0, v))

# ================================================================
# 语音生成
# ================================================================
async def gen_audio(text, path):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(path)
    print(f'  Audio saved: {path}')

def run_audio(text, path):
    asyncio.run(gen_audio(text, path))

# ================================================================
# 视频 1: 数据的集中趋势
# ================================================================
def make_video1_central():
    print('\n=== Video 1: 集中趋势 ===')

    data = np.array([62, 68, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92, 95, 96, 98])
    data_sort = np.sort(data)
    n = len(data)
    mean_val = np.mean(data)
    median_val = np.median(data)

    frames_dir = tempfile.mkdtemp(prefix='frames1_')
    total_frames = 64  # 8 seconds at 8fps

    fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [1.1, 1]})
    fig1.patch.set_facecolor('#FEFEFE')

    ax1.set_xlim(55, 105); ax1.set_ylim(-2, 6)
    ax1.set_title('数据的集中趋势 — 平均数、中位数、加权平均数、众数', fontsize=15, fontweight='bold', color='#1D3557')
    ax1.set_xlabel('成绩（分）', fontsize=12)
    ax1.set_yticks([])
    for spine in ax1.spines.values(): spine.set_visible(False)
    ax1.grid(axis='x', alpha=0.2)

    for val in data_sort:
        ax1.plot(val, 0.5 + np.random.uniform(-0.25, 0.25), 'o', ms=12, color='#457B9D', zorder=5,
                markeredgecolor='white', markeredgewidth=1.2)

    mean_arrow = ax1.annotate('', xy=(mean_val, 0), xytext=(mean_val, 2.5),
                              arrowprops=dict(arrowstyle='->', color='#E63946', lw=3), alpha=0)
    mean_txt = ax1.text(mean_val, 3, '', fontsize=13, color='#E63946', ha='center', fontweight='bold', alpha=0)
    median_line = ax1.axvline(x=median_val, color='#2A9D8F', lw=2.5, ls='--', alpha=0, zorder=4)
    median_txt = ax1.text(median_val, 4.5, '', fontsize=12, color='#2A9D8F', ha='center', fontweight='bold', alpha=0)

    # Weighted mean display
    ax2.set_xlim(0, 100); ax2.set_ylim(0, 5)
    ax2.axis('off')
    w_title = ax2.text(50, 4.5, '', ha='center', fontsize=14, fontweight='bold', color='#1D3557', alpha=0)
    w_formula = ax2.text(50, 3.2, '', ha='center', fontsize=13, color='#E63946', alpha=0)
    w_example = ax2.text(50, 1.8, '', ha='center', fontsize=12, color='#333', alpha=0)

    for frame in range(total_frames):
        t = frame / total_frames

        # Phase 1: data intro (0~0.15)
        # Phase 2: mean (0.15~0.40)
        if 0.15 < t <= 0.40:
            p = clamp((t - 0.15) / 0.25)
            mean_arrow.set_alpha(p)
            mean_txt.set_text(f'平均数 = {mean_val:.1f}')
            mean_txt.set_alpha(p)

        if t > 0.40:
            mean_arrow.set_alpha(1.0)
            mean_txt.set_text(f'平均数 = {mean_val:.1f}')
            mean_txt.set_alpha(1.0)

        # Phase 3: median (0.40~0.60)
        if 0.40 < t <= 0.60:
            p = clamp((t - 0.40) / 0.20)
            median_line.set_alpha(p)
            median_txt.set_text(f'中位数 = {median_val:.0f}')
            median_txt.set_alpha(p)

        if t > 0.60:
            median_line.set_alpha(1.0)
            median_txt.set_text(f'中位数 = {median_val:.0f}')
            median_txt.set_alpha(1.0)

        # Phase 4: weighted mean (0.60~0.90)
        if 0.60 < t <= 0.90:
            p = clamp((t - 0.60) / 0.30)
            w_title.set_text('加权平均数: 期末总评 = 平时×15% + 期中×30% + 期末×40%')
            w_title.set_alpha(p)
            w_formula.set_text('加权平均数 = (88×0.15 + 92×0.15 + 78×0.30 + 85×0.40) / 1.0')
            w_formula.set_alpha(p)
            w_example.set_text('= 13.2 + 13.8 + 23.4 + 34.0 = 84.4')
            w_example.set_alpha(p)

        if t > 0.90:
            w_title.set_alpha(1.0); w_formula.set_alpha(1.0); w_example.set_alpha(1.0)

        fname = os.path.join(frames_dir, f'frame_{frame:04d}.png')
        fig1.savefig(fname, dpi=DPI, bbox_inches='tight')

    plt.close(fig1)

    # Generate audio
    narration = (
        "这是一组十五名同学的数学测验成绩，从小到大排列。"
        "算术平均数，等于所有数据之和，除以数据的个数，它代表了数据的'平衡点'。"
        "中位数，是把数据排序后，正中间的那个数。"
        "当数据中有极端值时，中位数比平均数更稳健。"
        "加权平均数用于计算期末总评，不同项目的权重不同，期末考试权重最大。"
    )
    audio_path = f'{BASE}/narration_01_central.mp3'
    run_audio(narration, audio_path)

    # Assemble video
    from moviepy import ImageSequenceClip, AudioFileClip
    frame_files = sorted([os.path.join(frames_dir, f) for f in os.listdir(frames_dir)])
    clip = ImageSequenceClip(frame_files, fps=FPS)
    audio = AudioFileClip(audio_path)
    # Loop or trim audio to match video duration
    video_duration = len(frame_files) / FPS
    if audio.duration < video_duration:
        # pad silence isn't easy, just let audio end
        pass
    clip = clip.with_audio(audio)
    out = f'{BASE}/video_01_central.mp4'
    clip.write_videofile(out, codec='libx264', fps=FPS, logger=None)
    clip.close()
    audio.close()
    shutil.rmtree(frames_dir)
    print(f'  Video saved: {out}')

# ================================================================
# 视频 2: 离散程度
# ================================================================
def make_video2_dispersion():
    print('\n=== Video 2: 离散程度 ===')

    data_a = np.array([72, 74, 76, 78, 80, 82, 84, 86, 88, 90])
    mean_a = np.mean(data_a)
    q_a = np.sum((data_a - mean_a)**2)
    n_a = len(data_a)

    frames_dir = tempfile.mkdtemp(prefix='frames2_')
    total_frames = 64

    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [1, 0.7]})
    fig.patch.set_facecolor('#FEFEFE')

    ax_top.set_xlim(-0.5, n_a + 0.5); ax_top.set_ylim(55, 100)
    ax_top.set_title('数据的离散程度 — 离差、离差平方和、方差、标准差', fontsize=15, fontweight='bold', color='#1D3557')
    ax_top.set_ylabel('成绩（分）', fontsize=12)
    for spine in ax_top.spines.values(): spine.set_visible(False)
    ax_top.grid(axis='y', alpha=0.2)

    mean_line = ax_top.axhline(y=mean_a, color='#E63946', lw=2, ls='--', alpha=0, zorder=3)
    for i, val in enumerate(data_a):
        ax_top.plot(i, val, 'o', ms=18, color='#457B9D', zorder=5, markeredgecolor='white', markeredgewidth=2)

    dev_lines = []
    dev_texts = []
    for i, val in enumerate(data_a):
        dev = val - mean_a
        l, = ax_top.plot([i, i], [mean_a, val], '-', lw=2.5, alpha=0, zorder=2,
                        color='#E63946' if dev < 0 else '#2A9D8F')
        dev_lines.append(l)
        t = ax_top.text(i + 0.25, (mean_a + val) / 2, '', fontsize=9, alpha=0, fontweight='bold')
        dev_texts.append((t, dev))

    ax_bot.set_xlim(0, 10); ax_bot.set_ylim(0, 5)
    ax_bot.axis('off')
    q_title = ax_bot.text(5, 4.5, '', ha='center', fontsize=14, fontweight='bold', color='#1D3557', alpha=0)
    q_detail = ax_bot.text(5, 3.2, '', ha='center', fontsize=12, color='#333', alpha=0)
    var_text = ax_bot.text(5, 2, '', ha='center', fontsize=13, color='#E63946', fontweight='bold', alpha=0)
    std_text = ax_bot.text(5, 1, '', ha='center', fontsize=13, color='#2A9D8F', fontweight='bold', alpha=0)

    for frame in range(total_frames):
        t = frame / total_frames

        # Phase 1: mean line (0~0.15)
        if t <= 0.15:
            mean_line.set_alpha(t / 0.15)
        else:
            mean_line.set_alpha(1.0)

        # Phase 2: deviations (0.15~0.45)
        if 0.15 < t <= 0.45:
            p = clamp((t - 0.15) / 0.30)
            for l in dev_lines: l.set_alpha(p)
            for txt, dev in dev_texts:
                txt.set_text(f'{dev:+.1f}'); txt.set_alpha(p)

        if t > 0.45:
            for l in dev_lines: l.set_alpha(1.0)
            for txt, dev in dev_texts:
                txt.set_text(f'{dev:+.1f}'); txt.set_alpha(1.0)

        # Phase 3: Q and variance (0.45~0.80)
        if 0.45 < t <= 0.80:
            p = clamp((t - 0.45) / 0.35)
            q_title.set_text(f'离差平方和 Q = Σ(xi - x)^2 = {q_a:.1f}')
            q_title.set_alpha(p)
            q_detail.set_text('每个离差平方后相加，避免正负抵消')
            q_detail.set_alpha(p)
            var_text.set_text(f'方差 s^2 = Q / n = {q_a:.1f} / {n_a} = {np.var(data_a):.2f}')
            var_text.set_alpha(p)
            std_text.set_text(f'标准差 s = sqrt(s^2) = {np.std(data_a):.2f}')
            std_text.set_alpha(p)

        if t > 0.80:
            q_title.set_alpha(1.0); q_detail.set_alpha(1.0)
            var_text.set_alpha(1.0); std_text.set_alpha(1.0)

        fname = os.path.join(frames_dir, f'frame_{frame:04d}.png')
        fig.savefig(fname, dpi=DPI, bbox_inches='tight')

    plt.close(fig)

    narration = (
        "红色虚线是数据的平均数，所有数据到平均数的垂直距离，叫做离差。"
        "绿色线表示正离差，即高于平均数的部分。红色线表示负离差，即低于平均数的部分。"
        "把所有离差直接相加会正负抵消，所以要用离差平方和Q来衡量离散程度。"
        "离差平方和Q，等于每个离差的平方之和。方差等于Q除以数据个数。"
        "标准差等于方差的算术平方根，单位与原始数据一致。"
    )
    audio_path = f'{BASE}/narration_02_dispersion.mp3'
    run_audio(narration, audio_path)

    from moviepy import ImageSequenceClip, AudioFileClip
    frame_files = sorted([os.path.join(frames_dir, f) for f in os.listdir(frames_dir)])
    clip = ImageSequenceClip(frame_files, fps=FPS)
    audio = AudioFileClip(audio_path)
    clip = clip.with_audio(audio)
    out = f'{BASE}/video_02_dispersion.mp4'
    clip.write_videofile(out, codec='libx264', fps=FPS, logger=None)
    clip.close(); audio.close()
    shutil.rmtree(frames_dir)
    print(f'  Video saved: {out}')

# ================================================================
# 视频 3: 四分位数与箱线图
# ================================================================
def make_video3_quartile():
    print('\n=== Video 3: 四分位数与箱线图 ===')

    data = np.array([62, 68, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92, 95, 96, 98])
    data_sort = np.sort(data)
    n = len(data)
    q1 = np.percentile(data, 25)
    q2 = np.percentile(data, 50)
    q3 = np.percentile(data, 75)
    vmin, vmax = data_sort[0], data_sort[-1]
    iqr = q3 - q1

    frames_dir = tempfile.mkdtemp(prefix='frames3_')
    total_frames = 64

    fig, (ax_data, ax_box) = plt.subplots(2, 1, figsize=(9, 6.5), gridspec_kw={'height_ratios': [1.2, 1]})
    fig.patch.set_facecolor('#FEFEFE')

    # Top: data with quartile lines
    ax_data.set_xlim(-0.5, n + 0.5); ax_data.set_ylim(55, 105)
    ax_data.set_title('四分位数与箱线图 — 数据分布的可视化', fontsize=15, fontweight='bold', color='#1D3557')
    ax_data.set_xticks([]); ax_data.set_yticks(data_sort)
    for spine in ax_data.spines.values(): spine.set_visible(False)
    ax_data.grid(axis='y', alpha=0.2)

    Q1_C, Q2_C, Q3_C = '#E63946', '#1D3557', '#2A9D8F'
    ax_data.scatter(range(n), data_sort, s=100, c='#457B9D', zorder=5, ec='white', lw=1)
    for i, val in enumerate(data_sort):
        ax_data.text(i, val + 1.5, str(val), ha='center', fontsize=8, color='#333')

    idx_q1, idx_q2, idx_q3 = 3.5, 7, 10.5
    vl_q1 = ax_data.axvline(x=idx_q1, color=Q1_C, lw=2, ls='--', alpha=0)
    vl_q2 = ax_data.axvline(x=idx_q2, color=Q2_C, lw=2.5, ls='--', alpha=0)
    vl_q3 = ax_data.axvline(x=idx_q3, color=Q3_C, lw=2, ls='--', alpha=0)
    t_q1 = ax_data.text(idx_q1, 103, '', fontsize=11, color=Q1_C, ha='center', fontweight='bold', alpha=0)
    t_q2 = ax_data.text(idx_q2, 103, '', fontsize=11, color=Q2_C, ha='center', fontweight='bold', alpha=0)
    t_q3 = ax_data.text(idx_q3, 103, '', fontsize=11, color=Q3_C, ha='center', fontweight='bold', alpha=0)

    # Bottom: box plot build
    ax_box.set_xlim(55, 105); ax_box.set_ylim(-0.5, 1.5)
    ax_box.set_xlabel('成绩（分）', fontsize=12)
    for spine in ax_box.spines.values(): spine.set_visible(False)
    ax_box.grid(axis='x', alpha=0.2)

    box_patch = mpatches.Polygon([[q1,-0.25],[q1,0.25],[q3,0.25],[q3,-0.25]], closed=True,
                                  facecolor='#A8DADC', edgecolor='#457B9D', lw=2, alpha=0)
    ax_box.add_patch(box_patch)
    med_line = ax_box.axvline(x=q2, ymin=0.44, ymax=0.56, color='#1D3557', lw=3, alpha=0)
    w_low = ax_box.plot([vmin,q1], [0,0], color='#457B9D', lw=2, alpha=0)[0]
    w_high = ax_box.plot([q3,vmax], [0,0], color='#457B9D', lw=2, alpha=0)[0]
    c_low = ax_box.plot([vmin,vmin], [-0.12,0.12], color='#457B9D', lw=2, alpha=0)[0]
    c_high = ax_box.plot([vmax,vmax], [-0.12,0.12], color='#457B9D', lw=2, alpha=0)[0]
    sub_t = ax_box.text(80, 1.2, '', fontsize=12, ha='center', color='#666', alpha=0)

    for frame in range(total_frames):
        t = frame / total_frames

        # Q1 (0.05~0.20)
        if 0.05 < t <= 0.20:
            p = clamp((t - 0.05) / 0.15)
            vl_q1.set_alpha(p); t_q1.set_text(f'Q1 = {q1:.0f}'); t_q1.set_alpha(p)
        if t > 0.20: vl_q1.set_alpha(1.0); t_q1.set_text(f'Q1 = {q1:.0f}'); t_q1.set_alpha(1.0)

        # Q2 (0.20~0.35)
        if 0.20 < t <= 0.35:
            p = clamp((t - 0.20) / 0.15)
            vl_q2.set_alpha(p); t_q2.set_text(f'Q2 = {q2:.0f}'); t_q2.set_alpha(p)
        if t > 0.35: vl_q2.set_alpha(1.0); t_q2.set_text(f'Q2 = {q2:.0f}'); t_q2.set_alpha(1.0)

        # Q3 (0.35~0.50)
        if 0.35 < t <= 0.50:
            p = clamp((t - 0.35) / 0.15)
            vl_q3.set_alpha(p); t_q3.set_text(f'Q3 = {q3:.0f}'); t_q3.set_alpha(p)
        if t > 0.50: vl_q3.set_alpha(1.0); t_q3.set_text(f'Q3 = {q3:.0f}'); t_q3.set_alpha(1.0)

        # Box plot caps (0.50~0.60)
        if 0.50 < t <= 0.60:
            p = clamp((t - 0.50) / 0.10)
            c_low.set_alpha(p); c_high.set_alpha(p)
        if t > 0.60: c_low.set_alpha(1.0); c_high.set_alpha(1.0)

        # Box body (0.60~0.70)
        if 0.60 < t <= 0.70:
            p = clamp((t - 0.60) / 0.10)
            box_patch.set_alpha(p * 0.7); sub_t.set_text('箱体: Q1 到 Q3'); sub_t.set_alpha(p)
        if t > 0.70: box_patch.set_alpha(0.7)

        # Median line (0.70~0.80)
        if 0.70 < t <= 0.80:
            p = clamp((t - 0.70) / 0.10)
            med_line.set_alpha(p); sub_t.set_text('中位线: Q2'); sub_t.set_alpha(1.0)
        if t > 0.80: med_line.set_alpha(1.0)

        # Whiskers (0.80~0.90)
        if 0.80 < t <= 0.90:
            p = clamp((t - 0.80) / 0.10)
            w_low.set_alpha(p); w_high.set_alpha(p); sub_t.set_text('须线: min 到 max')
        if t > 0.90: w_low.set_alpha(1.0); w_high.set_alpha(1.0)

        # Done
        if t > 0.92:
            sub_t.set_text(f'完成! IQR = Q3-Q1 = {iqr:.0f}'); sub_t.set_alpha(1.0)

        fname = os.path.join(frames_dir, f'frame_{frame:04d}.png')
        fig.savefig(fname, dpi=DPI, bbox_inches='tight')

    plt.close(fig)

    narration = (
        "将十五名同学的成绩从小到大排列，我们现在要找三个四分位数分割点。"
        "Q1是第一四分位数，即第百分之二十五的位置，前四分之一的数小于它。"
        "Q2是中位数，也就是第二四分位数，正好在正中间。"
        "Q3是第三四分位数，即第百分之七十五的位置。"
        "现在我们来构建箱线图。先标记最小值和最大值。"
        "然后画出箱体，从Q1到Q3。"
        "在箱体内画出中位数线。"
        "最后从箱体两端向最小值和最大值画出须线。"
        "这就是箱线图，也叫盒须图。四分位距IQR等于Q三减Q一，反映了中间百分之五十数据的跨度。"
    )
    audio_path = f'{BASE}/narration_03_quartile.mp3'
    run_audio(narration, audio_path)

    from moviepy import ImageSequenceClip, AudioFileClip
    frame_files = sorted([os.path.join(frames_dir, f) for f in os.listdir(frames_dir)])
    clip = ImageSequenceClip(frame_files, fps=FPS)
    audio = AudioFileClip(audio_path)
    clip = clip.with_audio(audio)
    out = f'{BASE}/video_03_quartile.mp4'
    clip.write_videofile(out, codec='libx264', fps=FPS, logger=None)
    clip.close(); audio.close()
    shutil.rmtree(frames_dir)
    print(f'  Video saved: {out}')

# ================================================================
# 视频 4: 数据分组
# ================================================================
def make_video4_grouping():
    print('\n=== Video 4: 数据分组 ===')

    np.random.seed(42)
    scores = np.concatenate([
        np.random.normal(65, 7, 10), np.random.normal(75, 5, 15),
        np.random.normal(82, 4, 15), np.random.normal(90, 5, 10),
    ]).clip(40, 100).astype(int)
    scores.sort()
    n = len(scores)
    bins = [40, 50, 60, 70, 80, 90, 100]
    hist_counts, _ = np.histogram(scores, bins=bins)

    frames_dir = tempfile.mkdtemp(prefix='frames4_')
    total_frames = 64

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [0.55, 0.45]})
    fig.patch.set_facecolor('#FEFEFE')

    ax1.set_xlim(35, 105); ax1.set_ylim(-0.5, 5.5)
    ax1.set_title('数据的分组 — 组距、频数、频率分布直方图', fontsize=15, fontweight='bold', color='#1D3557')
    for spine in ax1.spines.values(): spine.set_visible(False)
    ax1.set_yticks([]); ax1.grid(axis='x', alpha=0.2)

    ax1.scatter(scores, np.random.uniform(1.5, 3.5, n), s=25, c='#457B9D', alpha=0.7, zorder=3)

    rects = []
    for left, right, cnt in zip(bins[:-1], bins[1:], hist_counts):
        r = mpatches.Rectangle((left, 4), right - left, 0, alpha=0, facecolor='#A8DADC',
                               edgecolor='#457B9D', lw=1.5, zorder=2)
        ax1.add_patch(r); rects.append(r)

    bin_lbls = []
    for left, right in zip(bins[:-1], bins[1:]):
        t = ax1.text((left + right) / 2, 4.8, f'{left}~{right}', ha='center', fontsize=8, alpha=0, color='#666')
        bin_lbls.append(t)

    freq_lbls = []
    for i, cnt in enumerate(hist_counts):
        t = ax1.text((bins[i] + bins[i+1]) / 2, 4.3, '', ha='center', fontsize=11, alpha=0,
                     fontweight='bold', color='#1D3557')
        freq_lbls.append(t)

    ax2.set_xlim(0, 10); ax2.set_ylim(0, 4)
    ax2.axis('off')
    tbl_title = ax2.text(5, 3.5, '', ha='center', fontsize=13, fontweight='bold', color='#1D3557', alpha=0)
    tbl_content = ax2.text(5, 2.5, '', ha='center', fontsize=10, color='#333', alpha=0)
    principle = ax2.text(5, 1.2, '', ha='center', fontsize=12, color='#E63946', fontweight='bold', alpha=0)

    for frame in range(total_frames):
        t = frame / total_frames

        # Bin labels (0~0.25)
        if t <= 0.25:
            p = t / 0.25
            for lbl in bin_lbls: lbl.set_alpha(p)
            tbl_title.set_text('Step 1: 确定组距和组数'); tbl_title.set_alpha(p)
            tbl_content.set_text(f'数据范围: {scores.min()}~{scores.max()}, 组距 = 10分, 共 6 组'); tbl_content.set_alpha(p)
        else:
            for lbl in bin_lbls: lbl.set_alpha(1.0)
            tbl_title.set_text('Step 1: 确定组距和组数'); tbl_title.set_text(''); tbl_content.set_text('')

        # Bars + count (0.25~0.55)
        if 0.25 < t <= 0.55:
            p = clamp((t - 0.25) / 0.30)
            for rect, cnt in zip(rects, hist_counts):
                target_h = cnt / max(hist_counts) * 1.2
                rect.set_height(target_h * p); rect.set_alpha(0.7 * p)
            tbl_title.set_text('Step 2: 统计每组频数'); tbl_title.set_alpha(1.0)
            if p > 0.5:
                pp = clamp((p - 0.5) / 0.5)
                for lbl, cnt in zip(freq_lbls, hist_counts):
                    lbl.set_text(f'{cnt}人'); lbl.set_alpha(pp)

        if t > 0.55:
            for rect, cnt in zip(rects, hist_counts):
                target_h = cnt / max(hist_counts) * 1.2
                rect.set_height(target_h); rect.set_alpha(0.7)
            for lbl, cnt in zip(freq_lbls, hist_counts):
                lbl.set_text(f'{cnt}人'); lbl.set_alpha(1.0)

        # Principle (0.55~0.85)
        if 0.55 < t <= 0.85:
            p = clamp((t - 0.55) / 0.30)
            tbl_title.set_text('Step 3: 验证分组原则'); tbl_title.set_alpha(1.0)
            principle.set_text('分组原则: 组内差异尽可能小, 组间差异尽可能大'); principle.set_alpha(p)

        if t > 0.85:
            tbl_title.set_text('频率分布直方图完成!'); tbl_title.set_alpha(1.0)
            principle.set_text('频率 = 频数 / 数据总数 = 频数 / 50'); principle.set_alpha(1.0)

        fname = os.path.join(frames_dir, f'frame_{frame:04d}.png')
        fig.savefig(fname, dpi=DPI, bbox_inches='tight')

    plt.close(fig)

    narration = (
        "五十名同学的成绩散落在数轴上，看起来杂乱无章。"
        "数据的第一个步骤，是确定组距和组数。"
        "这里我们选择组距为十分，从四十分到一百分，一共分为六组。"
        "第二步，统计每组有多少个数据，也就是频数。"
        "我们画出直方图，横轴是分数段，纵轴是频数，也就是每组的人数。"
        "第三步，验证分组原则。分组的原则是：组内差异尽可能小，组间差异尽可能大。"
        "同一组的分数相近，不同组的分数明显不同。这就是好的分组。"
    )
    audio_path = f'{BASE}/narration_04_grouping.mp3'
    run_audio(narration, audio_path)

    from moviepy import ImageSequenceClip, AudioFileClip
    frame_files = sorted([os.path.join(frames_dir, f) for f in os.listdir(frames_dir)])
    clip = ImageSequenceClip(frame_files, fps=FPS)
    audio = AudioFileClip(audio_path)
    clip = clip.with_audio(audio)
    out = f'{BASE}/video_04_grouping.mp4'
    clip.write_videofile(out, codec='libx264', fps=FPS, logger=None)
    clip.close(); audio.close()
    shutil.rmtree(frames_dir)
    print(f'  Video saved: {out}')

# ================================================================
# Main
# ================================================================
if __name__ == '__main__':
    print('生成带语音讲解的 MP4 视频 (使用微软晓晓中文语音)...')
    print(f'FPS={FPS}, DPI={DPI}, 每个视频约 8 秒')
    make_video1_central()
    make_video2_dispersion()
    make_video3_quartile()
    make_video4_grouping()
    print('\n=== 全部完成! ===')
    print('输出文件:')
    for i, name in enumerate(['集中趋势','离散程度','四分位数与箱线图','数据分组'], 1):
        print(f'  {i}. video_0{i}_{["central","dispersion","quartile","grouping"][i-1]}.mp4')
