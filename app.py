import streamlit as st
import pandas as pd

# 1. 页面基本配置
st.set_page_config(
    page_title="岛津代谢组学一站式交互向导系统",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 初始化全局状态（用于在不同步骤间传递数据）
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "project_name" not in st.session_state:
    st.session_state.project_name = ""
if "raw_files" not in st.session_state:
    st.session_state.raw_files = []
if "selected_ion_pairs" not in st.session_state:
    st.session_state.selected_ion_pairs = None

# 3. 导航控制函数
def next_step():
    st.session_state.current_step += 1

def prev_step():
    st.session_state.current_step -= 1

def go_to_step(step_num):
    st.session_state.current_step = step_num

# 4. 侧边栏：流程进度指示器
with st.sidebar:
    st.title("🔬 工作流导航")
    st.markdown("请按照以下步骤完成分析：")
    
    steps = [
        "1. 项目初始化 & 数据采集",
        "2. 格式转换 (MSConvert/LabSolutions)",
        "3. 非靶向注释 (Met4DX & MetDNA)",
        "4. 拟靶向离子对挑选 (IonFinder)",
        "5. RT校正 & MRM方法生成"
    ]
    
    for idx, step_name in enumerate(steps, 1):
        # 突出显示当前正在进行的步骤
        if st.session_state.current_step == idx:
            st.markdown(f"**👉 {step_name}**")
        else:
            if st.button(f"{idx}. {step_name.split('. ')[1]}", key=f"nav_btn_{idx}"):
                go_to_step(idx)
                st.rerun()
                
    st.divider()
    st.info("💡 提示：系统会自动检查路径中是否包含中文，避免后续 R 脚本报错。")

# 5. 主界面内容区域
st.title("岛津拟靶向/非靶向代谢组学一站式向导")
st.caption("基于 Streamlit 构建的跨平台实验与数据分析闭环指导系统")
st.divider()

# --- 步骤 1：项目初始化 ---
if st.session_state.current_step == 1:
    st.header("Step 1: 项目初始化 & QTOF 数据采集")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.project_name = st.text_input("请输入项目名称 / 批次号：", st.session_state.project_name)
        mode = st.radio("请选择分析模式：", ["非靶向组学 (Untargeted)", "拟靶向组学 (Pseudo-targeted)"])
    with col2:
        polarity = st.multiselect("选择电离模式（可多选）：", ["Positive", "Negative"], default=["Positive"])
    
    st.subheader("📋 QTOF 数据采集 SOP 确认")
    st.warning("⚠️ 实验提醒：前处理过程请务必确保全程冰上操作！")
    
    # 这里可以展示仪器参数推荐配置
    with st.expander("查看 9030/9050 QTOF 推荐液相梯度与质谱参数"):
        st.text("流速: 0.3 mL/min | 柱温: 40 ℃\nMS1 扫描范围: 70-1000 m/z\nMS2 DDA 碰撞能: CE 25±15 V")
    
    st.divider()
    if st.button("完成采集，进入下一步 ➡️", on_click=next_step):
        st.rerun()

# --- 步骤 2：格式转换 ---
elif st.session_state.current_step == 2:
    st.header("Step 2: 数据格式转换")
    st.markdown("将岛津原生的 `.lcd` 数据转换为后续生信软件通用的格式。")
    
    st.subheader("1. 非靶向/拟靶向通路：转换成 .mzML")
    st.info("操作指导：打开 LabSolutions 软件，选择[文件]—[导出]，选择 mzML 格式。")
    
    st.subheader("2. 拟靶向通路：提取二级数据转换成 .mgf")
    st.markdown("可以通过下方组件，由系统在后台调用 `MSConvert` 命令行自动转换：")
    
    output_dir = st.text_input("输入本地数据存放的绝对路径（避免中文）：", "D:/Metabolomics_Data/")
    
    # 路径防错检查
    if any(order in output_dir for order in ["稿", "文", "新", "中"]): # 简单示例，后续用正则精准匹配中文
         st.error("❌ 检测到路径中包含中文字符！MRM ionfinder 无法在中文路径下运行，请修改为全英文路径。")
         
    st.divider()
    col_nav1, col_nav2 = st.columns([1, 5])
    with col_nav1:
        st.button("⬅️ 上一步", on_click=prev_step)
    with col_nav2:
        st.button("进入下一步 ➡️", on_click=next_step)

# --- 步骤 3：非靶向注释 ---
elif st.session_state.current_step == 3:
    st.header("Step 3: 非靶向注释 (Met4DX & MetDNA)")
    st.markdown("在这里完成特征峰提取与基于大科学代谢物网络的化合物注释。")
    
    st.markdown("##### 1. 打开 Met4DX 处理 mzML 文件，导出 MS1 峰表（Peak Table）。")
    st.markdown("##### 2. 登录 MetDNA 平台上传数据：")
    st.info("需要准备三个文件：Sample Info (sample.info.csv)、MS1 Peak Table (data.csv)、MS/MS Data (spectra.msp)")
    
    st.subheader("📥 结果回验：上传 MetDNA 导出的鉴定表")
    uploaded_metdna = st.file_uploader("将 MetDNA 导出的 identification.csv 拖拽至此处，系统将自动帮您筛选高置信度代谢物", type=["csv"])
    
    if uploaded_metdna:
        df = pd.read_csv(uploaded_metdna)
        st.success("文件解析成功！")
        st.dataframe(df.head()) # 展示前几行
        
    st.divider()
    col_nav1, col_nav2 = st.columns([1, 5])
    with col_nav1:
        st.button("⬅️ 上一步", on_click=prev_step)
    with col_nav2:
        st.button("进入下一步 ➡️", on_click=next_step)

# --- 步骤 4：拟靶向离子对挑选 ---
elif st.session_state.current_step == 4:
    st.header("Step 4: 拟靶向离子对挑选 (MRM ionfinder)")
    st.markdown("利用 MS1 峰表和封装好的 MS2（.mgf）数据，挑选最强的特征碎片离子对。")
    
    st.subheader("⚙️ 运行参数配置")
    ion_mode = st.selectbox("选择分析的离子模式：", ["正离子 (POS)", "负离子 (NEG)"])
    rt_tolerance = st.slider("保留时间匹配窗口 (RT Tolerance / min):", 0.1, 1.0, 0.5, step=0.05)
    
    if st.button("⚡ 启动 MRM ionfinder 算法进行挑选"):
        with st.spinner("后台正在运行 R 脚本挑选最佳子离子，请稍候..."):
            # 后续在这里放入后台调用的 Python 代码
            st.success("🎉 离子对挑选完成！已自动剔除基线噪音及假阳性信号。")
            
    st.divider()
    col_nav1, col_nav2 = st.columns([1, 5])
    with col_nav1:
        st.button("⬅️ 上一步", on_click=prev_step)
    with col_nav2:
        st.button("进入下一步 ➡️", on_click=next_step)

# --- 步骤 5：RT 校正与方法文件生成 ---
elif st.session_state.current_step == 5:
    st.header("Step 5: 保留时间校正 & LabSolutions 方法生成")
    st.markdown("基于标准品（RTQC）校正保留时间飘移，并一键生成最终的 MRM 方法。")
    
    st.subheader("1. 输入当前批次内标（RTQC）的实际出峰时间")
    
    # 动态创建一个表格让用户填入实际 RT
    rt_data = {
        "标准品名称": ["L-Norleucine", "Kynurenic acid", "Flavone"],
        "文献参考 RT (min)": [1.07, 4.44, 6.80],
        "本批次实际 RT (min)": [1.07, 4.44, 6.80] # 允许用户在界面上修改
    }
    df_rt = pd.DataFrame(rt_data)
    edited_df = st.data_editor(df_rt, num_rows="fixed")
    
    st.subheader("2. 一键导出岛津化合物表")
    if st.button("生成最终方法化合物表 (.txt)"):
        # 后续在这里放入根据修正后的 RT 更新方法模板文件的逻辑
        st.success("生成成功！该文本文件可直接在 LabSolutions 软件的 [MRM方法数据表] 中通过右键[导入]一键加载。")
        st.download_button("💾 下载化合物表方法文件", data="化合物表文本内容占位符", file_name="Shimadzu_MRM_Method.txt")

    st.divider()
    if st.button("⬅️ 返回首步", on_click=go_to_step, args=(1,)):
        st.rerun()
