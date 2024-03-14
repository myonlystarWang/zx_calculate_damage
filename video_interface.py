import streamlit as st

def render_video_page():
    st.markdown("<h1 style='font-size: 40px; color: #333333; font-weight: bold; '>📽️ 视频合集</h1>", unsafe_allow_html=True) #text-align: center;

    st.subheader("💡 :blue[(原创)]六开空桑秒怪")
    st.markdown("**主演:** 星耀至尊-萝卜")
    st.markdown("**说明:** 鬼王搭配天音、天华、焚香、太昊、挂件，六开秒:red[空桑初]第三关黑心老人👇。")

    with st.expander("展开以查看视频"):   

        # 打开视频文件
        video_file = open('./video/6kongsang.mp4', 'rb')
        video_bytes = video_file.read()

        # 使用st.video函数播放视频
        st.video(video_bytes)

    st.subheader("💡 :blue[(转载)]英雄T15.5通关")
    st.markdown("**主演:** 幻月御风-暮雨潇湘【B站 刮痧归司南】")
    st.markdown("**说明:** 归云、涅羽、惊岚、天音、人马、释罗，:red[T15.5英雄本]一二关连过👇。")

    with st.expander("展开以查看视频"):   
        # 使用st.video函数播放视频
        #st.video("https://cn-jsnt-ct-01-24.bilivideo.com/upgcxcode/39/33/1230653339/1230653339-1-192.mp4?e=ig8euxZM2rNcNbNMhbdVhwdlhbKghwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1709184999&gen=playurlv2&os=bcache&oi=2043500563&trid=00006d535bb341604cd89f07739f5f6303f1T&mid=531653450&platform=html5&upsig=524bf3e3db8d9ba3e9ca1d4a6c1a2cdb&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&cdnid=9932&bvc=vod&nettype=0&bw=242994&orderid=0,1&buvid=&build=0&mobi_app=&f=T_0_0&logo=80000000")
        # 打开视频文件
        video_file = open('./video/yingxiong15.mp4', 'rb')
        video_bytes = video_file.read()

        # 使用st.video函数播放视频
        st.video(video_bytes)

    st.subheader("💡 :blue[(转载)]四象七通关-逐霜主C五保一")
    st.markdown("**主演:** 星耀至尊-柠檬水【B站 Rito】")
    st.markdown("**说明:** 仙逐霜带天音、天华、焚香、鬼道、挂件通关:red[四象七]👇。")

    with st.expander("展开以查看视频"):   
        # 使用st.video函数播放视频
        #st.video("https://upos-sz-mirror08c.bilivideo.com/upgcxcode/67/47/1073454767/1073454767-1-208.mp4?e=ig8euxZM2rNcNbhMnwdVhwdlhzK3hwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1709187721&gen=playurlv2&os=08cbv&oi=2043500563&trid=40d6ed5deb8141918d83581f342022b8T&mid=531653450&platform=html5&upsig=605989c4f963abc8e0a16b563d7f62cb&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&bw=348623&orderid=0,1&buvid=&build=0&mobi_app=&f=T_0_0&logo=80000000")
        # 打开视频文件
        video_file = open('./video/sixiang7.mp4', 'rb')
        video_bytes = video_file.read()

        # 使用st.video函数播放视频
        st.video(video_bytes)

    st.subheader("💡 :blue[(转载)]四象七通关-三输出平推")
    st.markdown("**主演:** 幻月御风-火箭【B站 刮痧归司南】")
    st.markdown("**说明:** 魔逐霜、涅羽、太昊带天音、焚香、青罗通关:red[四象七]👇。")

    with st.expander("展开以查看视频"):   
        # 使用st.video函数播放视频
        #st.video("https://upos-sz-mirror08c.bilivideo.com/upgcxcode/67/47/1073454767/1073454767-1-208.mp4?e=ig8euxZM2rNcNbhMnwdVhwdlhzK3hwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1709187721&gen=playurlv2&os=08cbv&oi=2043500563&trid=40d6ed5deb8141918d83581f342022b8T&mid=531653450&platform=html5&upsig=605989c4f963abc8e0a16b563d7f62cb&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&bvc=vod&nettype=0&bw=348623&orderid=0,1&buvid=&build=0&mobi_app=&f=T_0_0&logo=80000000")
        # 打开视频文件
        video_file = open('./video/sixiang7-2.mp4', 'rb')
        video_bytes = video_file.read()

        # 使用st.video函数播放视频
        st.video(video_bytes)
