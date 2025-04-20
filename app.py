from flask import Flask, render_template, request, jsonify
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

app = Flask(__name__)

# Production settings
app.config['JSON_SORT_KEYS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_time')
def get_time():
    try:
        # Get coordinates from request
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        
        # Validate coordinates
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return jsonify({'error': 'Invalid coordinates'}), 400

        # Find timezone
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=lat, lng=lng)
        
        if not timezone_str:
            return jsonify({'error': 'Unable to determine timezone'}), 404

        # Get current time in timezone
        timezone = pytz.timezone(timezone_str)
        current_time = datetime.now(timezone)
        
        # Format the timezone name for display
        display_timezone = timezone_str.split('/')[-1].replace('_', ' ')
        
        return jsonify({
            'time': current_time.strftime('%I:%M %p'),
            'date': current_time.strftime('%A, %B %d'),
            'timezone': display_timezone
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False) 