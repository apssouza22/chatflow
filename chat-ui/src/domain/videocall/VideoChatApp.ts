// Import socket.io-client
import io from "socket.io-client";
import {RtcConnHandler} from "./RtcConnHandler";

export class VideoChatApp {
    private localVideo: HTMLElement;
    private socket: io.socket;
    private remoteVideo: any;
    private localUserMediaStream: MediaStream;
    private rtcConns: Array<RtcConnHandler> = [];
    private userList: any;

    constructor(config) {
        this.localVideo = config.localVideo;
        this.socket = config.socket;
        this.remoteVideo = config.remoteVideo;
        this.userList = config.userList;
        this.addSocketListeners();
    }

    async start() {
        let localUserMediaStream = await window.navigator.mediaDevices.getUserMedia({
            audio: true,
            video: true
        });
        this.localVideo.srcObject = localUserMediaStream;
        this.localUserMediaStream = localUserMediaStream;
    }

    createRtcConnection(remoteVideo, socketId) {
        const rtcConn = new RtcConnHandler();
        rtcConn.onTrack((stream) => {
            if (remoteVideo.srcObject !== stream) {
                remoteVideo.srcObject = stream;
                console.log('received remote stream');
            }
        });
        rtcConn.onIceCandidate((candidate) => {
            if (candidate) {
                this.socket.emit("ice-candidate", {candidate, to: socketId});
            }
        });
        rtcConn.addStream(this.localUserMediaStream);
        this.rtcConns.push(rtcConn);
        return rtcConn;
    }

    async callUser(socketId) {
        let rtcConn = this.createRtcConnection(this.remoteVideo, socketId)
        const offer = await rtcConn.createOffer()
        console.log("call user", offer)
        this.socket.emit("call-user", {offer, to: socketId});
    }


    addSocketListeners() {
        this.socket.on("call-made", this.onCallMade.bind(this));
        this.socket.on("answer-made", async data => {
            console.log("answer made", data)
            try {
                await this.rtcConns.forEach(c => c.setAnswer(data.answer));
            } catch (e) {
                console.log(e)
            }
        });
        this.socket.on("ice-candidate-post", async data => {
            for (let i = this.rtcConns.length -1; i >= 0; i--) {
                try {
                    await this.rtcConns[i].addIceCandidate(data.candidate)
                } catch (e) {
                    // Remove the connection if it fails
                    console.log("failed to add ice candidate -  removing connection",e)
                    this.rtcConns.splice(i, 1)
                }
            }
        });
        this.socket.on("update-user-list", ({users}) => {
            this.userList(users)
        });

        this.socket.on("remove-user", ({socketId}) => {
            const elToRemove = document.getElementById(socketId);
            if (elToRemove) {
                elToRemove.remove();
            }
        });
    }

    async onCallMade(data) {
        console.log("call made", data)
        let rtcConn = this.createRtcConnection(this.remoteVideo, data.socket)
        const answer = await rtcConn.createAnswer(data.offer)
        this.socket.emit("make-answer", {answer, to: data.socket});
    }
}
