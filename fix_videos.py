"""
Regenerate ALL 4 narrated videos with working ffmpeg pipeline.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import asyncio, edge_tts, os, subprocess, shutil

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

BASE = 'E:/maths_work'
VOICE = 'zh-CN-XiaoxiaoNeural'
FPS = 10
DPI = 100
FFMPEG = r'C:\Users\86150\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'

def clamp(v): return max(0.0, min(1.0, v))

async def gen_audio(text, path):
    comm = edge_tts.Communicate(text, VOICE)
    await comm.save(path)
    print(f'  Audio: {os.path.getsize(path)} bytes')

def frames_to_video(frames_dir, audio_path, output_path, fps=FPS):
    cmd = [
        FFMPEG, '-y', '-framerate', str(fps),
        '-i', os.path.join(frames_dir, 'frame_%04d.png'),
        '-i', audio_path,
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast',
        '-movflags', '+faststart',
        '-c:a', 'aac', '-b:a', '64k',
        '-map', '0:v:0', '-map', '1:a:0', '-shortest',
        output_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f'  FFMPEG ERROR: {r.stderr[-300:]}')
        return False
    print(f'  Video: {os.path.getsize(output_path)//1024} KB')
    return True

def extract_poster(video_path, poster_path, t_frac=0.5):
    cmd = [FFMPEG, '-y', '-i', video_path, '-vframes', '1',
           '-ss', f'{t_frac}', '-q:v', '2', poster_path]
    subprocess.run(cmd, capture_output=True)

# ================================================================
def make_video1():
    print('\n### Video 1: Central Tendency ###')
    data = np.array([62, 68, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92, 95, 96, 98])
    data_sort = np.sort(data); n = len(data)
    mean_val = np.mean(data)

    frames_dir = f'{BASE}/_frames1'
    os.makedirs(frames_dir, exist_ok=True)
    total_frames = 80

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [1.1, 1]})
    fig.patch.set_facecolor('#FEFEFE')
    ax1.set_xlim(55, 105); ax1.set_ylim(-2, 6)
    ax1.set_title('数据的集中趋势', fontsize=16, fontweight='bold', color='#1D3557')
    ax1.set_xlabel('成绩（分）', fontsize=13)
    ax1.set_yticks([])
    for spine in ax1.spines.values(): spine.set_visible(False)
    ax1.grid(axis='x', alpha=0.15)

    for val in data_sort:
        ax1.plot(val, 0.5 + np.random.uniform(-0.25, 0.25), 'o', ms=14, color='#457B9D', zorder=5,
                markeredgecolor='white', markeredgewidth=1.5)

    mean_arrow = ax1.annotate('', xy=(mean_val, 0), xytext=(mean_val, 2.5),
                              arrowprops=dict(arrowstyle='->', color='#E63946', lw=3), alpha=0)
    mean_txt = ax1.text(mean_val, 3, '', fontsize=14, color='#E63946', ha='center', fontweight='bold', alpha=0)

    ax2.set_xlim(0, 100); ax2.set_ylim(0, 5); ax2.axis('off')
    w_title = ax2.text(50, 4.2, '', ha='center', fontsize=15, fontweight='bold', color='#1D3557', alpha=0)
    w_formula = ax2.text(50, 3, '', ha='center', fontsize=13, color='#E63946', alpha=0)

    plt.tight_layout(pad=1)
    for frame in range(total_frames):
        t = frame / total_frames
        if 0.15 < t <= 0.45:
            p = clamp((t - 0.15) / 0.30)
            mean_arrow.set_alpha(p)
            mean_txt.set_text(f'平均数 = {mean_val:.1f}'); mean_txt.set_alpha(p)
        if t > 0.45: mean_arrow.set_alpha(1.0); mean_txt.set_text(f'平均数 = {mean_val:.1f}'); mean_txt.set_alpha(1.0)

        if 0.55 < t <= 0.90:
            p = clamp((t - 0.55) / 0.35)
            w_title.set_text('加权平均数: 期末总评 = 平时x15% + 期中x30% + 期末x40% = 84.4'); w_title.set_alpha(p)
        if t > 0.90: w_title.set_alpha(1.0)

        fig.savefig(frames_dir + f'/frame_{frame:04d}.png', dpi=DPI,
                   facecolor='white')
    plt.close(fig)

    audio_path = f'{BASE}/narration_01_central.mp3'
    text = "这是一组15名同学的数学成绩。算术平均数等于所有数据之和除以个数，是数据的平衡点。加权平均数用于计算期末总评，不同项目权重不同，期末考试权重最大。"
    asyncio.run(gen_audio(text, audio_path))
    out = f'{BASE}/video_01_central.mp4'
    if frames_to_video(frames_dir, audio_path, out):
        extract_poster(out, f'{BASE}/poster_01_central.png', 0.5)
    shutil.rmtree(frames_dir)

# ================================================================
def make_video2():
    print('\n### Video 2: Dispersion ###')
    data_a = np.array([72, 74, 76, 78, 80, 82, 84, 86, 88, 90])
    mean_a = np.mean(data_a); n_a = len(data_a)

    frames_dir = f'{BASE}/_frames2'
    os.makedirs(frames_dir, exist_ok=True)
    total_frames = 80

    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [1, 0.7]})
    fig.patch.set_facecolor('#FEFEFE')
    ax_top.set_xlim(-0.5, n_a + 0.5); ax_top.set_ylim(55, 100)
    ax_top.set_title('数据的离散程度', fontsize=16, fontweight='bold', color='#1D3557')
    ax_top.set_ylabel('成绩（分）', fontsize=13)
    for spine in ax_top.spines.values(): spine.set_visible(False)
    ax_top.grid(axis='y', alpha=0.15)

    ax_top.axhline(y=mean_a, color='#E63946', lw=2.5, ls='--', alpha=0.6, zorder=3)
    ax_top.text(9.2, mean_a + 1, f'平均数={mean_a:.0f}', fontsize=11, color='#E63946', fontweight='bold', alpha=0.6)

    for i, val in enumerate(data_a):
        ax_top.plot(i, val, 'o', ms=20, color='#457B9D', zorder=5, markeredgecolor='white', markeredgewidth=2)
        ax_top.text(i, val + 2, str(val), ha='center', fontsize=9, color='#333')

    dev_lines = []; dev_texts = []
    for i, val in enumerate(data_a):
        dev = val - mean_a
        l, = ax_top.plot([i, i], [mean_a, val], '-', lw=3, alpha=0, zorder=2,
                        color='#E63946' if dev < 0 else '#2A9D8F')
        dev_lines.append(l)
        t = ax_top.text(i + 0.3, (mean_a + val) / 2, '', fontsize=10, alpha=0, fontweight='bold')
        dev_texts.append((t, dev))

    ax_bot.set_xlim(0, 10); ax_bot.set_ylim(0, 5.5); ax_bot.axis('off')
    q_title = ax_bot.text(5, 5, '', ha='center', fontsize=15, fontweight='bold', color='#1D3557', alpha=0)
    var_text = ax_bot.text(5, 3.5, '', ha='center', fontsize=14, color='#E63946', fontweight='bold', alpha=0)
    std_text = ax_bot.text(5, 2, '', ha='center', fontsize=14, color='#2A9D8F', fontweight='bold', alpha=0)

    for frame in range(total_frames):
        t = frame / total_frames
        if 0.15 < t <= 0.50:
            p = clamp((t - 0.15) / 0.35)
            for l in dev_lines: l.set_alpha(p * 0.85)
            for txt, dev in dev_texts: txt.set_text(f'{dev:+.1f}'); txt.set_alpha(p)
        if t > 0.50:
            for l in dev_lines: l.set_alpha(0.85)
            for txt, dev in dev_texts: txt.set_text(f'{dev:+.1f}'); txt.set_alpha(1.0)
        if 0.50 < t <= 0.85:
            p = clamp((t - 0.50) / 0.35)
            q_title.set_text(f'离差平方和 Q = {np.sum((data_a-mean_a)**2):.1f}'); q_title.set_alpha(p)
            var_text.set_text(f'方差 s^2 = Q / n = {np.var(data_a):.2f}'); var_text.set_alpha(p)
            std_text.set_text(f'标准差 s = {np.std(data_a):.2f}'); std_text.set_alpha(p)
        if t > 0.85:
            q_title.set_alpha(1.0); var_text.set_alpha(1.0); std_text.set_alpha(1.0)

        fig.savefig(frames_dir + f'/frame_{frame:04d}.png', dpi=DPI,
                   facecolor='white')
    plt.close(fig)

    audio_path = f'{BASE}/narration_02_dispersion.mp3'
    text = "红色虚线是平均数。绿色线表示正离差，红色线表示负离差。离差平方和Q等于每个离差的平方之和。方差等于Q除以n。标准差等于方差的算术平方根，是衡量数据离散程度最常用的指标。"
    asyncio.run(gen_audio(text, audio_path))
    out = f'{BASE}/video_02_dispersion.mp4'
    if frames_to_video(frames_dir, audio_path, out):
        extract_poster(out, f'{BASE}/poster_02_dispersion.png', 0.5)
    shutil.rmtree(frames_dir)

# ================================================================
def make_video3():
    print('\n### Video 3: Quartiles & Box Plot ###')
    data = np.array([62, 68, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92, 95, 96, 98])
    data_sort = np.sort(data); n = len(data)
    q1, q2, q3 = np.percentile(data, 25), np.percentile(data, 50), np.percentile(data, 75)
    vmin, vmax = data_sort[0], data_sort[-1]

    frames_dir = f'{BASE}/_frames3'
    os.makedirs(frames_dir, exist_ok=True)
    total_frames = 80

    fig, (ax_data, ax_box) = plt.subplots(2, 1, figsize=(9, 6.5), gridspec_kw={'height_ratios': [1.2, 1]})
    fig.patch.set_facecolor('#FEFEFE')
    ax_data.set_xlim(-0.5, n + 0.5); ax_data.set_ylim(55, 105)
    ax_data.set_title('四分位数与箱线图', fontsize=16, fontweight='bold', color='#1D3557')
    ax_data.set_xticks([]); ax_data.set_yticks(data_sort)
    for spine in ax_data.spines.values(): spine.set_visible(False)
    ax_data.grid(axis='y', alpha=0.15)

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

    ax_box.set_xlim(55, 105); ax_box.set_ylim(-0.5, 1.5)
    ax_box.set_xlabel('成绩（分）', fontsize=13)
    for spine in ax_box.spines.values(): spine.set_visible(False)
    ax_box.grid(axis='x', alpha=0.15)

    box_patch = mpatches.Polygon([[q1,-0.25],[q1,0.25],[q3,0.25],[q3,-0.25]], closed=True,
                                  facecolor='#A8DADC', edgecolor='#457B9D', lw=2, alpha=0)
    ax_box.add_patch(box_patch)
    med_line = ax_box.axvline(x=q2, ymin=0.44, ymax=0.56, color='#1D3557', lw=3, alpha=0)
    w_low = ax_box.plot([vmin,q1], [0,0], color='#457B9D', lw=2, alpha=0)[0]
    w_high = ax_box.plot([q3,vmax], [0,0], color='#457B9D', lw=2, alpha=0)[0]
    c_low = ax_box.plot([vmin,vmin], [-0.12,0.12], color='#457B9D', lw=2, alpha=0)[0]
    c_high = ax_box.plot([vmax,vmax], [-0.12,0.12], color='#457B9D', lw=2, alpha=0)[0]
    sub_t = ax_box.text(80, 1.2, '', fontsize=13, ha='center', color='#666', alpha=0)

    plt.tight_layout(pad=1)
    for frame in range(total_frames):
        t = frame / total_frames
        if 0.05 < t <= 0.18:
            p = clamp((t - 0.05) / 0.13); vl_q1.set_alpha(p); t_q1.set_text(f'Q1 = {q1:.0f}'); t_q1.set_alpha(p)
        if t > 0.18: vl_q1.set_alpha(1.0); t_q1.set_text(f'Q1 = {q1:.0f}'); t_q1.set_alpha(1.0)
        if 0.20 < t <= 0.33:
            p = clamp((t - 0.20) / 0.13); vl_q2.set_alpha(p); t_q2.set_text(f'Q2 = {q2:.0f}'); t_q2.set_alpha(p)
        if t > 0.33: vl_q2.set_alpha(1.0); t_q2.set_text(f'Q2 = {q2:.0f}'); t_q2.set_alpha(1.0)
        if 0.36 < t <= 0.49:
            p = clamp((t - 0.36) / 0.13); vl_q3.set_alpha(p); t_q3.set_text(f'Q3 = {q3:.0f}'); t_q3.set_alpha(p)
        if t > 0.49: vl_q3.set_alpha(1.0); t_q3.set_text(f'Q3 = {q3:.0f}'); t_q3.set_alpha(1.0)
        if 0.52 < t <= 0.62:
            p = clamp((t - 0.52) / 0.10); c_low.set_alpha(p); c_high.set_alpha(p)
        if t > 0.62: c_low.set_alpha(1.0); c_high.set_alpha(1.0)
        if 0.62 < t <= 0.74:
            p = clamp((t - 0.62) / 0.12); box_patch.set_alpha(p * 0.7); sub_t.set_text('画箱体: Q1 到 Q3'); sub_t.set_alpha(1.0)
        if t > 0.74: box_patch.set_alpha(0.7)
        if 0.74 < t <= 0.86:
            p = clamp((t - 0.74) / 0.12); med_line.set_alpha(p); sub_t.set_text('画中位线: Q2')
        if t > 0.86: med_line.set_alpha(1.0)
        if 0.86 < t <= 0.96:
            p = clamp((t - 0.86) / 0.10); w_low.set_alpha(p); w_high.set_alpha(p); sub_t.set_text('画须线: min 到 max')
        if t > 0.96: w_low.set_alpha(1.0); w_high.set_alpha(1.0); sub_t.set_text(f'完成! IQR = Q3-Q1 = {q3-q1:.0f}')

        fig.savefig(frames_dir + f'/frame_{frame:04d}.png', dpi=DPI,
                   facecolor='white')
    plt.close(fig)

    audio_path = f'{BASE}/narration_03_quartile.mp3'
    text = "Q1是第一四分位数。Q2是中位数，也是第二四分位数。Q3是第三四分位数。先标记最小值和最大值。然后从Q1到Q3画箱体。在箱体内画中位数线。从箱体向两端画须线。这就是箱线图。IQR等于Q三减Q一，反映中间百分之五十数据的跨度。"
    asyncio.run(gen_audio(text, audio_path))
    out = f'{BASE}/video_03_quartile.mp4'
    if frames_to_video(frames_dir, audio_path, out):
        extract_poster(out, f'{BASE}/poster_03_quartile.png', 0.5)
    shutil.rmtree(frames_dir)

# ================================================================
def make_video4():
    print('\n### Video 4: Data Grouping ###')
    np.random.seed(42)
    scores = np.concatenate([
        np.random.normal(65, 7, 10), np.random.normal(75, 5, 15),
        np.random.normal(82, 4, 15), np.random.normal(90, 5, 10),
    ]).clip(40, 100).astype(int)
    scores.sort(); n = len(scores)
    bins = [40, 50, 60, 70, 80, 90, 100]
    hist_counts, _ = np.histogram(scores, bins=bins)

    frames_dir = f'{BASE}/_frames4'
    os.makedirs(frames_dir, exist_ok=True)
    total_frames = 80

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [0.55, 0.45]})
    fig.patch.set_facecolor('#FEFEFE')
    ax1.set_xlim(35, 105); ax1.set_ylim(-0.5, 5.5)
    ax1.set_title('数据的分组', fontsize=16, fontweight='bold', color='#1D3557')
    for spine in ax1.spines.values(): spine.set_visible(False)
    ax1.set_yticks([]); ax1.grid(axis='x', alpha=0.15)
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

    ax2.set_xlim(0, 10); ax2.set_ylim(0, 4); ax2.axis('off')
    tbl_title = ax2.text(5, 3.5, '', ha='center', fontsize=14, fontweight='bold', color='#1D3557', alpha=0)
    principle = ax2.text(5, 1.5, '', ha='center', fontsize=13, color='#E63946', fontweight='bold', alpha=0)

    for frame in range(total_frames):
        t = frame / total_frames
        if t <= 0.22:
            p = t / 0.22
            for lbl in bin_lbls: lbl.set_alpha(p)
            tbl_title.set_text('Step 1: 确定组距 = 10分, 共6组'); tbl_title.set_alpha(p)
        else:
            for lbl in bin_lbls: lbl.set_alpha(1.0)
        if 0.25 < t <= 0.55:
            p = clamp((t - 0.25) / 0.30)
            for rect, cnt in zip(rects, hist_counts):
                rect.set_height(cnt / max(hist_counts) * 1.2 * p); rect.set_alpha(0.7 * p)
            tbl_title.set_text('Step 2: 统计每组频数'); tbl_title.set_alpha(1.0)
            if p > 0.5:
                pp = clamp((p - 0.5) / 0.5)
                for lbl, cnt in zip(freq_lbls, hist_counts): lbl.set_text(f'{cnt}A'); lbl.set_alpha(pp)
        if t > 0.55:
            for rect, cnt in zip(rects, hist_counts):
                rect.set_height(cnt / max(hist_counts) * 1.2); rect.set_alpha(0.7)
            for lbl, cnt in zip(freq_lbls, hist_counts): lbl.set_text(f'{cnt}A'); lbl.set_alpha(1.0)
        if 0.60 < t <= 0.90:
            p = clamp((t - 0.60) / 0.30)
            tbl_title.set_text('分组原则: 组内差异小, 组间差异大'); tbl_title.set_alpha(1.0)
            principle.set_text('同一组分数相近, 不同组分数明显不同'); principle.set_alpha(p)
        if t > 0.90: principle.set_text('频率 = 频数 / 数据总数'); principle.set_alpha(1.0)

        fig.savefig(frames_dir + f'/frame_{frame:04d}.png', dpi=DPI,
                   facecolor='white')
    plt.close(fig)

    audio_path = f'{BASE}/narration_04_grouping.mp3'
    text = "五十名同学的成绩散落在数轴上。第一步确定组距为十分，分为六组。第二步统计每组有多少个数据，即频数。画出直方图，横轴是分数段，纵轴是频数。分组原则：组内差异尽可能小，组间差异尽可能大。"
    asyncio.run(gen_audio(text, audio_path))
    out = f'{BASE}/video_04_grouping.mp4'
    if frames_to_video(frames_dir, audio_path, out):
        extract_poster(out, f'{BASE}/poster_04_grouping.png', 0.5)
    shutil.rmtree(frames_dir)

# ================================================================
if __name__ == '__main__':
    print('='*50)
    make_video1()
    make_video2()
    make_video3()
    make_video4()
    print('\n=== ALL 4 VIDEOS REGENERATED ===')
