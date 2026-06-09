/**
 * Visualizations.jsx  —  Interactive plots gallery
 *
 * Charts included:
 *   1. Elbow Method (WCSS vs k) — inertia curve
 *   2. Silhouette Score vs k    — line + bar
 *
 */
import { useMemo } from 'react'
import SectionHeader from '../components/common/SectionHeader'
import InteractivePlot from '../components/common/InteractivePlot'
import { elbowData, silhouetteByK, clusters } from '../data/clusterData'

export default function Visualizations() {

  // ── 1. Elbow chart ────────────────────────────────────────────
  const elbowTraces = useMemo(() => [
    {
      // TODO: replace elbowData.wcss with your actual inertia values
      type:        'scatter',
      mode:        'lines+markers',
      x:           elbowData.k,
      y:           elbowData.wcss,
      name:        'WCSS (Inertia)',
      line:        { color: '#7c3aed', width: 2.5, shape: 'spline' },
      marker:      { color: '#b78bfa', size: 8, line: { color: '#7c3aed', width: 2 } },
      hovertemplate: '<b>k = %{x}</b><br>WCSS: %{y:,.0f}<extra></extra>',
    },
    {
      // Vertical marker at the "elbow" — k=8
      type:  'scatter',
      mode:  'markers',
      x:     [8],
      y:     [elbowData.wcss[elbowData.k.indexOf(8)]],
      name:  '★ Optimal k',
      marker:{ color: '#f59e0b', size: 14, symbol: 'star', line: { color: '#fff', width: 1.5 } },
      hovertemplate: '<b>Optimal k = 8</b><br>WCSS: %{y:,.0f}<extra></extra>',
    },
  ], [])

  const elbowCsv = {
    headers: ['k', 'WCSS'],
    rows:    elbowData.k.map((k, i) => [k, elbowData.wcss[i]]),
  }

  // ── 2. Silhouette score per k ──────────────────────────────────
  const silTraces = useMemo(() => [
    {
      // TODO: replace silhouetteByK.scores with your actual silhouette_score() values
      type:        'bar',
      x:           silhouetteByK.k,
      y:           silhouetteByK.scores,
      name:        'Silhouette Score',
      marker: {
        color:   silhouetteByK.k.map(k => k === 8 ? '#7c3aed' : '#2dd4bf'),
        opacity: 0.85,
      },
      hovertemplate: '<b>k = %{x}</b><br>Silhouette: %{y:.3f}<extra></extra>',
    },
    {
      // Guideline at 0.5
      type:  'scatter', mode: 'lines',
      x:     [silhouetteByK.k[0], silhouetteByK.k.at(-1)],
      y:     [0.5, 0.5],
      name:  'Threshold (0.5)',
      line:  { color: '#f59e0b', width: 1.5, dash: 'dot' },
      hoverinfo: 'skip',
    },
  ], [])

  const silCsv = {
    headers: ['k', 'Silhouette Score'],
    rows:    silhouetteByK.k.map((k, i) => [k, silhouetteByK.scores[i]]),
  }

  return (
    <section id="visualizations" className="section">
      <div className="container">
        <div className="viz-gallery">

          {/* 1 — Elbow Method */}
          <InteractivePlot
            title="Elbow Method — WCSS vs k"
            description="Within-Cluster Sum of Squares (inertia) decreases as k grows. The 'elbow' at k=8 (★) marks the point of diminishing returns — our optimal cluster count."
            data={elbowTraces}
            layout={{
              xaxis: { title: { text: 'Number of Clusters (k)', font: { color: '#64748b' } }, dtick: 1 },
              yaxis: { title: { text: 'WCSS / Inertia',         font: { color: '#64748b' } } },
              showlegend: true,
            }}
            csvData={elbowCsv}
          >
            <p>
              <strong>Interpretation:</strong> The Elbow Method plots WCSS (Within-Cluster Sum of Squares) against cluster count (<em>k</em>). WCSS measures cluster compactness. The optimal number of clusters is identified at the "elbow" point (<em>k</em>=8), where adding more clusters yields diminishing returns in variance explanation.
            </p>
          </InteractivePlot>

          {/* 2 — Silhouette Score vs k */}
          <InteractivePlot
            title="Silhouette Score vs k"
            description="Silhouette score measures cluster cohesion and separation (−1 to 1, higher is better). k=8 achieves 0.138, which balances segment separation and model complexity."
            data={silTraces}
            layout={{
              xaxis: { title: { text: 'Number of Clusters (k)', font: { color: '#64748b' } }, dtick: 1 },
              yaxis: { title: { text: 'Silhouette Score',        font: { color: '#64748b' } }, range: [0, 0.2] },
              showlegend: true,
              bargap: 0.35,
            }}
            csvData={silCsv}
          >
            <p>
              <strong>Interpretation:</strong> The Silhouette Coefficient evaluates clustering quality by measuring how well each customer fits their assigned cluster (cohesion) versus neighboring clusters (separation), ranging from -1 to +1. Our peak score at <em>k</em>=8 indicates optimal segment boundaries.
            </p>
          </InteractivePlot>

        </div>
      </div>
    </section>
  )
}
