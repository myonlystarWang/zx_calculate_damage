# Hello.py
import streamlit as st
from damage_interface import render_setting_page
from damage_interface import render_attributes_page
from damage_interface import render_damage_calculation_page
from kongsang_interface import render_kongsang_page
from hello import render_hello_page
import streamlit_option_menu
from streamlit_option_menu import option_menu

initialized = False

my_attributes_default = {
    '主输出_职业': 0,
    '主输出_气血': 1500000,
    '主输出_真气': 1500000,
    '主输出_最小攻击': 120000,
    '主输出_最大攻击': 150000,
    '主输出_防御': 500000,
    '主输出_爆伤': 1600.0,
    '主输出_玄烛品质_云蒸霞蔚': '曦日',
    '主输出_赤乌品质_森罗削空斩': '曦日',
    '主输出_赤乌品质_大业浮屠': '曦日',
    '主输出_对怪增伤': 4.6,
    '主输出_减爆伤': 1000,
    '主输出_1%气血比面板气血': 2500,
    '主输出_1%真气比面板真气': 2500,
    '主输出_1%攻击比面板攻击': 100,
    '主输出_1%防御比面板防御': 100,
    '主输出_心法_乘时而化': True,
    '主输出_心法_太极_乘时而化': True,
    '主输出_心法_玄清_乘时而化': True,
    '主输出_心法_银鳞玄冰': False,
    '主输出_心法_般若_银鳞玄冰': False,
    '主输出_心法_幽录_银鳞玄冰': False,
    '主输出_技能_锐金咒': False,
    
}

boss_attributes_default = {'BOSS_气血': 10000000, 'BOSS_防御': 0, 'BOSS_减爆伤': 900, 'BOSS_厄运诅咒(绿点)': 900, 'BOSS_混乱诅咒': 120, 'BOSS_伤害压缩百分比': 0}

roles_para_default = {
    '天音': {'天音_真气': 2000000, '天音_技能_慈航法愿': True, '天音_最大攻击': 150000, '天音_玄烛品质_摩柯心经': '皓月'},
    '天华': {'天华_真气': 1800000, '天华_技能_金蛇狂舞': True, '天华_前世职业_凤求凰': '太昊', '天华_最大攻击': 150000, '天华_技能_秋声雅韵': True, '天华_技能_鸣泉雅韵': False},
    '昭冥': {'昭冥_气血': 1000000, '昭冥_真气': 1000000, '昭冥_防御': 0, '昭冥_技能_日月弘光': True, '昭冥_最小攻击': 0, '昭冥_最大攻击': 0, '昭冥_爆伤': 1500.0},
    '画影': {'画影_真气': 800000, '画影_技能_凌寒拂霜': True},
    '鬼王': {'鬼王_真气': 800000},
    '焚香': {'焚香_技能_祝融真典2': True},
    '青罗': {'青罗_技能_研彻晓光': True, '青罗_技能_缓分花陌2': True},
    '青云': {'青云_技能_五气朝元': True},
    '英招': {},#'英招_技能_天罡伏魔': True
    '九黎': {},#'九黎_技能_豪血': True, '九黎_技能_斗魂': True
    '百灵': {'百灵_技能_灵雨续春': False},

}

skill_para_default = {'苍龙玄_附加本体攻击百分比': 240, '苍龙玄_附加固定攻击值': 100, '苍龙玄_附加防御上限百分比': 0, '苍龙玄_附加气血上限百分比': 0, '苍龙玄_附加真气上限百分比': 48, '苍龙玄_附加爆伤': 48, '技能名称索引': 0, '技能名称': "苍龙玄"}

var_gains_para_default = {'九华淀魂曲': '4级', "八级雷煌闪": '4级', "三味真炎火": '4级', "雪琪的祈愿": 50, '副本赠送属性': '空桑兽神', "龙虎之力": '龙虎3','三碗不过岗': 20, '墨雪特效霜情': 20000, '情愫项链技能佳期': 10, '法宝融合爆伤': 0, '进阶家族技能等级(爆伤)': 0.0, '经典家族技能等级': "15阶", "星语拔山": 20}

selected_roles_default = ["天音", "天华", "昭冥", "画影", "鬼王", "焚香", "青罗", "青云", "英招", "九黎", "百灵"]

selected_gains_default = ["九华淀魂曲", "八级雷煌闪", "三味真炎火", "雪琪的祈愿", "副本赠送属性", "龙虎之力", "墨雪特效霜情", "三碗不过岗", "情愫项链技能佳期", "法宝融合爆伤", "进阶家族技能等级(爆伤)", "经典家族技能等级", "星语拔山"]

navi_option = ["🏠欢迎回来","🛠️伤害计算-参数设置","📝伤害计算-属性确认","💻伤害计算-结果模拟","📽️视频合集"]

def update_navi_selectbox():
    select_navi = st.session_state.get("sidebar_damage_select", None)
    st.session_state.current_page = select_navi

def initialize_session_state():
    global initialized
    if initialized == False :
        # 这里不能置None，必须给一个指定的值
        if "current_page" not in st.session_state:
            st.session_state.current_page = "🏠欢迎回来"
        if "damage_yi" not in st.session_state:
            st.session_state.damage_yi = 0
        if "damage_wan" not in st.session_state:
            st.session_state.damage_wan = 0           
        if "my_attributes" not in st.session_state:
            st.session_state.my_attributes = my_attributes_default
        if "boss_attributes" not in st.session_state:
            st.session_state.boss_attributes = boss_attributes_default
        if "selected_roles" not in st.session_state:
            st.session_state.selected_roles = selected_roles_default
        if "roles_para" not in st.session_state:
            st.session_state.roles_para = roles_para_default
        if "skill_para" not in st.session_state:
            st.session_state.skill_para = skill_para_default
        if "selected_gains" not in st.session_state:
            st.session_state.selected_gains = selected_gains_default
        if "var_gains_para" not in st.session_state:
            st.session_state.var_gains_para = var_gains_para_default
        if "my_gain_attributes" not in st.session_state:
            st.session_state.my_gain_attributes = None
        if "skill_gains_para" not in st.session_state:
            st.session_state.skill_gains_para = None
        if "real_damage" not in st.session_state:
            st.session_state.real_damage = None
        if "text_output" not in st.session_state:
            st.session_state.text_output = ""
        initialized = True

initialize_session_state()  # 确保 session_state 被初始化

st.set_page_config(
    page_title="萝卜的奇幻炼丹炉",
    layout="wide",
    initial_sidebar_state="auto"
)
# 隐藏右边的菜单以及页脚
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def main():
    # 自定义标题容器
    #st.title("诛仙3伤害计算")

    # with st.sidebar:
    #     selected = option_menu(
    #         menu_title = "诛仙3伤害计算",
    #         options = ["参数设置","属性确认","伤害计算"],
    #         icons = ["house","book","envelope"],
    #         menu_icon = "cast",
    #         default_index = 0,
    #     )    

    # if selected == "参数设置":
    #     render_setting_page()

    # elif selected == "属性确认":
    #     render_attributes_page()

    # elif selected == "伤害计算":
    #     render_damage_calculation_page()     

    # 为图片增加边框背景
    st.markdown("<style> img { border: 2px solid #333; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); } </style>", unsafe_allow_html=True)
    st.sidebar.image('./img/zhuxian_sidebar1.jpg', caption="⭐⭐萝卜的奇幻炼丹炉⭐⭐")#⚒️⚡🎉🎈💡✨📨💌👨‍💻⭕🧪🧙‍♂️🏅🚨🌀🔄ℹ️1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣❄️🦜️🔗🤷🏻🚀👈📊🔎🔍📸🚉🚚📋🌊🏠❔🧰⛏️⚒️🔧💳️📽️📹️💖❤️❌️⛔️🚫
    #st.markdown("<h1 style='text-align: left; background-color: #663399; color: #ffffff; padding: 10px;'>Step1: 参数设置</h1>", unsafe_allow_html=True)
    st.sidebar.markdown('---')

    # # 步骤导引
    # current_step = st.sidebar.radio("选择当前步骤", ["导入数据文件", "选择主输出职业", "选择组队职业", "设置BOSS属性", "选择输出技能", "选择可变增益项"])
    # 导航栏
    with st.sidebar:
        st.selectbox(
                    "**选择想看的页面👇**",
                    options=navi_option, 
                    key="sidebar_damage_select", 
                    on_change=update_navi_selectbox,
                    index=navi_option.index(st.session_state["current_page"])
                    )

    current_page = st.session_state["current_page"]

    if current_page == "🏠欢迎回来":
        render_hello_page()

    elif current_page == "🛠️伤害计算-参数设置":
        render_setting_page()

    elif current_page == "📝伤害计算-属性确认":
        render_attributes_page()

    elif current_page == "💻伤害计算-结果模拟":
        render_damage_calculation_page()

    elif current_page == "📽️视频合集":
        render_kongsang_page()

    st.sidebar.divider()
    st.sidebar.caption('有问题联系我：📧aben008@hotmail.com')
    st.sidebar.caption('🖼️ 萝卜 All Rights Reserved © 2024')
    #st.sidebar.markdown("---")
    #st.sidebar.markdown("<p class='copyright'>🖼️ 萝卜 All Rights Reserved © 2024</p>", unsafe_allow_html=True)
if __name__ == "__main__":
    main()
