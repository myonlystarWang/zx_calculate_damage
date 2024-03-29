# user_interface.py
import streamlit as st
from calculator import calculate_basic_damage
from calculator import my_gained_attribute_calculate
from calculator import roles_skill_gains_calculate, all_skill_gains_calculate
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
import os

# 主输出选项
output_options = ["逐霜", "鬼王", "太昊", "惊岚", "涅羽"]
output_en_options = ["zhushuang", "guiwang", "taihao", "jinglan", "nieyu"]

# 技能选项
skill_options = {
        "逐霜": {"values": ["苍龙玄", "苍龙煞", "银鳞玄冰"]},
        "鬼王": {"values": ["未名神通", "九变"]},
        "太昊": {"values": ["天地绝神通"]},
        "惊岚": {"values": ["森罗削空斩·赤乌"]},
        "涅羽": {"values": ["大业浮屠·赤乌"]},
    }
# 职业选项
profession_options = ["天音", "天华", "昭冥", "画影", "鬼王", "焚香", "青罗", "青云", "英招", "九黎", "百灵"]

# 通用增益选项
var_gain_options = ["九华淀魂曲" , "八级雷煌闪", "三味真炎火", "雪琪的祈愿", "副本赠送属性", "龙虎之力", "墨雪特效霜情", "三碗不过岗", "情愫项链技能佳期", "法宝融合爆伤", "进阶家族技能等级", "经典家族技能等级", "星语拔山"]

# 星宿品质选项
xingxiu_options = ["荧炬", "皓月", "曦日"]

# 三代品质选项
sandai_options = ["1级", "2级", "3级"]

# 前世职业选项
qianshi_options = ["太昊", "烈山", "其他"]

# 副本爆伤选项
fuben_options = ["无赠送", "T16以上", "空桑兽神", "四象七"]

# 副本爆伤选项
longhu_options = ["龙虎3", "龙虎4"]

# 项链技能等级选项
#ring_level_options = ["1级", "2级", "3级", "4级"]
ring_level_options = ["3级", "4级"]

# 家族技能等级选项
jiazu_level_options = ["1阶", "2阶", "3阶", "4阶", "5阶", "6阶", "7阶", "8阶", "9阶", "10阶", "11阶", "12阶", "13阶", "14阶", "15阶"]

# 技能输出字典
#仙涅羽赤乌多50%攻击  10%气血  5%真气
skills_detail_options = {
        "附加本体攻击百分比": {"step": 1, "default": 100, "min": 0, "max": 500, "values": {"苍龙玄": 240, "苍龙煞": 240, "银鳞玄冰": 290, "未名神通": 168, "九变": 130, "大业浮屠·赤乌": 290, "森罗削空斩·赤乌": 400, "天地绝神通": 200}},
        "附加防御上限百分比": {"step": 10, "default": 100, "min": 0, "max": 500, "values": {"苍龙玄": 0, "苍龙煞": 0, "银鳞玄冰": 0, "未名神通": 400, "九变": 0, "大业浮屠·赤乌": 0, "森罗削空斩·赤乌": 0, "天地绝神通": 0}},
        "附加气血上限百分比": {"step": 5, "default": 100, "min": 0, "max": 500, "values": {"苍龙玄": 0, "苍龙煞": 48, "银鳞玄冰": 40, "未名神通": 0, "九变": 20, "大业浮屠·赤乌": 60, "森罗削空斩·赤乌": 12, "天地绝神通": 26}},
        "附加真气上限百分比": {"step": 5, "default": 100, "min": 0, "max": 500, "values": {"苍龙玄": 48, "苍龙煞": 0, "银鳞玄冰": 40, "未名神通": 15, "九变": 20, "大业浮屠·赤乌": 30, "森罗削空斩·赤乌": 12, "天地绝神通": 26}},
        "附加爆伤": {"step": 5, "default": 100, "min": 0, "max": 500, "values": {"苍龙玄": 100, "苍龙煞": 100, "银鳞玄冰": 100, "未名神通": 100, "九变": 0, "大业浮屠·赤乌": 30, "森罗削空斩·赤乌": 100, "天地绝神通": 100}},
        "附加固定攻击值": {"step": 10, "default": 300, "min": 0, "max": 10000, "values": {"苍龙玄": 4000, "苍龙煞": 4000, "银鳞玄冰": 6000, "未名神通": 2720, "九变": 0, "大业浮屠·赤乌": 5000, "森罗削空斩·赤乌": 4800, "天地绝神通": 2750}},
    }

# 第二页显示主输出的键
keys_to_display = [
    "主输出_气血",
    "主输出_真气",
    "主输出_最小攻击",
    "主输出_最大攻击",
    "主输出_防御",
    "主输出_自身防御力",    
    "主输出_爆伤",
    "主输出_对怪增伤",
    "主输出_减爆伤",
]

# 技能段数
skills_period_option = {"苍龙玄": 9,"苍龙煞": 9,"银鳞玄冰": 6,"未名神通": 6,"九变": 9,"天地绝神通": 5,"森罗削空斩·赤乌": 15,"大业浮屠·赤乌": 8}

# 伤害上限
max_damage = 2147483647

# 涅羽凰吻2
fengwen2_options = {"附加本体攻击百分比": 50,"附加气血上限百分比": 10,"附加真气上限百分比": 5}

def render_attributes_page():
    st.markdown("<h1 style='font-size: 40px; color: #333333; font-weight: bold; '>📝 属性确认</h1>", unsafe_allow_html=True) #text-align: center;#📚
    #st.header("Step2: 属性确认")

    st.subheader("已选择职业项")

    col1, col2, col3 = st.columns([1,2,1])
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

    # 删除roles_para中不在selected_roles里的职业，形成一个新的变量传递给skill_gains_calculate函数
    roles_para_copy = copy.deepcopy(st.session_state.roles_para)
    roles_para_filtered = {role: values for role, values in roles_para_copy.items() if role in st.session_state.selected_roles}

    # 删除var_gains_para中不在selected_gains里的增益项，形成一个新的变量传递给skill_gains_calculate函数
    var_gains_para_copy = copy.deepcopy(st.session_state.var_gains_para)
    var_gains_para_filtered = {role: values for role, values in var_gains_para_copy.items() if role in st.session_state.selected_gains}

    roles_skill_gains_para = roles_skill_gains_calculate(st.session_state.my_attributes, roles_para_filtered, var_gains_para_filtered)
    skill_gains_para = all_skill_gains_calculate(st.session_state.my_attributes, roles_skill_gains_para, var_gains_para_filtered)

    # 分类后的变量
    skill_categories = {}
    # 遍历原始字典，按照不同类别分类
    for key, value in skill_gains_para.items():
        # 获取技能增益的类型（攻击、防御、真气、爆伤等）
        skill_type = key.split("_")[1]
        
        # 构建对应类型的字典，如果还没有创建
        if skill_type not in skill_categories:
            skill_categories[skill_type] = {}
        
        # 将键值对添加到相应的变量中
        skill_categories[skill_type][key] = value        

    # 显示所有技能增益
    st.subheader("技能增益项")
   
    # 按不同增益分开展示
    with st.expander(f"**展开以显示各类增益数值**"):   
        st.markdown("**已选择的通用增益项:**")
        formatted_gains = " ".join([f"{gain}" for gain in st.session_state.selected_gains])
        st.text(f"{formatted_gains}")
        
        # 将每一个分离出来的变量分列在不同列中        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.json(skill_categories.get("攻击", {}))
            st.json(skill_categories.get("攻击比", {}))
        with col2:
            st.json(skill_categories.get("气血", {}))
            st.json(skill_categories.get("气血比", {}))
            st.json(skill_categories.get("真气", {}))
            st.json(skill_categories.get("真气比", {}))
        with col3:
            st.json(skill_categories.get("防御", {}))
            st.json(skill_categories.get("自身防御力", {}))
            st.json(skill_categories.get("防御比", {}))
            st.json(skill_categories.get("对怪", {}))
        with col4:
            st.json(skill_categories.get("爆伤", {}))
            st.json(skill_categories.get("专注", {}))
            st.json(skill_categories.get("巫咒", {}))                  

    # 显示主输出满增益属性
    # st.markdown("**主输出御宝状态属性:**")
    # st.json(st.session_state.my_attributes)
    st.subheader("主输出满增益属性")
    my_gain_attributes = my_gained_attribute_calculate(st.session_state.my_attributes, skill_gains_para, st.session_state.var_gains_para, skill_categories)
    #st.json(my_gain_attributes)

    # 从原始数据中提取要显示的部分
    filtered_data = {key: my_gain_attributes[key] for key in keys_to_display}

    # 将结果转换为 JSON 格式并打印
    filtered_json = json.dumps(filtered_data, indent=4)
   
    # 显示技能伤害
    # st.subheader("技能附加伤害")
    # st.json(st.session_state.skill_para)

    # 显示通用增益项
    # st.subheader("通用增益项")
    # st.json(st.session_state.var_gains_para)

    # 显示boss属性
    # st.subheader("BOSS属性")
    # st.json(st.session_state.boss_attributes)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.json(filtered_json)

    with col2:
        #if st.button(f"**配置文件列表**", key="list_config", type="primary", use_container_width=True):
        on = st.toggle('**配置文件下载**')
        if on:
            # 获取config目录下所有yaml文件
            yaml_files = [f for f in os.listdir("./config") if f.endswith(".yaml")]
            
            # 获取config目录下所有yaml文件
            yaml_files = get_sorted_file_list("./config")

            # 检查yaml_files是否为空
            if not yaml_files:
                st.warning("当前没有可用的配置文件。")
            else:
                st.success("获取配置文件列表成功！")

                # 创建一个selectbox让用户选择要下载的文件
                selected_file = st.selectbox("选择要下载的配置文件:", yaml_files)

                # 获取文件的完整路径
                file_path = os.path.join("./config", selected_file)

                # 读取文件的二进制数据
                with open(file_path, "rb") as file:
                    file_data = file.read()

                # 使用st.download_button来下载文件
                st.download_button(
                    label="下载配置文件",
                    data=file_data,  # 传递文件的二进制数据
                    file_name=selected_file,  # 设置下载文件的名称
                    key="download_cfg", 
                    mime="text/plain"  # 设置文件的MIME类型，这里假设是纯文本
                )

    if st.button(f"**属性确认完成**", key="attributes_to_caculation", type="primary", use_container_width=True):
        st.session_state["current_page"] = "💻伤害计算-结果模拟"
        st.rerun()

    #col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
    # col1, col2 = st.columns(2)
    # with col1:
    #     if st.button(f"**属性确认完成**", key="attributes_to_caculation", type="primary", use_container_width=True):
    #         st.session_state["current_page"] = "💻伤害计算-结果模拟"
    #         st.rerun()
    # with col2:
    #     if st.button(f"**返回参数设置**", key="attributes_to_setting", use_container_width=True):
    #         st.session_state["current_page"] = "🛠️伤害计算-参数设置"
    #         st.rerun()     

    st.session_state.my_gain_attributes = my_gain_attributes
    st.session_state.skill_gains_para = skill_gains_para            
    return

def render_damage_calculation_page():
    st.markdown("<h1 style='font-size: 40px; color: #333333; font-weight: bold; '>💻 结果模拟</h1>", unsafe_allow_html=True) #text-align: center;
    #st.header("Step3: 伤害计算")
    
    # # 提取特征标签

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
               st.session_state.skill_gains_para.get("技能增益_专注_怒龙吞海2", 0) + \
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
    real_damage["出爆最小伤害"] = min(int(damage_coeff.get("累积增伤系数", 0) * damage_coeff.get("总爆伤系数", 0) * basic_damage.get("最小基础伤害", 0)), max_damage)
    real_damage["出爆最大伤害"] = min(int(damage_coeff.get("累积增伤系数", 0) * damage_coeff.get("总爆伤系数", 0) * basic_damage.get("最大基础伤害", 0)), max_damage)

    # 选择一个伤害值作为目标标签
    target_label = real_damage["出爆最大伤害"]  # 或者选择 real_damage["出爆最小伤害"]

    # 进行数据保存
    save_to_csv(st.session_state.my_attributes, target_label)

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
        col1, col2, col3, col4 = st.columns(4)
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
            damage_min_i = int(real_damage["出爆最小伤害"] * (1 + 0.3) ** i)
            increasing_min_damage.append(min(damage_min_i, max_damage))   

            damage_max_i = int(real_damage["出爆最大伤害"] * (1 + 0.3) ** i)
            increasing_max_damage.append(min(damage_max_i, max_damage))            
        
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

    col1, col2, col3, col4, col5 = st.columns(5)
    #col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
    with col1:
        moni_button = st.button(f"**模拟技能伤害**", key="moni", type="primary", use_container_width=True)
        
    with col2:
        if st.button(f"**返回欢迎页面**", key="caculation_to_setting", use_container_width=True):#返回参数设置
            st.session_state["current_page"] = "🏠欢迎回来"#"🛠️伤害计算-参数设置"
            st.rerun()

    if moni_button:
        if skill in ["苍龙玄", "苍龙煞", "未名神通"]:
            st.markdown(f"*抱歉，由于{skill}存在伤害递增，以上伤害结果为计算出的最后一段伤害数值*")

        col1, col2 = st.columns(2)
        with col1:
            tab1, tab2 = st.tabs([f"📊 模拟单次技能伤害", "📋 模拟持续技能伤害"])    
            with tab1:                
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
            with tab2:                
                text_area = st.empty()
                updated_texts = []

                for i in range(1, 100):  # 替换为你需要的更新次数
                    time.sleep(1)
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if skill in ["九变"]:
                        random_values = [random.randint(min_val, max_val) for min_val, max_val in zip(increasing_min_damage, increasing_max_damage)]
                        updated_text = f"{current_time} :green[你对boss造成了]:red[{random_values[i % 9]}]:green[点伤害]"
                    else:
                        random_value = random.randint(real_damage["出爆最小伤害"],real_damage["出爆最大伤害"])
                        updated_text = f"{current_time} :green[你对boss造成了]:red[{random_value}]:green[点伤害]"
                    updated_texts.append(updated_text)
                    # 仅保留可见行数的内容
                    updated_texts = updated_texts[-8:]

                    text_area.markdown("<br>".join(updated_texts), unsafe_allow_html=True)
                    #text_area.text("\n".join(updated_texts))
                st.session_state.real_damage = real_damage
    return 

def render_setting_page():  
    #st.markdown('<a name="top"></a>', unsafe_allow_html=True)

    # 使用的是这里的进度条方案
    # # 计算完成的步骤数量
    # current_step = 3  # 假设已完成3个步骤
    # total_steps = 8  # 总步骤数

    # # 计算进度百分比
    # progress_percent = (current_step / total_steps) * 100

    # # 计算文字位置百分比
    # text_position_percent = (current_step / 8) * 100

    # progress_bar_html = f"""
    # <div style="display: flex; flex-direction: column; align-items: center; margin-top: 20px; margin-bottom: 20px;">
    #     <div style="position: relative; width: 100%;">
    #         <div style="background-color: #f0f0f0; border-radius: 5px; height: 10px; position: relative; z-index: 0; margin-bottom: -40px;">
    #             <div style="background-color: #3498db; border-radius: 5px; height: 100%; width: {progress_percent}%; position: absolute; z-index: 1;"></div>
    #         </div>
    #         <span style="position: absolute; left: {text_position_percent}%; transform: translateX(-50%); z-index: 2; color: #3498db; font-size: 18px; font-weight: bold;">第{current_step}步</span>
    #     </div>
    # </div>
    # """
    # # 使用st.markdown显示进度条
    # st.markdown(progress_bar_html, unsafe_allow_html=True)

    st.markdown("<h1 style='font-size: 40px; color: #333333; font-weight: bold; '>🛠️ 参数设置</h1>", unsafe_allow_html=True) #text-align: center;
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
        st.session_state.selected_roles = uploaded_data.get("selected_roles", {})
        st.session_state.roles_para = uploaded_data.get("roles_para", {})
        st.session_state.skill_para = uploaded_data.get("skill_para", {})
        st.session_state.var_gains_para = uploaded_data.get("var_gains_para", {})
        st.session_state.selected_gains = uploaded_data.get("selected_gains", {})
        st.info("数据文件已导入！如果希望在导入数据的基础上修改设置，请点击已上传配置文件右侧的x，删除文件后再修改！")

    st.subheader(f"选择主输出职业(必选)")
    global selected_output

    #先选择主输出职业
    selected_output = st.radio(
                            ":green[*(惊岚未测试)*]", 
                            output_options, 
                            key="output_radio", 
                            on_change=update_prof_index,
                            horizontal=True, 
                            index=st.session_state.my_attributes["主输出_职业"]
                        )

    # 为主输出设置属性
    with st.expander(f"**填写主输出属性：**"):   
        st.caption(':green[*(均填写御宝白状态属性)*]') 
        set_role_attributes("主输出")

    # 选择组队职业（多选框）
    st.subheader(f"选择组队职业")
    #这里判断如果主C是鬼王，组队职业里就不要鬼王了，同时需要看增益中是否还有鬼王
    # print(st.session_state.selected_roles)
    # if selected_output == "鬼王":
    #     # 如果selected_output是“鬼王”，并且“鬼王”在列表中，则移除
    #     if '鬼王' in st.session_state.selected_roles:
    #         st.session_state.selected_roles.remove('鬼王')
    #         profession_options.remove('鬼王')
    # else:
    #     # 如果selected_output不是“鬼王”，并且“鬼王”不在列表中，则添加
    #     if '鬼王' not in st.session_state.selected_roles and st.session_state.selected_roles != []:
    #         st.session_state.selected_roles.append('鬼王')
    #         profession_options.append('鬼王')

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
            if selected_class in ["天音", "天华", "昭冥", "画影", "鬼王"]:
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

    # 选择通用增益项（多选框）
    st.subheader(f"选择通用增益项")
    st.multiselect(
                ":green[*(在下方多选框中添加或删除增益项，神爆、龙虎1、佛尊1、佛尊2为默认存在项)*]", 
                var_gain_options, 
                key="selected_gains_multiselect", 
                on_change=update_selected_gains,
                default = st.session_state.selected_gains
                )

    # 为每个通用增益项设置属性
    with st.expander(f"**通用增益参数**", expanded = False):
        set_gain_attributes(st.session_state.selected_gains)

    # 保存和跳转
    save_to_file = st.checkbox("是否保存所有设置到文件？", value=False)#💾
    save_button = st.button(f"**参数设置完成**", key="setting_to_attribute", type="primary", use_container_width=True)

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

        st.session_state["current_page"] = "📝伤害计算-属性确认"
        st.rerun()
    
    #st.markdown('[返回顶部](#top)')    
    return

def save_toast_info(flag):
    if flag:
        msg = st.toast("配置文件已成功保存到 config 目录!")
        time.sleep(1)

def save_session_state_to_yaml():
    
    # 获取所有控件的值并保存到字典中
    config_dict = {
        "my_attributes": st.session_state.my_attributes,
        "boss_attributes": st.session_state.boss_attributes,
        "selected_roles": st.session_state.selected_roles,
        "roles_para": st.session_state.roles_para,
        "skill_para": st.session_state.skill_para,
        "selected_gains": st.session_state.selected_gains,
        "var_gains_para": st.session_state.var_gains_para,
    }

    # 生成带有当前日期的文件名
    output = st.session_state.my_attributes["主输出_职业"]
    prof = output_options[output]
    current_date = datetime.now().strftime("%Y年%m月%d日%H时%M分%S秒")
    file_name = f"./config/{prof}设置_{current_date}.yaml"

    # 弹出文件保存对话框
    #file_path = filedialog.asksaveasfilename(defaultextension=".yaml", filetypes=[("YAML files", "*.yaml")])
    
    if file_name:
        # 保存到 YAML 文件
        with open(file_name, 'w', encoding='utf-8') as file:
            yaml.dump(config_dict, file, allow_unicode=True)

    return True

def move_specific_items_to_end(items, specific_items):
    for item in specific_items:
        if item in items:
            items.remove(item)
            items.append(item)

def set_gain_attributes(selected_gains):
    #move_specific_items_to_end(selected_gains, ["经典家族技能等级"])
    num_columns = 8
    columns_content = [selected_gains[i::num_columns] for i in range(num_columns)]

    columns = st.columns(num_columns)
    for i, column_content in enumerate(columns_content):
        with columns[i]:
            for content in column_content:
                gain_attribute_input(content)

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
    elif attribute in ["九华淀魂曲", "三味真炎火", "八级雷煌闪"]:
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
    elif attribute in ["副本赠送属性"]:
        st.selectbox(
                    f"{attribute}",
                    options=fuben_options, 
                    key=unique_key, 
                    on_change=partial(update_gains_item, attribute, unique_key),
                    index=fuben_options.index(st.session_state.var_gains_para[attribute])
                    )
        return
    
    elif attribute in ["龙虎之力"]:
        st.selectbox(
                    f"{attribute}",
                    options=longhu_options, 
                    key=unique_key, 
                    on_change=partial(update_gains_item, attribute, unique_key),
                    index=longhu_options.index(st.session_state.var_gains_para[attribute])
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
    elif attribute in ["进阶家族技能等级"]:
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
        st.selectbox(f"{attribute}",options=[20000], key=unique_key, index=0)

    elif attribute in ["三碗不过岗", "星语拔山"]:
        st.selectbox(f"{attribute}",options=[20], key=unique_key, index=0)

    elif attribute in ["情愫项链技能佳期"]:
        st.selectbox(f"{attribute}",options=[10], key=unique_key, index=0)

    elif attribute in ["雪琪的祈愿"]:
        st.selectbox(f"{attribute}",options=[50], key=unique_key, index=0)

    return 

def set_skill_attributes(selected_skill):
    # 根据选择的技能填写技能附加值
    skill_attributes_dict = {}
    if selected_skill == "":
        return

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        skill_attributes_dict[f"{selected_skill}_附加本体攻击百分比"] = skill_attribute_input(selected_skill,"附加本体攻击百分比")
    with col2:
        skill_attributes_dict[f"{selected_skill}_附加固定攻击值"] = skill_attribute_input(selected_skill,"附加固定攻击值")
    with col3:
        skill_attributes_dict[f"{selected_skill}_附加防御上限百分比"] = skill_attribute_input(selected_skill,"附加防御上限百分比")
    with col4:
        skill_attributes_dict[f"{selected_skill}_附加气血上限百分比"] = skill_attribute_input(selected_skill,"附加气血上限百分比")
    with col5:
        skill_attributes_dict[f"{selected_skill}_附加真气上限百分比"] = skill_attribute_input(selected_skill,"附加真气上限百分比")
    with col6:
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
  
    # 涅羽和惊岚需要根据赤乌品质计算技能附加值
    if selected_output == "涅羽":
        # 获取赤乌品质
        quality = xingxiu_options.index(st.session_state.my_attributes.get("主输出_赤乌品质_大业浮屠", ""))

        # 分别修正攻击比、气血、真气、爆伤
        if attribute == "附加本体攻击百分比":
            default_value = default_value + 25 * quality + fengwen2_options[attribute]
        elif attribute == "附加真气上限百分比":
            default_value = default_value + 5 * quality + fengwen2_options[attribute]
        elif attribute == "附加气血上限百分比":
            default_value = default_value + 10 * quality + fengwen2_options[attribute]
        elif attribute == "附加爆伤":
            default_value = default_value + 10 * quality
    elif selected_output == "惊岚":
        # 获取赤乌品质
        quality = xingxiu_options.index(st.session_state.my_attributes.get("主输出_赤乌品质_森罗削空斩", ""))

        # 分别修正攻击比、气血、真气、爆伤
        if attribute == "附加本体攻击百分比":
            default_value = default_value + 25 * quality
        elif attribute == "附加真气上限百分比":
            default_value = default_value + 5 * quality
        elif attribute == "附加气血上限百分比":
            default_value = default_value + 10 * quality
        elif attribute == "附加爆伤":
            default_value = default_value + 10 * quality

    #selected_value = st.slider(f"{attribute}", min_value=min_value, max_value=max_value, value=default_value, step=step, key=unique_key)
    selected_value = st.number_input(f"{attribute}", min_value=min_value, max_value=max_value, value=default_value, step=step, key=unique_key, disabled=True)
    return selected_value

def set_role_attributes(prefix):
    if prefix == "BOSS":
        col1, col2, col3, col4, col5, col6, col7= st.columns(7)
        with col1:
            # 只在 BOSS 类型下显示 "减爆伤" 属性，单独一列
            role_attribute_input(prefix,"气血")
        with col2:
            role_attribute_input(prefix,"防御")
        with col3:
            role_attribute_input(prefix, "减爆伤")
        with col4:
            role_attribute_input(prefix, "厄运诅咒(绿点)")
        with col5:
            role_attribute_input(prefix, "混乱诅咒")
        with col6:
            role_attribute_input(prefix, "伤害压缩百分比", disabled=True)
   
    elif prefix == "天音":
        col1, col2, col3, col4, col5, col6, col7= st.columns(7)
        with col1:
            role_attribute_input(prefix,"真气")
        with col2:
            role_attribute_input(prefix,"最大攻击")
        with col3:
            role_attribute_input(prefix,"玄烛品质_摩柯心经")
        with col4:
            st.text('法宝技能是否+1')
            role_attribute_input(prefix,"技能_慈航法愿")

    elif prefix == "天华":
        col1, col2, col3, col4, col5, col6, col7= st.columns(7)
        with col1:
            role_attribute_input(prefix,"真气")
        with col2:
            role_attribute_input(prefix,"最大攻击")
        with col3:
            role_attribute_input(prefix,"前世职业_凤求凰")
        with col4:
            st.text('法宝技能是否+1')
            role_attribute_input(prefix,"技能_金蛇狂舞")
        with col5:
            st.text('法宝技能是否+1')
            role_attribute_input(prefix,"技能_秋声雅韵")
        with col6:
            st.text('法宝技能是否+1')
            role_attribute_input(prefix,"技能_鸣泉雅韵")

    elif prefix == "画影":
        col1, col2, col3, col4, col5, col6, col7= st.columns(7)
        with col1:
            role_attribute_input(prefix,"真气")
        with col2:
            st.text('法宝技能是否+1')
            role_attribute_input(prefix,"技能_凌寒拂霜")

    elif prefix == "鬼王":
        if selected_output == "鬼王":
            pass
        else:
            col1, col2, col3, col4, col5, col6, col7= st.columns(7)
            with col1:
                role_attribute_input(prefix,"真气")

    elif prefix == "昭冥":
        col1, col2, col3, col4, col5, col6, col7= st.columns(7)
        with col1:
            role_attribute_input(prefix,"气血")
        with col2:
            role_attribute_input(prefix,"真气")
        with col3:
            role_attribute_input(prefix,"最小攻击")
        with col4:
            role_attribute_input(prefix,"最大攻击")
        with col5:
            role_attribute_input(prefix,"防御")
        with col6:
            role_attribute_input(prefix,"爆伤")
        with col7:
            st.text('法宝技能是否+1')
            role_attribute_input(prefix,"技能_日月弘光")

    elif prefix == "青罗":
        col1, col2, col3, col4, col5, col6, col7= st.columns(7)
        with col1:
            role_attribute_input(prefix,"技能_研彻晓光")
        with col2:
            role_attribute_input(prefix,"技能_缓分花陌2")

    elif prefix == "焚香":
        # col1, col2, col3, col4, col5, col6, col7= st.columns(7)
        # with col1:
        #     role_attribute_input(prefix,"技能_祝融真典2")
        pass

    elif prefix == "青云":
        # col1, col2, col3, col4, col5, col6, col7= st.columns(7)
        # with col1:
        #     role_attribute_input(prefix,"技能_五气朝元")
        pass

    elif prefix == "百灵":
        col1, col2, col3, col4, col5, col6, col7= st.columns(7)
        with col1:
            st.text('法宝技能是否+1')
            role_attribute_input(prefix,"技能_灵雨续春")

    elif prefix == "英招":
        pass

    elif prefix == "九黎":
        pass

    else:        
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
        with col1:
            role_attribute_input(prefix,"气血")
            role_attribute_input(prefix,"1%气血比面板气血")#"分别记录更换气血比荧惑前后的面板气血，作差后除以该气血比荧惑的数值即为填写值"

        with col2:
            role_attribute_input(prefix,"真气")
            role_attribute_input(prefix,"1%真气比面板真气")

        with col3:
            role_attribute_input(prefix,"最小攻击")
            role_attribute_input(prefix,"1%攻击比面板攻击")

        with col4:
            role_attribute_input(prefix,"最大攻击")
            role_attribute_input(prefix,"1%防御比面板防御")

        with col5:
            role_attribute_input(prefix,"防御")
            if selected_output == "逐霜":
                role_attribute_input(prefix,"玄烛品质_云蒸霞蔚")
            elif selected_output == "惊岚":
                role_attribute_input(prefix,"赤乌品质_森罗削空斩")
            elif selected_output == "涅羽":
                role_attribute_input(prefix,"赤乌品质_大业浮屠")
            elif selected_output == "鬼王":
                role_attribute_input(prefix,"自身防御力")    
            elif selected_output == "太昊":
                role_attribute_input(prefix,"三代白虎_天罡正觉神")

        with col6:
            role_attribute_input(prefix,"爆伤")
            if selected_output == "鬼王":
                role_attribute_input(prefix,"玄烛品质_痴情咒")
            elif selected_output == "太昊":
                st.text('三代白虎技能系列')
                role_attribute_input(prefix,"技能_碧海系")
            elif selected_output == "涅羽":
                role_attribute_input(prefix,"玄烛品质_毒祭无常业")

        with col7:
            role_attribute_input(prefix,"对怪增伤")#"属性面板滚轮向下即可看到【对怪物增伤】"
            if selected_output == "鬼王":
                st.text('法宝技能是否+1')
                role_attribute_input(prefix,"技能_锐金咒")
            elif selected_output == "太昊":
                st.text('法宝技能是否+1')
                role_attribute_input(prefix,"技能_地煞狂灵形")

        with col8:
            role_attribute_input(prefix,"减爆伤", True)

        if selected_output in ["逐霜"]:
            st.text(f'心法技能')
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                role_attribute_input(prefix,"心法_乘时而化")
            with col2:
                role_attribute_input(prefix,"心法_太极_乘时而化")
            with col3:
                role_attribute_input(prefix,"心法_玄清_乘时而化")
            with col4:
                role_attribute_input(prefix,"心法_银鳞玄冰")
            with col5:
                role_attribute_input(prefix,"心法_般若_银鳞玄冰")         
            with col6:
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
    if attribute in ["气血", "真气"]:
        step = 10000  # 设置为1万
        min_value = 0
        max_value = 10000000
    elif attribute in ["爆伤"]:
        step = 0.1  # 设置为0.1
        min_value = 0.0
        max_value = 3000.0
    elif attribute in ["对怪增伤"]:
        step = 0.1  # 设置为0.1
        min_value = 0.0
        max_value = 30.0
    elif attribute in ["防御"]:
        # 当prefix为主输出，并且选择职业不为鬼王、惊岚时，防御默认设置为0
        
        step = 500  # 设置为500
        min_value = 0
        max_value = 500000
    elif attribute in ["最小攻击", "最大攻击"]:
        step = 500  # 设置为500
        min_value = 0
        max_value = 750000        
    elif attribute in ["1%攻击比面板攻击", "1%防御比面板防御"]:
        step = 10  # 10
        min_value = 0
        max_value = 500
        help = "通过装卸称号、荧惑、重华产生的属性变化来计算1%百分比对应的数值"
    elif attribute in ["自身防御力"]:
        step = 500  # 10
        min_value = 0
        max_value = 200000
        help = "切换到防御套后记录面板防御值，点击万法不侵或枯木咒后记录面版防御值，两者做差除以3或2.5就是自身防御力"
    elif attribute in ["1%气血比面板气血", "1%真气比面板真气"]:
        step = 100  # 100
        min_value = 0
        max_value = 10000
        help = "通过装卸称号、荧惑、重华产生的属性变化来计算1%百分比对应的数值"
    elif attribute in ["减爆伤"]:
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
        if prefix == "主输出":
            st.checkbox(
                    f"{attribute}",
                    value=st.session_state.my_attributes[f"{prefix}_{attribute}"], 
                    on_change = partial(update_checkbox_value, prefix, attribute, unique_key),
                    key=unique_key
                    )
        else:
            st.checkbox(
                    f"{attribute}",
                    value=st.session_state.roles_para[prefix][f"{prefix}_{attribute}"], 
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
    
    elif "三代" in attribute:
        if prefix == "主输出":
                st.selectbox(
                        f"{attribute}",
                        options=sandai_options, 
                        index=sandai_options.index(st.session_state.my_attributes[f"{prefix}_{attribute}"]), 
                        on_change = partial(update_selectbox_value,prefix, attribute, unique_key),
                        key=unique_key
                        )
        else:
                st.selectbox(
                        f"{attribute}",
                        options=sandai_options, 
                        index=sandai_options.index(st.session_state.roles_para[prefix][f"{prefix}_{attribute}"]), 
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
    
# 保存数据到CSV文件
def save_to_csv(my_attributes, labels):
    # 如果文件不存在，则创建新文件，并添加表头
    if not os.path.exists('data.csv'):
        df = pd.DataFrame(columns=['zhiye', 'qixue', 'zhenqi', 'low_gongji', 'up_gongji', 'defense', 'baoshang', 
                                   'duiguai', '1%_qixue', '1%_zhenqi', '1%_gongji', '1%_fangyu', 'zishen_defense', 'up_damage'])
        df.to_csv('data.csv', encoding='utf-8', index=False)

    # 提取主输出属性相关的特征和标签
    main_output_features = {
        'zhiye': my_attributes.get('主输出_职业', 0),
        'qixue': my_attributes.get('主输出_气血', 0),
        'zhenqi': my_attributes.get('主输出_真气', 0),
        'low_gongji': my_attributes.get('主输出_最小攻击', 0),
        'up_gongji': my_attributes.get('主输出_最大攻击', 0),
        'defense': my_attributes.get('主输出_防御', 0),
        'baoshang': my_attributes.get('主输出_爆伤', 0),
        'duiguai': my_attributes.get('主输出_对怪增伤', 0),
        '1%_qixue': my_attributes.get('主输出_1%气血比面板气血', 0),
        '1%_zhenqi': my_attributes.get('主输出_1%真气比面板真气', 0),
        '1%_gongji': my_attributes.get('主输出_1%攻击比面板攻击', 0),
        '1%_fangyu': my_attributes.get('主输出_1%防御比面板防御', 0),
        'zishen_defense': my_attributes.get('主输出_自身防御力', 0),
    }
    main_output_labels = labels  # 出爆最大伤害

    # 将新数据添加到文件末尾
    new_data = {**main_output_features, 'up_damage': main_output_labels}

    df = pd.DataFrame([new_data], columns=['zhiye', 'qixue', 'zhenqi', 'low_gongji', 'up_gongji', 'defense', 'baoshang', 
                                         'duiguai', '1%_qixue', '1%_zhenqi', '1%_gongji', '1%_fangyu', 'zishen_defense', 'up_damage'])
    df.to_csv('data.csv', mode='a', encoding='utf-8',index=False, header=False)

# 定义函数获取文件列表并按照修改时间排序
def get_sorted_file_list(folder_path):
    file_list = os.listdir(folder_path)
    file_list = [f for f in file_list if f.endswith(".yaml")]
    file_list = sorted(file_list, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
    return file_list