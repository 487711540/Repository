from exts import db


class Food(db.Model):  # 食物
    __tablename__ = 'food'  # 表名为food

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键ID
    name = db.Column(db.String(100), nullable=False)  # 食物名称
    description = db.Column(db.Text)  # 食物介绍（做法）
    image = db.Column(db.String(200))  # 食物图片链接
    average_score = db.Column(db.Float)  # 食物平均评分
    big_type = db.Column(db.String(100)) # 大类


    # 关联关系
    ratings = db.relationship('Rating', backref='food', lazy='dynamic')  # 与评分表的关系
    comments = db.relationship('Comment', backref='food', lazy='dynamic')  # 与评论表的关系
    favorites = db.relationship('Favorite', backref='food', lazy='dynamic')  # 与收藏表的关系
    food_flavor_association = db.relationship('FoodFlavorAssociation', backref='food', lazy='dynamic')  # 与食物所属风味关联表的关系


class User(db.Model):  # 用户
    __tablename__ = 'user'  # 表名为user

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键ID
    username = db.Column(db.String(100), unique=True, nullable=False)  # 用户名，唯一
    password = db.Column(db.String(200), nullable=False)  # 密码

    # 关联关系
    ratings = db.relationship('Rating', backref='user', lazy='dynamic')  # 与评分表的关系
    comments = db.relationship('Comment', backref='user', lazy='dynamic')  # 与评论表的关系
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic')  # 与收藏表的关系
    flavor_preferences = db.relationship('FlavorPreference', backref='user', lazy='dynamic')  # 与口味喜好表的关系
    # recommendations = db.relationship('Recommendation', backref='user', lazy='dynamic')  # 与推荐表的关系


class Flavor(db.Model):  # 小类
    __tablename__ = 'flavor'  # 表名为flavor

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键ID
    flavor_type = db.Column(db.String(100), nullable=False)  # 小类

    # 关联关系
    flavor_preference = db.relationship('FlavorPreference', backref='flavor', lazy='dynamic')  # 与口味喜好关联表的关系
    food_flavor_association = db.relationship('FoodFlavorAssociation', backref='flavor', lazy='dynamic')  # 与风味所属表的关系


class Rating(db.Model):  # 评分
    __tablename__ = 'rating'  # 表名为rating

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 用户ID，外键
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)  # 食物ID，外键
    score = db.Column(db.Float, nullable=False)  # 评分


class Comment(db.Model):  # 评论
    __tablename__ = 'comment'  # 表名为comment

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 用户ID，外键
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)  # 食物ID，外键
    content = db.Column(db.Text, nullable=False)  # 评论内容


class Favorite(db.Model):  # 收藏
    __tablename__ = 'favorite'  # 表名为favorite

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 用户ID，外键
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)  # 食物ID，外键


class FlavorPreference(db.Model):  # 用户的口味偏好
    __tablename__ = 'flavor_preference'  # 表名为flavor_association

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键ID
    flavor_id = db.Column(db.Integer, db.ForeignKey('flavor.id'), nullable=False)  # 口味ID，外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 用户ID，外键


class FoodFlavorAssociation(db.Model):  # 食物属于哪一种口味（风味所属）
    __tablename__ = 'food_flavor_association'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键ID
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)  # 食物ID，外键
    flavor_id = db.Column(db.Integer, db.ForeignKey('flavor.id'), nullable=False)  # 口味ID，外键


# class Recommendation(db.Model):  # 推荐
#     __tablename__ = 'recommendation'  # 表名为recommendation
#
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # 用户ID，外键，主键
#     food_id = db.Column(db.Integer, db.ForeignKey('food.id'), primary_key=True)  # 食物ID，外键，主键
#     is_recommended = db.Column(db.Boolean, default=False)  # 是否推荐
