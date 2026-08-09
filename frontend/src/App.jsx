import { useAudioCapture } from './hooks/useAudioCapture';

function App() {
  const { start, stop, status, transcript, assistantReply } = useAudioCapture(
    `${import.meta.env.VITE_WS_URL}/ws/session/test-session`
  );

  return (
    <div>
      <p>Status: {status}</p>
      <button onClick={start} disabled={status !== 'idle'}>Start</button>
      <button onClick={stop} disabled={status === 'idle'}>Stop</button>
      <p><strong>You:</strong> {transcript}</p>
      <p><strong>Tutor:</strong> {assistantReply}</p>
    </div>
  );
}

export default App;