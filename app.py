from flask import Flask, request, jsonify, send_from_directory, render_template
import requests
from flask_cors import CORS





app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/api/check-halal', methods=['POST'])


def check_halal():
    data = request.get_json()
    barcode = data.get('barcode')
    
    print("📦 Barcode received:", data) 
    if not barcode:
        return jsonify({'error': 'No barcode provided'}), 400

    # Query OpenFoodFacts
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return jsonify({'error': f'Failed to fetch product info: {str(e)}'}), 500

    if data.get('status') != 1:
        return jsonify({'error': 'Product not found'}), 404

    product = data['product']
    product_name = product.get('product_name', 'Unknown')
    labels = product.get('labels_tags', [])
    categories = product.get('categories_tags', [])
    ingredients_analysis = product.get('ingredients_analysis_tags', [])

    is_halal = any('en:halal' in tag for tag in (labels + categories + ingredients_analysis))

    return jsonify({
        'barcode': barcode,
        'product_name': product_name,
        'halal': is_halal,
        'source': 'OpenFoodFacts'
    })

if __name__ == '__main__':
    app.run(debug=True)
