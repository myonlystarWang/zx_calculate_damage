import streamlit as st
import pandas as pd
from data import load_comments_data, save_comments_data
import datetime

# 假设我们有以下图片列表
images = ["img/step1.png", "img/step2.png", "img/step3.png", "img/step4.png", "img/step5.png", "img/step6.png", "img/step7.png", "img/step8.png"]
captions = ["伤害计算入口", "设置主输出属性", "设置辅助职业属性", "设置BOSS属性&选择输出技能", "设置通用增益项", "确认主输出&各类增益属性", "伤害计算结果模拟", "模拟持续输出伤害"]
        
def prev_click():
    st.session_state.current_index = (st.session_state.current_index - 1) % len(images)

def next_click():
    st.session_state.current_index = (st.session_state.current_index + 1) % len(images)

def update_visit_count():
    # 文件路径
    file_path = 'visit_count.txt'

    # 读取当前访问次数
    try:
        with open(file_path, 'r') as file:
            visit_count = int(file.read())
    except FileNotFoundError:
        # 如果文件不存在，说明是第一次访问，初始化为0
        visit_count = 0

    # 更新访问次数
    visit_count += 1

    # 写入新的访问次数
    with open(file_path, 'w') as file:
        file.write(str(visit_count))

    return visit_count

# def jump_to_setting():
#     st.session_state["current_page"] = "🛠️伤害计算-参数设置"
#     st.rerun()

def render_hello_page():
    st.markdown("<h1 style='font-size: 48px; color: #333333; font-weight: bold; '>⭐⭐欢迎来到萝卜的奇幻炼丹炉⭐⭐</h1>", unsafe_allow_html=True) #text-align: center;
    # 在每个页面的 header 下调用该函数
    visit_count = update_visit_count()

    # 在页面渲染之前加载留言数据
    comments_data = load_comments_data()
    
    #st.caption(f'创建时间:   访问量:{visit_count}')
    #st.markdown(f"<span style='font-size:16px; color:#a9a9a9;'><b>📅 2023-02-29 16:00:00 </b> | <b> 🔍 {visit_count}</b></span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:16px; color:#a9a9a9;'><b>📅 2023-02-29 16:00:00</b>&nbsp;&nbsp; &nbsp;&nbsp; <b>🔍 {visit_count}</b></span>", unsafe_allow_html=True)

    st.markdown("在这个独特而充满创意的炼丹炉中，我将与你一同探索各种诛仙世界的瑰宝，你将发现关于诛仙3游戏玩法、工具、视频等等的炼丹秘籍，希望你能在这里找到有趣和有用的信息。")
    st.subheader("🚨 伤害计算")#💡

    st.markdown("伤害计算工具旨在帮助你逐步了解自己角色输出能力以及队伍角色辅助能力，你将可以获得：")
    st.markdown(
        """
    - 如何计算针对某个BOSS你自己的伤害输出范围
    - 如何调整自己的属性已达到伤害输出的最大收益
    - 如何搭配队友职业，帮助队友调整最适合副本的属性
    """
    )

    with st.expander("【使用说明】**:red[新手初次使用必看！！！]**"):   
        st.markdown("初次进入网站使用伤害计算工具时，需要先进行参数设置。❌️不可直接点击结果模拟页面")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.image("./img/shuoming1.png",use_column_width=True,caption="在左侧边页面中找到导航选项")#use_column_width=True,
        #with col2:
        #    st.image("./img/mobile_shuoming1.jpg",use_column_width=True,caption="手机打开网页时需要点击左上角小三角标志")#
        with col2:
            st.image("./img/shuoming2.png",use_column_width=True,caption="选择伤害计算-参数设置")#

        st.markdown("伤害计算具体使用方法如下：点击按钮查看下一张")


        col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12  = st.columns(12)
        with col6:
            st.button("⬅️上一张", key="left", on_click=prev_click, use_container_width=True)
        with col7:
            st.button("下一张➡️", key="right", on_click=next_click, use_container_width=True)
        # 显示当前图片
        st.image(images[st.session_state.current_index], caption=captions[st.session_state.current_index], use_column_width=True)

    with st.expander("【版本更新说明】"):   
        st.markdown("<h1 style='font-size: 28px; color: #333333; font-weight: bold; '>V1.1.6</h1>", unsafe_allow_html=True) #text-align: center;#📚
        st.caption('2024-03-27')
        st.markdown("**BUG修复：**")
        st.markdown("· 修复涅羽伤衣神通遗漏每10万真气兑换1%对怪伤害的问题")
        st.markdown("**敬请期待：**")
        st.markdown("· BOSS混乱诅咒根据选择的职业和队友职业自动计算")
        st.markdown("· 惊岚职业的技能伤害计算")
        st.markdown("· 从辅助职业御宝白状态计算其满状态攻击值、真气值")

        st.markdown("<h1 style='font-size: 28px; color: #333333; font-weight: bold; '>V1.1.5</h1>", unsafe_allow_html=True) #text-align: center;#📚
        st.caption('2024-03-25')
        st.markdown("**功能新增：**")
        st.markdown("· 增加【实用工具】中四象七、T16、多人塔怪物属性等链接")
        st.markdown("· 增加【视频合集】中涅羽五保一秒四象七视频")
        
        st.markdown("<h1 style='font-size: 28px; color: #333333; font-weight: bold; '>V1.1.4</h1>", unsafe_allow_html=True) #text-align: center;#📚
        st.caption('2024-03-19')
        st.markdown("**BUG修复：**")
        st.markdown("· 对配置文件下载时的列表显示进行时间倒序排序")
        st.markdown("· 修复保存配置文件时组队职业和通用技能未保存的BUG")
        
        st.markdown("<h1 style='font-size: 28px; color: #333333; font-weight: bold; '>V1.1.3</h1>", unsafe_allow_html=True) #text-align: center;#📚
        st.caption('2024-03-15')
        st.markdown("**BUG修复：**")
        st.markdown("· 修复配置文件保存、下载逻辑")
        
        st.markdown("<h1 style='font-size: 28px; color: #333333; font-weight: bold; '>V1.1.2</h1>", unsafe_allow_html=True) #text-align: center;#📚
        st.caption('2024-03-14')
        st.markdown("**功能新增：**")
        st.markdown("· 完善伤害计算使用说明配图")
        st.markdown("· 完成太昊、涅羽职业伤害计算测试")
        st.markdown("**BUG修复：**")
        st.markdown("· 由于B站外链失效，将视频播放从网络修改为本地")
        st.markdown("· 增加每一级计算时75w攻击50w防御、除人族外400w血蓝的限制")
        st.markdown("· 修正逐霜增益，区分仙逐霜和魔逐霜")
        st.markdown("· 暂时修改保存配置文件到服务器config目录")
        st.markdown("· 锁定技能附加数值，不能修改")

        st.markdown("<h1 style='font-size: 28px; color: #333333; font-weight: bold; '>V1.1.1</h1>", unsafe_allow_html=True) #text-align: center;#📚
        st.caption('2024-03-13')
        st.markdown("**功能新增：**")
        st.markdown("· 增加从主输出御宝白状态计算其满状态攻击值、气血值、防御值")
        st.markdown("**BUG修复：**")
        st.markdown("· 部分技能和增益计算有误，已修正")

        st.markdown("<h1 style='font-size: 28px; color: #333333; font-weight: bold; '>V1.1.0</h1>", unsafe_allow_html=True) #text-align: center;#📚
        st.caption('2024-03-02')
        st.markdown("**功能新增：**")
        st.markdown("· 添加辅助职业：英招、百灵、九黎、鬼王及其对应的技能")
        st.markdown("· 添加通用技能增益项：八级雷煌闪、三味真炎火、雪琪的祈愿、龙虎之力、星语拔山")
        st.markdown("**BUG修复：**")
        st.markdown("· 修改太昊、惊岚、涅羽技能附加伤害数值")
        st.markdown("· 修改通用增益项的增删逻辑BUG，该BUG会导致删除的通用增益项仍然生效")

        st.markdown("<h1 style='font-size: 28px; color: #333333; font-weight: bold; '>V1.0.0</h1>", unsafe_allow_html=True) #text-align: center;#📚
        st.caption('2024-02-29')
        st.markdown("**功能新增：**")
        st.markdown("· 初始创建")

    # 跳转按钮    
    if st.button("立即体验", key="jump_to_setting", type="primary"):#🔗
        st.session_state["current_page"] = "🛠️伤害计算-参数设置"
        st.rerun()

        # col1, col2 = st.columns(2)
        # with col1:
        #     st.info("第一步：设置")

        #st.markdown("---")

    st.subheader("⛏️ 实用工具")#💡
    st.markdown("这里搜罗了诛仙3各种实用属性、表格、攻略等，请随意查阅。")
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        with st.expander("BOSS属性"):
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=297828&highlight=BOSS%2B%E5%B1%9E%E6%80%A7", label=f":blue[T13-T15 BOSS属性表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=391769&highlight=%E6%80%AA%E7%89%A9%2B%E5%B1%9E%E6%80%A7", label=f":blue[劫起空桑BOSS属性表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=115479&highlight=%E5%85%BD%E7%A5%9E%2B%E5%B1%9E%E6%80%A7", label=f":blue[兽神BOSS属性表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=361182&highlight=%E5%A4%9A%E4%BA%BA%2B%E6%80%AA%E7%89%A9", label=f":blue[多人塔81-100层怪物属性表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=595735&extra=page%3D1", label=f":blue[四象七BOSS属性表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=595737&extra=page%3D1", label=f":blue[T16 BOSS属性表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=573423&highlight=%E6%B2%89%E6%B8%8A%2B%2B%E5%B1%9E%E6%80%A7", label=f":blue[沉渊之墟怪物属性表]", icon=None, help=None, disabled=False, use_container_width=None)

    with col2:
        with st.expander("装备相关"):
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=352263&extra=page%3D1", label=f":blue[宝石升品属性表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=88078", label=f":blue[圣粹佩章初始及成长属性表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=414789&highlight=%E6%96%B0%E4%BD%A9%E7%AB%A0", label=f":blue[新圣粹佩章隐藏属性表（含瑛）]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://tieba.baidu.com/photo/p?kw=%E8%AF%9B%E4%BB%99%E7%BD%91%E6%B8%B8&flux=1&tid=4126657273&pic_id=456974d98d1001e9d3efbf81be0e7bec56e79797&pn=1&fp=2&see_lz=1&red_tag=g2857778287", label=f":blue[天命装备天缘属性表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=278770", label=f":blue[神级首饰属性和效果汇总]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://www.bilibili.com/read/cv25087711/", label=f":blue[积分项链属性技能和升级方式]", icon=None, help=None, disabled=False, use_container_width=None)

    with col3:
        with st.expander("各类细节"):
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=88779", label=f":blue[普通轩辕策属性表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=89245", label=f":blue[阵灵和聚灵消耗一览表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=93166", label=f":blue[贺岁时装技能汇总]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=86074", label=f":blue[星宿系统星辰属性及升星增益表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://www.bilibili.com/read/cv25048840/", label=f":blue[经典&进阶家族技能满级效果]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=88691&highlight=%E5%9B%9B%E4%BB%A3", label=f":blue[全职业四代技能效果汇总]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=562866&highlight=%E4%B8%89%E4%BB%A3%E6%8A%80%E8%83%BD", label=f":blue[全职业三代技能效果汇总]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=588740&highlight=%E5%BF%83%E6%B3%95", label=f":blue[全职业心法五代技能效果汇总]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("http://bbs.wanmei.com/forum.php?mod=viewthread&tid=572441", label=f":blue[全职业飞升造化技能汇总]", icon=None, help=None, disabled=False, use_container_width=None)

    with col4:
        with st.expander("角色养成"):
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=296720&extra=page%3D3", label=f":blue[如何堆减免属性]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=259416&highlight=%E6%98%AD%E5%86%A5%2B%E9%80%A0", label=f":blue[辅助挂件打造方案]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=506324", label=f":blue[天华PVE&PVP科普]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=378188&highlight=%E5%87%8F%E6%9A%B4%E5%87%BB", label=f":blue[如何堆减暴击属性]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://mp.weixin.qq.com/s/jyMN43lgIevsZgkgt4uyYA", label=f":blue[如何堆减爆伤属性]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://mp.weixin.qq.com/s/K_416tmgwVwkDRG4j1b0AA", label=f":blue[如何堆攻击属性]", icon=None, help=None, disabled=False, use_container_width=None)

    with col5:
        with st.expander("杂七杂八"):
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=494732&highlight=%E7%BE%8A%E7%9A%AE%E7%BA%B8", label=f":blue[T10铁玉隐藏坐标图]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=474725&highlight=%E5%AE%B6%E6%97%8F%E6%8A%80%E8%83%BD", label=f":blue[家族技能升级消耗]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://gitmind.cn/app/docs/ms39vjmj", label=f":blue[元神轮回世界思维导图]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=88348", label=f":blue[人物传攻略汇总]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=583266&extra=page%3D1%26filter%3Dtypeid%26typeid%3D267", label=f":blue[魔化百罹分布图]", icon=None, help=None, disabled=False, use_container_width=None)
            #st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=528855", label=f":blue[PVE辅助技能汇总]", icon=None, help=None, disabled=False, use_container_width=None)
    
    st.subheader("📽️ 视频合集")
    st.markdown("各类原创或转载的诛仙3副本开荒、通关视频。")

    # 跳转按钮    
    if st.button("前往观看", key="jump_to_video", type="primary"):#🔗
        st.session_state["current_page"] = "📽️视频合集"
        st.rerun()

    st.subheader("💌 仙炉加注")#💡#捐赠支持
    with st.expander("作为一个免费、纯净无广告的网站，能得到大家的喜欢真的是意外又惊喜。由于维护也需要时间和精力。如果经济允许，可以赞助支持一下哦，感谢您的慷慨支持💖") :   
        col1,col2,col3,col4,col5,col6,col7,col8,col9,col10 = st.columns(10)

        with col1:
            # 显示微信支付二维码
            st.image("./img/wechat_zanshang_code.jpg", caption='微信')

        with col3:
            # 显示支付宝收款二维码
            st.image("./img/139_zhifubao_qr_code.jpg", caption='支付宝')

    st.subheader("💬 留言板")#💡✍🏼🗨️

    # 显示留言输入表单
    with st.form("留言表单"):
        nickname = st.text_input("昵称")
        contact_info = st.text_input("联系方式 (邮箱/微信/QQ)")
        message = st.text_area("留言内容", max_chars=500)
        # 使用 Chat API 创建一个简单的聊天窗口
        #reply = st.chat_input("回复内容:")            
        submit_button = st.form_submit_button("提交留言")

    # 如果表单被提交
    if submit_button:
        # 检查昵称和留言是否填写
        if not nickname: 
            st.error("请填写昵称!")
        elif not message:
            st.error("请填写留言内容!")
        elif nickname.isdigit() or not any(c.isalpha() for c in nickname):
            st.error("昵称不能为纯数字或纯符号")        
        else:
            # 获取当前时间
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 进行留言内容的屏蔽处理，可以根据需求定制
            censored_message = message.replace("操你", "*").replace("傻逼", "*")

            # 将留言添加到数据中
            new_comment = pd.DataFrame([{
                "时间": current_time,                
                "昵称": nickname,
                "联系方式": contact_info,
                "留言": censored_message,
                "回复": ""
            }])
            comments_data = pd.concat([comments_data, new_comment], ignore_index=True)

            # 保存留言数据
            save_comments_data(comments_data)

            # 显示留言
            #st.info(f"**{nickname}** 说：{censored_message}")
            st.info(f"留言成功")

            # 清空输入框
            #st.rerun()

    with st.expander(f"🗨️ 共有{len(comments_data)}条留言") :   
        for index, row in comments_data.iterrows():
            #st.write(f"**{row['昵称']}** 留言：{row['留言']}")
            #st.chat_message("user").write(f"**{row['昵称']}**\n{row['时间']}\n{row['留言']}")
            st.chat_message("user").write(f"{row['时间']} &nbsp;**{row['昵称']}**：{row['留言']}")

            if not pd.isna(row['回复']):
                st.chat_message("assistant").write(f"{row['回复']}")

            # # 显示回复表单
            # with st.form(f"回复_{index}"):
            #     reply = st.text_area("回复内容", max_chars=500)
            #     reply_button = st.form_submit_button("提交回复")

            # # 如果回复表单被提交
            # if reply_button:
            #     # 更新数据中的回复字段
            #     comments_data.at[index, "回复"] = reply
            #     # 保存留言数据
            #     save_comments_data(comments_data)
            #     # 显示回复
            #     st.write(f"**回复：** {reply}")
