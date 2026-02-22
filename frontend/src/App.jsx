import { useState } from 'react'

export default function App() {
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showRound1, setShowRound1] = useState(false)
  const [showRound2, setShowRound2] = useState(false)

  const handleSubmit = async () => {
    if (!question) return
    setLoading(true)
    setResult(null)

    const res = await fetch('http://localhost:8000/debate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    })

    const data = await res.json()
    setResult(data)
    setLoading(false)
  }

  return (
    <div className='min-h-screen bg-gray-950 text-white p-8'>
      <h1 className='text-3xl font-bold text-center mb-8'>
        Multi-Agent AI Debate
      </h1>

      <div className='flex gap-2 max-w-2xl mx-auto mb-8'>
        <input
          className='flex-1 p-3 rounded bg-gray-800 outline-none'
          placeholder='Ask anything...'
          value={question}
          onChange={e => setQuestion(e.target.value)}
        />
        <button
          onClick={handleSubmit}
          disabled={loading}
          className='bg-blue-600 px-6 py-3 rounded font-bold hover:bg-blue-700'
        >
          {loading ? 'Debating...' : 'Ask'}
        </button>
      </div>

      {loading && (
        <p className='text-center text-yellow-400'>
          Running debate... this takes 20-30 seconds
        </p>
      )}

      {result && (
        <>
          <Section title='Round 1 — Initial Answers' data={result.round1} show={showRound1} onToggle={() => setShowRound1(!showRound1)} />
          <Section title='Round 2 — After Cross Examination' data={result.round2} show={showRound2} onToggle={() => setShowRound2(!showRound2)} />
          <div className='max-w-3xl mx-auto bg-green-900 p-6 rounded-xl mt-6'>
            <h2 className='text-xl font-bold mb-3'>Final Answer</h2>
            <p className='whitespace-pre-wrap'>{result.final}</p>
          </div>
        </>
      )}
    </div>
  )
}

function Section({ title, data, show, onToggle }) {
  return (
    <div className='max-w-5xl mx-auto mb-10'>
      <div className='flex items-center gap-2 mb-4'>
        <h2 className='text-xl font-bold text-blue-400'>{title}</h2>
        <button
          onClick={onToggle}
          className='text-xs bg-gray-700 hover:bg-gray-600 px-2 py-1 rounded text-gray-300'
        >
          {show ? 'Hide' : 'Show'}
        </button>
      </div>
      {show && (
        <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
          {Object.entries(data).map(([agent, answer]) => (
            <div key={agent} className='bg-gray-800 p-4 rounded-xl'>
              <h3 className='font-bold text-purple-400 capitalize mb-2'>{agent}</h3>
              <p className='text-sm whitespace-pre-wrap'>{answer}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}