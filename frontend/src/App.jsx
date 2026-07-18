import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import { useAudioCapture } from './hooks/useAudioCapture';

function App() {
  const { start, stop, status, transcript } = useAudioCapture(
    `${import.meta.env.VITE_WS_URL}/ws/session/test-session`
  );

  return (
    <div>
      <p>Status: {status}</p>
      <button onClick={start} disabled={status !== 'idle'}>Start</button>
      <button onClick={stop} disabled={status === 'idle'}>Stop</button>
      <p>{transcript}</p>
    </div>
  );
}

export default App
