/**
 * Visualizations.jsx  —  Interactive plots gallery
 *
 * Charts included:
 *   1. Elbow Method (WCSS vs k) — inertia curve
 *   2. Silhouette Score vs k    — line + bar
 *   3. PCA 2D Scatter Plot      — cluster projection
 *   4. Silhouette by Cluster    — horizontal bar
 *
 * TODO: Replace placeholder data arrays with real values exported from your
 *       notebook. Each TODO comment marks exactly where to plug in your data.
 */
import { useMemo } from 'react'
import SectionHeader from '../components/common/SectionHeader'
import InteractivePlot from '../components/common/InteractivePlot'
import { elbowData, silhouetteByK, pcaData, clusters } from '../data/clusterData'

const CLUSTER_COLORS = ['#f59e0b', '#3b82f6', '#2dd4bf', '#f43f5e', '#a78bfa', '#06b6d4']

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
      // Vertical marker at the "elbow" — k=6
      type:  'scatter',
      mode:  'markers',
      x:     [6],
      y:     [elbowData.wcss[elbowData.k.indexOf(6)]],
      name:  '★ Optimal k',
      marker:{ color: '#f59e0b', size: 14, symbol: 'star', line: { color: '#fff', width: 1.5 } },
      hovertemplate: '<b>Optimal k = 6</b><br>WCSS: %{y:,.0f}<extra></extra>',
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
        color:   silhouetteByK.k.map(k => k === 6 ? '#7c3aed' : '#2dd4bf'),
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

  // ── 3. UMAP 2D projection scatter ─────────────────────────────────────────
  const pcaTraces = useMemo(() =>
    pcaData.map((group, i) => ({
      // TODO: replace pcaData with actual UMAP coordinates from notebook
      type:        'scatter',
      mode:        'markers',
      name:        clusters[i]?.name || `Cluster ${group.cluster}`,
      x:           group.x,
      y:           group.y,
      marker: {
        color:   CLUSTER_COLORS[group.cluster],
        size:    7,
        opacity: 0.75,
        line:    { color: 'rgba(0,0,0,0.3)', width: 0.5 },
      },
      hovertemplate: `<b>${clusters[i]?.name}</b><br>UMAP1: %{x:.2f}<br>UMAP2: %{y:.2f}<extra></extra>`,
    }))
  , [])

  // ── 4. Silhouette per cluster (synthetic) ─────────────────────
  // TODO: replace with actual per-sample silhouette values from:
  //   sklearn.metrics.silhouette_samples(X_scaled, labels)
  const silSampleTraces = useMemo(() => {
    const clusterNames  = clusters.map(c => c.name)
    const avgSilhouette = [0.12, 0.11, 0.14, 0.09, 0.13, 0.10]  // TODO: replace with real values

    return clusterNames.map((name, i) => ({
      type:        'bar',
      orientation: 'h',
      name,
      x:           [avgSilhouette[i]],
      y:           [name],
      marker:      { color: CLUSTER_COLORS[i], opacity: 0.85 },
      text:        [`${avgSilhouette[i].toFixed(3)}`],
      textposition:'outside',
      hovertemplate: `<b>${name}</b><br>Avg Silhouette: ${avgSilhouette[i]}<extra></extra>`,
    }))
  }, [])

  return (
    <section id="visualizations" className="section">
      <div className="container">

        <SectionHeader
          badge="📈 Visualizations"
          badgeClass="badge-blue"
          title="Interactive "
          highlight="Chart Gallery"
          subtitle="All plots support zoom, pan, and PNG export via the Plotly toolbar. Hover over any data point for detailed tooltips."
        />

        {/* Notice about placeholder data */}
        <div className="placeholder-notice">
          ⚠️ Charts use <strong>placeholder data</strong>. Replace the arrays in{' '}
          <code>src/data/clusterData.js</code> with exports from your notebook to see real results.
        </div>

        <div className="viz-gallery">

          {/* 1 — Elbow Method */}
          <InteractivePlot
            title="Elbow Method — WCSS vs k"
            description="Within-Cluster Sum of Squares (inertia) decreases as k grows. The 'elbow' at k=6 (★) marks the point of diminishing returns — our optimal cluster count."
            data={elbowTraces}
            layout={{
              xaxis: { title: { text: 'Number of Clusters (k)', font: { color: '#64748b' } }, dtick: 1 },
              yaxis: { title: { text: 'WCSS / Inertia',         font: { color: '#64748b' } } },
              showlegend: true,
            }}
            csvData={elbowCsv}
          />

          {/* 2 — Silhouette Score per k */}
          <InteractivePlot
            title="Silhouette Score vs k"
            description="Silhouette score measures cluster cohesion and separation (−1 to 1, higher is better). k=6 achieves 0.101, which balances segment separation and model complexity."
            data={silTraces}
            layout={{
              xaxis: { title: { text: 'Number of Clusters (k)', font: { color: '#64748b' } }, dtick: 1 },
              yaxis: { title: { text: 'Silhouette Score',        font: { color: '#64748b' } }, range: [0, 0.2] },
              showlegend: true,
              bargap: 0.35,
            }}
            csvData={silCsv}
          />

          {/* 3 — UMAP 2D projection scatter (wide) */}
          <div className="viz-wide">
            <InteractivePlot
              title="UMAP 2D Projection — Cluster Separation"
              description="Customer feature space reduced to 2 UMAP coordinates (UMAP1, UMAP2). Well-separated clusters indicate meaningful segmentation. Each point is one customer."
              data={pcaTraces}
              layout={{
                xaxis: { title: { text: 'UMAP Coordinate 1', font: { color: '#64748b' } } },
                yaxis: { title: { text: 'UMAP Coordinate 2', font: { color: '#64748b' } } },
                showlegend: true,
              }}
              height={480}
            />
          </div>

          {/* 4 — Per-cluster silhouette */}
          <InteractivePlot
            title="Average Silhouette per Cluster"
            description="Premium Large Families and Groceries Heavy Omnivores are the most tightly clustered. Promo-Sensitive Shoppers show lower cohesion, suggesting potential overlap."
            data={silSampleTraces}
            layout={{
              xaxis: { title: { text: 'Avg Silhouette Score', font: { color: '#64748b' } }, range: [0, 0.25] },
              showlegend: false,
              bargap:     0.4,
            }}
          />

          {/* 5 — Feature importance (placeholder) */}
          <InteractivePlot
            title="Feature Importance for Clustering"
            description="Variance explained by each feature after scaling. Features with high variance contribute more to cluster differentiation. TODO: replace with your PCA loadings or ANOVA F-scores."
            data={[{
              // TODO: replace with real feature importance from notebook
              type:        'bar',
              x:           [0.31, 0.26, 0.19, 0.14, 0.10],
              y:           ['Recency (days)', 'Avg Spend (€)', 'Purchase Frequency', 'Product Variety', 'Promo Sensitivity'],
              orientation: 'h',
              marker: {
                color:   ['#7c3aed','#7c3aed','#2dd4bf','#2dd4bf','#94a3b8'],
                opacity: 0.85,
              },
              text:        ['31%','26%','19%','14%','10%'],
              textposition:'outside',
              hovertemplate: '<b>%{y}</b><br>Importance: %{x:.0%}<extra></extra>',
            }]}
            layout={{
              xaxis:      { title: { text: 'Relative Importance', font: { color: '#64748b' } }, tickformat: '.0%' },
              showlegend: false,
              bargap:     0.35,
            }}
          />

        </div>
      </div>
    </section>
  )
}
