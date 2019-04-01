# pip install flask-swagger-ui
# pip install flask_swagger

from flask import Flask, jsonify, abort, request
from flask_swagger import swagger

from flask_swagger_ui import get_swaggerui_blueprint
import logging
from sgment_words import jiebahelper
from flask import make_response

logger = logging.getLogger(__name__)
app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/') 
API_URL = '/swagger'

# Call factory function to create our blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "JieBa Application"
    }
)

# Register blueprint at URL
# (URL must match the one given to factory function above)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.route("/swagger")
def spec():
    swags = swagger(app)
    swags['info']['version'] = "1.0"
    swags['info']['title'] = "Segment API"
    return jsonify(swags)


@app.route('/')
def index():
    return 'JieBa Segment API by Python.'


@app.errorhandler(404)
def not_found(error):
    # 当我们请求  # 2 id的资源时，可以获取，但是当我们请求#3的资源时返回了404错误。并且返回了一段奇怪的HTML错误，
    # 而不是我们期望的JSON，这是因为Flask产生了默认的404响应。客户端需要收到的都是JSON的响应，因此我们需要改进404错误处理：
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def para_error(error):
    # 数据错误
    return make_response(jsonify({'error': 'Parameter Error'}), 400)


@app.route('/segment', methods=['POST'])
def segment():
    """
        切词。不带词性，去停词
        ---
        tags:
          - Segment
        parameters:
          - in: body
            name: body
            description: 内容
            required: true
            schema:
                type: string
     """
    sentence = request.data.strip()
    logger.info('request', request)
    if sentence == '':
        abort(400)
    sentence = str(sentence, encoding="utf-8")
    logger.info('request', '开始')
    ret = jiebahelper.segment(sentence)
    return ret


@app.route('/add_dict', methods=['POST'])
def add_user_dict():
    """
    添加自定义词典,（发现新词，手动添加到词典里）
    例子：氪金 打call
    ---
    tags:
        - AddUserDict
    parameters:
      - in: body
        name: body
        description: 内容
        required: true
        schema:
            type: string
    """
    sentence = request.data.strip()
    if sentence == '':
        abort(400)
    sentence = str(sentence, encoding="utf-8")
    ret = jiebahelper.add_dict(sentence)
    return ret


if __name__ == "__main__":
    app.run(host="10.12.8.242", port=5000, debug=True)
