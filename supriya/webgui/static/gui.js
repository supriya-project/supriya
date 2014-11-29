var updater = {
    socket: null,

    handle_meters: function(data) {
        var in_peaks = data['input_meter_peak_levels'];
        var in_rms = data['input_meter_rms_levels'];
        var out_peaks = data['output_meter_peak_levels'];
        var out_rms = data['output_meter_rms_levels'];

        var canvas = $('canvas#meters')[0];
        var context = canvas.getContext('2d');

        context.clearRect(0, 0, canvas.width, canvas.height);

        var gutter = 5;
        var width = 15;
        var left = gutter;

        for (var i = 0; i < in_rms.length; i++) {
            var rms = 10 * Math.log10(in_rms[i]);
            rms = Math.max(rms, -40);
            rms = Math.min(0, rms);
            rms = rms * 2;
            var rms_top = gutter - rms;
            var rms_height = 80 + rms;
            context.fillRect(left, rms_top, width, rms_height);
            var peak = 10 * Math.log10(in_peaks[i]);
            peak = Math.max(peak, -40);
            peak = Math.min(0, peak);
            peak = peak * 2;
            var peak_top = gutter - peak;
            context.beginPath();
            context.moveTo(left, peak_top);
            context.lineTo(left + width, peak_top);
            context.stroke();
            left = left + width + gutter; 
        }
        for (var i = 0; i < out_rms.length; i++) {
            var rms = 10 * Math.log10(out_rms[i]);
            rms = Math.max(rms, -40);
            rms = Math.min(0, rms);
            rms = rms * 2;
            var rms_top = gutter - rms;
            var rms_height = 80 + rms;
            context.fillRect(left, rms_top, width, rms_height);
            var peak = 10 * Math.log10(out_peaks[i]);
            peak = Math.max(peak, -40);
            peak = Math.min(0, peak);
            peak = peak * 2;
            var peak_top = gutter - peak;
            context.beginPath();
            context.moveTo(left, peak_top);
            context.lineTo(left + width, peak_top);
            context.stroke();
            left = left + width + gutter; 
        }
    },

    handle_status: function(data) {

    },

    start: function() {
        var url = "ws://" + location.host + "/websocket";
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function(event) {
            var data = JSON.parse(event.data);
            if (data['topic'] == 'server-status') {
                updater.handle_status(data);
            } else if (data['topic'] == 'server-meters') {
                updater.handle_meters(data);
            }
        }
    }
};

$(document).ready(function(){
    updater.start();
});