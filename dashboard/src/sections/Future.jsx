/**
 * Future.jsx  —  Future Analysis / Roadmap section
 *
 * A placeholder section showing upcoming features.
 * Each card has:
 *   - Icon, title, description
 *   - "COMING SOON" ribbon
 *   - A "TODO" placeholder indicating what needs to be built
 *
 * Add new feature cards here as the project grows.
 */
import SectionHeader from '../components/common/SectionHeader'

const futureFeatures = [
  {
    emoji: '🤖',
    title: 'Real-Time Recommendations',
    desc: 'Live product recommendation engine driven by customer history and segment membership.',
    todo: 'Integrate with REST API endpoint returning model predictions per customer_id.',
    status: 'Planned',
    statusColor: 'var(--purple-light)',
  },
  {
    emoji: '📉',
    title: 'Churn Prediction',
    desc: 'Logistic regression / XGBoost model to predict 30-day churn probability per customer.',
    todo: 'Train on At-Risk cluster features. Export churn_proba column to CSV for this dashboard.',
    status: 'In Progress',
    statusColor: 'var(--amber)',
  },
  {
    emoji: '🗺️',
    title: 'Customer Journey Map',
    desc: 'Visualise how customers transition between segments over time (e.g., Regular → Premium).',
    todo: 'Build a Sankey or chord diagram once multi-period transaction data is available.',
    status: 'Planned',
    statusColor: 'var(--purple-light)',
  },
  {
    emoji: '📦',
    title: 'Inventory Optimisation',
    desc: 'Use basket analysis lift rules to recommend stock levels for frequently co-purchased items.',
    todo: 'Combine association rules with inventory CSV. Add a heatmap of stock vs demand.',
    status: 'Planned',
    statusColor: 'var(--purple-light)',
  },
  {
    emoji: '🧪',
    title: 'A/B Testing Framework',
    desc: 'Compare promotion strategies across segments and measure uplift against control groups.',
    todo: 'Placeholder UI for defining test groups and uploading result CSVs.',
    status: 'Backlog',
    statusColor: 'var(--text-muted)',
  },
  {
    emoji: '🌐',
    title: 'Live CSV Data Loading',
    desc: 'Allow the dashboard to load fresh exports from the notebook automatically via file drag-and-drop or API.',
    todo: 'Implement a FileReader-based CSV parser using Papa Parse. Replace static data/ files.',
    status: 'In Progress',
    statusColor: 'var(--amber)',
  },
]

export default function Future() {
  return (
    <section id="future" className="section" style={{ background: 'var(--bg-surface)' }}>
      <div className="container">

        <SectionHeader
          badge="🚀 Roadmap"
          badgeClass="badge-rose"
          title="Future "
          highlight="Extensions"
          subtitle="Placeholder space for upcoming analytical features. Each card documents exactly what needs to be built to bring it to life."
        />

        {/* Feature cards */}
        <div className="future-grid">
          {futureFeatures.map((feat, i) => (
            <div
              key={feat.title}
              className="future-card animate-in"
              style={{ animationDelay: `${i * 0.1}s` }}
            >
              <div className="future-card-icon" style={{ animationDelay: `${i * 0.3}s` }}>
                {feat.emoji}
              </div>

              <h3>{feat.title}</h3>
              <p style={{ marginBottom: '1rem' }}>{feat.desc}</p>

              {/* Status badge */}
              <span style={{
                display: 'inline-block',
                padding: '0.2rem 0.65rem',
                borderRadius: '999px',
                fontSize: '0.72rem',
                fontWeight: 700,
                background: `${feat.statusColor}18`,
                color: feat.statusColor,
                border: `1px solid ${feat.statusColor}44`,
                marginBottom: '1rem',
              }}>
                {feat.status}
              </span>

              {/* TODO note */}
              <div style={{
                background:   'rgba(245,158,11,0.07)',
                border:       '1px solid rgba(245,158,11,0.2)',
                borderRadius: 'var(--radius-sm)',
                padding:      '0.6rem 0.8rem',
                fontSize:     '0.75rem',
                color:        'var(--amber)',
                textAlign:    'left',
              }}>
                <strong>TODO:</strong> {feat.todo}
              </div>
            </div>
          ))}
        </div>

        <div className="divider" />

        {/* Progress timeline */}
        <div className="card">
          <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', marginBottom: '1.5rem' }}>
            Development Roadmap
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {[
              { phase: 'Phase 1 — Complete', desc: 'EDA, K-Means clustering, silhouette analysis, PCA, basket analysis',      done: true  },
              { phase: 'Phase 2 — Complete', desc: 'Interactive dashboard template with all charts and placeholder data',      done: true  },
              { phase: 'Phase 3 — Next',     desc: 'Connect real notebook exports: replace clusterData.js and basketData.js', done: false },
              { phase: 'Phase 4 — Future',   desc: 'Churn model, live CSV ingestion, A/B testing framework',                  done: false },
              { phase: 'Phase 5 — Future',   desc: 'Real-time recommendation API and customer journey visualisation',         done: false },
            ].map((step, i) => (
              <div key={i} style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                {/* Timeline dot */}
                <div style={{ flexShrink: 0, marginTop: '3px' }}>
                  <div style={{
                    width: 14, height: 14,
                    borderRadius: '50%',
                    background: step.done ? 'var(--teal)' : 'var(--bg-elevated)',
                    border: `2px solid ${step.done ? 'var(--teal)' : 'var(--border-soft)'}`,
                    boxShadow: step.done ? '0 0 10px rgba(45,212,191,0.4)' : 'none',
                  }} />
                </div>
                {/* Text */}
                <div>
                  <div style={{ fontSize: '0.875rem', fontWeight: 600, color: step.done ? 'var(--text-primary)' : 'var(--text-secondary)' }}>
                    {step.phase}
                    {step.done && <span style={{ marginLeft: '0.5rem', color: 'var(--teal)', fontSize: '0.75rem' }}>✓ Done</span>}
                  </div>
                  <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                    {step.desc}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </section>
  )
}
