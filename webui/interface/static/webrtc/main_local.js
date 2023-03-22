var isMozilla = window.mozRTCPeerConnection && !window.webkitRTCPeerConnection;
if (isMozilla) {
    window.webkitURL = window.URL;
    navigator.webkitGetUserMedia = navigator.mozGetUserMedia;
    window.webkitRTCPeerConnection = window.mozRTCPeerConnection;
    window.RTCSessionDescription = window.mozRTCSessionDescription;
    window.RTCIceCandidate = window.mozRTCIceCandidate;
}

var remoteView;
var signalingChannel;
var pc;
var peer;
var localStream;
var channel;

if (!window.hasOwnProperty("orientation"))
    window.orientation = -90;

window.onload = function () {
    remoteView = document.getElementById("remote_view");

    function peerJoin() {
        signalingChannel = new SignalingChannel("robco");

        // another peer has joined our session
        signalingChannel.onpeer = function (evt) {

            peer = evt.peer;
            peer.onmessage = handleMessage;

            peer.ondisconnect = function () {
                remoteView.style.visibility = "hidden";
                if (pc)
                    pc.close();
                pc = null;
            };
        };
    };
    navigator.webkitGetUserMedia({ "audio": "true",
        "video": false}, function (stream) {
        // .. and keep it to be sent later
        localStream = stream;
        
        peerJoin();
    }, logError);
};

// handle signaling messages received from the other peer
function handleMessage(evt) {
    var message = JSON.parse(evt.data);

    if (!pc && (message.sdp || message.candidate))
        start(false);

    if (message.sdp) {
        var desc = new RTCSessionDescription(message.sdp);
        pc.setRemoteDescription(desc, function () {
            // if we received an offer, we need to create an answer
            if (pc.remoteDescription.type == "offer")
                pc.createAnswer(localDescCreated, logError);
        }, logError);
    } else if (!isNaN(message.orientation) && remoteView) {
        var transform = "rotate(" + message.orientation + "deg)";
        //remoteView.style.transform = remoteView.style.webkitTransform = transform;
    } else
        pc.addIceCandidate(new RTCIceCandidate(message.candidate), function () {}, logError);
}

// call start() to initiate
function start(isInitiator) {
    pc = new webkitRTCPeerConnection(null);

    // send any ice candidates to the other peer
    pc.onicecandidate = function (evt) {
        if (evt.candidate)
            peer.send(JSON.stringify({ "candidate": evt.candidate }));
    };

    // let the "negotiationneeded" event trigger offer generation
    pc.onnegotiationneeded = function () {
        // check signaling state here because Chrome dispatches negotiationeeded during negotiation
        if (pc.signalingState == "stable")
            pc.createOffer(localDescCreated, logError);
    };

    // once the remote stream arrives, show it in the remote video element
    pc.onaddstream = function (evt) {
        remoteView.src = URL.createObjectURL(evt.stream);
        remoteView.style.visibility = "visible";
        sendOrientationUpdate();
    };

    pc.addStream(localStream);

    // the negotiationneeded event is not supported in Firefox
    if (isMozilla && isInitiator)
        pc.onnegotiationneeded();
}

function localDescCreated(desc) {
    pc.setLocalDescription(desc, function () {
        peer.send(JSON.stringify({ "sdp": pc.localDescription }));
    }, logError);
}

function sendOrientationUpdate() {
    peer.send(JSON.stringify({ "orientation": window.orientation + 90 }));
}

window.onorientationchange = function () {
    if (peer)
        sendOrientationUpdate();
};

function logError(error) {
    return;
    if (error) {
        if (error.name && error.message)
            log(error.name + ": " + error.message);
        else
            log(error);
    } else
        log("Error (no error message)");
}


