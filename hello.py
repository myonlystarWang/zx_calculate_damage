import streamlit as st
import pandas as pd
from data import load_comments_data, save_comments_data
import datetime

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
    st.subheader("🚨 伤害计算使用说明")#💡

    st.markdown("伤害计算工具旨在帮助你逐步了解自己角色输出能力以及队伍角色辅助能力，你将可以获得：")
    st.markdown(
        """
    - 如何计算针对某个BOSS你自己的伤害输出范围
    - 如何调整自己的属性已达到伤害输出的最大收益
    - 如何搭配队友职业，帮助队友调整最适合副本的属性
    """
    )

    with st.expander("展开以查看使用说明"):   
        st.markdown(":red[注意：]初次进入网站使用伤害计算工具时，需要先进行参数设置。❌️不可直接点击结果模拟页面")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.image("./img/shuoming1.png",use_column_width=True,caption="在左侧导航栏中选择伤害计算-参数设置")#use_column_width=True,
        with col2:
            st.image("./img/shuoming2.png",use_column_width=True,caption="在左侧导航栏中选择伤害计算-参数设置")#
        st.markdown(":blue[其他图文说明待补充，请稍后......]")
        
        # col1, col2 = st.columns(2)
        # with col1:
        #     st.info("第一步：设置")

        #st.markdown("---")

    st.subheader("⛏️ 其他实用工具链接")#💡
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        with st.expander("BOSS属性"):
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=297828&highlight=BOSS%2B%E5%B1%9E%E6%80%A7", label=f":blue[T13-T15 BOSS属性表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=391769&highlight=%E6%80%AA%E7%89%A9%2B%E5%B1%9E%E6%80%A7", label=f":blue[劫起空桑BOSS属性表]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=115479&highlight=%E5%85%BD%E7%A5%9E%2B%E5%B1%9E%E6%80%A7", label=f":blue[兽神BOSS属性表]", icon=None, help=None, disabled=False, use_container_width=None)

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
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=88691&highlight=%E5%9B%9B%E4%BB%A3", label=f":blue[全职业四代技能效果汇总]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=387604&extra=page%3D1", label=f":blue[全职业三代技能效果汇总]", icon=None, help=None, disabled=False, use_container_width=None)
            st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=588740&highlight=%E5%BF%83%E6%B3%95", label=f":blue[全职业心法五代技能效果汇总]", icon=None, help=None, disabled=False, use_container_width=None)

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
            #st.page_link("https://bbs.wanmei.com/forum.php?mod=viewthread&tid=528855", label=f":blue[PVE辅助技能汇总]", icon=None, help=None, disabled=False, use_container_width=None)
    
    
    
    st.subheader("💌 仙炉灵草加注")#💡#捐赠支持
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
