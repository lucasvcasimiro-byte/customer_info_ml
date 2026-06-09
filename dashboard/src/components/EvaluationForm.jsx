import { useState } from 'react'

export default function EvaluationForm() {
  const [rating, setRating] = useState(0)
  const [hoverRating, setHoverRating] = useState(0)
  const [comment, setComment] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (rating === 0) {
      alert('Please select a rating between 1 and 5 stars.')
      return
    }
    // Save to localStorage
    const feedback = { rating, comment, date: new Date().toISOString() }
    localStorage.setItem('clusternova_app_evaluation', JSON.stringify(feedback))
    setSubmitted(true)
  }

  return (
    <section id="evaluation" className="section" style={{ background: 'var(--bg-base)', borderTop: '1px solid var(--border-subtle)', padding: '4rem 1rem' }}>
      <div className="container" style={{ maxWidth: '600px', margin: '0 auto', textAlign: 'center' }}>
        
        <div className="evaluation-card card" style={{ 
          padding: '2.5rem', 
          background: 'var(--bg-surface)', 
          border: '1px solid var(--border-soft)',
          borderRadius: 'var(--radius-lg)',
          boxShadow: 'var(--shadow-md)'
        }}>
          {!submitted ? (
            <form onSubmit={handleSubmit}>
              <div style={{ marginBottom: '1.5rem' }}>
                <span className="badge badge-purple" style={{ marginBottom: '0.5rem', background: 'rgba(124,58,237,0.18)', color: 'var(--purple-light)', padding: '0.2rem 0.65rem', borderRadius: '999px', fontSize: '0.72rem', fontWeight: 700, border: '1px solid rgba(124,58,237,0.4)' }}>⭐ Evaluation</span>
                <h2 style={{ fontSize: '1.75rem', fontFamily: 'var(--font-display)', marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
                  What did you think of ClusterNova?
                </h2>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                  Your opinion is very important to us! Please rate our Machine Learning II practical project.
                </p>
              </div>

              {/* Stars container */}
              <div style={{ display: 'flex', justifyContent: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setRating(star)}
                    onMouseEnter={() => setHoverRating(star)}
                    onMouseLeave={() => setHoverRating(0)}
                    style={{
                      background: 'none',
                      border: 'none',
                      cursor: 'pointer',
                      fontSize: '2.5rem',
                      padding: 0,
                      color: (hoverRating || rating) >= star ? 'var(--amber)' : 'rgba(255,255,255,0.15)',
                      transform: (hoverRating || rating) >= star ? 'scale(1.15)' : 'scale(1)',
                      transition: 'all 0.15s ease',
                    }}
                    aria-label={`Rate ${star} star${star > 1 ? 's' : ''}`}
                  >
                    ★
                  </button>
                ))}
              </div>

              {/* Comment text area */}
              <div style={{ marginBottom: '1.5rem', textAlign: 'left' }}>
                <label 
                  htmlFor="eval-comments"
                  style={{
                    display: 'block',
                    fontSize: '0.8rem',
                    fontWeight: 600,
                    color: 'var(--text-secondary)',
                    marginBottom: '0.5rem',
                    letterSpacing: '0.05em'
                  }}
                >
                  COMMENTS OR FEEDBACK
                </label>
                <textarea
                  id="eval-comments"
                  rows="4"
                  placeholder="Leave your feedback, comments, or suggestions here..."
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  style={{
                    width: '100%',
                    background: 'var(--bg-input)',
                    border: '1px solid var(--border-soft)',
                    borderRadius: 'var(--radius-md)',
                    padding: '0.75rem 1rem',
                    color: 'var(--text-primary)',
                    fontFamily: 'var(--font-body)',
                    fontSize: '0.875rem',
                    resize: 'vertical',
                    outline: 'none',
                    transition: 'border-color 0.2s',
                  }}
                />
              </div>

              <button
                type="submit"
                className="btn-primary"
                style={{
                  width: '100%',
                  padding: '0.85rem',
                  fontSize: '0.9rem',
                  fontWeight: 600,
                  borderRadius: 'var(--radius-md)',
                  background: 'var(--grad-purple)',
                  border: 'none',
                  color: '#fff',
                  boxShadow: 'var(--shadow-purple)',
                  cursor: 'pointer',
                }}
              >
                Submit Evaluation
              </button>
            </form>
          ) : (
            <div className="animate-in" style={{ padding: '1.5rem 0' }}>
              <div style={{ fontSize: '3rem', color: 'var(--teal)', marginBottom: '1rem' }}>✓</div>
              <h2 style={{ fontSize: '1.75rem', fontFamily: 'var(--font-display)', marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
                Thank You Very Much!
              </h2>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
                Your rating of <strong>{rating} stars</strong> has been successfully recorded. We appreciate your feedback!
              </p>
              <button
                type="button"
                onClick={() => setSubmitted(false)}
                style={{
                  background: 'rgba(255,255,255,0.06)',
                  border: '1px solid rgba(255,255,255,0.12)',
                  color: 'var(--text-primary)',
                  padding: '0.5rem 1.25rem',
                  borderRadius: 'var(--radius-md)',
                  fontSize: '0.82rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                Edit Evaluation
              </button>
            </div>
          )}
        </div>

      </div>
    </section>
  )
}
