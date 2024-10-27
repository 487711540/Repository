from flask import Flask, request, jsonify
from models import db, Food  # Ensure you have the correct imports for your database and models
from models import Food, User, Flavor, Rating, Comment, Favorite, FlavorPreference, FoodFlavorAssociation, Recommendation
app = Flask(__name__)

@app.route('/search', methods=['POST']) #搜索食物内容
def search_food():
    # Get the search keyword from the request
    key = request.form.get('key', '')

    # Query the database for food items with matching names
    foods = Food.query.filter(Food.name.ilike(f'%{key}%')).all()

    # Prepare the response data
    food_list = []
    for food in foods:
        food_data = {
            'id': food.id,
            'name': food.name,
            'description': food.description,
            'image': food.image,
            'average_score': food.average_score,
            'ratings': [rating.to_dict() for rating in food.ratings],  # Assuming you have a to_dict method
            'comments': [comment.to_dict() for comment in food.comments],  # Assuming you have a to_dict method
            'favorites': [favorite.to_dict() for favorite in food.favorites],  # Assuming you have a to_dict method
            'flavors': [flavor.to_dict() for flavor in food.food_flavor_association],  # Assuming you have a to_dict method
        }
        food_list.append(food_data)

    return jsonify(food_list)


@app.route('/comment', methods=['POST'])  #发表评论
def post_comment():
    # Get data from request
    user_id = request.form.get('user_id')
    food_id = request.form.get('food_id')
    content = request.form.get('content')

    # Validate input
    if not user_id or not food_id or not content:
        return jsonify({"error": "Missing data"}), 400

    # Check if user and food exist
    user = User.query.get(user_id)
    food = Food.query.get(food_id)
    if not user or not food:
        return jsonify({"error": "User or food not found"}), 404

    # Create new comment
    new_comment = Comment(user_id=user_id, food_id=food_id, content=content)
    db.session.add(new_comment)
    db.session.commit()

    # Prepare response data
    comments = Comment.query.filter_by(food_id=food_id).all()
    comment_list = [{
        'id': comment.id,
        'user_id': comment.user_id,
        'food_id': comment.food_id,
        'content': comment.content
    } for comment in comments]

    food_data = {
        'id': food.id,
        'name': food.name,
        'description': food.description,
        'image': food.image,
        'average_score': food.average_score
    }

    user_data = {
        'id': user.id,
        'username': user.username
    }

    response = {
        'food': food_data,
        'user': user_data,
        'comments': comment_list
    }

    return jsonify(response)

# Configure your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/your_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/dishname_comments', methods=['GET'])#接收评论
def get_food_evaluations():
    foods = Food.query.all()
    result = []

    for food in foods:
        food_data = {
            'id': food.id,
            'name': food.name,
            'description': food.description,
            'image': food.image,
            'average_score': food.average_score,
            'ratings': [{'user_id': rating.user_id, 'score': rating.score} for rating in food.ratings],
            'comments': [{'user_id': comment.user_id, 'content': comment.content} for comment in food.comments],
            'flavors': [{'flavor_type': assoc.flavor.flavor_type} for assoc in food.food_flavor_association]
        }
        result.append(food_data)

    return jsonify(result)
if __name__ == '__main__':
    app.run(debug=True)
