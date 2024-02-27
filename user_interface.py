# user_interface.py
import streamlit as st
from calculator import calculate_basic_damage
from calculator import my_gained_attribute_calculate
from calculator import skill_gains_calculate
import yaml
from tkinter import filedialog
from functools import partial
import json
import random
import pandas as pd
import numpy as np
import plotly.express as px
import copy
import time
from datetime import datetime

# 主输出选项
output_options = ["逐霜", "鬼王", "太昊", "惊岚", "涅羽"]

# 技能选项
skill_options = {
        "逐霜": {"values": ["苍龙玄", "苍龙煞", "银鳞玄冰"]},
        "鬼王": {"values": ["未名神通", "九变"]},
        "太昊": {"values": ["天地绝神通"]},
        "惊岚": {"values": ["森罗削空斩·赤乌"]},
        "涅羽": {"values": ["大业浮屠·赤乌"]},
    }
# 职业选项
profession_options = ["天音", "天华", "画影", "焚香", "青罗", "青云", "昭冥"]

# 可变增益选项
var_gain_options = ["九华奠魂曲", "副本赠送爆伤", "墨雪特效霜情", "三碗不过岗", "情愫项链技能佳期", "法宝融合爆伤", "进阶家族技能等级(爆伤)", "经典家族技能等级"]

# 默认可变增益选项
default_var_gain_options = ["九华奠魂曲", "副本赠送爆伤", "三碗不过岗", "进阶家族技能等级(爆伤)", "经典家族技能等级"]

# 星宿品质选项
xingxiu_options = ["荧炬", "皓月", "曦日"]

# 前世职业选项
qianshi_options = ["太昊", "烈山", "其他"]

# 副本爆伤选项
fuben_options = ["无赠送", "T16以上", "空桑兽神", "四象七"]

# 项链技能等级选项
ring_level_options = ["1级", "2级", "3级", "4级"]

# 家族技能等级选项
jiazu_level_options = ["1阶", "2阶", "3阶", "4阶", "5阶", "6阶", "7阶", "8阶", "9阶", "10阶", "11阶", "12阶", "13阶", "14阶", "15阶"]

# 技能输出字典
skills_detail_options = {
        "附加本体攻击百分比": {"step": 1, "default": 100, "min": 0, "max": 500, "values": {"苍龙玄": 240, "苍龙煞": 240, "银鳞玄冰": 290, "未名神通": 168, "九变": 130, "大业浮屠·赤乌": 340, "森罗削空斩·赤乌": 400, "天地绝神通": 100}},
        "附加防御上限百分比": {"step": 10, "default": 100, "min": 0, "max": 500, "values": {"苍龙玄": 0, "苍龙煞": 0, "银鳞玄冰": 0, "未名神通": 400, "九变": 0, "大业浮屠·赤乌": 0, "森罗削空斩·赤乌": 0, "天地绝神通": 0}},
        "附加气血上限百分比": {"step": 5, "default": 100, "min": 0, "max": 500, "values": {"苍龙玄": 0, "苍龙煞": 48, "银鳞玄冰": 40, "未名神通": 0, "九变": 20, "大业浮屠·赤乌": 80, "森罗削空斩·赤乌": 12, "天地绝神通": 100}},
        "附加真气上限百分比": {"step": 5, "default": 100, "min": 0, "max": 500, "values": {"苍龙玄": 48, "苍龙煞": 0, "银鳞玄冰": 40, "未名神通": 15, "九变": 20, "大业浮屠·赤乌": 40, "森罗削空斩·赤乌": 12, "天地绝神通": 100}},
        "附加爆伤": {"step": 5, "default": 100, "min": 0, "max": 500, "values": {"苍龙玄": 100, "苍龙煞": 100, "银鳞玄冰": 100, "未名神通": 100, "九变": 0, "大业浮屠·赤乌": 50, "森罗削空斩·赤乌": 100, "天地绝神通": 100}},
        "附加固定攻击值": {"step": 10, "default": 300, "min": 0, "max": 10000, "values": {"苍龙玄": 4000, "苍龙煞": 4000, "银鳞玄冰": 6000, "未名神通": 2720, "九变": 0, "大业浮屠·赤乌": 5000, "森罗削空斩·赤乌": 4800, "天地绝神通": 100}},
    }

# 第二页显示主输出的键
keys_to_display = [
    "主输出_气血",
    "主输出_真气",
    "主输出_最小攻击",
    "主输出_最大攻击",
    "主输出_防御",
    "主输出_爆伤",
    "主输出_对怪增伤",
    "主输出_减爆伤",
]

# 技能段数
skills_period_option = {"苍龙玄": 9,"苍龙煞": 9,"银鳞玄冰": 6,"未名神通": 6,"九变": 9,"天地绝神通": 5,"森罗削空斩·赤乌": 15,"大业浮屠·赤乌": 8}

def render_attributes_page():
    st.image('zhuxian.jpeg')
    st.markdown("<h1 style='font-size: 36px; color: #333333; font-weight: bold; '>Step2: 属性确认</h1>", unsafe_allow_html=True) #text-align: center;
    #st.header("Step2: 属性确认")

    st.subheader("已选择职业项")

    col1, col2 = st.columns(2)
    with col1:
    # 显示职业
        st.markdown("**主输出职业:**")
        output = st.session_state.my_attributes["主输出_职业"]
        st.text(f"{output_options[output]}")

    with col2:
        #显示队友，需要和之前选择的selected_roles匹配
        st.markdown("**队友职业:**")
        #st.text(f"{st.session_state.selected_roles}")
        formatted_roles = " ".join([f"{role}" for role in st.session_state.selected_roles])
        st.text(f"{formatted_roles}")

    # 显示所有技能增益
    st.subheader("技能增益项")
    # 删除roles_para中不在selected_roles里的职业，形成一个新的变量传递给skill_gains_calculate函数
    roles_para_copy = copy.deepcopy(st.session_state.roles_para)
    roles_para_filtered = {role: values for role, values in roles_para_copy.items() if role in st.session_state.selected_roles}
    skill_gains_para = skill_gains_calculate(st.session_state.my_attributes, roles_para_filtered)
    with st.expander(f"**展开以显示各职业技能增益数值**"):    
        st.json(skill_gains_para)

    # 显示主输出满增益属性
    # st.markdown("**主输出御宝状态属性:**")
    # st.json(st.session_state.my_attributes)
    st.subheader("主输出满增益属性")
    my_gain_attributes = my_gained_attribute_calculate(st.session_state.my_attributes, skill_gains_para, st.session_state.var_gains_para)
    #st.json(my_gain_attributes)

    # 从原始数据中提取要显示的部分
    filtered_data = {key: my_gain_attributes[key] for key in keys_to_display}

    # 将结果转换为 JSON 格式并打印
    filtered_json = json.dumps(filtered_data, indent=4)
    st.json(filtered_json)
   
    # 显示技能伤害
    # st.subheader("技能附加伤害")
    # st.json(st.session_state.skill_para)

    # 显示可变增益项
    # st.subheader("可变增益项")
    # st.json(st.session_state.var_gains_para)

    # 显示boss属性
    # st.subheader("BOSS属性")
    # st.json(st.session_state.boss_attributes)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"**确认完成**", key="attributes_to_caculation", type="primary"):
            st.session_state["current_page"] = "伤害计算"
            st.rerun()
    with col2:
        if st.button(f"**返回首页**", key="attributes_to_setting"):
            st.session_state["current_page"] = "参数设置"
            st.rerun()     

    st.session_state.my_gain_attributes = my_gain_attributes
    st.session_state.skill_gains_para = skill_gains_para            
    return

def render_damage_calculation_page():
    st.image('zhuxian.jpeg')
    st.markdown("<h1 style='font-size: 36px; color: #333333; font-weight: bold; '>Step3: 伤害计算</h1>", unsafe_allow_html=True) #text-align: center;
    #st.header("Step3: 伤害计算")

    # 添加伤害计算的内容
    basic_damage, skill_bs = calculate_basic_damage(st.session_state.my_gain_attributes, st.session_state.boss_attributes, st.session_state.roles_para, st.session_state.skill_para, st.session_state.var_gains_para)

    #st.subheader("基础伤害")
    #st.json(basic_damage)

    #st.subheader("伤害系数")
    damage_coeff = {}

    #st.markdown("**总爆伤系数**")
    bs = st.session_state.my_gain_attributes.get("主输出_爆伤", 0) + st.session_state.boss_attributes["BOSS_厄运诅咒(绿点)"] + skill_bs - st.session_state.boss_attributes["BOSS_减爆伤"]
    damage_coeff["总爆伤系数"] = round(bs / 100, 6)

    #st.markdown("**混乱诅咒系数**")
    damage_coeff["混乱诅咒系数"] = 1 + round(st.session_state.boss_attributes["BOSS_混乱诅咒"] / 100, 6)

    #st.markdown("**技能伤害增加系数**")
    zhuanzhu = st.session_state.skill_gains_para.get("技能增益_专注_慈航法愿", 0) + \
               st.session_state.skill_gains_para.get("技能增益_专注_秋声雅韵", 0) + \
               st.session_state.skill_gains_para.get("技能增益_专注_金蛇狂舞", 0) + \
               st.session_state.skill_gains_para.get("技能增益_专注_凌寒拂霜", 0) + \
               st.session_state.skill_gains_para.get("技能增益_专注_祝融真典2", 0) + \
               st.session_state.skill_gains_para.get("技能增益_专注_日月弘光", 0) + \
               st.session_state.skill_gains_para.get("技能增益_专注_清啸", 0) + \
               st.session_state.skill_gains_para.get("技能增益_专注_枕戈待旦", 0) + \
               st.session_state.skill_gains_para.get("技能增益_专注_乘时", 0) + \
               st.session_state.var_gains_para.get("三碗不过岗", 0)
    
    damage_coeff["技能伤害增加系数"] = 1 + round(zhuanzhu / 100, 6)

    #st.markdown("**所有伤害增加系数**")
    wuzhou = st.session_state.skill_gains_para.get("技能增益_巫咒_日月弘光", 0)
    damage_coeff["所有伤害增加系数"] = 1 + round(wuzhou / 100, 6)

    #st.markdown("**面板对怪增伤系数**")
    duiguai = st.session_state.skill_gains_para.get("技能增益_对怪_附骨生灵2", 0) + st.session_state.my_gain_attributes.get("主输出_对怪增伤", 0)
    damage_coeff["面板对怪增伤系数"] = 1 + round(duiguai / 100, 6)

    #st.markdown("**累积增伤系数**")
    total_damage_coeff = 1
    # 循环遍历 damage_coeff 字典的所有值，并累加到 total_damage_coeff
    for coeff_name, coeff_value in damage_coeff.items():
        if coeff_name != "总爆伤系数":
            total_damage_coeff = total_damage_coeff * coeff_value
    damage_coeff["累积增伤系数"] = round(total_damage_coeff, 6)
    #st.json(damage_coeff)

    # 需要根据不同的技能来呈现不同段数的伤害
    skill = st.session_state.skill_para["技能名称"]
    period = skills_period_option[skill]

    #计算实际伤害
    st.subheader(f"{skill}实际伤害")
    real_damage = {}
    real_damage["出爆最小伤害"] = int(damage_coeff.get("累积增伤系数", 0) * damage_coeff.get("总爆伤系数", 0) * basic_damage.get("最小基础伤害", 0))
    real_damage["出爆最大伤害"] = int(damage_coeff.get("累积增伤系数", 0) * damage_coeff.get("总爆伤系数", 0) * basic_damage.get("最大基础伤害", 0))

    #st.markdown("**精确到万位：**")
    real_damage_wan = {}
    real_damage_wan["出爆最小伤害"] = "{:.4f}万".format(real_damage["出爆最小伤害"] / 10000)
    real_damage_wan["出爆最大伤害"] = "{:.4f}万".format(real_damage["出爆最大伤害"] / 10000)
    #st.json(real_damage_wan)

    #st.markdown("**精确到亿位：**")
    real_damage_yi = {}
    real_damage_yi["出爆最小伤害"] = "{:.4f}亿".format(real_damage["出爆最小伤害"] / 1e8)
    real_damage_yi["出爆最大伤害"] = "{:.4f}亿".format(real_damage["出爆最大伤害"] / 1e8)
    #st.json(real_damage_yi)
    
    #选择显示内容
    if real_damage["出爆最小伤害"] > 1e8:  # 超过1亿使用 real_damage_yi
        # 与上次伤害相比
        delta = "{:.4f}亿".format(convert_to_number(real_damage_yi["出爆最大伤害"]) - st.session_state.damage_yi)
        st.session_state.damage_yi = convert_to_number(real_damage_yi["出爆最大伤害"])
        curr_value = real_damage_yi["出爆最大伤害"]
        col1, col2 = st.columns(2)
        with col1:
            st.json(real_damage_yi)

        with col2:
            st.metric(label="**相比上次伤害变化：**", value=f"{curr_value}", delta=f"{delta}",delta_color="inverse")

    elif real_damage["出爆最小伤害"] > 1e4:  # 超过1万使用 real_damage_wan
        st.json(real_damage_wan)
        # 与上次伤害相比
        delta = "{:.4f}万".format(convert_to_number(real_damage_wan["出爆最大伤害"]) - st.session_state.damage_wan)
        st.session_state.damage_wan = convert_to_number(real_damage_wan["出爆最大伤害"])
        curr_value = real_damage_wan["出爆最大伤害"]
        st.metric(label="**相比上次伤害：**", value=f"{curr_value}", delta=f"{delta}",delta_color="inverse")

    if skill in ["九变"]:
        increasing_min_damage = []
        increasing_max_damage = []

        # 逐段判断是否超过最大伤害，如果超过则设置为最大值
        for i in range(0, 9):
            damage_min_i = real_damage["出爆最小伤害"] * (1 + 0.3) ** i
            increasing_min_damage.append(min(damage_min_i, 21.04e8))   

            damage_max_i = real_damage["出爆最大伤害"] * (1 + 0.3) ** i
            increasing_max_damage.append(min(damage_max_i, 21.04e8))            
        
        # 使用函数转换为亿
        increasing_min_damage_in_yi = convert_to_units(increasing_min_damage, '亿')
        increasing_max_damage_in_yi = convert_to_units(increasing_max_damage, '亿')

        # 使用函数转换为万
        increasing_min_damage_in_wan = convert_to_units(increasing_min_damage, '万')
        increasing_max_damage_in_wan = convert_to_units(increasing_max_damage, '万')

        # 判断使用哪个数据来画图
        if increasing_min_damage[0] > 1e8:  # 超过1亿使用 yi
            data = pd.DataFrame({
                '段数': np.arange(1, period + 1),
                '实际伤害': [np.random.uniform(min_damage, max_damage + 0.000001) for min_damage, max_damage in zip(increasing_min_damage_in_yi, increasing_max_damage_in_yi)]
            })
            unit_label = '（亿）'
        elif increasing_min_damage[0] > 1e4:  # 超过1万使用 wan
            data = pd.DataFrame({
                '段数': np.arange(1, period + 1),
                '实际伤害': [np.random.uniform(min_damage, max_damage + 0.000001) for min_damage, max_damage in zip(increasing_min_damage_in_wan, increasing_max_damage_in_wan)]
            })
            unit_label = '（万）'

    elif skill in ["苍龙玄", "苍龙煞", "银鳞玄冰", "未名神通", "天地绝神通", "森罗削空斩·赤乌", "大业浮屠·赤乌"]:
        # 判断使用哪个数据来画图
        if real_damage["出爆最小伤害"] > 1e8:  # 超过1亿使用 real_damage_yi
            data = pd.DataFrame({
                '段数': np.arange(1, period + 1),
                '实际伤害': np.random.uniform(convert_to_number(real_damage_yi["出爆最小伤害"]), convert_to_number(real_damage_yi["出爆最大伤害"]) + 0.000001, size=period)
            })
            unit_label = '（亿）'
        elif real_damage["出爆最小伤害"] > 1e4:  # 超过1万使用 real_damage_wan
            data = pd.DataFrame({
                '段数': np.arange(1, period + 1),
                '实际伤害': np.random.uniform(convert_to_number(real_damage_wan["出爆最小伤害"]), convert_to_number(real_damage_wan["出爆最大伤害"]) + 0.000001, size=period)
            })
            unit_label = '（万）'

    col1, col2 = st.columns(2)
    with col1:
        moni_button = st.button(f"**模拟完整技能伤害**", key="moni", type="primary")
        # st.text_area('输出', st.session_state.text_output, key='output')
        # for i in range(10):  # 示例循环，每秒更新一次
        #     time.sleep(1)  # 等待1秒
        #     st.session_state.text_output += f"{time.time}文字更新于 \n"
        #     st.rerun()
        
    with col2:
        if st.button(f"**返回首页**", key="caculation_to_setting"):
            st.session_state["current_page"] = "参数设置"
            st.rerun()

    if moni_button:
        if skill in ["苍龙玄", "苍龙煞", "未名神通"]:
            st.markdown(f"*抱歉，该技能由于存在伤害递增，暂时无法模拟。以上伤害结果为计算出的最后一段伤害数值*")
        else:
            progress_text = "正在计算中... 请稍后."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()

            # 显示图表
            data['实际伤害'] = data['实际伤害'].round(4) 
            fig = px.bar(data, x='段数', y='实际伤害', title=f"{skill}{period}段伤害：", labels={'实际伤害': f'实际伤害{unit_label}'})
            st.plotly_chart(fig)

        text_area = st.empty()
        updated_texts = []

        for i in range(1, 11):  # 替换为你需要的更新次数
            time.sleep(1)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated_text = f"{current_time} :red[更新中]... 第 {i} 秒"
            updated_texts.append(updated_text)
            # 仅保留可见行数的内容
            updated_texts = updated_texts[-5:]

            text_area.markdown("<br>".join(updated_texts), unsafe_allow_html=True)
            #text_area.text("\n".join(updated_texts))
        st.session_state.real_damage = real_damage
    return 

def render_setting_page():
    #st.markdown('<a name="top"></a>', unsafe_allow_html=True)

    # 为图片增加边框背景
    #st.markdown("<style> img { border: 2px solid #333; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); } </style>", unsafe_allow_html=True)
    st.image('zhuxian.jpeg', use_column_width = True)#caption='图片来源自www.baidu.com'
    #st.markdown("<h1 style='text-align: left; background-color: #663399; color: #ffffff; padding: 10px;'>Step1: 参数设置</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 36px; color: #333333; font-weight: bold; '>Step1: 参数设置</h1>", unsafe_allow_html=True) #text-align: center;
    st.subheader("导入数据文件")

    # 创建一个按钮用于上传文件
    uploaded_file = st.file_uploader(":green[*(上传已保存的数据文件)*]", type=["yaml"])

    # 如果有文件上传，读取并加载 YAML 文件
    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        uploaded_data = yaml.safe_load(file_contents)

        # 更新 st.session_state 中的数据
        st.session_state.my_attributes = uploaded_data.get("my_attributes", {})
        st.session_state.boss_attributes = uploaded_data.get("boss_attributes", {})
        st.session_state.roles_para = uploaded_data.get("roles_para", {})
        st.session_state.skill_para = uploaded_data.get("skill_para", {})
        st.session_state.var_gains_para = uploaded_data.get("var_gains_para", {})

        st.success("数据文件导入成功！")

    st.subheader(f"选择主输出职业(必选)")
    global selected_output

    #先选择主输出职业
    selected_output = st.radio(
                            ":green[*(目前仅测试了仙逐霜)*]", 
                            output_options, 
                            key="output_radio", 
                            on_change=update_prof_index,
                            horizontal=True, 
                            index=st.session_state.my_attributes["主输出_职业"]
                        )

    # 为主输出设置属性
    with st.expander(f"**填写主输出属性：**"):   
        st.caption(':green[*(以下气血、攻击、防御填写满状态属性，其余均为御宝白状态属性)*]') 
        set_role_attributes("主输出")

    # 选择组队职业（多选框）
    st.subheader(f"选择组队职业")
    st.multiselect(
                ":green[*(选择一个或多个组队职业并在下方修改属性)*]", 
                profession_options, 
                key="profession_options_multiselect", 
                on_change=update_prof_options,
                default = st.session_state.selected_roles
                )

    # 为每个职业设置属性
    for selected_class in st.session_state.selected_roles:
        with st.expander(f"**填写{selected_class}属性：**"):
            if selected_class in ["天音", "天华", "昭冥", "画影"]:
                st.caption(f':green[*(以下填写{selected_class}满状态属性)*]') 
            else:
                pass
            set_role_attributes(selected_class)

    # 为boss设置属性
    st.subheader(f"设置BOSS属性")
    with st.expander(f"**填写BOSS属性：**"):
        st.caption(':green[*(暂不支持天界BOSS)*]') 
        set_role_attributes("BOSS")

    # 选择输出技能（单选）
    st.subheader(f"选择输出技能(必选)")

    #根据职业提供技能列表，特别的根据心法选择银鳞玄冰
    changed_skill_options = skill_options[selected_output]["values"]
    if selected_output == "逐霜" and st.session_state.my_attributes["主输出_心法_银鳞玄冰"] == False:
        changed_skill_options = ["苍龙玄", "苍龙煞"]

    #print("input_skill_index", st.session_state.skill_para["技能名称索引"])

    # 增加一个判断，如果获取到的index大于changed_skill_options数组长度，则将index置为0
    if st.session_state.skill_para["技能名称索引"] > len(changed_skill_options) - 1:
        st.session_state.skill_para["技能名称索引"] = 0

    selected_skill = st.radio(
                        ":green[*(只可选择下方列表中的一个技能)*]", 
                        changed_skill_options, 
                        key="radio1", 
                        on_change=update_skill_index,
                        horizontal=True, 
                        index=st.session_state.skill_para["技能名称索引"])

    # 展示出来技能增益参数
    with st.expander(f"**{selected_skill}技能增益参数**", expanded = False):
        if selected_skill in ["银鳞玄冰"]:
            st.caption(':green[*(目前银鳞玄冰的技能附加值是按照心法全满计算的)*]') 
        st.session_state.skill_para = set_skill_attributes(selected_skill)

    st.session_state.skill_para["技能名称索引"] = changed_skill_options.index(selected_skill)
    st.session_state.skill_para["技能名称"] = selected_skill

    # 选择可变增益项（多选框）
    st.subheader(f"选择可变增益项")
    st.multiselect(
                ":green[*(在下方多选框中添加或删除增益项)*]", 
                var_gain_options, 
                key="selected_gains_multiselect", 
                on_change=update_selected_gains,
                default = st.session_state.selected_gains, 
                help="选择一个或多个增益项目并在下方修改属性")

    # 为每个可变增益项设置属性
    with st.expander(f"**可变增益参数**", expanded = False):
        set_gain_attributes(st.session_state.selected_gains)

    # 保存和跳转
    save_to_file = st.checkbox("是否保存所有数据到文件？", value=False)
    save_button = st.button(f"**设置完成**", key="setting_to_attribute", type="primary")

    # 当按钮被点击且复选框为 True 时执行保存逻辑
    if save_button:
        # if selected_skill == "":
        #     st.warning("请选择一个输出技能！")
        #     return  {}, {}, {}, {}, {}# 不执行跳转

        # if selected_output == "":
        #     st.warning("请选择一个主输出职业！")
        #     return  {}, {}, {}, {}, {}# 不执行跳转
        if save_to_file:
            save_session_state_to_yaml()
        st.session_state["current_page"] = "属性确认"
        st.rerun()

    #st.markdown('[返回顶部](#top)')    
    return

def save_session_state_to_yaml():
    # 获取所有控件的值并保存到字典中
    config_dict = {
        "my_attributes": st.session_state.my_attributes,
        "boss_attributes": st.session_state.boss_attributes,
        "roles_para": st.session_state.roles_para,
        "skill_para": st.session_state.skill_para,
        "var_gains_para": st.session_state.var_gains_para,
    }

    # 弹出文件保存对话框
    file_path = filedialog.asksaveasfilename(defaultextension=".yaml", filetypes=[("YAML files", "*.yaml")])
    
    if file_path:
        # 保存到 YAML 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(config_dict, file, allow_unicode=True)

def move_specific_items_to_end(items, specific_items):
    for item in specific_items:
        if item in items:
            items.remove(item)
            items.append(item)

def set_gain_attributes(selected_gains):
    move_specific_items_to_end(selected_gains, ["经典家族技能等级"])

    half_len = len(selected_gains) // 2
    column1_content = selected_gains[:half_len]
    column2_content = selected_gains[half_len:]

    col1, col2 = st.columns(2)
    with col1:
        for content1 in column1_content:
           gain_attribute_input(content1)
    with col2:
        for content2 in column2_content:
            gain_attribute_input(content2)


def gain_attribute_input(attribute):
    step = 1  # 默认步长为1
    min_value = 0
    max_value = 1
    unique_key = f"{attribute}_slider"  # 使用属性名称作为唯一的 key

    # 根据属性名称设置不同的步长
    if attribute in ["法宝融合爆伤"]:
        step = 5  # 设置为10
        min_value = 0
        max_value = 200
        st.number_input(
                    f"{attribute}", 
                    key=unique_key, 
                    min_value=min_value, 
                    max_value=max_value, 
                    value=st.session_state.var_gains_para[attribute], 
                    on_change=partial(update_gains_item, attribute, unique_key),
                    step=step
                    )
        return
    elif attribute in ["九华奠魂曲"]:
        step = 10  
        min_value = 110
        max_value = 140
        st.selectbox(
                    f"{attribute}",
                    options=ring_level_options, 
                    key=unique_key, 
                    on_change=partial(update_gains_item, attribute, unique_key),
                    index=ring_level_options.index(st.session_state.var_gains_para[attribute])
                    )
        return
    elif attribute in ["副本赠送爆伤"]:
        st.selectbox(
                    f"{attribute}",
                    options=fuben_options, 
                    key=unique_key, 
                    on_change=partial(update_gains_item, attribute, unique_key),
                    index=fuben_options.index(st.session_state.var_gains_para[attribute])
                    )
        return
    elif attribute in ["经典家族技能等级"]:
        step = 1  
        min_value = 0
        max_value = 15
        #st.slider(
        st.selectbox(
                f"{attribute}",
                #min_value=min_value, 
                #max_value=max_value, 
                options=jiazu_level_options, 
                #value=st.session_state.var_gains_para[attribute], 
                key=unique_key, 
                on_change=partial(update_gains_item, attribute, unique_key),
                index=jiazu_level_options.index(st.session_state.var_gains_para[attribute])
                #step=step
                )
        return
    elif attribute in ["进阶家族技能等级(爆伤)"]:
        step = 0.1  
        min_value = 0.0
        max_value = 30.0
        st.number_input(
                    f"{attribute}", 
                    min_value=min_value, 
                    max_value=max_value, 
                    value=st.session_state.var_gains_para[attribute], 
                    on_change=partial(update_gains_item, attribute, unique_key),
                    key=unique_key, 
                    step=step
                    )
        return

    elif attribute in ["墨雪特效霜情"]:
        step = 5000
        st.selectbox(f"{attribute}",options=[20000], key=unique_key, index=0)
    elif attribute in ["三碗不过岗"]:
        step = 5000
        st.selectbox(f"{attribute}",options=[20], key=unique_key, index=0)

    elif attribute in ["情愫项链技能佳期"]:
        step = 1
        st.selectbox(f"{attribute}",options=[10], key=unique_key, index=0)

    return 

def set_skill_attributes(selected_skill):
    # 根据选择的技能填写技能附加值
    skill_attributes_dict = {}
    if selected_skill == "":
        return

    col1, col2 = st.columns(2)
    with col1:
        skill_attributes_dict[f"{selected_skill}_附加本体攻击百分比"] = skill_attribute_input(selected_skill,"附加本体攻击百分比")
        skill_attributes_dict[f"{selected_skill}_附加固定攻击值"] = skill_attribute_input(selected_skill,"附加固定攻击值")
        skill_attributes_dict[f"{selected_skill}_附加防御上限百分比"] = skill_attribute_input(selected_skill,"附加防御上限百分比")
    with col2:
        skill_attributes_dict[f"{selected_skill}_附加气血上限百分比"] = skill_attribute_input(selected_skill,"附加气血上限百分比")
        skill_attributes_dict[f"{selected_skill}_附加真气上限百分比"] = skill_attribute_input(selected_skill,"附加真气上限百分比")
        skill_attributes_dict[f"{selected_skill}_附加爆伤"] = skill_attribute_input(selected_skill,"附加爆伤")
    return skill_attributes_dict

def skill_attribute_input(selected_skill, attribute, help_text=None):
    step = 1  # 默认步长为1
    default_value = 1
    min_value = 0
    max_value = 1
    unique_key = f"{attribute}_slider"  # 使用属性名称作为唯一的 key

    # 获取对应属性的默认值字典
    attribute_values = skills_detail_options.get(attribute, {})

    # 设置默认值
    step = attribute_values.get("step", 1)
    default_value = attribute_values.get("default", 100)
    min_value = attribute_values.get("min", 0)
    max_value = attribute_values.get("max", 10000)

    if selected_skill in attribute_values.get("values", {}):
        default_value = attribute_values["values"][selected_skill]
        
    #selected_value = st.slider(f"{attribute}", min_value=min_value, max_value=max_value, value=default_value, step=step, key=unique_key)
    selected_value = st.number_input(f"{attribute}", min_value=min_value, max_value=max_value, value=default_value, step=step, key=unique_key)
    return selected_value

def set_role_attributes(prefix):
    if prefix == "BOSS":
        col1, col2 = st.columns(2)
        with col1:
            # 只在 BOSS 类型下显示 "减爆伤" 属性，单独一列
            role_attribute_input(prefix,"气血")
            role_attribute_input(prefix,"防御")
            role_attribute_input(prefix, "减爆伤")
        with col2:
            role_attribute_input(prefix, "厄运诅咒(绿点)")
            role_attribute_input(prefix, "混乱诅咒")
            role_attribute_input(prefix, "伤害压缩百分比", disabled=True)
   
    elif prefix == "天音":
        col1, col2 = st.columns(2)
        with col1:
            role_attribute_input(prefix,"真气")
            role_attribute_input(prefix,"玄烛品质_摩柯心经")
        with col2:
            role_attribute_input(prefix,"最大攻击")
            st.text('法宝技能是否+1')
            role_attribute_input(prefix,"技能_慈航法愿")

    elif prefix == "天华":
        col1, col2 = st.columns(2)
        with col1:
            role_attribute_input(prefix,"真气")
            role_attribute_input(prefix,"前世职业_凤求凰")
            st.text('法宝技能是否+1')
            role_attribute_input(prefix,"技能_金蛇狂舞")
        with col2:
            role_attribute_input(prefix,"最大攻击")
            st.text('法宝技能是否+1')
            role_attribute_input(prefix,"技能_秋声雅韵")

    elif prefix == "画影":
        col1, col2 = st.columns(2)
        with col1:
            role_attribute_input(prefix,"真气")
        with col2:
            st.text('法宝技能是否+1')
            role_attribute_input(prefix,"技能_凌寒拂霜")
    elif prefix == "昭冥":
        col1, col2 = st.columns(2)
        with col1:
            role_attribute_input(prefix,"气血")
            role_attribute_input(prefix,"真气")
            role_attribute_input(prefix,"防御")
            st.text('法宝技能是否+1')
            role_attribute_input(prefix,"技能_日月弘光")
        with col2:
            role_attribute_input(prefix,"最小攻击")
            role_attribute_input(prefix,"最大攻击")
            role_attribute_input(prefix,"爆伤")

    elif prefix == "青罗":
        col1, col2 = st.columns(2)
        with col1:
            role_attribute_input(prefix,"技能_研彻晓光")
        with col2:
            role_attribute_input(prefix,"技能_缓分花陌2")

    elif prefix == "焚香":
        col1, col2 = st.columns(2)
        with col1:
            role_attribute_input(prefix,"技能_祝融真典2")

    elif prefix == "青云":
        col1, col2 = st.columns(2)
        with col1:
            role_attribute_input(prefix,"技能_五气朝元")

    else:        
        col1, col2 = st.columns(2)
        with col1:
            role_attribute_input(prefix,"气血")
            role_attribute_input(prefix,"真气")
            role_attribute_input(prefix,"最小攻击")
            role_attribute_input(prefix,"最大攻击")
            role_attribute_input(prefix,"防御")
            role_attribute_input(prefix,"爆伤")
            if selected_output == "逐霜":
                role_attribute_input(prefix,"玄烛品质_云蒸霞蔚")
            elif selected_output == "惊岚":
                role_attribute_input(prefix,"赤乌品质_森罗削空斩")
            elif selected_output == "涅羽":
                role_attribute_input(prefix,"赤乌品质_大业浮屠")

        with col2:
            role_attribute_input(prefix,"对怪增伤")#"属性面板滚轮向下即可看到【对怪物增伤】"
            role_attribute_input(prefix,"减爆伤", True)
            role_attribute_input(prefix,"1%气血比对应面板气血")#"分别记录更换气血比荧惑前后的面板气血，作差后除以该气血比荧惑的数值即为填写值"
            role_attribute_input(prefix,"1%真气比对应面板真气")
            role_attribute_input(prefix,"1%攻击比对应面板攻击")
            role_attribute_input(prefix,"1%防御比对应面板防御")
        if selected_output == "逐霜":
            st.text(f'心法技能')
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                role_attribute_input(prefix,"心法_乘时而化")
                role_attribute_input(prefix,"心法_银鳞玄冰")
            with col2:
                role_attribute_input(prefix,"心法_太极_乘时而化")
                role_attribute_input(prefix,"心法_般若_银鳞玄冰")         
            with col3:
                role_attribute_input(prefix,"心法_玄清_乘时而化")
                role_attribute_input(prefix,"心法_幽录_银鳞玄冰")   

def role_attribute_input(prefix, attribute, disabled = False):
    # 设置默认值
    step = 1  # 默认步长为1
    min_value = 0
    max_value = 1
    unique_key = f"{prefix}_{attribute}_slider"  # 使用属性名称作为唯一的 key
    help = None
    disabled = False

    # 根据属性名称设置不同的步长
    if attribute in ["气血", "真气", "满状态气血", "满状态真气", "御宝状态气血", "御宝状态真气"]:
        step = 10000  # 设置为1万
        min_value = 0
        max_value = 10000000
    elif attribute in ["爆伤", "御宝状态爆伤", "满状态爆伤"]:
        step = 0.1  # 设置为0.1
        min_value = 0.0
        max_value = 3000.0
    elif attribute in ["对怪增伤"]:
        step = 0.1  # 设置为0.1
        min_value = 0.0
        max_value = 30.0
    elif attribute in ["防御","御宝状态防御","满状态防御"]:
        step = 500  # 设置为500
        min_value = 0
        max_value = 500000
    elif attribute in ["最小攻击", "最大攻击", "御宝状态最小攻击", "御宝状态最大攻击", "满状态最小攻击", "满状态最大攻击"]:
        step = 500  # 设置为500
        min_value = 0
        max_value = 750000        
    elif attribute in ["1%攻击比对应面板攻击", "1%防御比对应面板防御"]:
        step = 10  # 10
        min_value = 0
        max_value = 500
        help = "通过装卸称号、荧惑、重华产生的属性变化来计算1%百分比对应的数值"
    elif attribute in ["1%气血比对应面板气血", "1%真气比对应面板真气"]:
        step = 100  # 100
        min_value = 0
        max_value = 10000
        help = "通过装卸称号、荧惑、重华产生的属性变化来计算1%百分比对应的数值"
    elif attribute in ["减爆伤", "御宝状态减爆伤"]:
        step = 1  # 设置为10%
        min_value = 0
        max_value = 3000
    elif attribute in ["伤害压缩百分比"]:
        step = 5  # 设置为10%
        min_value = 0
        max_value = 100
    elif attribute in ["混乱诅咒"]:
        step = 1  # 设置为10
        min_value = 0
        max_value = 120
    elif attribute in ["厄运诅咒(绿点)"]:
        step = 10  # 设置为10
        min_value = 0
        max_value = 900
    elif "技能" in attribute:
        st.checkbox(
                f"{attribute}",
                value=st.session_state.roles_para[prefix][f"{prefix}_{attribute}"], 
                #on_change = update_checkbox_value(prefix, attribute, unique_key),
                on_change = partial(update_checkbox_value, prefix, attribute, unique_key),
                key=unique_key
                )
        return 
    elif "心法" in attribute:
        if attribute in ["心法_玄清_乘时而化", "心法_般若_银鳞玄冰", "心法_幽录_银鳞玄冰"]:
            disabled = True
        st.checkbox(
                f"{attribute}",
                value=st.session_state.my_attributes[f"{prefix}_{attribute}"], 
                on_change = partial(update_checkbox_value,prefix, attribute, unique_key),
                disabled = disabled,
                key=unique_key
                )
        check_val = st.session_state.my_attributes[f"{prefix}_{attribute}"]
        #st.write(f"{check_val}")
        #print("st.write", st.session_state.my_attributes[f"{prefix}_{attribute}"])

        return 
    elif "品质" in attribute:
        if prefix == "主输出":
                st.selectbox(
                        f"{attribute}",
                        options=xingxiu_options, 
                        index=xingxiu_options.index(st.session_state.my_attributes[f"{prefix}_{attribute}"]), 
                        on_change = partial(update_selectbox_value,prefix, attribute, unique_key),
                        key=unique_key
                        )
        else:
                st.selectbox(
                        f"{attribute}",
                        options=xingxiu_options, 
                        index=xingxiu_options.index(st.session_state.roles_para[prefix][f"{prefix}_{attribute}"]), 
                        on_change = partial(update_selectbox_value,prefix, attribute, unique_key),
                        key=unique_key
                        )
                
        return 
    elif "前世" in attribute:
        st.selectbox(
                f"{attribute}",
                options=qianshi_options, 
                index=qianshi_options.index(st.session_state.roles_para[prefix][f"{prefix}_{attribute}"]), 
                on_change = partial(update_selectbox_value,prefix, attribute, unique_key),
                key=unique_key
                )
        
        return 

    #判断是否存在缓存值，存在的话直接根据prefix和 attribute获取确定的值
    if prefix == "主输出":
        st.number_input(
                    f"{attribute}", 
                    min_value=min_value, 
                    max_value=max_value, 
                    value=st.session_state.my_attributes[f"{prefix}_{attribute}"], 
                    on_change = partial(update_number_input_value,prefix, attribute, unique_key),
                    step=step, 
                    key=unique_key, 
                    help = help,
                    disabled = disabled
                    )
    elif prefix == "BOSS":
        st.number_input(
                    f"{attribute}", 
                    min_value=min_value, 
                    max_value=max_value, 
                    value=st.session_state.boss_attributes[f"{prefix}_{attribute}"], 
                    on_change = partial(update_number_input_value,prefix, attribute, unique_key),
                    step=step, 
                    key=unique_key, 
                    disabled = disabled
                    )
    else:
        st.number_input(
                    f"{attribute}", 
                    min_value=min_value, 
                    max_value=max_value, 
                    value=st.session_state.roles_para[prefix][f"{prefix}_{attribute}"], 
                    on_change = partial(update_number_input_value,prefix, attribute, unique_key),
                    step=step, 
                    key=unique_key, 
                    disabled = disabled
                    )    
        
def update_prof_index():
    prof = st.session_state.get("output_radio", None)
    st.session_state.my_attributes["主输出_职业"] = output_options.index(prof)

def update_prof_options():
    select_profession_options = st.session_state.get("profession_options_multiselect", None)
    st.session_state.selected_roles = select_profession_options

def update_selected_gains():
    select_gains_options = st.session_state.get("selected_gains_multiselect", None)
    st.session_state.selected_gains = select_gains_options
    
def update_gains_item(attribute, unique_key):
    gains_value = st.session_state.get(unique_key, None)
    #print(unique_key, gains_value)
    st.session_state.var_gains_para[attribute] = gains_value
    
def update_skill_index():
    skill = st.session_state.get("radio1", None)
    prof = st.session_state.my_attributes["主输出_职业"]
    prof_name = output_options[prof]
    changed_skill_options = skill_options[prof_name]["values"]
    st.session_state.skill_para["技能名称索引"] = changed_skill_options.index(skill)

def update_number_input_value(prefix, attribute, unique_key):
    curr_value = st.session_state.get(unique_key, None)

    if prefix == "主输出":
        st.session_state.my_attributes[f"{prefix}_{attribute}"] = curr_value
    elif prefix == "BOSS":
        st.session_state.boss_attributes[f"{prefix}_{attribute}"] = curr_value
    else:
        st.session_state.roles_para[prefix][f"{prefix}_{attribute}"] = curr_value
    
def update_selectbox_value(prefix, attribute, unique_key):
    curr_value = st.session_state.get(unique_key, None)

    if prefix == "主输出":
        st.session_state.my_attributes[f"{prefix}_{attribute}"] = curr_value
    else:
        st.session_state.roles_para[prefix][f"{prefix}_{attribute}"] = curr_value

def update_checkbox_value(prefix, attribute, unique_key):
    curr_value = st.session_state.get(unique_key, None)

    if prefix == "主输出":
        st.session_state.my_attributes[f"{prefix}_{attribute}"] = curr_value
    else:
        st.session_state.roles_para[prefix][f"{prefix}_{attribute}"] = curr_value

def convert_to_number(value):
    if "亿" in value:
        return float(value.replace("亿", ""))
    elif "万" in value:
        return float(value.replace("万", ""))
    else:
        return float(value)    
    
def convert_to_units(numbers, unit='亿'):
    if unit == '亿':
        return [round(num / 1e8, 4) for num in numbers]
    elif unit == '万':
        return [round(num / 1e4, 4) for num in numbers]
    else:
        return numbers