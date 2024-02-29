# calculator.py
import re

#定义乘数
bool_dict = {
    True: 1,
    False: 0,
}
moke_dict = {
    "荧炬": 4,
    "皓月": 6,
    "曦日": 8
}
cihang_dict = {
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
bs_fqh_dict = {
    "太昊": 150,
    "烈山": 130,
    "其他": 100
}
yunzheng_dict = {
    "荧炬": 30,
    "皓月": 60,
    "曦日": 90
}
bs_jiuhua_dict = {
    "1级": 110,
    "2级": 120,
    "3级": 130,
    "4级": 140
}
bs_zengsong_dict = {
    "无赠送": 0,
    "T16以上": 65,
    "四象七": 50,
    "空桑兽神": 60
}

def skill_gains_calculate(my_attributes, roles_para):
    # 在这里进行各个技能增益属性计算
    skill_gains_para = {}

    #先遍历roles_para
    for role_para in roles_para:    
        if role_para == "天音":
            skill_gains_para["技能增益_专注_慈航法愿"] = cihang_dict.get(roles_para[role_para].get("天音_技能_慈航法愿", False), 18)    
            skill_gains_para["技能增益_气血_摩柯心经"] = roles_para[role_para].get("天音_最大攻击", 0) * moke_dict.get(roles_para[role_para].get("天音_玄烛品质_摩柯心经", 0), 4)  
            skill_gains_para["技能增益_防御_金刚不坏"] = roles_para[role_para].get("天音_真气", 0) * 0.15    
            skill_gains_para["技能增益_防御_金刚不坏2"] = roles_para[role_para].get("天音_真气", 0) * 0.1265    

        elif role_para == "天华":
            skill_gains_para["技能增益_专注_秋声雅韵"] = zz_qiusheng_dict.get(roles_para[role_para].get("天华_技能_秋声雅韵", False), 35)   
            skill_gains_para["技能增益_防御_秋声雅韵"] = roles_para[role_para].get("天华_最大攻击", 0) * 1.5  
            skill_gains_para["技能增益_爆伤_秋声雅韵"] = 60 + roles_para[role_para].get("天华_真气", 0) / 100000  
            skill_gains_para["技能增益_专注_金蛇狂舞"] = zz_jinshe_dict.get(roles_para[role_para].get("天华_技能_金蛇狂舞", False), 18)     
            skill_gains_para["技能增益_爆伤_金蛇狂舞"] = 60 * bool_dict.get(roles_para[role_para].get("天华_技能_金蛇狂舞", False), False)  
            skill_gains_para["技能增益_爆伤_凤求凰"] = round(bs_fqh_dict.get(roles_para[role_para].get("天华_前世职业_凤求凰", 0), 100) + roles_para[role_para].get("天华_真气", 0) / 30000, 2) 
            skill_gains_para["技能增益_气血_云水雅韵2"] = roles_para[role_para].get("天华_最大攻击", 0) * 2.5  
            skill_gains_para["技能增益_真气_云水雅韵2"] = roles_para[role_para].get("天华_最大攻击", 0) * 5  

        elif role_para == "青罗":
            skill_gains_para["技能增益_爆伤_研彻晓光"] = 200 * bool_dict.get(roles_para[role_para].get("青罗_技能_研彻晓光", False), False)
            skill_gains_para["技能增益_爆伤_缓分花陌2"] = 80 * bool_dict.get(roles_para[role_para].get("青罗_技能_缓分花陌2", False), False)

        elif role_para == "画影":
            skill_gains_para["技能增益_专注_凌寒拂霜"] = zz_linghan_dict.get(roles_para[role_para].get("画影_技能_凌寒拂霜", 0), 26) + roles_para[role_para].get("画影_真气", 0) / 400000  

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

        else:
            pass

    prof = my_attributes.get("主输出_职业", 0)
    #if prof == "逐霜":
    if prof == 0:
        skill_gains_para["技能增益_专注_清啸"] = 44 
        skill_gains_para["技能增益_专注_枕戈待旦"] = 20 
        skill_gains_para["技能增益_爆伤_枕戈待旦"] = 75
        skill_gains_para["技能增益_爆伤_云蒸霞蔚2"] = 50
        skill_gains_para["技能增益_专注_乘时"] = 15 * bool_dict.get(my_attributes.get("主输出_心法_乘时而化", False), 0)
        skill_gains_para["技能增益_真气比_太极_乘时"] = 10 * bool_dict.get(my_attributes.get("主输出_心法_太极_乘时而化", False), 0)
        skill_gains_para["技能增益_真气比_云蒸霞蔚"] = yunzheng_dict.get(my_attributes.get("主输出_玄烛品质_云蒸霞蔚", 30), 30)

    elif prof == "鬼王":
        pass

    return skill_gains_para
   
def my_gained_attribute_calculate(my_attributes, skill_gains_para, var_gains_para):
    #计算主C满增益属性
    my_gain_attributes = {}
    
    for key, value in my_attributes.items():
        # 根据不同名目进行赋值
        if  key == "主输出_爆伤":
            # print("原始爆伤", value)
            # print("法宝融合爆伤", var_gains_para.get("法宝融合爆伤", 0) )
            # print("九华奠魂曲", bs_jiuhua_dict.get(var_gains_para.get("九华奠魂曲", 0), 0) )
            # print("进阶家族技能等级(爆伤)", var_gains_para.get("进阶家族技能等级(爆伤)", 0.0))
            # print("副本赠送爆伤", bs_zengsong_dict.get(var_gains_para.get("副本赠送爆伤", 0), 0))
            # print("情愫项链技能佳期", var_gains_para.get("情愫项链技能佳期", 0))
            # print("技能增益_爆伤_附骨生灵2", skill_gains_para.get("技能增益_爆伤_附骨生灵2", 0))
            # print("技能增益_爆伤_凤求凰", skill_gains_para.get("技能增益_爆伤_凤求凰", 0))
            # print("技能增益_爆伤_秋声雅韵", skill_gains_para.get("技能增益_爆伤_秋声雅韵", 0))
            # print("技能增益_爆伤_研彻晓光", skill_gains_para.get("技能增益_爆伤_研彻晓光", 0))
            # print("技能增益_爆伤_缓分花陌2", skill_gains_para.get("技能增益_爆伤_缓分花陌2", 0))
            # print("技能增益_爆伤_枕戈待旦", skill_gains_para.get("技能增益_爆伤_枕戈待旦", 0))
            # print("技能增益_爆伤_云蒸霞蔚2", skill_gains_para.get("技能增益_爆伤_云蒸霞蔚2", 0))
            new_value = value + \
                        var_gains_para.get("法宝融合爆伤", 0) + \
                        bs_jiuhua_dict.get(var_gains_para.get("九华奠魂曲", 0), 0) + \
                        var_gains_para.get("进阶家族技能等级(爆伤)", 0.0) + \
                        bs_zengsong_dict.get(var_gains_para.get("副本赠送爆伤", 0), 0) + \
                        var_gains_para.get("情愫项链技能佳期", 0) + \
                        skill_gains_para.get("技能增益_爆伤_附骨生灵2", 0) + \
                        skill_gains_para.get("技能增益_爆伤_凤求凰", 0) + \
                        skill_gains_para.get("技能增益_爆伤_秋声雅韵", 0) + \
                        skill_gains_para.get("技能增益_爆伤_研彻晓光", 0) + \
                        skill_gains_para.get("技能增益_爆伤_缓分花陌2", 0) + \
                        skill_gains_para.get("技能增益_爆伤_枕戈待旦", 0) + \
                        skill_gains_para.get("技能增益_爆伤_云蒸霞蔚2", 0)
            # print("new_value", new_value)
            
            if new_value > 3000:
                new_value = 3000

        elif key == "主输出_真气":
            jiazu_value = var_gains_para.get("经典家族技能等级", 0)
            number_str = jiazu_value.split('阶')[0]
            number = int(number_str)
            new_value = value + \
                        skill_gains_para.get("技能增益_真气_附骨生灵2", 0) + \
                        skill_gains_para.get("技能增益_真气_云水雅韵2", 0) + \
                        my_attributes.get("主输出_1%真气比面板真气", 0) * (number + skill_gains_para.get("技能增益_真气比_云蒸霞蔚", 0) + skill_gains_para.get("技能增益_真气比_太极_乘时", 0) + skill_gains_para.get("技能增益_真气比_五气朝元", 0)) + \
                        var_gains_para.get("墨雪特效霜情", 0) + \
                        200 + number * 100
            if my_attributes.get("主输出_职业", None) is not None and my_attributes.get("主输出_职业", None) != "鬼王":
                if new_value > 4000000:
                    new_value = 4000000
                
        elif "最大攻击" in key:
            new_value = value
            if new_value > 750000:
                new_value = 750000
        elif "最小攻击" in key:
            new_value = value
            if new_value > 750000:
                new_value = 750000
        elif key == "主输出_防御":
            new_value = value
            if new_value > 500000:
                new_value = 500000
        elif key == "主输出_气血":
            new_value = value
            if my_attributes.get("主输出_职业", None) is not None and my_attributes.get("主输出_职业", None) != "鬼王":
                if new_value > 4000000:
                    new_value = 4000000
        #     new_value = value + \
        #                 skill_gains_para.get("技能增益_气血_附骨生灵2", 0) + \
        #                 max(skill_gains_para.get("技能增益_气血_摩柯心经", 0), skill_gains_para.get("技能增益_气血_云水雅韵2", 0)) + \
        #                 skill_gains_para.get("主输出_1%气血比面板气血", 0) * (var_gains_para.get("经典家族技能等级", 0) + 0) + \
        #                 200 + var_gains_para.get("经典家族技能等级", 0) * 100
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

    attack_min = my_gain_attributes.get("主输出_最小攻击", 0) * attack_coeff + attack_fixed
    attack_max = my_gain_attributes.get("主输出_最大攻击", 0) * attack_coeff + attack_fixed

    fangyu = my_gain_attributes.get("主输出_防御", 0) * fangyu_coeff
    qixue = my_gain_attributes.get("主输出_气血", 0) * qixue_coeff
    zhenqi = my_gain_attributes.get("主输出_真气", 0) * zhenqi_coeff

    basic_damage["最小基础伤害"] = attack_min + fangyu + qixue + zhenqi - boss_attributes.get("BOSS_防御", 0) 
    basic_damage["最大基础伤害"] = attack_max + fangyu + qixue + zhenqi - boss_attributes.get("BOSS_防御", 0)

    return basic_damage, skill_bs