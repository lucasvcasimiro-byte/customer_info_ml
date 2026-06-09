/**
 * Clustering.jsx  —  Clustering Analysis section
 *
 * Features:
 *   • Dropdown controls: choose Scaler and number of clusters (k)
 *   • Metrics (silhouette, inertia) update for each scaler × k combination
 *   • Radar chart, bar chart, and cluster cards ALL update when k changes
 *   • clustersByK in clusterData.js holds the profiles for k=3, 4, 5
 *
 * TODO: When you have real results, update clusterConfigs.metrics AND
 *       clustersByK in clusterData.js with your notebook exports.
 */
import { useState } from 'react'
import SectionHeader    from '../components/common/SectionHeader'
import ClusterCard      from '../components/common/ClusterCard'
import { clustersByK, clusterConfigs } from '../data/clusterData'

export default function Clustering() {
  const [selectedScaler, setSelectedScaler] = useState('RobustScaler')
  const [selectedK, setSelectedK]           = useState(7)

  // ── Derive the active cluster list from the selected k ─────────────────────
  const activeClusters = clustersByK[selectedK] ?? clustersByK[6]

  // ── Metrics for the current scaler × k combination ──────────────────────────
  const configKey      = `${selectedScaler}__${selectedK}`
  const currentMetrics = clusterConfigs.metrics[configKey] || {}

  return (
    <section id="clustering" className="section" style={{ background: 'var(--bg-surface)' }}>
      <div className="container">

        <SectionHeader
          badge="🔮 Clustering Analysis"
          badgeClass="badge-teal"
          title="Customer "
          highlight="Segments"
          subtitle="Hierarchical clustering (Ward linkage) applied to RFM + demographic features. Change the scaler or k below — the charts and cards update immediately."
        />

        {/* ── Interactive Controls ──────────────────────────────── */}
        <div className="clustering-controls">

          {/* Scaler selector */}
          <div className="control-group">
            <label className="control-label" htmlFor="scaler-select">Scaler</label>
            <select
              id="scaler-select"
              className="select"
              value={selectedScaler}
              onChange={e => setSelectedScaler(e.target.value)}
            >
              {clusterConfigs.scalers.map(s => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          {/* K selector */}
          <div className="control-group">
            <label className="control-label" htmlFor="k-select">Clusters (k)</label>
            <select
              id="k-select"
              className="select"
              value={selectedK}
              onChange={e => setSelectedK(Number(e.target.value))}
            >
              {clusterConfigs.kValues.map(k => (
                <option key={k} value={k}>k = {k}</option>
              ))}
            </select>
          </div>

          {/* Live metrics for the current config */}
          {currentMetrics.silhouette && (
            <>
              <div style={{ width: '1px', background: 'var(--border-subtle)', margin: '0 0.5rem' }} />
              <MetricPill label="Silhouette" value={currentMetrics.silhouette} color="var(--teal)" />
              <MetricPill label="Inertia"    value={currentMetrics.inertia?.toLocaleString()} color="var(--purple-light)" />
              {currentMetrics.note && (
                <span style={{
                  fontSize: '0.8rem', color: 'var(--amber)',
                  background: 'rgba(245,158,11,0.1)', padding: '0.3rem 0.7rem',
                  borderRadius: '6px', border: '1px solid rgba(245,158,11,0.25)',
                }}>
                  {currentMetrics.note}
                </span>
              )}
            </>
          )}

          {/* Active config label */}
          <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <span style={{
              fontSize: '0.78rem', fontWeight: 600,
              color: 'var(--text-muted)', background: 'var(--bg-elevated)',
              padding: '0.3rem 0.75rem', borderRadius: '6px',
              border: '1px solid var(--border-subtle)',
            }}>
              Showing: <span style={{ color: 'var(--purple-light)' }}>{selectedK} clusters</span>
              {' · '}
              <span style={{ color: 'var(--teal)' }}>{selectedScaler}</span>
            </span>
          </div>
        </div>

        {/* ── Cluster Cards — update when k changes ─────────────── */}
        <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.3rem', marginBottom: '1.5rem', marginTop: '2.5rem' }}>
          Segment Profiles
          <span style={{ marginLeft: '0.75rem', fontSize: '0.85rem', fontWeight: 400, color: 'var(--text-muted)' }}>
            — k = {selectedK}, {selectedScaler}
          </span>
        </h3>

        {/* Grid adapts column count to k */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${Math.min(selectedK, 4)}, 1fr)`,
          gap: '1.5rem',
        }}>
          {activeClusters.map((cluster, i) => (
            <ClusterCard key={`${selectedK}-${cluster.id}`} cluster={cluster} index={i} />
          ))}
        </div>

      </div>
    </section>
  )
}

/** Small inline metric badge used in the controls bar */
function MetricPill({ label, value, color }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '2px' }}>
      <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>{label}</span>
      <span style={{ fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: '0.95rem', color }}>{value}</span>
    </div>
  )
}
