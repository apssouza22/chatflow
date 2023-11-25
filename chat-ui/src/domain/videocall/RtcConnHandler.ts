export class RtcConnHandler {
    #hasAnswerReceived;
    #ices = ['stun:stun1.l.google.com:19302', 'stun:stun2.l.google.com:19302'];
    #isCaller = false;
    #eventHandlers = {
        onicecandidateerror: (e) => {
            console.log(e);
        }
    }
    private rtcConn: RTCPeerConnection;

    constructor() {
        const servers = {
            iceServers: [{
                urls: this.#ices,
            }],
            iceCandidatePoolSize: 10,
        };
        this.rtcConn = new RTCPeerConnection(servers);
        this.rtcConn.ontrack = (e) => {
            this.#eventHandlers["ontrack"](e.streams[0]);
        }
        this.rtcConn.onicecandidateerror = (e) => {
            this.#eventHandlers["onicecandidateerror"](e);
        }
        this.rtcConn.onicecandidate = (e) => {
            this.#eventHandlers["onicecandidate"](e.candidate);
        }
    }

    onTrack(trackListener) {
        this.#eventHandlers["ontrack"] = trackListener;
    }

    onIceCandidate(sendCandidate) {
        this.#eventHandlers["onicecandidate"] = sendCandidate;
    }


    async createOffer() {
        const offer = await this.rtcConn.createOffer({
            offerToReceiveAudio: true,
            offerToReceiveVideo: true
        });
        let rtcSessionDescription = new RTCSessionDescription(offer);
        await this.rtcConn.setLocalDescription(rtcSessionDescription);
        this.#isCaller = true;
        return offer;
    }

    async createAnswer(offer) {
        let sessionDescription = new RTCSessionDescription(offer);
        await this.rtcConn.setRemoteDescription(sessionDescription);

        const answer = await this.rtcConn.createAnswer();
        let rtcSessionDescription = new RTCSessionDescription(answer);
        await this.rtcConn.setLocalDescription(rtcSessionDescription);
        return answer;
    }

    async setAnswer(desc) {
        this.#hasAnswerReceived = desc;
        let rtcSessionDescription = new RTCSessionDescription(desc);
        await this.rtcConn.setRemoteDescription(rtcSessionDescription);
    }

    /**
     *
     * @param {MediaStream} userUserMediaStream
     */
    addStream(userUserMediaStream) {
        const audioTracks = userUserMediaStream.getAudioTracks();
        const videoTracks = userUserMediaStream.getVideoTracks();
        for (const audioTrack of audioTracks) {
            console.log(`Using audio device: ${audioTrack.label}`);
        }
        for (const videoTrack of videoTracks) {
            console.log(`Using video device: ${videoTrack.label}`);
        }

        userUserMediaStream.getTracks().forEach(track => {
            this.rtcConn.addTrack(track, userUserMediaStream)
        });
    }

    close() {
        this.rtcConn.close();
    }

    async addIceCandidate(candidate) {
        if (this.#isCaller && !this.#hasAnswerReceived) {
            return;
        }

        if (this.#isCaller && this.#hasAnswerReceived) {
            await this.rtcConn.addIceCandidate(candidate);
            return
        }
        await this.rtcConn.addIceCandidate(candidate);
    }
}