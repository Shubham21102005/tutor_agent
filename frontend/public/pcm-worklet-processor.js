class PCMWorkletProcessor extends AudioWorkletProcessor {
    constructor(){
        super();
        this.bufferSize = 2048
        this.buffer = new Float32Array(this.bufferSize)
        this.bufferIndex = 0
    }

    process(inputs){
        const input = inputs[0]
        if(inputs.length>0){
            const channelData = input[0]
            for(let i = 0; i< channelData.length; i++){
                this.buffer[this.bufferIndex++] = channelData[i]
                if(this.bufferIndex >= this.bufferSize){
                    this.flush()
                }
            }
        }
        return true
    }
    flush(){
        const pcm16 = new Int16Array(this.bufferIndex)
        for(let i = 0; i< this.bufferIndex; i++){
            const s = Math.max(-1, Math.min(1, this.buffer[i]))
            pcm16[i] = s< 0 ? s * 0x8000 : s*0x7fff
        }
        this.port.postMessage(pcm16.buffer, [pcm16.buffer])
        this.bufferIndex = 0
    }
}

registerProcessor('pcm-worklet-processor', PCMWorkletProcessor)