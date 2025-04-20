from flask import Flask, render_template, request, jsonify
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Production settings
app.config['JSON_SORT_KEYS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = False

# Initialize TimezoneFinder once
tf = TimezoneFinder()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_time')
def get_time():
    try:
        # Get coordinates from request
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        
        logger.info(f"Received coordinates - lat: {lat}, lng: {lng}")
        
        # Validate coordinates
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            logger.error(f"Invalid coordinates - lat: {lat}, lng: {lng}")
            return jsonify({'error': 'Invalid coordinates'}), 400

        # Find timezone using the correct method for version 5.2.0
        timezone_str = tf.timezone_at(lng=lng, lat=lat)
        logger.info(f"Found timezone: {timezone_str}")
        
        if not timezone_str:
            logger.error("No timezone found for coordinates")
            return jsonify({'error': 'Unable to determine timezone'}), 404

        # Get current time in timezone
        timezone = pytz.timezone(timezone_str)
        current_time = datetime.now(timezone)
        
        # Format the timezone name for display
        display_timezone = timezone_str.split('/')[-1].replace('_', ' ')
        
        response = {
            'time': current_time.strftime('%I:%M %p'),
            'date': current_time.strftime('%A, %B %d'),
            'timezone': display_timezone
        }
        logger.info(f"Returning response: {response}")
        
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False) 
