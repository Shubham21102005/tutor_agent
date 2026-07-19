import {useRef, useCallback, useState} from 'react';

export function useAudioCapture(wsUrl){
    const wsRef = useRef(null)
    const audioCtxRef = useRef(null)
    const workletNodeRef = useRef(null)
    const streamRef = useRef(null)
    const [status, setStatus] = useState('idle');
    const [transcript, setTranscript] = useState('');

    const start = useCallback(async ()=>{
        setStatus('connecting');
        const ws = new WebSocket(wsUrl)
        ws.binaryType = 'arraybuffer';
        wsRef.current = ws;


        ws.onopen = async () =>{
            const stream = await navigator.mediaDevices.getUserMedia({audio: true});
            streamRef.current = stream;
            const audioCtx = new AudioContext({sampleRate: 16000});
            audioCtxRef.current = audioCtx;

            await audioCtx.audioWorklet.addModule('pcm-worklet-processor.js');

            const source = audioCtx.createMediaStreamSource(stream);
            const workletNode = new AudioWorkletNode(audioCtx, 'pcm-worklet-processor');
            workletNodeRef.current = workletNode;

            workletNode.port.onmessage = (event) => {
                if(ws.readyState === WebSocket.OPEN){
                    ws.send(event.data);
                }
            }
            source.connect(workletNode)
            setStatus('listening')

        }
        ws.onmessage = (event) => {
            try {
                const msg = JSON.parse(event.data);
                if (msg.type === 'transcript' && msg.text) {
                    setTranscript(prev => msg.is_final ? prev + ' ' + msg.text : prev);
                    console.log(msg.is_final ? 'FINAL:' : 'interim:', msg.text);
                }else if(msg.type === 'utterance_complete'){
                    console.log('TURN COMPLETE:', msg.text)
                }
            } catch (e) {
                console.error('bad message', event.data);
            }
        }
        ws.onclose = () => setStatus('idle')
        ws.onerror = (error) => console.error('WebSocket error:', error)
    }, [wsUrl])

    const stop = useCallback(() => {
        workletNodeRef.current?.disconnect();
        streamRef.current?.getTracks().forEach((t) => t.stop());
        audioCtxRef.current?.close();
        wsRef.current?.close();
        setStatus('idle');
    },[])

    return {start, stop, status, transcript}
}
