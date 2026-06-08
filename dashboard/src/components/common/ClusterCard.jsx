/**
 * ClusterCard.jsx
 * Displays a single cluster profile with stats, tags, and a mini progress bar.
 * Props: cluster object from clusterData.js
 */
export default function ClusterCard({ cluster, index }) {
  const { name, emoji, color, colorLight, colorBorder, count, percentage, avgSpend, frequency, recency, description, tags, radar } = cluster

  // Compute a "score" as the mean of the radar values (0-100)
  const overallScore = Math.round(
    Object.values(radar).reduce((a, b) => a + b, 0) / Object.values(radar).length
  )

  return (
    <div
      className="cluster-card animate-in"
      style={{
        border: `1px solid ${colorBorder}`,
        animationDelay: `${index * 0.1}s`,
      }}
    >
      {/* Subtle background glow */}
      <div
        style={{
          position: 'absolute',
          top: 0, left: 0, right: 0, height: '3px',
          background: `linear-gradient(90deg, ${color}, transparent)`,
          borderRadius: '16px 16px 0 0',
        }}
        aria-hidden="true"
      />

      {/* Header row */}
      <div className="cluster-card-header">
        <span className="cluster-emoji" role="img" aria-label={name}>{emoji}</span>
        <span
          className="cluster-number"
          style={{ background: colorLight, color, border: `1px solid ${colorBorder}` }}
        >
          Cluster {cluster.id}
        </span>
      </div>

      {/* Name & description */}
      <div className="cluster-name" style={{ color }}>{name}</div>
      <div className="cluster-desc">{description}</div>

      {/* Key stats */}
      <div className="cluster-stats">
        <div className="cluster-stat">
          <div className="cluster-stat-value" style={{ color }}>{avgSpend}</div>
          <div className="cluster-stat-label">Avg Spend</div>
        </div>
        <div className="cluster-stat">
          <div className="cluster-stat-value" style={{ color }}>{frequency}</div>
          <div className="cluster-stat-label">Frequency</div>
        </div>
        <div className="cluster-stat">
          <div className="cluster-stat-value" style={{ color }}>{recency}</div>
          <div className="cluster-stat-label">Recency</div>
        </div>
      </div>

      {/* Overall score bar */}
      <div style={{ marginBottom: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
            Value Score
          </span>
          <span style={{ fontSize: '0.78rem', fontWeight: 700, color }}>{overallScore}/100</span>
        </div>
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${overallScore}%`, background: `linear-gradient(90deg, ${color}, ${color}aa)` }}
          />
        </div>
      </div>

      {/* Customer count */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
          {count.toLocaleString()} customers
        </span>
        <span style={{ fontSize: '0.78rem', fontWeight: 700, color }}>{percentage}%</span>
      </div>

      {/* Tags */}
      <div className="cluster-tags">
        {tags.map(tag => (
          <span key={tag} className="cluster-tag">{tag}</span>
        ))}
      </div>
    </div>
  )
}
