from flask import Flask, jsonify
import subprocess

from cam import Cam

app = Flask(__name__)
pipeline = None  # Placeholder for the GStreamer pipeline

cams = [Cam(), Cam()]
is_streaming = False
process: subprocess.Popen = None

@app.route('/start', methods=['GET'])
def start_stream():
    global is_streaming, process, cams

    if not is_streaming:
        pipe = [
            'gst-launch-1.0',
            'filesrc', 'location=wall.jpg', '!', 'jpegdec', '!', 'imagefreeze', '!', 'videoconvert', '!',
            'compositor', 'name=comp', 'sink_0::xpos=0', 'sink_0::ypos=0', 'sink_1::xpos=8', 'sink_1::ypos=360',
            'sink_2::xpos=1284', 'sink_2::ypos=360', '!', 'video/x-raw,width=2560,height=1440', '!', 'vaapipostproc', '!',
            'x264enc', 'bitrate=2000', 'tune=zerolatency', 'key-int-max=60', '!', 'video/x-h264,profile=main', '!',
            'flvmux', 'streamable=true', 'name=mux', '!', 'rtmpsink', 'location=rtmp://a.rtmp.youtube.com/live2/tm8k-wc2t-h2ek-demw-b044',
            'audiotestsrc', 'wave=silence', '!', 'mux.'
        ]
        for cam in cams:
            pipe += cam.get_source() + ['!', 'vaapipostproc', '!', 'queue', '!', 'comp.']

        print(pipe)

        process = subprocess.Popen(pipe, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        is_streaming = True

    else:
        process.terminate()
        is_streaming = False

    return jsonify({"status": is_streaming})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4444, debug=True)