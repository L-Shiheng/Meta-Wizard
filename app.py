import streamlit as st

# ==============================================================================
# 页面全局配置
# ==============================================================================
st.set_page_config(
    page_title="代谢组学一站式辅助系统",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 侧边栏导航控制中心
# ==============================================================================
st.sidebar.image("https://img.icons8.com/external-flatart-icons-flat-flatart-icons/128/external-laboratory-science-flatart-icons-flat-flatart-icons-1.png", width=80)
st.sidebar.title("🔬 代谢组学中心")
st.sidebar.markdown("基于岛津质谱及高水平文献的一站式工作流")

# 顶层两大核心模块切换
main_module = st.sidebar.radio(
    "请选择核心研究策略：",
    ["非靶向代谢组学 (Untargeted)", "拟靶向代谢组学 (Quasi-targeted)"]
)

st.sidebar.divider()
st.sidebar.info("💡 提示：本系统聚焦于基于液相色谱-质谱 (LC-MS) 的分析技术路线，所有前处理方法均锚定领域内公认的高引文献。")

# ==============================================================================
# 核心模块一：非靶向代谢组学 (Untargeted Metabolomics)
# ==============================================================================
if main_module == "非靶向代谢组学 (Untargeted)":
    st.header("🎯 非靶向代谢组学一站式工作流")
    
    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
        "1️⃣ 样品前处理 SOP", 
        "2️⃣ 数据采集指南 (LC-MS)", 
        "3️⃣ 原始数据预处理 (Met4DX)", 
        "4️⃣ 化合物智能注释 (MetDNA)"
    ])
    
    # --------------------------------------------------------------------------
    # 子模块 1：样品前处理 SOP (已深度整合高水平文献)
    # --------------------------------------------------------------------------
    with sub_tab1:
        st.subheader("🧪 实验第一步：标准化样品前处理")
        
        col1, col2 = st.columns(2)
        with col1:
            matrix = st.selectbox("请选择生物基质类型：", ["血清/血浆 (Serum/Plasma)", "动物组织 (Tissue)", "细胞 (Cells)", "尿液 (Urine)"])
        with col2:
            if matrix == "尿液 (Urine)":
                omic_type = st.radio("请选择分析目标：", ["极性代谢物 (Polar Metabolites)"], horizontal=True)
            else:
                omic_type = st.radio("请选择分析目标：", ["极性代谢物 (Polar Metabolites)", "脂质组学 (Lipidomics)"], horizontal=True)
        
        st.markdown("---")
        
        # --- 血清/血浆前处理 ---
        if matrix == "血清/血浆 (Serum/Plasma)":
            if omic_type == "极性代谢物 (Polar Metabolites)":
                st.info("📚 **核心参考文献**: Want, E. J. et al. Global metabolic profiling procedures for instruments such as liquid chromatography–quadrupole time-of-flight mass spectrometry. *Nature Protocols*, 5(6), 1005-1018 (2010).")
                st.caption("💡 方法特性：领域公认的血清大规模代谢组学沉淀法，有机相/水相极性质控稳定。")
                
                step_a, step_b, step_c = st.tabs(["1. 有机相淬灭与沉淀", "2. 离心收集", "3. 复溶上机"])
                with step_a:
                    st.markdown("""
                    1. 将血清/血浆样品在冰上缓慢解冻。
                    2. 吸取 **50 μL** 血浆至 1.5 mL 离心管中。
                    3. 加入 **150 μL 冰冷的甲醇 (MeOH)**（体积比 1:3 沉淀），可在此步加入靶向同位素内标。
                    4. 剧烈涡旋 **15-30 秒**，置于 **-20 ℃** 冰箱中静置孵育 **20 分钟**，以确保蛋白大分子彻底沉淀。
                    """)
                with step_b:
                    st.markdown("""
                    1. 在 **4 ℃** 环境下，以 **12000-14000 g** 的离心力高转速离心 **15 分钟**。
                    2. 小心吸取尽可能多的上清液（通常约 **180 μL**）转移至全新的进样小瓶中。
                    3. *(可选干燥)* 使用真空离心浓缩仪将上清液挥干，干品可于 -80 ℃ 长期保存。
                    """)
                with step_c:
                    st.markdown("""
                    1. 若样品经过干燥，临上机前加入 **50 μL 乙腈/水 (50:50, v/v)** 溶液复溶。
                    2. 涡旋 **30 秒**，4 ℃ 超声 **10 分钟**，再次于 **12000 g** 离心 **10 分钟**。
                    3. 将上清液转移至带内衬管的色谱进样瓶中，置于自动进样器（设为 4 ℃）等待上机。
                    """)
                    
            elif omic_type == "脂质组学 (Lipidomics)":
                st.info("📚 **核心参考文献**: Matyash, V. et al. Lipid extraction by methyl-tert-butyl ether for high-throughput lipidomics. *Journal of Lipid Research*, 49(5), 1137-1146 (2008).")
                st.caption("💡 方法特性：替代传统 Folch 法的 MTBE 高通量法，脂质富集在最上层，极其方便自动化或手动移液，无氯仿毒性。")
                
                step_a, step_b, step_c = st.tabs(["1. 均相混合与相分离", "2. 离心与收集", "3. 浓缩干燥与复溶"])
                with step_a:
                    st.markdown("""
                    1. 吸取 **20-50 μL** 血清/血浆转移至玻璃管或抗腐蚀离心管中。
                    2. 加入 **225 μL 冰冷的甲醇 (MeOH)**，涡旋 10 秒（破乳并沉淀蛋白）。
                    3. 加入 **750 μL 甲基叔丁基醚 (MTBE)**，在室温下置于摇床振荡 **1 小时**。
                    4. 加入 **188 μL 质谱级纯水** 以诱导两相分离，涡旋 **20 秒** 并静置 **10 分钟**。
                    """)
                with step_b:
                    st.markdown("""
                    1. 在 **4 ℃**、**1000 g** 的条件下离心 **10 分钟**。
                    2. 此时液体分为两层：**上层有机相（含脂质）** 和下层水相及中间蛋白沉淀层。
                    3. 小心吸取上方约 **600 μL** 的 MTBE 脂质提取层，转移至新管。
                    """)
                with step_c:
                    st.markdown("""
                    1. 使用氮气吹扫仪（N2流）或真空离心浓缩仪，将提取出的有机相蒸发至完全干燥。
                    2. 加入 **100 μL 异丙醇/甲醇/水 (65:30:5, v/v/v)**（或其他适合您仪器的起始流动相）进行复溶。
                    3. 涡旋超声后进行 LC-MS 分析。
                    """)

        # --- 动物组织前处理 ---
        elif matrix == "动物组织 (Tissue)":
            if omic_type == "极性代谢物 (Polar Metabolites)":
                st.info("📚 **核心参考文献**: Dunn, W. B. et al. Procedures for large-scale metabolic profiling of serum and plasma using gas chromatography and liquid chromatography mass spectrometry. *Nature Protocols*, 6(7), 1060-1083 (2011).")
                st.caption("💡 方法特性：组织匀浆提取标准，结合甲醇快速失活内源性代谢酶。")
                
                step_a, step_b, step_c = st.tabs(["1. 物理匀浆与酶失活", "2. 超声提取与离心", "3. 浓缩与复溶"])
                with step_a:
                    st.markdown("""
                    1. 在液氮中快速取样并称重（通常取 **20-30 mg**）。
                    2. 按照 **1 mg 组织 : 15 μL 提取液** 的比例，加入预冷的 **甲醇/水 (80:20, v/v)** 混合溶剂（内置研磨珠）。
                    3. 使用低温高通量组织研磨仪（如 50 Hz，匀浆 2 分钟），确保组织完全破碎，同时冷甲醇迅速使代谢酶失活。
                    """)
                with step_b:
                    st.markdown("""
                    1. 匀浆后置于冰上静置 **10 分钟**。
                    2. 转移至 **4 ℃** 水浴超声仪中处理 **15 分钟**，进一步释放细胞内代谢物。
                    3. 在 **4 ℃** 环境下，以 **14000 g** 离心 **15 分钟**，彻底沉淀细胞碎片与不溶性蛋白。
                    """)
                with step_c:
                    st.markdown("""
                    1. 小心转移上清液至新管中，通过真空离心浓缩仪干燥。
                    2. 加入与初始组织重量相匹配体积的 **乙腈/水 (50:50, v/v)** 复溶。
                    3. 涡旋并再次离心以去除残留微粒，取上清液至色谱瓶上机。
                    """)
                    
            elif omic_type == "脂质组学 (Lipidomics)":
                st.info("📚 **核心参考文献**: Matyash, V. et al. *Journal of Lipid Research*, 49(5), 1137-1146 (2008).")
                st.caption("💡 方法特性：针对实体组织的 MTBE 萃取法，兼容 BCA 蛋白定量。")
                
                step_a, step_b, step_c = st.tabs(["1. 匀浆与蛋白定量预留", "2. MTBE 相分离", "3. 收集与上机预备"])
                with step_a:
                    st.markdown("""
                    1. 称取 **10-20 mg** 组织样本，加入 **200 μL 纯水** 和研磨珠。
                    2. 低温匀浆机破碎至均一状态。
                    3. *(关键点)* 从匀浆液中吸取 **10 μL** 用于后续 BCA 蛋白质浓度测定，以此作为数据归一化的依据。
                    """)
                with step_b:
                    st.markdown("""
                    1. 向剩余的匀浆液中依次加入 **1.5 mL 甲醇** 和 **5 mL MTBE**（可按组织量等比例缩减溶剂）。
                    2. 室温下剧烈振荡或摇床孵育 **1 小时**。
                    3. 按比例加入纯水（如原液量按缩减比例加入对应体积水）诱导相分离，静置 **10 分钟**。
                    """)
                with step_c:
                    st.markdown("""
                    1. **1000 g** 离心 **10 分钟**。
                    2. 收集上层有机相（MTBE层），将其转移并使用氮气吹干。
                    3. 用适用于您流动相体系的溶剂（如 二氯甲烷/甲醇 或 异丙醇体系）复溶并上机。
                    """)

        # --- 细胞前处理 ---
        elif matrix == "细胞 (Cells)":
            st.info("📚 **核心参考文献 (Rabinowitz Lab Protocol)**: Lu, W. et al. Metabolite Measurement: Pitfalls to Avoid and Practices to Follow. *Annual Review of Biochemistry*, 86, 277-304 (2017).")
            st.caption("💡 方法特性：普林斯顿大学经典的 40:40:20 (甲醇:乙腈:水) 冷淬灭法，极大限度抑制代谢物降解，适合贴壁及悬浮细胞。")
            
            cell_method = st.selectbox("请指定细胞培养类型：", ["极性代谢物 - 贴壁细胞", "极性代谢物 - 悬浮细胞", "脂质组学细胞提取"])
            
            if "极性代谢物" in cell_method:
                st.warning("⚠️ 试剂准备：预先配制 **甲醇/乙腈/水 (40:40:20, v/v/v)** 混合液，加入 0.5% 甲酸，并在使用前于 -20 ℃ 至少预冷 1 小时。")
                step_a, step_b, step_c = st.tabs(["1. 快速淬灭代谢", "2. 细胞内容物刮取/提取", "3. 离心与保存"])
                with step_a:
                    if "悬浮细胞" in cell_method:
                        st.markdown("""
                        1. 悬浮细胞培养物转移至离心管，**4 ℃，500 g** 快速离心 2 分钟。
                        2. 彻底吸干上清液（非常关键），用极少量 4 ℃ PBS 快速漂洗一次，再次离心弃上清。
                        3. 立即加入预冷的 **-20 ℃ 提取液（40:40:20）** 重悬细胞沉淀。
                        """)
                    else:
                        st.markdown("""
                        1. 移走培养基，使用 37 ℃ 温 PBS 极速冲洗贴壁细胞一次（整个过程应 < 5秒），立即将培养皿平放于**干冰**上。
                        2. 迅速向培养皿中加入预冷的 **-20 ℃ 提取液（40:40:20）**（例如 6孔板每孔加 1 mL）。
                        3. 置于 -20 ℃ 孵育 **15-20 分钟**。
                        """)
                with step_b:
                    st.markdown("""
                    1. 对于贴壁细胞：使用细胞刮刀将皿底所有细胞及其提取液彻底刮下，转移至 1.5 mL EP 管中。
                    2. 将装有细胞悬液的 EP 管在振荡器上高频涡旋 **30 秒**，或在冰水浴中短时间超声，确保细胞膜彻底破裂。
                    """)
                with step_c:
                    st.markdown("""
                    1. 在 **4 ℃** 环境下，**16000 g** 高速离心 **10 分钟**。
                    2. 小心吸取上清液（此即为非靶向极性代谢物提取物）。
                    3. 可选择直接上机，或使用真空浓缩仪干燥后冻存于 -80 ℃。
                    *(注：沉淀物可通过强裂解液溶解后进行 BCA 蛋白定量归一化)*
                    """)
            else:
                st.markdown("""
                **脂质组学细胞提取 (基于 MTBE 改良法)**
                1. 细胞沉淀收集后，加入 **200 μL 纯水** 或 PBS 重悬。
                2. 进行 3 次 **液氮冻融-冰水浴超声** 循环彻底破壁。取 10 μL 进行 BCA 定量。
                3. 向剩余液体中加入 **1.5 mL 甲醇** 和 **5 mL MTBE**（根据体积等比例调整）。
                4. 后续操作与组织/血清 MTBE 脂质分离法一致。
                """)

        # --- 尿液前处理 ---
        elif matrix == "尿液 (Urine)":
            st.info("📚 **核心参考文献**: Gika, H. G. et al. Global metabolic profiling procedures for instruments such as liquid chromatography–quadrupole time-of-flight mass spectrometry. *Nature Protocols*, 5(6), 1005-1018 (2010).")
            st.caption("💡 方法特性：由于尿液本身基质较清澈，通常采用温和的稀释法（Dilute-and-Shoot）或离心沉淀法，防止过度处理导致损失。")
            st.markdown("""
            **规范实验步骤：**
            1. 样本解冻：将尿液样本置于冰上缓慢解冻，解冻后涡旋混匀 **30 秒** 以重悬可能析出的微粒。
            2. 去除杂质：在 **4 ℃** 下以 **14000 g** 的转速离心 **15 分钟**，去除尿液中的细胞碎片、细菌及沉淀盐类。
            3. **直接稀释法 (Dilute-and-Shoot)**：
               * 小心吸取 **50 μL** 尿液上清。
               * 加入 **150 μL 质谱级纯水** (含内标) 进行 1:4 稀释（若使用 HILIC 色谱柱，则应使用乙腈/水体系稀释以匹配强洗脱起步强度）。
            4. 再次在 4 ℃ 下以 **14000 g** 离心 **10 分钟**。
            5. 吸取上清液至进样瓶上机检测。
            
            *(⚠️ **归一化提示**：由于饮水量差异，不同个体的尿液浓度差异极大，测试前或分析数据时，必须进行肌酐测定或渗透压校正。)*
            """)

    # --------------------------------------------------------------------------
    # 子模块 2：数据采集指南 (LC-MS)
    # --------------------------------------------------------------------------
    with sub_tab2:
        st.subheader("📊 仪器配置：岛津 LC-MS 数据采集参数")
        
        mode = st.radio("请选择液相色谱分离模式：", ["HILIC 模式 (亲水相互作用色谱)", "反相色谱模式 (RPLC)"], horizontal=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🧪 液相流动相配制标准")
            if "HILIC" in mode:
                st.code("""
色谱柱: Waters BEH Amide
流动相 A: 水 + 25 mM 乙酸铵 + 25 mM 氨水
流动相 B: 100% 乙腈
                """, language="text")
            else:
                st.code("""
色谱柱: Phenomenex Kinetex C18
流动相 A: 水 + 0.1% 甲酸
流动相 B: 100% 乙腈 + 0.1% 甲酸
                """, language="text")
        
        with col2:
            st.markdown("### ⚡ 质谱扫描参数 (DDA 模式)")
            st.markdown("""
            *   **扫描模式**：MS1 SCAN (m/z 60 ~ 1200) + MS2 DDA (m/z 25 ~ 1200)
            *   **源参数设置**：接口温度 300 ℃ / DL 温度 250 ℃ / 加热块 400 ℃
            *   **气体流量**：雾化气 3.0 L/min / 加热气 10 L/min / 干燥气 10 L/min
            """)
            
        st.markdown("### ⏱️ 保留时间质控 (RTQC) 与日常进样批处理序列")
        st.markdown("""
        标准的日批处理序列排布推荐如下：
        Blank -> QC -> RTQC -> Sample_001 -> Sample_002 -> ... -> QC
        """)

    # --------------------------------------------------------------------------
    # 子模块 3：原始数据预处理 (Met4DX)
    # --------------------------------------------------------------------------
    with sub_tab3:
        st.subheader("💻 数据处理：LabSolutions 转换与 Met4DX 提取")
        st.markdown("""
        **1. 格式转换：** 在岛津 LabSolutions 软件中完成采集后，将原始数据（.lcd）导出并转换为国际标准 **.mzML** 格式。
        
        **2. Met4DX 工程配置：**
        * 新建项目（New Project），指定色谱柱类型与高分辨质谱类型。
        * 将 mzML 文件按 `Sample`、`QC`、`Blank` 归类。
        * 下发峰提取（Peak Picking）与对齐（Alignment）工作流任务。
        
        **3. 关键文件导出：**
        * `sample.info.csv` —— 分组及属性映射信息表
        * `data.csv` —— **MS1 峰表** (m/z, RT, 峰面积)
        * `spectra.msp` —— **MS/MS 谱图文件**
        """)

    # --------------------------------------------------------------------------
    # 子模块 4：化合物智能注释 (MetDNA)
    # --------------------------------------------------------------------------
    with sub_tab4:
        st.subheader("🌐 云端分析：MetDNA 代谢物自动化注释")
        st.markdown("""
        对接朱正江课题组 MetDNA 平台（zhulab.cn）：
        1.  登录新建非靶向任务。
        2.  上传 Met4DX 导出的三个核心文件。
        3.  配置质量容差（MS1: 15 ppm, MS2: 20 ppm）及加合离子库。
        4.  提交运行，在线查看或下载化合物鉴定报告。
        """)

# ==============================================================================
# 核心模块二：拟靶向代谢组学 (Quasi-targeted Metabolomics)
# ==============================================================================
elif main_module == "拟靶向代谢组学 (Quasi-targeted)":
    st.header("🎯 拟靶向代谢组学高通量定量工作流")
    st.warning("📊 拟靶向模块目前处于高标准架构规划中。其底层设计将直接继承上方【非靶向模块】鉴定出的化合物保留时间库与离子对。")
    
    q_tab1, q_tab2, q_tab3 = st.tabs(["1️⃣ 拟靶向方法建立", "2️⃣ 靶向 MRM 数据采集", "3️⃣ 定量数据处理"])
    
    with q_tab1:
        st.markdown("### 🛠️ 离子对 (Transitions) 自动下发生成")
        st.markdown("功能占位区...")
    with q_tab2:
        st.markdown("### ⚡ 三重四极杆/Q-TOF 仪器方法配置")
        st.markdown("功能占位区...")
    with q_tab3:
        st.markdown("### 📈 峰积分、归一化与多变量统计")
        st.markdown("功能占位区...")

# ==============================================================================
# 底部全局增强：大模型实时实验答疑助手
# ==============================================================================
st.divider()
st.subheader("🤖 实验遇阻？代谢组学 AI 助手实时答疑")
st.caption("实操过程中遇到异常，可在此发起询问。")

user_question = st.chat_input("✍️ 输入遇到的技术问题...")
if user_question:
    with st.chat_message("user"):
        st.write(user_question)
    with st.chat_message("assistant"):
        st.markdown("💡 此处预留了大模型核心的安全交互接口，待后续打通。")
