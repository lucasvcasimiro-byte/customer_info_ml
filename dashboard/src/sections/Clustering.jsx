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
import { useState, useMemo } from 'react'
import SectionHeader    from '../components/common/SectionHeader'
import ClusterCard      from '../components/common/ClusterCard'
import InteractivePlot  from '../components/common/InteractivePlot'
import { clustersByK, clusterConfigs } from '../data/clusterData'

// Extended colour palette — covers up to 7 clusters
const RADAR_COLORS = ['#f59e0b', '#3b82f6', '#2dd4bf', '#f43f5e', '#a78bfa', '#06b6d4', '#10b981']

export default function Clustering() {
  const [selectedScaler, setSelectedScaler] = useState('RobustScaler')
  const [selectedK, setSelectedK]           = useState(7)

  // ── Derive the active cluster list from the selected k ─────────────────────
  // This is the key fix: every chart below reads `activeClusters`, not the
  // hardcoded `clusters` array. When selectedK changes, everything re-renders.
  const activeClusters = clustersByK[selectedK] ?? clustersByK[6]

  // ── Metrics for the current scaler × k combination ──────────────────────────
  const configKey      = `${selectedScaler}__${selectedK}`
  const currentMetrics = clusterConfigs.metrics[configKey] || {}

  // ── Radar chart traces (depend on activeClusters) ─────────────────────────
  const radarTraces = useMemo(() =>
    activeClusters.map((c, i) => ({
      type:      'scatterpolar',
      r:         [...Object.values(c.radar), Object.values(c.radar)[0]],
      theta:     [...Object.keys(c.radar),   Object.keys(c.radar)[0]],
      name:      c.name,
      fill:      'toself',
      fillcolor: `${RADAR_COLORS[i] ?? '#888'}22`,
      line:      { color: RADAR_COLORS[i] ?? '#888', width: 2 },
      marker:    { color: RADAR_COLORS[i] ?? '#888' },
      hovertemplate: `<b>${c.name}</b><br>%{theta}: %{r}<extra></extra>`,
    }))
  , [activeClusters])   // ← depends on activeClusters, so it re-runs on k change

  const radarLayout = {
    polar: {
      bgcolor: 'rgba(0,0,0,0)',
      radialaxis: {
        visible:   true,
        range:     [0, 100],
        gridcolor: 'rgba(124,58,237,0.15)',
        linecolor: 'rgba(124,58,237,0.2)',
        tickfont:  { color: '#64748b', size: 10 },
      },
      angularaxis: {
        gridcolor: 'rgba(124,58,237,0.15)',
        linecolor: 'rgba(124,58,237,0.2)',
        tickfont:  { color: '#94a3b8', size: 11 },
      },
    },
    showlegend: true,
    margin: { l: 50, r: 50, t: 30, b: 30 },
  }

  const radarCsv = {
    headers: ['Feature', ...activeClusters.map(c => c.name)],
    rows:    Object.keys(activeClusters[0].radar).map(feat => [
      feat,
      ...activeClusters.map(c => c.radar[feat]),
    ]),
  }

  // ── Bar chart trace (depends on activeClusters) ────────────────────────────
  const barTrace = useMemo(() => [{
    type:        'bar',
    x:           activeClusters.map(c => c.name),
    y:           activeClusters.map(c => c.count),
    marker: {
      color:   activeClusters.map((c, i) => RADAR_COLORS[i] ?? c.color),
      opacity: 0.85,
      line:    { color: activeClusters.map((c, i) => RADAR_COLORS[i] ?? c.color), width: 1.5 },
    },
    text:        activeClusters.map(c => `${c.percentage}%`),
    textposition:'outside',
    hovertemplate: '<b>%{x}</b><br>Customers: %{y}<extra></extra>',
  }], [activeClusters])   // ← also depends on activeClusters

  return (
    <section id="clustering" className="section" style={{ background: 'var(--bg-surface)' }}>
      <div className="container">

        <SectionHeader
          badge="🔮 Clustering Analysis"
          badgeClass="badge-teal"
          title="Customer "
          highlight="Segments"
          subtitle="K-Means clustering applied to RFM + demographic features. Change the scaler or k below — the charts and cards update immediately."
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

        {/* ── Charts row ────────────────────────────────────────── */}
        <div className="clustering-charts">

          {/* Radar — updates when activeClusters changes */}
          <InteractivePlot
            key={`radar-${selectedK}`}   /* force Plotly remount on k change */
            title={`Cluster Profile Radar (k=${selectedK})`}
            description="Normalised feature scores (0–100) per cluster. Larger polygon area = higher overall customer value."
            data={radarTraces}
            layout={radarLayout}
            csvData={radarCsv}
            height={420}
          />

          {/* Bar chart — updates when activeClusters changes */}
          <InteractivePlot
            key={`bar-${selectedK}`}     /* force Plotly remount on k change */
            title={`Customer Distribution (k=${selectedK})`}
            description="Number of customers per cluster. Highly unbalanced clusters may suggest k is too high or too low."
            data={barTrace}
            layout={{
              xaxis:      { tickfont: { size: 10 } },
              yaxis:      { title: { text: 'Customers', font: { color: '#64748b' } } },
              showlegend: false,
              bargap:     0.35,
            }}
            height={420}
          />
        </div>

        <div className="divider" />

        {/* ── Cluster Cards — update when k changes ─────────────── */}
        <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.3rem', marginBottom: '1.5rem' }}>
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
