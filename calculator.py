# calculator.py
import re
import streamlit as st

#定义乘数
bool_dict = {
    True: 1,
    False: 0,
}
qx_moke_dict = {
    "荧炬": 4,
    "皓月": 6,
    "曦日": 8
}
zz_cihang_dict = {
    True: 20,
    False: 18,
}
zz_qiusheng_dict = {
    True: 42,
    False: 35,
}
zz_jinshe_dict = {
    True: 20,
    False: 18,
}
zz_linghan_dict = {
    True: 27,
    False: 24,
}
zz_riyue_dict = {
    True: 60,
    False: 52.5,
}
gj_mingquan_dict = {
    True: 12,
    False: 10,
}
gj_zengsong_dict = {
    "无赠送": 0,
    "T16以上": 3500,
    "四象七": 2500,
    "空桑兽神": 4000
}
gj_sanwei_dict = {
    #"1级": 110,
    #"2级": 120,
    "3级": 3275,
    "4级": 4913
}
gj_longhu_dict = {
    "龙虎1": 100,
    "龙虎3": 100,
    "龙虎4": 800
}
fy_shangyishentong_dict = {
    "荧炬": 100,
    "皓月": 125,
    "曦日": 150
}
gjb_longhu_dict = {
    "龙虎1": 10,
    "龙虎3": 30,
    "龙虎4": 50
}
gjb_tiangang3_dict = {
    "1级": 1,
    "2级": 2,
    "3级": 3,
}
fy_longhu_dict = {
    "龙虎1": 5,
    "龙虎3": 100,
    "龙虎4": 800
}
fyb_longhu_dict = {
    "龙虎1": 5,
    "龙虎3": 20,
    "龙虎4": 50
}
fy_baji_dict = {
    #"1级": 110,
    #"2级": 120,
    "3级": 8275,
    "4级": 11000
}
fy_chiqing_dict = {
    "荧炬": 2,
    "皓月": 2.5,
    "曦日": 3
}
bs_fqh_dict = {
    "太昊": 150,
    "烈山": 130,
    "其他": 100
}
bs_jiuhua_dict = {
    #"1级": 110,
    #"2级": 120,
    "3级": 130,
    "4级": 140
}
bs_zengsong_dict = {
    "无赠送": 0,
    "T16以上": 65,
    "四象七": 50,
    "空桑兽神": 60
}
zq_yunzheng_dict = {
    "荧炬": 30,
    "皓月": 60,
    "曦日": 90
}

def roles_skill_gains_calculate(my_attributes, roles_para, var_gains_para):
    # 在这里进行各个技能增益属性计算
    skill_gains_para = {}

    #先遍历roles_para
    for role_para in roles_para:    
        if role_para == "天音":
            skill_gains_para["技能增益_专注_慈航法愿"] = zz_cihang_dict.get(roles_para[role_para].get("天音_技能_慈航法愿", False), 18)    
            skill_gains_para["技能增益_气血_摩柯心经"] = roles_para[role_para].get("天音_最大攻击", 0) * qx_moke_dict.get(roles_para[role_para].get("天音_玄烛品质_摩柯心经", '荧炬'), 4)  
            skill_gains_para["技能增益_防御_金刚不坏"] = roles_para[role_para].get("天音_真气", 0) * 0.15    
            skill_gains_para["技能增益_防御_金刚不坏2"] = roles_para[role_para].get("天音_真气", 0) * 0.1265    
            skill_gains_para["技能增益_气血比_大慈悲"] = round(10 * (1 + 0.12), 1)    

        elif role_para == "天华":
            skill_gains_para["技能增益_专注_秋声雅韵"] = zz_qiusheng_dict.get(roles_para[role_para].get("天华_技能_秋声雅韵", False), 35)   
            skill_gains_para["技能增益_防御_秋声雅韵"] = roles_para[role_para].get("天华_最大攻击", 0) * 1.5  
            skill_gains_para["技能增益_爆伤_秋声雅韵"] = 60 + roles_para[role_para].get("天华_真气", 0) / 100000  
            skill_gains_para["技能增益_专注_金蛇狂舞"] = zz_jinshe_dict.get(roles_para[role_para].get("天华_技能_金蛇狂舞", False), 18)     
            #skill_gains_para["技能增益_爆伤_金蛇狂舞"] = 60 
            skill_gains_para["技能增益_攻击比_金蛇狂舞"] = 40  
            skill_gains_para["技能增益_攻击比_鸣泉雅韵"] = 10 + 3 + 2 * bool_dict.get(roles_para[role_para].get("天华_技能_鸣泉雅韵", False), False) + roles_para[role_para].get("天华_真气", 0) / 50000                
            skill_gains_para["技能增益_爆伤_凤求凰"] = round(bs_fqh_dict.get(roles_para[role_para].get("天华_前世职业_凤求凰", 0), 100) + roles_para[role_para].get("天华_真气", 0) / 30000, 1) 
            skill_gains_para["技能增益_气血_云水雅韵2"] = roles_para[role_para].get("天华_最大攻击", 0) * 2.5  
            skill_gains_para["技能增益_真气_云水雅韵2"] = roles_para[role_para].get("天华_最大攻击", 0) * 5  
            skill_gains_para["技能增益_攻击_云水雅韵2"] = 10000 + 25 * roles_para[role_para].get("天华_真气", 0) / 1000  

        elif role_para == "青罗":
            skill_gains_para["技能增益_爆伤_研彻晓光"] = 200 * bool_dict.get(roles_para[role_para].get("青罗_技能_研彻晓光", False), False)
            skill_gains_para["技能增益_爆伤_缓分花陌2"] = 80 * bool_dict.get(roles_para[role_para].get("青罗_技能_缓分花陌2", False), False)

        elif role_para == "画影":
            skill_gains_para["技能增益_专注_凌寒拂霜"] = zz_linghan_dict.get(roles_para[role_para].get("画影_技能_凌寒拂霜", 0), 26) + roles_para[role_para].get("画影_真气", 0) / 400000  
            skill_gains_para["技能增益_攻击比_凌寒拂霜"] = 10  

        elif role_para == "焚香":
            skill_gains_para["技能增益_专注_祝融真典2"] = 22 * bool_dict.get(roles_para[role_para].get("焚香_技能_祝融真典2", False), False)

        elif role_para == "青云":
            skill_gains_para["技能增益_真气比_五气朝元"] = 56 * bool_dict.get(roles_para[role_para].get("青云_技能_五气朝元", False), False)

        elif role_para == "昭冥":
            skill_gains_para["技能增益_真气_附骨生灵2"] = 0.05 * roles_para[role_para].get("昭冥_真气", 0)
            skill_gains_para["技能增益_气血_附骨生灵2"] = 0.05 * roles_para[role_para].get("昭冥_气血", 0)
            skill_gains_para["技能增益_最小攻击_附骨生灵2"] = 0.05 * roles_para[role_para].get("昭冥_最小攻击", 0)
            skill_gains_para["技能增益_最大攻击_附骨生灵2"] = 0.05 * roles_para[role_para].get("昭冥_最大攻击", 0)
            skill_gains_para["技能增益_防御_附骨生灵2"] = 0.05 * roles_para[role_para].get("昭冥_防御", 0)
            skill_gains_para["技能增益_爆伤_附骨生灵2"] = 0.05 * roles_para[role_para].get("昭冥_爆伤", 0)
            skill_gains_para["技能增益_对怪_附骨生灵2"] = 5
            skill_gains_para["技能增益_专注_日月弘光"] = zz_riyue_dict.get(roles_para[role_para].get("昭冥_技能_日月弘光", False), 52.5)
            skill_gains_para["技能增益_巫咒_日月弘光"] = 22.5 

        elif role_para == "英招":
            skill_gains_para["技能增益_攻击比_天罡伏魔"] = 16 
            skill_gains_para["技能增益_防御比_五行八卦"] = 16 

        elif role_para == "百灵":
            skill_gains_para["技能增益_气血比_灵雨续春"] = 10 + 2 * roles_para[role_para].get("百灵_技能_灵雨续春", False)
            skill_gains_para["技能增益_攻击比_灵雨续春2"] = 20

        elif role_para == "九黎":
            skill_gains_para["技能增益_气血比_豪血"] = 10
            skill_gains_para["技能增益_攻击比_豪血"] = 17.5
            skill_gains_para["技能增益_爆伤_斗魂"] = 50

        elif role_para == "鬼王":
            skill_gains_para["技能增益_攻击比_天魔附体"] = 15 + 5 + round(roles_para[role_para].get("鬼王_真气", 0) / 50000, 1)

        else:
            pass

    return skill_gains_para
   
def all_skill_gains_calculate(my_attributes, skill_gains_para, var_gains_para):
    jiazu_value = var_gains_para.get("经典家族技能等级", "")
    if jiazu_value != "":
        number_str = jiazu_value.split('阶')[0]    
    number = 0  
    
    prof = my_attributes.get("主输出_职业", 0)
    #if prof == "逐霜":
    if prof == 0:
        if st.session_state.skill_para["技能名称"] == "苍龙玄":
            # 仙逐霜特有
            skill_gains_para["技能增益_专注_怒龙吞海2"] = 30 
            skill_gains_para["技能增益_爆伤_云蒸霞蔚2"] = 50
        elif st.session_state.skill_para["技能名称"] == "苍龙煞":
            # 魔逐霜特有
            #skill_gains_para["技能增益_真气比_造化技能空灵"] = 10 
            #skill_gains_para["技能增益_气血比_造化技能狂神"] = 10
            skill_gains_para["技能增益_气血比_霜池煞"] = 20

        skill_gains_para["技能增益_专注_怒龙吞海"] = 14 
        skill_gains_para["技能增益_专注_枕戈待旦"] = 20 
        skill_gains_para["技能增益_爆伤_枕戈待旦"] = 75
        skill_gains_para["技能增益_专注_乘时"] = 15 * bool_dict.get(my_attributes.get("主输出_心法_乘时而化", False), 0)
        skill_gains_para["技能增益_真气比_太极_乘时"] = 10 * bool_dict.get(my_attributes.get("主输出_心法_太极_乘时而化", False), 0)
        skill_gains_para["技能增益_真气比_云蒸霞蔚"] = zq_yunzheng_dict.get(my_attributes.get("主输出_玄烛品质_云蒸霞蔚", '荧炬'), 30)
        skill_gains_para["技能增益_攻击比_披霞揽星"] = 14 #20

    elif prof == 1:#"鬼王"
        skill_gains_para["技能增益_猛火咒3"] = 25 / 100
        skill_gains_para["技能增益_防御_厚土咒"] = 3600 
        skill_gains_para["技能增益_攻击系数_锐金咒"] = (100 + 20 * bool_dict.get(my_attributes.get("主输出_技能_锐金咒", False), 0)) / 100

        #这里的主输出_真气是御宝状态真气，需要换算为增益后的真气。注意选取的增益项
        #skill_gains_para.get("技能增益_真气_附骨生灵2", 0) + \
        all_zhenqi = my_attributes.get("主输出_真气", 0) + \
                                      skill_gains_para.get("技能增益_真气_云水雅韵2", 0) + \
                                      my_attributes.get("主输出_1%真气比面板真气", 0) * (number + skill_gains_para.get("技能增益_真气比_五气朝元", 0)) + \
                                      var_gains_para.get("墨雪特效霜情", 0) + \
                                      200 + number * 100

        skill_gains_para["技能增益_攻击比_天魔附体"] = 15 + 5 + round(all_zhenqi / 50000, 1)
        #skill_gains_para["技能增益_自身防御力"] = my_attributes.get("主输出_自身防御力", 0)
        skill_gains_para["技能增益_自身防御力_枯木咒"] = fy_chiqing_dict.get(my_attributes.get("主输出_玄烛品质_痴情咒", '荧炬'), 2.5)

    elif prof == 2:#"太昊"
        skill_gains_para["技能增益_爆伤_地煞神2"] = 50
        skill_gains_para["技能增益_爆伤_伏羲魂神通"] = 100
        skill_gains_para["技能增益_爆伤_天罡神3"] = 20
        skill_gains_para["技能增益_攻击比_地煞狂灵形"] = 100 + 20 * bool_dict.get(my_attributes.get("主输出_技能_地煞狂灵形", False), 0) + 30 
        skill_gains_para["技能增益_攻击比_天罡神3"] = (3 + 15) * gjb_tiangang3_dict.get(my_attributes.get("主输出_三代白虎_天罡正觉神", '2级'), 0) * bool_dict.get(my_attributes.get("主输出_技能_碧海系", False), 0)
        skill_gains_para["技能增益_气血比_地煞狂灵形"] = 150 + 30 * bool_dict.get(my_attributes.get("主输出_技能_地煞狂灵形", False), 0) + 60 

    elif prof == 3:#"惊岚"
        pass

    elif prof == 4:#"涅羽"
        #要先算出涅羽真气最大值        
        all_zhenqi = min((my_attributes.get("主输出_真气", 0) + \
                          skill_gains_para.get("技能增益_真气_云水雅韵2", 0) + \
                          skill_gains_para.get("技能增益_真气_附骨生灵2", 0) + \
                          my_attributes.get("主输出_1%真气比面板真气", 0) * (number + var_gains_para.get("星语拔山", 0) / 2 + skill_gains_para.get("技能增益_真气比_五气朝元", 0)) + \
                          var_gains_para.get("墨雪特效霜情", 0) + \
                          200 + number * 100), 4000000)
        print(all_zhenqi)
        skill_gains_para["技能增益_攻击_伤衣神通"] = int((all_zhenqi / 10000))*(350 + fy_shangyishentong_dict.get(my_attributes.get("主输出_玄烛品质_毒祭无常业", '荧炬'), 0))
        skill_gains_para["技能增益_专注_伤衣神通"] = 70

    else:
        pass

    # 其他类型增益在此添加
    skill_gains_para["技能增益_攻击比_龙虎1"] = 10 
    skill_gains_para["技能增益_防御比_龙虎1"] = 5
    skill_gains_para["技能增益_攻击_龙虎1"] = 100 
    skill_gains_para["技能增益_防御_龙虎1"] = 70
    skill_gains_para["技能增益_攻击比_龙虎之力"] = gjb_longhu_dict.get(var_gains_para.get("龙虎之力", 0), 0) 
    skill_gains_para["技能增益_防御比_龙虎之力"] = fyb_longhu_dict.get(var_gains_para.get("龙虎之力", 0), 0) 
    skill_gains_para["技能增益_攻击_龙虎之力"] = gj_longhu_dict.get(var_gains_para.get("龙虎之力", 0), 0)  
    skill_gains_para["技能增益_防御_龙虎之力"] = fy_longhu_dict.get(var_gains_para.get("龙虎之力", 0), 0)
    skill_gains_para["技能增益_攻击比_佛尊庇佑"] = 50 
    #skill_gains_para["技能增益_防御_佛尊庇佑"] = 1200 
    skill_gains_para["技能增益_攻击_天罡战意"] = 1071 
    skill_gains_para["技能增益_防御_佛尊庇佑2"] = 2520
    skill_gains_para["技能增益_自身防御_万法不侵"] = 300
    skill_gains_para["技能增益_攻击比_神力爆发"] = 20
    skill_gains_para["技能增益_防御_八级雷煌闪"] = fy_baji_dict.get(var_gains_para.get("八级雷煌闪", 0), 0) 
    skill_gains_para["技能增益_攻击_三味真炎火"] = gj_sanwei_dict.get(var_gains_para.get("三味真炎火", 0), 0) 
    skill_gains_para["技能增益_攻击比_星语拔山"] = var_gains_para.get("星语拔山", 0)
    skill_gains_para["技能增益_防御比_星语拔山"] = var_gains_para.get("星语拔山", 0)
    skill_gains_para["技能增益_气血比_星语拔山"] = var_gains_para.get("星语拔山", 0) / 2
    skill_gains_para["技能增益_真气比_星语拔山"] = var_gains_para.get("星语拔山", 0) / 2
    skill_gains_para["技能增益_攻击_副本赠送"] = gj_zengsong_dict.get(var_gains_para.get("副本赠送属性", 0), 0)
    skill_gains_para["技能增益_攻击比_家族技能"] = round((8 / 15) * number, 1)
    skill_gains_para["技能增益_攻击_家族技能"] = round(75 + 82 * (1 + 0.3),1) if number != 0 else 0
    skill_gains_para["技能增益_防御比_雪琪的祈愿"] = var_gains_para.get("雪琪的祈愿", 0)
    skill_gains_para["技能增益_爆伤_九华淀魂曲"] = bs_jiuhua_dict.get(var_gains_para.get("九华淀魂曲", 0), 0)
    skill_gains_para["技能增益_爆伤_副本赠送"] = bs_zengsong_dict.get(var_gains_para.get("副本赠送属性", 0), 0)
    skill_gains_para["技能增益_真气_墨雪特效霜情"] = var_gains_para.get("墨雪特效霜情", 0)
    skill_gains_para["技能增益_真气_家族技能"] = 200 + number * 100 if number != 0 else 0
    skill_gains_para["技能增益_真气比_家族技能"] = number
    skill_gains_para["技能增益_气血_家族技能"] = 200 + number * 100 if number != 0 else 0
    skill_gains_para["技能增益_气血比_家族技能"] = round((10 / 15) * number, 1)
    skill_gains_para["技能增益_爆伤_情愫技能佳期"] = var_gains_para.get("情愫项链技能佳期", 0)
    skill_gains_para["技能增益_爆伤_法宝融合爆伤"] = var_gains_para.get("法宝融合爆伤", 0)
    skill_gains_para["技能增益_爆伤_家族技能"] = var_gains_para.get("进阶家族技能等级", 0.0)

    return skill_gains_para

def my_gained_attribute_calculate(my_attributes, skill_gains_para, var_gains_para, skill_categories):
    #计算主C满增益属性
    my_gain_attributes = {}
    for key, value in my_attributes.items():
        # 根据不同名目进行赋值
        if  key == "主输出_爆伤":
            bs_sum = sum(skill_categories["爆伤"].values())
            new_value = min(value + bs_sum, 3000)
            
        elif key == "主输出_真气":
            zqb_sum = sum(skill_categories["真气比"].values())
            zq_sum = sum(skill_categories["真气"].values())
            new_value =  value + zq_sum + zqb_sum * my_attributes.get("主输出_1%真气比面板真气", 0)
            # 不是鬼王则需要限制真气
            if my_attributes.get("主输出_职业", 0) != 1:
                new_value = min(new_value, 4000000)
       
        elif "最大攻击" in key or "最小攻击" in key:          
            # 单独计算挂件大小攻击
            if "最大攻击" in key:
                zhaoming_gj = skill_gains_para.get("技能增益_最大攻击_附骨生灵2", 0)
            elif "最小攻击" in key:
                zhaoming_gj = skill_gains_para.get("技能增益_最小攻击_附骨生灵2", 0)

            # 攻击计算
            gjb_sum = sum(skill_categories["攻击比"].values())
            gj_sum = sum(skill_categories["攻击"].values()) + zhaoming_gj

            # 主输出是鬼王需要额外计算攻击
            if my_attributes.get("主输出_职业", 0) == 1:
                # 第一轮枯木前的最大攻击
                before1_kumu_gj = min(value + zhaoming_gj +\
                                skill_gains_para.get("技能增益_攻击_副本赠送", 0) + \
                                skill_gains_para.get("技能增益_攻击_龙虎1", 0) + \
                                skill_gains_para.get("技能增益_攻击_龙虎之力", 0) + \
                                skill_gains_para.get("技能增益_攻击_天罡战意", 0) + \
                                skill_gains_para.get("技能增益_攻击_家族技能", 0) + \
                                (skill_gains_para.get("技能增益_攻击比_金蛇狂舞", 0) + \
                                 skill_gains_para.get("技能增益_攻击比_鸣泉雅韵", 0) + \
                                 skill_gains_para.get("技能增益_攻击比_天魔附体", 0) + \
                                 skill_gains_para.get("技能增益_攻击比_天罡伏魔", 0) + \
                                 skill_gains_para.get("技能增益_攻击比_豪血", 0) + \
                                 skill_gains_para.get("技能增益_攻击比_灵雨续春2", 0) + \
                                 skill_gains_para.get("技能增益_攻击比_家族技能", 0) + \
                                 skill_gains_para.get("技能增益_攻击比_龙虎1", 0) + \
                                 skill_gains_para.get("技能增益_攻击比_龙虎之力", 0) 
                                ) * my_attributes.get("主输出_1%攻击比面板攻击", 0), 750000)
                print("before1_kumu_gj", before1_kumu_gj)

                # 第一轮枯木后的防御，枯木算的是自身防御的3倍，自身防御是所有吃百分比增益的防御固定值
                after1_kumu_fy = min(my_attributes.get("主输出_防御", 0) + \
                                skill_gains_para.get("技能增益_自身防御力_枯木咒", 0) * my_attributes.get("主输出_自身防御力", 0) + \
                                skill_gains_para.get("技能增益_防御_龙虎1", 0) + \
                                skill_gains_para.get("技能增益_防御_龙虎之力", 0) + \
                                (skill_gains_para.get("技能增益_防御比_龙虎1", 0) + \
                                 skill_gains_para.get("技能增益_防御比_龙虎之力", 0) + \
                                 skill_gains_para.get("技能增益_防御比_五行八卦", 0) + \
                                 skill_gains_para.get("技能增益_防御比_雪琪的祈愿", 0)
                                 ) * my_attributes.get("主输出_1%防御比面板防御", 0), 500000)
                print("after1_kumu_fy", after1_kumu_fy)

                # 第一轮锐金后的最大攻击
                after1_ruijin_gj = min(before1_kumu_gj + min(after1_kumu_fy, before1_kumu_gj * skill_gains_para.get("技能增益_攻击系数_锐金咒", 0)), 750000)
                print("after1_ruijin_gj", after1_ruijin_gj)
                
                # 第二轮枯木/万法后的满状态防御，筛选金刚护体1 2，秋声之间的最大值
                specific_skills = ["技能增益_防御_金刚不坏", "技能增益_防御_金刚不坏2", "技能增益_防御_秋声雅韵"]
                present_skills = [skill for skill in specific_skills if skill in skill_categories["防御"]]
                
                # 如果存在，找出最大值
                max_value = max([
                    skill_categories["防御"][skill] for skill in present_skills
                ]) if present_skills else 0

                # 计算总和，不包括其他特定的技能值，还需要加上枯木或万法的3倍自身防御增益
                fy_sum = sum([skill_value for skill, skill_value in skill_categories["防御"].items() if skill not in specific_skills]) + max_value + 3 * my_attributes.get("主输出_自身防御力", 0)
                fyb_sum = sum(skill_categories["防御比"].values())
                after2_kumu_fy = min(my_attributes.get("主输出_防御", 0) + fy_sum + fyb_sum * my_attributes.get("主输出_1%防御比面板防御", 0), 500000)
                print("after2_kumu_fy", after2_kumu_fy)

                # 第二轮枯木后锐金前的满状态最大攻击
                before2_ruijin_gj = min(value + sum(skill_categories["攻击"].values()) + sum(skill_categories["攻击比"].values()) * my_attributes.get("主输出_1%攻击比面板攻击", 0), 750000)
                print("before2_ruijin_gj", before2_ruijin_gj)

                # 第二轮枯木后锐金后的满状态最大攻击
                after2_ruijin_gj = min(before2_ruijin_gj + min(after2_kumu_fy, before2_ruijin_gj * skill_gains_para.get("技能增益_攻击系数_锐金咒", 0)), 750000)
                print("after2_ruijin_gj", after2_ruijin_gj)

                # 第二轮猛火后的满状态最大攻击
                after2_menghuo_gj = min(int(after2_ruijin_gj * (1 + skill_gains_para.get("技能增益_猛火咒3", 0))), 750000)
                print("after2_menghuo_gj", after2_menghuo_gj)
                new_value = after2_menghuo_gj

            else:
                new_value = min(value + gj_sum + gjb_sum * my_attributes.get("主输出_1%攻击比面板攻击", 0), 750000)

        elif key == "主输出_防御":
            # 筛选金刚护体1 2，秋声之间的最大值
            specific_skills = ["技能增益_防御_金刚不坏", "技能增益_防御_金刚不坏2", "技能增益_防御_秋声雅韵"]
            present_skills = [skill for skill in specific_skills if skill in skill_categories["防御"]]
            
            # 如果存在，找出最大值
            max_value = max([skill_categories["防御"][skill] for skill in present_skills]) if present_skills else 0

            # 计算总和，不包括其他特定的技能值，还需要加上枯木或万法的3倍自身防御增益
            fy_sum = sum([value for skill, value in skill_categories["防御"].items() if skill not in specific_skills]) + max_value + 3 * my_attributes.get("主输出_自身防御力", 0)
            fyb_sum = sum(skill_categories["防御比"].values())
            new_value = min(value + fy_sum + fyb_sum * my_attributes.get("主输出_1%防御比面板防御", 0), 500000)

        elif key == "主输出_气血":
            qxb_sum = sum(skill_categories["气血比"].values())
            qx_sum = sum(skill_categories["气血"].values())
            new_value = value + qx_sum + qxb_sum * my_attributes.get("主输出_1%气血比面板气血", 0)
            
            if my_attributes.get("主输出_职业", 0) != 1:
                new_value = min(new_value, 4000000)
        else:
            # 其他属性保持不变
            new_value = value
    
        # 将结果存储到新的字典中
        my_gain_attributes[key] = new_value
    return my_gain_attributes

def calculate_basic_damage(my_gain_attributes, boss_attributes, roles_para, skill_para, var_gains_para):
    # 在这里进行伤害计算
    basic_damage = {}

    for key, value in skill_para.items():
        if "本体攻击" in key:
            attack_coeff = (1 + round(value / 100, 6))
        elif "固定攻击" in key:
            attack_fixed = value
        elif "防御" in key:
            fangyu_coeff =  round(value / 100, 6)
        elif "气血" in key:
            qixue_coeff =  round(value / 100, 6)
        elif "真气" in key:
            zhenqi_coeff =  round(value / 100, 6)
        elif "爆伤" in key:
            skill_bs = value

    # 计算基础伤害
    attack_min = my_gain_attributes.get("主输出_最小攻击", 0) * attack_coeff + attack_fixed
    attack_max = my_gain_attributes.get("主输出_最大攻击", 0) * attack_coeff + attack_fixed

    fangyu = my_gain_attributes.get("主输出_防御", 0) * fangyu_coeff
    qixue = my_gain_attributes.get("主输出_气血", 0) * qixue_coeff
    zhenqi = my_gain_attributes.get("主输出_真气", 0) * zhenqi_coeff

    basic_damage["最小基础伤害"] = attack_min + fangyu + qixue + zhenqi - boss_attributes.get("BOSS_防御", 0) 
    basic_damage["最大基础伤害"] = attack_max + fangyu + qixue + zhenqi - boss_attributes.get("BOSS_防御", 0)

    return basic_damage, skill_bs