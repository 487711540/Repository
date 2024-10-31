from time import sleep
from math import *
from flask import render_template, request, redirect, url_for, Blueprint, jsonify, make_response
from sqlalchemy import null
from sqlalchemy.testing.suite.test_reflection import users
import random
from exts import *
from models import User, Food, Favorite, Rating, FoodFlavorAssociation, Flavor, Comment, FlavorPreference

bp = Blueprint('user', __name__, url_prefix='/')


@bp.route('/')
def Index():
    return "首页"


# 登录
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 用户名或密码未输入
        if username == "" or password == "":
            return jsonify({'code': 200, 'msg': '未输入用户名或密码'})
        users = User.query.filter_by(username=username).first()
        # 用户名不存在
        if users is None:
            return jsonify({'code': 200, 'msg': '用户名错误'})

        if username == users.username and password == users.password:
            # 设置cookie （未完成）
            response = make_response(jsonify({'code': 200, 'msg': '登录成功', 'username':username}))
            response.set_cookie('username', username, max_age=3600 * 24 * 7)
            return response
        else:
            return jsonify({'code': 200, 'msg': '密码错误'})
    else:
        return jsonify({'code': 200, 'msg': '进入登录界面'})


# 注册
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form.get('username') == "" or request.form.get('password') == "":
            return jsonify({'code': 200, 'msg': '未输入用户名或密码'})

        users = User.query.filter_by(username=request.form['username']).first()
        # users存在时
        if users:
            return jsonify({'code': 200, 'msg': '用户名已被注册'})
        else:
            # 不存在将写进数据库
            new_user = User(username=request.form['username'], password=request.form['password'])
            db.session.add(new_user)
            db.session.commit()
            response = make_response(jsonify({'code': 200, 'msg': '注册成功'}))
            response.set_cookie('username', new_user.username, max_age=3600 * 24 * 7)
            return response
    else:
        return jsonify({'code': 200, 'msg': "刷新了页面"})


# 个人主页(展示用户收藏页面)
@bp.route('/selectfavorites', methods=['GET'])
def personal():

        users = User.query.filter_by(username=request.args.get('username')).first()
        # 创建用于存放收藏的食物名称和类型
        foods = []

        for favorite in users.favorites:
            food = Food.query.filter_by(id=favorite.food_id).first()
            # 查询食物口味所属表
            # for food_flavor_associations in food.food_flavor_association:
            #     # 根据food_flavor_associations.flavor_id找到口味所属的类型
            #     types = Flavor.query.filter_by(id=food_flavor_associations.flavor_id).first()
            #     food_name_types = [food.name,food.big_type,types.flavor_type]
            #     # 将收藏的食物名称和类型放入列表
            #     foods.append(food_name_types)
            food_name_types = [food.name, food.big_type]
            foods.append(food_name_types)

        return jsonify({'code': 200, 'msg': '成功', 'data': foods})


# 注销
@bp.route('/logout', methods=['GET'])
def logout():
    cookies = request.cookies
    if cookies.get('username'):
        response = make_response({'code': 200, 'msg': '注销成功'})
        # 删除cookies
        response.delete_cookie('username')
        # response = redirect('/login')
        return response
    else:
        return jsonify({'code': 200, 'msg': '失败'})
        # return redirect('/login')




# 注册时选择喜好
@bp.route('/choose', methods=['POST'])
def choose():

    users = User.query.filter_by(username=request.form.get('username')).first()
    if 1:

        if len(list(users.flavor_preferences)) != 0:

            return jsonify({'code': 200, 'msg': '失败'})
        food = []
        for requests in request.form.getlist('tags'):
            # 根据传来的tags查询小类标签
            flavors = Flavor.query.filter_by(flavor_type=requests).first()
            # 根据小类标签id查询食物对应的小类标签（食物风味）
            food_flavor_associations = FoodFlavorAssociation.query.filter_by(flavor_id=flavors.id).all()
            # 根据小类标签查询所有满足条件食物
            for food_flavor_association in food_flavor_associations:
                foods = Food.query.filter_by(id=food_flavor_association.food_id).first()
                food_name_image=[foods.name,foods.image]

                food.append(food_name_image)
            # 将用户和喜好的口味做关联
            flavor_preferences = FlavorPreference(flavor_id = flavors.id, user_id=users.id)
            db.session.add(flavor_preferences)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '成功', 'data': food})
    else:
        return jsonify({'code': 200, 'msg': '失败'})



# 进行收藏
@bp.route('/favorites', methods=['POST'])
def collection():

    if 1:
        users = User.query.filter_by(username=request.form.get('username')).first()
        foods = Food.query.filter_by(name=request.form.get('dishname')).first()
        # 检查是否重复收藏
        for favorite in users.favorites:
            food = Food.query.filter_by(id=favorite.food_id).first()
            if food.name == request.form.get('dishname'):
                return jsonify({'code': 200, 'msg': '您已经收藏过了'})

        # 添加user.id food.id
        favorites = Favorite(user_id=users.id, food_id=foods.id)
        db.session.add(favorites)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '收藏成功'})
    else:
        return jsonify({'code': 200, 'msg': '错误'})


# 取消收藏
@bp.route('/delete_favorites', methods=['POST'])
def delete_favorites():

    if 1:
        users = User.query.filter_by(username=request.form.get('username')).first()
        # 查询用户收藏表
        for favorite in users.favorites:
            food = Food.query.filter_by(id=favorite.food_id).first()
            if food.name == request.form.get('dishname'):
                db.session.delete(favorite)
                db.session.commit()
                return jsonify({'code': 200, 'msg': '删除成功'})
        return jsonify({'code': 200, 'msg': '您没有收藏该食物'})
    else:
        return jsonify({'code': 200, 'msg': '错误'})





@bp.route('/rate', methods=['POST'])
def rate_view():
    # 验证评分范围
    if request.form['score'] == '' or float(request.form['score']) > 5 or float(request.form['score']) < 0:
        return jsonify({'code': 400, 'msg': '请输入评分0-5之间的评分'})  # 修改返回代码为400表示请求错误

    users = User.query.filter_by(username=request.form.get('username')).first()
    foods = Food.query.filter_by(name=request.form['dishname']).first()

    # 查找用户的评分记录
    existing_rating = Rating.query.filter_by(user_id=users.id, food_id=foods.id).first()

    if existing_rating:
        # 更新评分
        existing_rating.score = request.form['score']
    else:
        # 添加新评分
        existing_rating = Rating(user_id=users.id, food_id=foods.id, score=request.form['score'])
        db.session.add(existing_rating)

    db.session.commit()

    # 计算食物的平均分
    account = sum(rating.score for rating in foods.ratings)  # 使用评分的总和
    total_ratings = Rating.query.filter_by(food_id=foods.id).count()  # 获取评分数量
    average_score = account / total_ratings if total_ratings > 0 else 0  # 防止除以零
    foods.average_score = average_score
    db.session.commit()

    return jsonify({'code': 200, 'msg': '成功'})



# 修改密码
@bp.route('/change', methods=['POST'])
def change():

    if request.form.get('username') == "" or request.form.get('password') == "" :
        return jsonify({'code': 200, 'msg': '未输入密码或出现错误'})
    if 1:
        users = User.query.filter_by(username=request.form['username']).first()
        users.password = request.form['password']
        db.session.commit()
        return jsonify({'code': 200, 'msg': "修改成功"})
    else:
        return jsonify({'code': 200, 'msg': "修改失败"})


# 协同过滤推荐 个性化推荐
@bp.route('/recommend', methods=['get'])
def recommend():
    users = User.query.filter_by(username=request.args.get('username')).first()
    # 如果用户没有评过分
    if list(users.ratings) is not None:
        random_integer11 = random.randint(1, 2337)
        random_integer21 = random.randint(1, 2337)
        food01 = Food.query.filter_by(id=random_integer11).first()
        food11 = Food.query.filter_by(id=random_integer21).first()
        food21 = Food.query.filter_by(name='奶油夹心马卡龙').first()
        food31 = Food.query.filter_by(name='辣子鸡丁').first()
        foods_all1 = [[food01.name, food01.image], [food11.name, food11.image], [food21.name, food21.image],
                     [food31.name, food31.image]]
        return jsonify({'code': 200, 'msg': '成功', 'data': foods_all1})


    ratings = Rating.query.all()
    rating_list = []
    for rating in ratings:
        list1 = [rating.user_id, rating.food_id, rating.score]
        rating_list.append(list1)

    # 创建一个空字典来存储分类后的结果
    data = {}

    # 遍历原始列表
    for sublist in rating_list:
        # 获取第一位数字作为主键
        key1 = sublist[0]
        # 获取第二位数字作为次键，第三位数字作为值
        key2 = sublist[1]
        value = sublist[2]

        # 如果主键不存在于字典中，则创建一个新字典作为值
        if key1 not in data:
            data[key1] = {}

            # 将次键和值添加到对应主键的字典中
        data[key1][key2] = value

    # print(data)

    def Euclid(user1: int, user2: int):
        # 取出两位用户打过分的食物和评分
        user1_data = data[user1]
        user2_data = data[user2]
        distance = 0
        # 找到两位用户都打过分的食物，并计算欧式距离
        for key in user1_data.keys():
            if key in user2_data.keys():
                # 注意，distance越大表示两者越相似
                distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)

        return 1 / (1 + sqrt(distance))  # 这里返回值越小，相似度越大

    # 计算某个用户与其他用户的相似度
    def top_similar(user_id):
        res = []
        for userid in data.keys():
            # 排除与自己计算相似度
            if not userid == user_id:
                similar = Euclid(user_id, userid)
                res.append((userid, similar))
        res.sort(key=lambda val: val[1])
        # print(res)
        return res

    def recommend(user):
        # 相似度最高的用户
        top_sim_user = top_similar(user)[0][0]
        # 相似度最高的用户评分记录

        items = data[top_sim_user]
        # print(items)
        recommendations = []
        # 筛选出该用户未评分的食物并添加到列表中
        for item in items.keys():
            if item not in data[user].keys():
                recommendations.append((item, items[item]))
        recommendations.sort(key=lambda val: val[1], reverse=True)  # 按照评分排序

        return recommendations


    food_all = []


    if recommend(users.id):
        for food_id in recommend(users.id):
            foods = Food.query.filter_by(id=food_id[0]).first()
            food_name_image = [foods.name, foods.image]
            food_all.append(food_name_image)
        # print(food_all)
        return jsonify({'code': 200, 'msg': '成功', 'data': food_all})
    else:
        random_integer1 = random.randint(1, 2337)
        random_integer2 = random.randint(1, 2337)
        food0 = Food.query.filter_by(id=random_integer1).first()
        food1 = Food.query.filter_by(id=random_integer2).first()
        food2 = Food.query.filter_by(name='奶油夹心马卡龙').first()
        food3 = Food.query.filter_by(name='辣子鸡丁').first()
        foods_all =[[food0.name, food0.image], [food1.name, food1.image], [food2.name, food2.image], [food3.name, food3.image]]
        return jsonify({'code': 200, 'msg': '成功', 'data': foods_all})





# ————————————————————————————————————————————————————————
# ————————————————————————————————————————————————————————

# 排行榜
@bp.route('/sort', methods=['POST'])
def sort():
    bigtype = request.form.get('bigtype')
    smalltype = request.form.get('smalltype')

    # 基于大类过滤菜品
    query = Food.query
    if bigtype:
        query = query.filter_by(big_type=bigtype)

    # 如果传入了小类，通过联表查询food_flavor和flavor进行过滤
    if smalltype:
        query = query.join(FoodFlavorAssociation, Food.id == FoodFlavorAssociation.food_id) \
                     .join(Flavor, FoodFlavorAssociation.flavor_id == Flavor.id) \
                     .filter(Flavor.flavor_type == smalltype)

    # 按评分从高到低排序，并限制结果为前10个
    sorted_foods = query.order_by(Food.average_score.desc()).limit(10).all()

    # 构建返回的列表
    sort_list = []
    for f in sorted_foods:
        food_item = {
            "name": f.name,
            "average_score": f.average_score
        }
        sort_list.append(food_item)

    return jsonify({'code': 200, 'msg': "成功", "data": sort_list})




# 获取菜品信息
@bp.route('/info', methods=['POST'])
def info():
    dishname = request.form.get('dishname')

    if not dishname:
        return jsonify({'code': 400, 'msg': "菜品名称未提供", 'data': {}})

    print(dishname)
    try:
        food = Food.query.filter_by(name=dishname).first()

        print(food)
        if not food:
            return jsonify({'code': 404, 'msg': "菜品不存在", 'data': {}})

        img = food.image
        desc = food.description
        score = food.average_score
        bigtype = food.big_type

        return jsonify(
            {'code': 200, 'msg': "成功", 'data': {'dishname': dishname, 'img': img, 'desc': desc, 'score': score, 'bigtype': bigtype}})

    except Exception as e:
        return jsonify({'code': 500, 'msg': f"服务器错误: {str(e)}", 'data': {}})

# 返回食物的大小类
@bp.route('/classes', methods=['GET'])
def classes():
    categories = {
        "按菜品口味": ['超辣', '葱香', '怪味', '果味', '酱香', '咖喱', '苦味', '麻辣', '麻香', '奶香', '清淡',
                       '酸辣', '酸甜', '酸咸', '蒜香', '甜辣', '甜味', '甜香', '微辣', '五香', '咸甜', '咸鲜', '咸香',
                       '香草', '香辣', '鱼香', '原味', '糟香', '中辣', '孜然'],
        "按所需时间": ['半小时', '廿分钟', '三刻钟', '十分钟', '数天', '数小时', '一天', '一小时'],
        "按制作难度": ['简单', '普通', '高级', '神级'],
        "按主要工艺": ['扒', '蒸', '拔丝', '煮', '拌', '堡', '爆', '焯', '炒', '调味', '炖', '干煸', '干锅', '烘焙', '烩',
                       '火锅', '技巧', '煎', '酱', '焗', '烤', '烙', '冷冻', '溜', '卤', '焖', '炝', '砂锅',
                       '烧', '生鲜', '酥', '铁板', '氽', '微波', '煨', '熏', '腌', '炸', '榨汁'],
        "常见菜式": ['海鲜', '烘焙', '火锅', '家常菜', '烤箱菜', '凉菜', '零食', '泡酱腌菜', '热菜', '汤羹', '西餐',
                     '小吃', '宴客菜', '饮品', '主食', '自制食材'],
        "场景": ['二人世界', '开胃菜', '快餐', '快手菜', '私房菜', '宿舍时代', '西式宴请', '下午茶', '野餐', '早餐',
                 '中式宴请'],
        "节日食俗": ['白露', '雨水', '处暑', '元宵节', '春分', '中秋', '大寒', '重阳节', '大暑', '大雪', '冬至',
                     '端午节', '儿童节', '二月二', '父亲节', '复活节', '感恩节', '谷雨', '寒露', '节日习俗', '惊蛰', '腊八', '立春', '立冬',
                     '立秋', '立夏', '芒种', '母亲节', '年夜饭', '七夕', '清明', '情人节', '秋分', '圣诞节', '霜降',
                     '贴秋膘', '万圣节', '夏至', '小寒', '小满', '小暑', '小雪'],
        "食疗食补": ['便秘', '补钙', '防辐射', '护肝明目', '减肥瘦身', '健康食谱', '健脾养胃', '抗过敏', '流感',
                     '排毒养颜', '贫血', '清肺止咳', '清热祛火', '秋冬进补', '驱寒暖身', '提高免疫力', '痛经', '下奶',
                     '消暑解渴', '醒酒', '壮阳', '滋润补水', '滋阴'],
        "适宜人群": ['哺乳期', '产妇', '儿童', '老人', '青少年', '婴儿', '幼儿', '孕妇'],
        "甜品饮品": ['饮品', '冰淇淋', '布丁', '豆浆', '果冻', '果酱', '果汁', '鸡尾酒', '咖啡', '奶昔', '酸奶', '糖水',
                     '甜品'],
        "外国美食": ['法国菜', '韩国料理', '墨西哥菜', '日本料理', '泰国菜', '外国美食', '西班牙菜', '意大利菜',
                     '印度菜', '英国菜', '越南菜'],
        "饮食方式": ['春季食谱', '冬季食谱', '高颜值', '清真菜', '秋季食谱', '素菜', '素食', '夏季食谱', '小清新'],
        "中式菜系": ['澳门美食', '北京菜', '川菜', '东北菜', '鄂菜', '赣菜', '贵州菜', '淮扬菜', '徽菜', '晋菜', '客家菜',
                   '鲁菜', '闽菜', '上海菜', '苏菜', '台湾美食', '西北菜', '香港美食', '湘菜', '新疆菜', '豫菜', '粤菜',
                   '云南菜', '浙菜', '中式菜系'],
        "主食小吃": ['包子', '北京小吃', '饼', '炒饭', '东北小吃', '福建小吃', '广东小吃', '河南小吃', '湖北小吃',
                     '湖南小吃', '馄饨', '江西小吃', '江浙小吃', '饺子', '馒头花卷', '米饭', '面食', '面条', '山东小吃',
                     '山西小吃', '陕西小吃', '上海小吃', '四川小吃', '台湾小吃', '天津小吃', '五谷杂粮', '西北小吃',
                     '云贵小吃', '重庆小吃', '粥'],
        "传统美食": ['传统美食', '春饼', '春卷', '腊八粥', '青团', '汤圆', '元宵', '月饼', '粽子'],
        "烘焙": ['饼干', '蛋糕', '蛋糕卷', '翻糖', '玛芬蛋糕', '面包', '慕斯', '奶油蛋糕', '派塔', '批萨', '戚风蛋糕',
                 '曲奇', '乳酪蛋糕', '吐司', '芝士蛋糕', '纸杯蛋糕']
    }

    return jsonify({'code': 200, 'msg': "成功", 'data': categories})

# ————————————————————————————————————————————————————————————————————————————————
# 搜索食物内容
@bp.route('/search', methods=['POST'])
def search_food():

    key = request.form.get('key', '')

    foods = Food.query.filter(Food.name.ilike(f'%{key}%')).all()

    food_list = []
    for food in foods:
        food_list.append(food.name)

    return jsonify({'code': 200, 'msg': '成功', 'data': food_list})


# 发表评论
@bp.route('/comment', methods=['POST'])
def post_comment():

    user_name = request.form.get('username')
    food_name = request.form.get('dishname')
    content = request.form.get('comment')


    if not user_name or not food_name or not content:
        return jsonify({'code': 200, 'msg': '请输入评论'})


    user = User.query.filter_by(username=user_name).first()
    food = Food.query.filter_by(name=food_name).first()
    if not user or not food:
        return jsonify({"msg": "User or food not found"}), 404


    new_comment = Comment(user_id=user.id, food_id=food.id, content=content)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '成功'})


# 获取评论
@bp.route('/dishname_comment', methods=['POST'])
def get_food_evaluations():
    food_name = request.form.get('dishname')
    if not food_name:
        return jsonify({'code': 200, 'msg': '错误'})
    foods = Food.query.filter_by(name=food_name).first()
    result = []

    for food in foods.comments:
        food_id = food.food_id
        food_comments = food.content
        users = User.query.filter_by(id=food.user_id).first()
        rating = Rating.query.filter_by(food_id=food_id, user_id=users.id).first()
        if rating:
            temp = [users.username, food_comments, rating.score]
        else:
            temp = [users.username, food_comments, 3]

        result.append(temp)

    return jsonify({'code': 200, 'msg': '成功', 'data': result})

# __________________

# @bp.route('/addfood', methods=['get']) # 批量上传脚本
# def addCategory():
#     # 指定目标文件夹的路径，使用双反斜杠或原始字符串
#     folder_path = r'C:\Users\PC\Documents\WeChat Files\wxid_bdybechriykt22\FileStorage\File\2024-10\source\source\按菜品口味'
#
#     # 遍历指定文件夹下的所有文件
#     for filename in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, filename)
#
#         # 检查是否是CSV文件
#         if os.path.isfile(file_path) and filename.endswith('.csv'):
#             print(f"处理文件: {filename}")
#
#             # 打开文件并读取内容
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 for line in file:
#                     # 将行中的逗号删除并转换为列表
#                     elements = line.strip().replace('，', '').split(',')
#                     elements = [elem.strip() for elem in elements if elem]  # 去掉空元素
#
#                     # 确保元素足够
#                     if len(elements) < 5:
#                         print(f"跳过无效行: {line}")
#                         continue
#
#                     # 查找或创建食物
#                     food1 = Food.query.filter_by(name=elements[0]).first()
#                     if food1 is None:
#                         food1 = Food(name=elements[0], description=elements[1], image=elements[2], big_type=elements[3])
#                         db.session.add(food1)
#
#                     # 查找或创建口味
#                     flavor = Flavor.query.filter_by(flavor_type=elements[4]).first()
#                     if flavor is None:
#                         flavor = Flavor(flavor_type=elements[4])
#                         db.session.add(flavor)
#
#                     # 关联食物和口味
#                     food_flavor_association = FoodFlavorAssociation.query.filter_by(food_id=food1.id,
#                                                                                     flavor_id=flavor.id).first()
#                     if food_flavor_association is None:
#                         food_flavor_association = FoodFlavorAssociation(food_id=food1.id, flavor_id=flavor.id)
#                         db.session.add(food_flavor_association)
#
#                 # 提交所有更改
#                 db.session.commit()
#
#                 # try:
#                 #     print(elements)
#                 # except UnicodeEncodeError:
#                 #     print("包含无法编码的字符。")
#
#     print("处理完成。")
#     return jsonify({'code': 200, 'msg': "处理完成"})