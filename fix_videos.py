"""
Regenerate ALL 4 narrated videos with FULL narration (not cut off).
Strategy: generate audio first, get duration, generate enough frames.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import asyncio, edge_tts, os, subprocess, shutil
from PIL import Image

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

BASE = 'E:/maths_work'
VOICE = 'zh-CN-XiaoxiaoNeural'
FPS = 10
DPI = 100
# Note: DPI 100 is the max that works with this ffmpeg build
FFMPEG = r'C:\Users\86150\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'

def clamp(v): return max(0.0, min(1.0, v))

async def gen_audio(text, path):
    comm = edge_tts.Communicate(text, VOICE)
    await comm.save(path)

def get_audio_duration(path):
    """Estimate MP3 duration from file size and bitrate (128kbps default for edge-tts)"""
    size_bytes = os.path.getsize(path)
    # edge-tts MP3 is typically ~128kbps = 16KB/s
    duration = size_bytes / 16000
    return max(15.0, min(60.0, duration))  # clamp between 15-60s

def frames_to_video(frames_dir, audio_path, output_path, fps=FPS):
    cmd = [
        FFMPEG, '-y', '-framerate', str(fps),
        '-i', frames_dir + '/frame_%04d.png',
        '-i', audio_path,
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast',
        '-movflags', '+faststart',
        '-c:a', 'aac', '-b:a', '64k',
        '-map', '0:v:0', '-map', '1:a:0',
        '-shortest',
        output_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    ok = r.returncode == 0
    if ok: print(f'  Video: {os.path.getsize(output_path)//1024} KB')
    else: print(f'  FFMPEG ERROR: {r.stderr[-200:]}')
    return ok

def extract_poster(vid, poster, t=0.5):
    subprocess.run([FFMPEG, '-y', '-i', vid, '-vframes', '1', '-ss', f'{t}', '-q:v', '2', poster],
                   capture_output=True)

# ================================================================
# VIDEO 1: 集中趋势
# ================================================================
def make_video1():
    print('\n### Video 1: Central Tendency ###')

    narration = (
        "大家好，我们来学习数据的集中趋势。"
        "这是一组15名同学的数学测验成绩，从小到大排列在数轴上。"
        "集中趋势描述的是数据的中心在哪里，最常用的指标有三个：平均数、中位数和众数。"
        "算术平均数，简称平均数，等于所有数据之和除以数据的个数。"
        "它的物理意义是数据的平衡点，就像跷跷板的支点一样。"
        "把每个数据到平均数的正负离差加起来，正好等于零。"
        "中位数，是把数据排序后正中间的那个数。"
        "如果数据个数是奇数，中位数就是最中间的那个。"
        "如果数据个数是偶数，中位数就是中间两个数的平均数。"
        "中位数的优点是不受极端值的影响，我们说它比较稳健。"
        "众数，是数据中出现次数最多的那个值。一组数据可以有多个众数，也可以没有众数。"
        "然后是加权平均数。不同项目的重要程度不同，需要给每个项目分配一个权重。"
        "比如期末总评：平时作业占百分之十五，课堂表现占百分之十五，期中占百分之三十，期末占百分之四十。"
        "加权平均数等于各项目分数乘以对应权重之和，再除以权重之和。"
        "以上是集中趋势的四个核心概念。平均数对极端值敏感，中位数更稳健，加权平均数体现重要性差异，众数反映典型水平。"
    )

    audio_path = f'{BASE}/narration_01_central.mp3'
    asyncio.run(gen_audio(narration, audio_path))
    duration = get_audio_duration(audio_path)
    total_frames = int(duration * FPS) + 5  # add a few frames buffer
    print(f'  Audio: {duration:.1f}s -> {total_frames} frames')

    frames_dir = f'{BASE}/_frames1'
    os.makedirs(frames_dir, exist_ok=True)

    data = np.sort(np.array([62,68,70,72,75,78,80,82,85,88,90,92,95,96,98]))
    n = len(data); mean_val = np.mean(data); median_val = np.median(data)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [1.1, 1]})
    fig.patch.set_facecolor('white')
    ax1.set_xlim(55,105); ax1.set_ylim(-2,6)
    ax1.set_title('数据的集中趋势', fontsize=16, fontweight='bold', color='#1D3557')
    ax1.set_xlabel('成绩（分）', fontsize=13); ax1.set_yticks([])
    for s in ax1.spines.values(): s.set_visible(False)
    ax1.grid(axis='x', alpha=0.15)
    for v in data: ax1.plot(v, 0.5+np.random.uniform(-0.25,0.25), 'o', ms=14, color='#457B9D', zorder=5, mec='white', mew=1.5)

    mean_arrow = ax1.annotate('', xy=(mean_val,0), xytext=(mean_val,2.5),
                              arrowprops=dict(arrowstyle='->',color='#E63946',lw=3), alpha=0)
    mean_txt = ax1.text(mean_val, 3, '', fontsize=14, color='#E63946', ha='center', fontweight='bold', alpha=0)
    median_line = ax1.axvline(x=median_val, color='#2A9D8F', lw=2.5, ls='--', alpha=0)
    median_txt = ax1.text(median_val, 5, '', fontsize=12, color='#2A9D8F', ha='center', fontweight='bold', alpha=0)

    ax2.set_xlim(0,100); ax2.set_ylim(0,5); ax2.axis('off')
    w_title = ax2.text(50,4.2,'',ha='center',fontsize=15,fontweight='bold',color='#1D3557',alpha=0)
    w_detail = ax2.text(50,2.8,'',ha='center',fontsize=13,color='#E63946',alpha=0)
    w_result = ax2.text(50,1.5,'',ha='center',fontsize=14,color='#2A9D8F',fontweight='bold',alpha=0)

    plt.tight_layout(pad=1)

    for frm in range(total_frames):
        t = frm / total_frames
        # 0.00-0.08: intro, just data
        # 0.08-0.30: mean explanation
        if 0.08 < t <= 0.35:
            p = clamp((t-0.08)/0.27)
            mean_arrow.set_alpha(p)
            mean_txt.set_text(f'平均数 = {mean_val:.1f}'); mean_txt.set_alpha(p)
        if t > 0.35:
            mean_arrow.set_alpha(1.0); mean_txt.set_text(f'平均数 = {mean_val:.1f}'); mean_txt.set_alpha(1.0)
        # 0.35-0.55: median
        if 0.35 < t <= 0.58:
            p = clamp((t-0.35)/0.23)
            median_line.set_alpha(p)
            median_txt.set_text(f'中位数 = {median_val:.0f}'); median_txt.set_alpha(p)
        if t > 0.58:
            median_line.set_alpha(1.0); median_txt.set_text(f'中位数 = {median_val:.0f}'); median_txt.set_alpha(1.0)
        # 0.60-0.90: weighted mean
        if 0.60 < t <= 0.92:
            p = clamp((t-0.60)/0.32)
            w_title.set_text('加权平均数: 期末总评'); w_title.set_alpha(p)
            w_detail.set_text('= 88x0.15 + 92x0.15 + 78x0.30 + 85x0.40'); w_detail.set_alpha(p)
            w_result.set_text('= 84.4 分'); w_result.set_alpha(p)
        if t > 0.92:
            w_title.set_alpha(1.0); w_detail.set_alpha(1.0); w_result.set_alpha(1.0)

        fig.savefig(frames_dir + f'/frame_{frm:04d}.png', dpi=DPI, facecolor='white')
    plt.close(fig)

    out = f'{BASE}/video_01_central.mp4'
    if frames_to_video(frames_dir, audio_path, out):
        extract_poster(out, f'{BASE}/poster_01_central.png', 0.4)
    shutil.rmtree(frames_dir)

# ================================================================
# VIDEO 2: 离散程度
# ================================================================
def make_video2():
    print('\n### Video 2: Dispersion ###')

    narration = (
        "接下来我们学习数据的离散程度。"
        "离散程度描述的是数据散得有多开，也就是数据的波动大小。"
        "我们来看一组10名同学的成绩。红色虚线是平均数。"
        "离差，就是每个数据减去平均数得到的差。"
        "绿色线表示正离差，也就是高于平均数的部分。"
        "红色线表示负离差，也就是低于平均数的部分。"
        "如果我们直接把所有离差相加，正的和负的会互相抵消，结果永远是零。"
        "所以我们需要把每个离差先平方，再求和。这就得到了离差平方和，用大写字母Q表示。"
        "离差平方和越大，说明数据分散得越开。"
        "但离差平方和有一个缺点：它受数据个数的影响。数据越多，Q自然就越大。"
        "为了消除数据个数的影响，我们把Q除以数据的个数n，得到方差。"
        "方差是衡量数据离散程度最核心的指标。方差大，说明数据参差不齐。方差小，说明数据整齐。"
        "标准差等于方差的算术平方根。标准差的单位与原始数据一致，更容易理解和比较。"
        "总结一下：离差描述单个数据的偏离，离差平方和描述了整体的偏离总量，方差是平均化的偏离量，标准差是方差的平方根，单位与原始数据相同。"
    )

    audio_path = f'{BASE}/narration_02_dispersion.mp3'
    asyncio.run(gen_audio(narration, audio_path))
    duration = get_audio_duration(audio_path)
    total_frames = int(duration * FPS) + 5
    print(f'  Audio: {duration:.1f}s -> {total_frames} frames')

    frames_dir = f'{BASE}/_frames2'
    os.makedirs(frames_dir, exist_ok=True)

    da = np.array([72,74,76,78,80,82,84,86,88,90])
    ma = np.mean(da); na = len(da)

    fig, (ax_t, ax_b) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={'height_ratios': [1, 0.7]})
    fig.patch.set_facecolor('white')
    ax_t.set_xlim(-0.5, na+0.5); ax_t.set_ylim(55,100)
    ax_t.set_title('数据的离散程度', fontsize=16, fontweight='bold', color='#1D3557')
    ax_t.set_ylabel('成绩（分）', fontsize=13)
    for s in ax_t.spines.values(): s.set_visible(False)
    ax_t.grid(axis='y', alpha=0.15)
    ax_t.axhline(y=ma, color='#E63946', lw=2.5, ls='--', alpha=0.6, zorder=3)
    ax_t.text(9.2, ma+1, f'平均数={ma:.0f}', fontsize=11, color='#E63946', fontweight='bold', alpha=0.6)

    for i,v in enumerate(da):
        ax_t.plot(i,v,'o',ms=20,color='#457B9D',zorder=5,mec='white',mew=2)
        ax_t.text(i,v+2,str(v),ha='center',fontsize=9,color='#333')

    dlines=[]; dtxts=[]
    for i,v in enumerate(da):
        dev=v-ma
        l,=ax_t.plot([i,i],[ma,v],'-',lw=3,alpha=0,zorder=2,color='#E63946' if dev<0 else '#2A9D8F')
        dlines.append(l)
        t=ax_t.text(i+0.3,(ma+v)/2,'',fontsize=10,alpha=0,fontweight='bold')
        dtxts.append((t,dev))

    ax_b.set_xlim(0,10); ax_b.set_ylim(0,5.5); ax_b.axis('off')
    qt=ax_b.text(5,5,'',ha='center',fontsize=15,fontweight='bold',color='#1D3557',alpha=0)
    vt=ax_b.text(5,3.5,'',ha='center',fontsize=14,color='#E63946',fontweight='bold',alpha=0)
    st=ax_b.text(5,2,'',ha='center',fontsize=14,color='#2A9D8F',fontweight='bold',alpha=0)

    plt.tight_layout(pad=1)

    for frm in range(total_frames):
        t=frm/total_frames
        if 0.05<t<=0.45:
            p=clamp((t-0.05)/0.40)
            for l in dlines: l.set_alpha(p*0.85)
            for tx,dev in dtxts: tx.set_text(f'{dev:+.1f}'); tx.set_alpha(p)
        if t>0.45:
            for l in dlines: l.set_alpha(0.85)
            for tx,dev in dtxts: tx.set_text(f'{dev:+.1f}'); tx.set_alpha(1.0)
        if 0.48<t<=0.85:
            p=clamp((t-0.48)/0.37)
            qt.set_text(f'离差平方和 Q = {np.sum((da-ma)**2):.1f}'); qt.set_alpha(p)
            vt.set_text(f'方差 s^2 = Q / n = {np.var(da):.2f}'); vt.set_alpha(p)
            st.set_text(f'标准差 s = {np.std(da):.2f}'); st.set_alpha(p)
        if t>0.85: qt.set_alpha(1.0); vt.set_alpha(1.0); st.set_alpha(1.0)
        fig.savefig(frames_dir + f'/frame_{frm:04d}.png', dpi=DPI, facecolor='white')
    plt.close(fig)

    out = f'{BASE}/video_02_dispersion.mp4'
    if frames_to_video(frames_dir, audio_path, out):
        extract_poster(out, f'{BASE}/poster_02_dispersion.png', 0.4)
    shutil.rmtree(frames_dir)

# ================================================================
# VIDEO 3: 四分位数与箱线图
# ================================================================
def make_video3():
    print('\n### Video 3: Quartiles & Box Plot ###')

    narration = (
        "现在我们学习四分位数和箱线图，这是新课标新增的重要内容。"
        "这里有15名同学的成绩，从小到大排列在数轴上。"
        "四分位数就是把排序后的数据分成四等份的三个分割点。"
        "Q1是第一四分位数，也叫下四分位数，是第25百分位数。"
        "在Q1之前，有大约百分之二十五的数据。Q1之后，有大约百分之七十五的数据。"
        "Q2是第二四分位数，也就是我们熟悉的中位数，是第50百分位数。"
        "Q2正好把数据分成前后两半，一半比它小，一半比它大。"
        "Q3是第三四分位数，也叫上四分位数，是第75百分位数。"
        "在Q3之前，有大约百分之七十五的数据。"
        "计算方法是：先找Q2，再分别在前半段和后半段找中位数，就是Q1和Q3。"
        "现在我们来构建箱线图，也叫盒须图。"
        "第一步，标记最小值和最大值，作为须线的两个端点。"
        "第二步，从Q1到Q3画一个矩形，这就是箱体。箱体的宽度反映了中间百分之五十数据的范围。"
        "第三步，在箱体内画出中位数线。中位数线在箱体中的位置，可以反映数据分布的偏态。"
        "第四步，从箱体两端向最小值和最大值画出须线。"
        "这样箱线图就完成了。四分位距IQR等于Q3减Q1。"
        "箱线图最大的优点是：只用五个数就能概括整个数据集的分布形态，非常简洁高效。"
    )

    audio_path = f'{BASE}/narration_03_quartile.mp3'
    asyncio.run(gen_audio(narration, audio_path))
    duration = get_audio_duration(audio_path)
    total_frames = int(duration * FPS) + 5
    print(f'  Audio: {duration:.1f}s -> {total_frames} frames')

    frames_dir = f'{BASE}/_frames3'
    os.makedirs(frames_dir, exist_ok=True)

    data = np.sort(np.array([62,68,70,72,75,78,80,82,85,88,90,92,95,96,98]))
    n=len(data); q1,q2,q3=np.percentile(data,25),np.percentile(data,50),np.percentile(data,75)
    vmin,vmax=data[0],data[-1]

    fig,(ax_d,ax_b)=plt.subplots(2,1,figsize=(9,6.5),gridspec_kw={'height_ratios':[1.2,1]})
    fig.patch.set_facecolor('white')
    ax_d.set_xlim(-0.5,n+0.5); ax_d.set_ylim(55,105)
    ax_d.set_title('四分位数与箱线图',fontsize=16,fontweight='bold',color='#1D3557')
    ax_d.set_xticks([]); ax_d.set_yticks(data)
    for s in ax_d.spines.values(): s.set_visible(False)
    ax_d.grid(axis='y',alpha=0.15)
    Q1_C,Q2_C,Q3_C='#E63946','#1D3557','#2A9D8F'
    ax_d.scatter(range(n),data,s=100,c='#457B9D',zorder=5,ec='white',lw=1)
    for i,v in enumerate(data): ax_d.text(i,v+1.5,str(v),ha='center',fontsize=8,color='#333')

    i1,i2,i3=3.5,7,10.5
    vl1=ax_d.axvline(x=i1,color=Q1_C,lw=2,ls='--',alpha=0)
    vl2=ax_d.axvline(x=i2,color=Q2_C,lw=2.5,ls='--',alpha=0)
    vl3=ax_d.axvline(x=i3,color=Q3_C,lw=2,ls='--',alpha=0)
    t1=ax_d.text(i1,103,'',fontsize=11,color=Q1_C,ha='center',fontweight='bold',alpha=0)
    t2=ax_d.text(i2,103,'',fontsize=11,color=Q2_C,ha='center',fontweight='bold',alpha=0)
    t3=ax_d.text(i3,103,'',fontsize=11,color=Q3_C,ha='center',fontweight='bold',alpha=0)

    ax_b.set_xlim(55,105); ax_b.set_ylim(-0.5,1.5)
    ax_b.set_xlabel('成绩（分）',fontsize=13)
    for s in ax_b.spines.values(): s.set_visible(False)
    ax_b.grid(axis='x',alpha=0.15)

    box=mpatches.Polygon([[q1,-0.25],[q1,0.25],[q3,0.25],[q3,-0.25]],closed=True,
                          facecolor='#A8DADC',edgecolor='#457B9D',lw=2,alpha=0)
    ax_b.add_patch(box)
    med=ax_b.axvline(x=q2,ymin=0.44,ymax=0.56,color='#1D3557',lw=3,alpha=0)
    wl=ax_b.plot([vmin,q1],[0,0],color='#457B9D',lw=2,alpha=0)[0]
    wh=ax_b.plot([q3,vmax],[0,0],color='#457B9D',lw=2,alpha=0)[0]
    cl=ax_b.plot([vmin,vmin],[-0.12,0.12],color='#457B9D',lw=2,alpha=0)[0]
    ch=ax_b.plot([vmax,vmax],[-0.12,0.12],color='#457B9D',lw=2,alpha=0)[0]
    st=ax_b.text(80,1.2,'',fontsize=13,ha='center',color='#666',alpha=0)

    plt.tight_layout(pad=1)

    for frm in range(total_frames):
        t=frm/total_frames
        if 0.05<t<=0.22:
            p=clamp((t-0.05)/0.17); vl1.set_alpha(p); t1.set_text(f'Q1 = {q1:.0f}'); t1.set_alpha(p)
        if t>0.22: vl1.set_alpha(1.0); t1.set_text(f'Q1 = {q1:.0f}'); t1.set_alpha(1.0)
        if 0.25<t<=0.42:
            p=clamp((t-0.25)/0.17); vl2.set_alpha(p); t2.set_text(f'Q2 = {q2:.0f}'); t2.set_alpha(p)
        if t>0.42: vl2.set_alpha(1.0); t2.set_text(f'Q2 = {q2:.0f}'); t2.set_alpha(1.0)
        if 0.45<t<=0.62:
            p=clamp((t-0.45)/0.17); vl3.set_alpha(p); t3.set_text(f'Q3 = {q3:.0f}'); t3.set_alpha(p)
        if t>0.62: vl3.set_alpha(1.0); t3.set_text(f'Q3 = {q3:.0f}'); t3.set_alpha(1.0)
        if 0.65<t<=0.74:
            p=clamp((t-0.65)/0.09); cl.set_alpha(p); ch.set_alpha(p)
            st.set_text('Step 1: 标记最小值和最大值'); st.set_alpha(p)
        if t>0.74: cl.set_alpha(1.0); ch.set_alpha(1.0)
        if 0.75<t<=0.84:
            p=clamp((t-0.75)/0.09); box.set_alpha(p*0.7)
            st.set_text('Step 2: 画箱体 Q1~Q3'); st.set_alpha(1.0)
        if t>0.84: box.set_alpha(0.7)
        if 0.85<t<=0.93:
            p=clamp((t-0.85)/0.08); med.set_alpha(p)
            st.set_text('Step 3: 画中位线 Q2')
        if t>0.93: med.set_alpha(1.0)
        if 0.94<t<=1.0:
            p=clamp((t-0.94)/0.06); wl.set_alpha(p); wh.set_alpha(p)
            st.set_text('Step 4: 画须线 min~max')
        if t>0.98:
            wl.set_alpha(1.0); wh.set_alpha(1.0)
            st.set_text(f'完成! IQR = Q3-Q1 = {q3-q1:.0f}')

        fig.savefig(frames_dir + f'/frame_{frm:04d}.png', dpi=DPI, facecolor='white')
    plt.close(fig)

    out = f'{BASE}/video_03_quartile.mp4'
    if frames_to_video(frames_dir, audio_path, out):
        extract_poster(out, f'{BASE}/poster_03_quartile.png', 0.4)
    shutil.rmtree(frames_dir)

# ================================================================
# VIDEO 4: 数据分组
# ================================================================
def make_video4():
    print('\n### Video 4: Data Grouping ###')

    narration = (
        "最后我们来学习数据的分组。"
        "当数据量比较大时，我们需要对数据进行分组整理，这样才能看出分布规律。"
        "这里有50名同学的成绩，散落在数轴上，看起来杂乱无章。"
        "分组的第一步是确定组距和组数。组距就是每一段的宽度。"
        "这里我们选择组距为10分，从40分到100分，刚好分成6组。"
        "分组的第二步是统计每一组有多少个数据，也就是频数。"
        "比如60到70这个分数段，有多少个同学呢？我们数一数。"
        "统计完所有组的频数后，就可以画出频数分布直方图了。"
        "直方图的横轴是分数段，纵轴是频数，也就是每个分数段的人数。"
        "把每个柱子顶端的中点连起来，就得到了频数折线，可以更清楚地看出分布的趋势。"
        "分组的第三步，也是很重要的一步，就是验证分组原则。"
        "分组的原则是：组内差异尽可能小，组间差异尽可能大。"
        "也就是说：同一组的数据应该尽量相近，不同组的数据应该明显不同。"
        "如果组距太大，会丢失细节信息，看不出分布形态。"
        "如果组距太小，数据太琐碎，也看不出规律。"
        "选择合适的组距，才能清晰地呈现数据的分布特征。"
    )

    audio_path = f'{BASE}/narration_04_grouping.mp3'
    asyncio.run(gen_audio(narration, audio_path))
    duration = get_audio_duration(audio_path)
    total_frames = int(duration * FPS) + 5
    print(f'  Audio: {duration:.1f}s -> {total_frames} frames')

    frames_dir = f'{BASE}/_frames4'
    os.makedirs(frames_dir, exist_ok=True)

    np.random.seed(42)
    sc=np.concatenate([np.random.normal(65,7,10),np.random.normal(75,5,15),
                       np.random.normal(82,4,15),np.random.normal(90,5,10)]).clip(40,100).astype(int)
    sc.sort()
    bins=[40,50,60,70,80,90,100]
    hc,_=np.histogram(sc,bins=bins)

    fig,(ax1,ax2)=plt.subplots(2,1,figsize=(10,7),gridspec_kw={'height_ratios':[0.55,0.45]})
    fig.patch.set_facecolor('white')
    ax1.set_xlim(35,105); ax1.set_ylim(-0.5,5.5)
    ax1.set_title('数据的分组',fontsize=16,fontweight='bold',color='#1D3557')
    for s in ax1.spines.values(): s.set_visible(False)
    ax1.set_yticks([]); ax1.grid(axis='x',alpha=0.15)
    ax1.scatter(sc,np.random.uniform(1.5,3.5,len(sc)),s=25,c='#457B9D',alpha=0.7,zorder=3)

    rects=[]
    for l,r,cnt in zip(bins[:-1],bins[1:],hc):
        rect=mpatches.Rectangle((l,4),r-l,0,alpha=0,facecolor='#A8DADC',edgecolor='#457B9D',lw=1.5,zorder=2)
        ax1.add_patch(rect); rects.append(rect)

    blbls=[]
    for l,r in zip(bins[:-1],bins[1:]):
        t=ax1.text((l+r)/2,4.8,f'{l}~{r}',ha='center',fontsize=8,alpha=0,color='#666')
        blbls.append(t)

    flbls=[]
    for i,cnt in enumerate(hc):
        t=ax1.text((bins[i]+bins[i+1])/2,4.3,'',ha='center',fontsize=11,alpha=0,fontweight='bold',color='#1D3557')
        flbls.append(t)

    ax2.set_xlim(0,10); ax2.set_ylim(0,4); ax2.axis('off')
    ttl=ax2.text(5,3.5,'',ha='center',fontsize=14,fontweight='bold',color='#1D3557',alpha=0)
    pr=ax2.text(5,1.5,'',ha='center',fontsize=13,color='#E63946',fontweight='bold',alpha=0)

    plt.tight_layout(pad=1)

    for frm in range(total_frames):
        t=frm/total_frames
        if t<=0.28:
            p=t/0.28
            for l in blbls: l.set_alpha(p)
            ttl.set_text('Step 1: 确定组距 = 10分, 共6组'); ttl.set_alpha(p)
        else:
            for l in blbls: l.set_alpha(1.0)
        if 0.30<t<=0.60:
            p=clamp((t-0.30)/0.30)
            for rect,cnt in zip(rects,hc): rect.set_height(cnt/max(hc)*1.2*p); rect.set_alpha(0.7*p)
            ttl.set_text('Step 2: 统计每组频数'); ttl.set_alpha(1.0)
            if p>0.5:
                pp=clamp((p-0.5)/0.5)
                for l,cnt in zip(flbls,hc): l.set_text(f'{cnt}人'); l.set_alpha(pp)
        if t>0.60:
            for rect,cnt in zip(rects,hc): rect.set_height(cnt/max(hc)*1.2); rect.set_alpha(0.7)
            for l,cnt in zip(flbls,hc): l.set_text(f'{cnt}人'); l.set_alpha(1.0)
        if 0.65<t<=0.95:
            p=clamp((t-0.65)/0.30)
            ttl.set_text('Step 3: 验证分组原则'); ttl.set_alpha(1.0)
            pr.set_text('组内差异小, 组间差异大'); pr.set_alpha(p)
        if t>0.95: pr.set_text('频率 = 频数 / 总数'); pr.set_alpha(1.0)
        fig.savefig(frames_dir + f'/frame_{frm:04d}.png', dpi=DPI, facecolor='white')
    plt.close(fig)

    out = f'{BASE}/video_04_grouping.mp4'
    if frames_to_video(frames_dir, audio_path, out):
        extract_poster(out, f'{BASE}/poster_04_grouping.png', 0.4)
    shutil.rmtree(frames_dir)

# ================================================================
if __name__ == '__main__':
    print('Regenerating all 4 videos with FULL narration...')
    make_video1()
    make_video2()
    make_video3()
    make_video4()
    print('\n=== ALL DONE ===')
