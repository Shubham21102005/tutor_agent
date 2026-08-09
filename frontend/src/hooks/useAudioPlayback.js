import { useRef, useCallback } from 'react';

export function useAudioPlayback(sampleRate = 24000) {
  const ctxRef = useRef(null);
  const nextStartTimeRef = useRef(0);

  const getContext = useCallback(() => {
    if (!ctxRef.current) {
      ctxRef.current = new AudioContext({ sampleRate });
      nextStartTimeRef.current = ctxRef.current.currentTime;
    }
    return ctxRef.current;
  }, [sampleRate]);

  const playChunk = useCallback((arrayBuffer) => {
    const ctx = getContext();

    const int16 = new Int16Array(arrayBuffer);
    const float32 = new Float32Array(int16.length);
    for (let i = 0; i < int16.length; i++) {
      float32[i] = int16[i] / 32768;
    }

    const audioBuffer = ctx.createBuffer(1, float32.length, sampleRate);
    audioBuffer.copyToChannel(float32, 0);

    const source = ctx.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(ctx.destination);

    const startAt = Math.max(ctx.currentTime, nextStartTimeRef.current);
    source.start(startAt);
    nextStartTimeRef.current = startAt + audioBuffer.duration;
  }, [getContext, sampleRate]);

  const reset = useCallback(() => {
    if (ctxRef.current) {
      nextStartTimeRef.current = ctxRef.current.currentTime;
    }
  }, []);

  return { playChunk, reset };
}