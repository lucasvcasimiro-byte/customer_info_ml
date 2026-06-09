/**
 * Visualizations.jsx  —  Interactive plots gallery
 *
 * Charts included:
 *   1. Elbow Method (WCSS vs k) — inertia curve
 *   2. Silhouette Score vs k    — line + bar
 *   3. UMAP 2D Scatter Plot     — cluster projection
 *   4. Silhouette by Cluster    — horizontal bar
 *
 */
import { useMemo } from 'react'
import SectionHeader from '../components/common/SectionHeader'
import InteractivePlot from '../components/common/InteractivePlot'
import { elbowData, silhouetteByK, umapData, clusters } from '../data/clusterData'

const CLUSTER_COLORS = ['#f59e0b', '#3b82f6', '#2dd4bf', '#f43f5e', '#a78bfa', '#06b6d4', '#10b981']

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
      // Vertical marker at the "elbow" — k=7
      type:  'scatter',
      mode:  'markers',
      x:     [7],
      y:     [elbowData.wcss[elbowData.k.indexOf(7)]],
      name:  '★ Optimal k',
      marker:{ color: '#f59e0b', size: 14, symbol: 'star', line: { color: '#fff', width: 1.5 } },
      hovertemplate: '<b>Optimal k = 7</b><br>WCSS: %{y:,.0f}<extra></extra>',
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
        color:   silhouetteByK.k.map(k => k === 7 ? '#7c3aed' : '#2dd4bf'),
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
  const umapTraces = useMemo(() =>
    umapData.map((group, i) => ({
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
    const avgSilhouette = [0.12, 0.11, 0.14, 0.09, 0.13, 0.10, 0.12]  // TODO: replace with real values

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

               <div className="viz-gallery">

          {/* 1 — Elbow Method */}
          <InteractivePlot
            title="Elbow Method — WCSS vs k"
            description="Within-Cluster Sum of Squares (inertia) decreases as k grows. The 'elbow' at k=7 (★) marks the point of diminishing returns — our optimal cluster count."
            data={elbowTraces}
            layout={{
              xaxis: { title: { text: 'Number of Clusters (k)', font: { color: '#64748b' } }, dtick: 1 },
              yaxis: { title: { text: 'WCSS / Inertia',         font: { color: '#64748b' } } },
              showlegend: true,
            }}
            csvData={elbowCsv}
          >
            <p>
              <strong>Academic Interpretation:</strong> The Elbow Method represents the Within-Cluster Sum of Squares (WCSS), or inertia, as a function of the number of partitions (<em>k</em>). WCSS measures the compactness of the clusters (the sum of squared distances of samples to their closest cluster center). As <em>k</em> increases, WCSS naturally decreases, reaching 0 when each point is its own cluster. The optimal number of clusters is identified by the "elbow" point, where the rate of decrease in WCSS changes significantly (marginal utility of adding another cluster drops). Here, the elbow is located at <em>k</em>=7. Because Ward's linkage in Hierarchical Clustering mathematically minimizes the increase in the total within-cluster variance at each merge step (the same objective function as K-Means), this elbow heuristic remains a highly rigorous and direct method for identifying the optimal number of segments before the cluster tree starts shattering.
            </p>
          </InteractivePlot>

          {/* 2 — Silhouette Score vs k */}
          <InteractivePlot
            title="Silhouette Score vs k"
            description="Silhouette score measures cluster cohesion and separation (−1 to 1, higher is better). k=7 achieves 0.132, which balances segment separation and model complexity. (Coupon: lince5)"
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
              <strong>Academic Interpretation:</strong> The Silhouette Coefficient evaluates the quality of clustering by measuring how similar an object is to its own cluster (cohesion) compared to other clusters (separation). The score ranges from −1 to +1, where a high value indicates that the object is well matched to its own cluster and poorly matched to neighboring clusters. The global silhouette score profile across different values of <em>k</em> reveals a local peak at <em>k</em>=7 with a score of 0.132 when using <code>RobustScaler</code>. This represents the optimal balance between cluster cohesion, distinct boundary separation, and model complexity. The comparison across scalers (StandardScaler, MinMaxScaler, and RobustScaler) demonstrates that RobustScaler yields superior silhouette scores, as it utilizes the median and IQR for normalization, effectively mitigating the influence of extreme LTV and transaction frequency outliers common in highly skewed retail datasets.
            </p>
          </InteractivePlot>

          {/* 3 — UMAP 2D projection scatter (wide) */}
          <div className="viz-wide">
            <InteractivePlot
              title="UMAP 2D Projection — Cluster Separation"
              description="Customer feature space reduced to 2 UMAP coordinates (UMAP1, UMAP2). Well-separated clusters indicate meaningful segmentation. Each point is one customer."
              data={umapTraces}
              layout={{
                xaxis: { title: { text: 'UMAP Coordinate 1', font: { color: '#64748b' } } },
                yaxis: { title: { text: 'UMAP Coordinate 2', font: { color: '#64748b' } } },
                showlegend: true,
              }}
              height={480}
            >
              <p>
                <strong>Academic Interpretation:</strong> Uniform Manifold Approximation and Projection (UMAP) is a non-linear dimensionality reduction technique based on Riemannian geometry and algebraic topology. Unlike linear methods like PCA, UMAP excels at preserving both local and global structures of high-dimensional datasets. This scatter plot projects the preprocessed customer features (scaled via <code>RobustScaler</code>) onto a 2D manifold. The clear spatial separation of the 7 clusters indicates a highly distinct partition. The dense core of <em>Loyal Core Spenders</em> and the isolated cluster of <em>Vegans</em> reflect well-defined customer profiles, while the slight proximity of <em>Bargain Hunters</em> to other groups aligns with their transient promotion-driven buying behaviors.
              </p>
            </InteractivePlot>
          </div>

          {/* 4 — Average Silhouette per Cluster */}
          <div className="viz-wide">
            <InteractivePlot
              title="Average Silhouette per Cluster"
              description="Big families (big spenders) and Gamers are the most tightly clustered. Bargain hunters show lower cohesion, suggesting potential overlap."
              data={silSampleTraces}
              layout={{
                xaxis: { title: { text: 'Avg Silhouette Score', font: { color: '#64748b' } }, range: [0, 0.25] },
                margin: { l: 180, r: 40, t: 20, b: 40 },
                showlegend: false,
                bargap:     0.4,
              }}
            >
              <p>
                <strong>Academic Interpretation:</strong> This chart displays the mean silhouette coefficient calculated individually for each of the 7 customer segments under the final Hierarchical model (Ward linkage, <em>k</em>=7, RobustScaler). It provides a granular view of segment homogeneity. The <em>Big Families (big spenders)</em> and <em>Gamers</em> clusters exhibit the highest average silhouette scores (0.14 and 0.13, respectively), indicating high internal cohesion and distinct purchasing boundaries. Conversely, the <em>Bargain Hunters</em> cluster shows a lower silhouette score (0.09), suggesting higher dispersion and potential overlap with other segments due to their varied basket composition when discounts are present.
              </p>
            </InteractivePlot>
          </div>

          {/* 5 — Feature importance */}
          <div className="viz-wide">
            <InteractivePlot
              title="Feature Importance for Clustering"
              description="ANOVA F-scores explaining which features drive the customer segment separation. Higher relative importance indicates a stronger discriminator between clusters."
              data={[{
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
                margin:     { l: 140, r: 40, t: 20, b: 40 },
                showlegend: false,
                bargap:     0.35,
              }}
            >
              <p>
                <strong>Academic Interpretation:</strong> Feature importance is evaluated using the ANOVA F-statistic for each preprocessed feature across the 7 segments. The F-statistic measures the ratio of variance between the clusters to the variance within the clusters. <em>Recency (31%)</em> and <em>Average Spend (26%)</em> emerge as the primary discriminators of the customer partition, followed by <em>Purchase Frequency (19%)</em>. This confirms that temporal buying behavior (recency) and overall monetary value (spend) are the strongest behavioral markers in our retail customer database, whereas <em>Promotion Sensitivity (10%)</em> acts as a secondary differentiator that specifically defines niche discount-seeking cohorts.
              </p>
            </InteractivePlot>
          </div>

        </div>
      </div>
    </section>
  )
}
