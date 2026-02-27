import { useState } from 'react'
import './SummaryTool.css'

function SummaryTool() {
  const [text, setText] = useState('')
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSummary(null)

    try {
      const response = await fetch('http://localhost:8000/assistant/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text })
      })

      if (!response.ok) {
        throw new Error('Error al generar resumen')
      }

      const data = await response.json()
      setSummary(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setText('')
    setSummary(null)
    setError(null)
  }

  const exampleTexts = [
    {
      title: "Python",
      text: "Python es un lenguaje de programación de alto nivel, interpretado y de propósito general. Fue creado por Guido van Rossum y lanzado por primera vez en 1991. Python enfatiza la legibilidad del código y permite a los programadores expresar conceptos en menos líneas de código que en lenguajes como C++ o Java."
    },
    {
      title: "IA",
      text: "La inteligencia artificial (IA) es la simulación de procesos de inteligencia humana por parte de máquinas, especialmente sistemas informáticos. Estos procesos incluyen el aprendizaje, el razonamiento y la autocorrección. Las aplicaciones de la IA incluyen sistemas expertos, reconocimiento de voz y visión artificial."
    }
  ]

  return (
    <div className="card summary-tool">
      <h2>🤖 Asistente de Resumen con IA</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="text">Texto a resumir</label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Escribe o pega el texto que quieres resumir..."
            rows={8}
            required
            minLength={10}
          />
          <div className="char-count">
            {text.length} caracteres
          </div>
        </div>

        <div className="example-buttons">
          <span className="example-label">Ejemplos:</span>
          {exampleTexts.map((example, index) => (
            <button
              key={index}
              type="button"
              onClick={() => setText(example.text)}
              className="btn-example"
            >
              {example.title}
            </button>
          ))}
        </div>

        {error && (
          <div className="error-message">
            ❌ {error}
          </div>
        )}

        <div className="button-group">
          <button 
            type="submit" 
            className="btn-primary"
            disabled={loading || text.length < 10}
          >
            {loading ? '⏳ Generando resumen...' : '✨ Generar Resumen'}
          </button>
          
          {text && (
            <button 
              type="button"
              onClick={handleClear}
              className="btn-secondary"
            >
              🗑️ Limpiar
            </button>
          )}
        </div>
      </form>

      {summary && (
        <div className="summary-result">
          <h3>📝 Resumen Generado</h3>
          <div className="summary-content">
            {summary.summary}
          </div>
          
          <div className="summary-metadata">
            <div className="metadata-item">
              <span className="metadata-label">Modelo:</span>
              <span className="metadata-value">{summary.model_used}</span>
            </div>
            <div className="metadata-item">
              <span className="metadata-label">Tokens:</span>
              <span className="metadata-value">{summary.tokens_used}</span>
            </div>
            <div className="metadata-item">
              <span className="metadata-label">ID:</span>
              <span className="metadata-value">#{summary.id}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default SummaryTool
