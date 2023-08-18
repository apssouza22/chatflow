// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import AudioRecorder from 'audio-recorder-polyfill';

export class AudioMediaRecorder {
  private static instance: AudioMediaRecorder;

  static getInstance(): AudioMediaRecorder {
    if (!this.instance) {
      this.instance = new AudioMediaRecorder();
    }

    return this.instance;
  }

  private md?: MediaRecorder;

  private recordChunks: Blob[];

  constructor() {
    if (!window.MediaRecorder) {
      window.MediaRecorder = AudioRecorder;
    }
    this.recordChunks = [];
  }

  async initialize(): Promise<AudioMediaRecorder> {
    if (this.md) {
      return this;
    }

    const stream = await navigator.mediaDevices.getUserMedia({
      audio: true,
      video: false,
    });
    this.md = new MediaRecorder(stream);
    this.recordChunks = [];

    return this;
  }

  async startRecord(): Promise<void> {
    return new Promise((resolve) => {
      if (!this.md) {
        throw new Error('Must be initialized.');
      }

      this.recordChunks = [];

      this.md.addEventListener('start', () => {
        resolve();
      });

      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      this.md.addEventListener('dataavailable', (e: BlobEvent) => {
        if (e.data.size > 0) {
          this.recordChunks.push(e.data);
        }
      });

      this.md.start();
    });
  }

  async stopRecord(): Promise<Blob> {
    return new Promise((resolve) => {
      if (!this.md) {
        throw new Error('Must be initialized.');
      }

      this.md.addEventListener('stop', () => {
        resolve(new Blob(this.recordChunks));
      });

      this.md.stop();
    });
  }
}
