from flask import Flask, render_template, request, jsonify
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

app = Flask(__name__)

# Make the timezone finder
tf = TimezoneFinder()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_time')
def get_time():
    # Get the coordinates from the URL
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))
    
    # Find the timezone
    timezone_str = tf.timezone_at(lng=lng, lat=lat)
    
    # Get the time
    timezone = pytz.timezone(timezone_str)
    current_time = datetime.now(timezone)
    
    # Make the response
    return jsonify({
        'time': current_time.strftime('%I:%M %p'),
        'date': current_time.strftime('%A, %B %d'),
        'timezone': timezone_str.split('/')[-1].replace('_', ' ')
    })

if __name__ == '__main__':
    app.run() 
