import subprocess
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///database.db"
db = SQLAlchemy(app)

class ProductResult(db.Model):
    id = db.Column(db.Integer, primary_keys = True)
    name = db.Column(db.String(1000))
    img = db.Column(db.String(1000))
    url = db.Column(db.String(1000))
    price = db.Column(db.Float)
    created_at db.Column(db.DateTime, default = datetime.utcnow)
    search_text = db.Column(db.String(255))
    source = db.Column(db.String(255))

    def __init__(self, name, img, url, price, search_text, source):
        self.name = name
        self.img = img
        self.url = url
        self.price = price
        self.search_text = search_text
        self.source = source

class TrackedProducts(db.Model):
    id = db.Column(db.Integer, primary_keys = True)
    name = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tracked = db.Column(db.Boolean, default=True)

    def __init__(self, name, tracked=True):
        self.name = name
        self.tracked = tracked

@app.route('/results', methods = ['POST'])
def submit_results():
    results = requests.json.get('data')
    search_text = request.json.get("search_text")
    source = request.json.get("source")
    
    for result in results:
        product_result = ProductResult(
            name = result['name']
            url = result['url']
            img = result['img']
            price = result['price']
            search_text= search_text
            source = source
        )
        db.session.add(product_result)

    db.session.commit()
    response = {"message": "Successfully received data"}
    return jsonify(response), 200

@app.route('/unique_search_texts', methods=['GET'])
def get_unique_search_texts():
    unique_search_texts = db.session.query(
        ProductResult.search_text).distinct().all()
    unique_search_texts = [text[0] for text in unique_search_texts]
    return jsonify(unique_search_texts)

@app.route('/results')
def get_product_results():
    search_text = request.args.get('search_text')
    results = ProductResult.query.filter_by(search_text=search_text).order_by(
        ProductResult.created_at.desc()).all()

    product_dict = {}
    for result in results:
        url = result.url
        if url not in product_dict:
            product_dict[url] = {
                'name': result.name,
                'url': result.url,
                "img": result.img,
                "source": result.source,
                "created_at": result.created_at,
                'priceHistory': []
            }
        product_dict[url]['priceHistory'].append({
            'price': result.price,
            'date': result.created_at
        })

    formatted_results = list(product_dict.values())

    return jsonify(formatted_results)

@app.route('/all-results', methods = ['GET'])
def get_results():
    results = ProductResult.query.all()
    product_results = []
    for result in results:
        product_results.append({
            'name': result.name,
            'url': result.url,
            'price': result.price,
            'img': result.img,
            'date': result.date,
            'created_at': result.created_at,
            'search_text': result.search_text,
            'source': result.source
        })
    return jsonify(product_results)

@app.route('/start-scrapper', methods = ['POST'])
def start_scraper():
    url = request.json.get('url')
    search_text = request.json.get('search_text')
    #should be python process for asynch running