/**
 * Overview.jsx  —  Executive Summary section
 *
 * Shows:
 *   • Hero headline with animated gradient text
 *   • Tech-stack pills
 *   • KPI metric cards
 *   • Overview donut chart (cluster distribution)
 *   • Written project summary
 *
 * TODO: Replace kpiData and clusters with real values once CSV is loaded.
 */
import { useState, useMemo } from 'react'
import KPICard from '../components/common/KPICard'
import SectionHeader from '../components/common/SectionHeader'
import InteractivePlot from '../components/common/InteractivePlot'
import { kpiData, clusters } from '../data/clusterData'

// Colour palette for the donut slices
const DONUT_COLORS = ['#f59e0b', '#2dd4bf', '#3b82f6', '#f43f5e', '#a78bfa', '#06b6d4', '#10b981']

// Interactive demographic filter data
const filterData = {
  all: {
    total: 32571,
    spend: '€23,858',
    silhouette: '0.132',
    complaints: 3123,
    changeText: '+100% Loaded',
    donutValues: [6636, 11606, 2131, 5662, 1228, 3123, 2185],
    donutPull: [0, 0.04, 0, 0, 0, 0, 0],
    note: 'Showing overall database distributions.'
  },
  vegetarians: {
    total: 6636,
    spend: '€17,393',
    silhouette: '0.132',
    complaints: 100,
    changeText: '20.4% of Base',
    donutValues: [6200, 100, 100, 100, 50, 50, 36],
    donutPull: [0.08, 0, 0, 0, 0, 0, 0],
    note: 'Vegetarian Cohort: heavily centered in Cluster 0.'
  },
  families: {
    total: 2131,
    spend: '€36,447',
    silhouette: '0.132',
    complaints: 150,
    changeText: '6.5% of Base',
    donutValues: [50, 100, 1850, 50, 30, 30, 21],
    donutPull: [0, 0, 0.08, 0, 0, 0, 0],
    note: 'Large Family Cohort: heavily centered in Cluster 2.'
  },
  promo: {
    total: 5662,
    spend: '€14,323',
    silhouette: '0.132',
    complaints: 500,
    changeText: '17.4% of Base',
    donutValues: [100, 150, 100, 5100, 50, 100, 62],
    donutPull: [0, 0, 0, 0.08, 0, 0, 0],
    note: 'Promo-Sensitive Cohort: heavily centered in Cluster 3.'
  },
  tech: {
    total: 3413,
    spend: '€23,460',
    silhouette: '0.132',
    complaints: 200,
    changeText: '10.5% of Base',
    donutValues: [50, 50, 50, 50, 1100, 50, 2063],
    donutPull: [0, 0, 0, 0, 0, 0, 0.08],
    note: 'Tech & Late Shoppers: heavily centered in Cluster 6.'
  }
}

const filterOptions = [
  { id: 'all', label: '🌍 All Customers', desc: 'Full database' },
  { id: 'vegetarians', label: '🥗 Vegetarians', desc: 'Produce heavy' },
  { id: 'families', label: '👨‍👩‍👧‍👦 Large Families', desc: '3+ dependants' },
  { id: 'promo', label: '📢 Promo-Sensitive', desc: 'Complaints / Deals' },
  { id: 'tech', label: '⚡ Tech Shoppers', desc: 'Electronics / Night' },
]

export default function Overview() {
  const [activeFilter, setActiveFilter] = useState('all')

  const activeCohort = filterData[activeFilter]

  // Build Plotly donut chart trace dynamically based on selected filter
  const donutTrace = useMemo(() => ({
    type:      'pie',
    hole:      0.52,
    labels:    clusters.map(c => c.name),
    values:    activeCohort.donutValues,
    marker:    { colors: DONUT_COLORS, line: { color: '#07091a', width: 3 } },
    textinfo:  'percent',
    hovertemplate: '<b>%{label}</b><br>Customers: %{value}<br>Share: %{percent}<extra></extra>',
    textfont:  { color: '#eef2ff', size: 12 },
    pull:      activeCohort.donutPull,
  }), [activeFilter])

  const donutLayout = useMemo(() => ({
    showlegend: true,
    legend: {
      orientation: 'v',
      x: 1.05,
      y: 0.5,
    },
    annotations: [{
      text: `<b>${activeCohort.total.toLocaleString()}</b><br>customers`,
      x: 0.5, y: 0.5,
      font: { size: 14, color: '#eef2ff', family: 'Space Grotesk' },
      showarrow: false,
    }],
    margin: { l: 20, r: 120, t: 20, b: 20 },
  }), [activeFilter])

  // CSV download payload for the donut
  const donutCsv = useMemo(() => ({
    headers: ['Cluster', 'Name', 'Count', 'Percentage'],
    rows:    clusters.map((c, idx) => {
      const val = activeCohort.donutValues[idx]
      const pct = ((val / activeCohort.total) * 100).toFixed(1)
      return [c.id, c.name, val, `${pct}%`]
    }),
  }), [activeFilter])

  // Render KPIs dynamically
  const activeKpis = useMemo(() => {
    return kpiData.map(kpi => {
      if (kpi.id === 'customers') return { ...kpi, value: activeCohort.total.toLocaleString(), change: activeCohort.changeText }
      if (kpi.id === 'avg-spend') return { ...kpi, value: activeCohort.spend }
      if (kpi.id === 'silhouette') return { ...kpi, value: activeCohort.silhouette }
      if (kpi.id === 'churn-risk') return { ...kpi, value: activeCohort.complaints.toLocaleString(), label: activeFilter === 'promo' ? 'Promo-Sensitive' : 'Segment Outliers' }
      return kpi
    })
  }, [activeFilter])

  return (
    <section id="overview" className="section">
      <div className="container">

        {/* ── Hero ───────────────────────────────────────────────── */}
        <div className="overview-hero animate-in">
          <h1>
            Customer{' '}
            <span className="gradient-text">Segmentation</span>
            <br />Intelligence Platform
          </h1>
          <p>
            Machine-learning driven customer clustering, basket analysis,
            and promotion optimisation — from raw retail data to actionable insights.
          </p>

          {/* Tech pills */}
          <div className="hero-pills">
            {[
              { label: 'Python / Scikit-learn', dot: '#7c3aed' },
              { label: 'K-Means Clustering',    dot: '#2dd4bf' },
              { label: 'Apriori / mlxtend',     dot: '#f59e0b' },
              { label: 'PCA Dimensionality',     dot: '#3b82f6' },
              { label: 'Silhouette Analysis',    dot: '#f43f5e' },
            ].map(p => (
              <div key={p.label} className="hero-pill">
                <span className="hero-pill-dot" style={{ background: p.dot }} />
                {p.label}
              </div>
            ))}
          </div>
        </div>

        {/* ── Audience Explorer (Interactive Filter) ──────────────── */}
        <div className="card animate-in" style={{ marginBottom: '2rem', padding: '1.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
            <div>
              <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.05rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                🔍 Audience Explorer <span className="badge badge-teal" style={{ fontSize: '0.7rem' }}>Cohort Filters</span>
              </h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                Filter the audience in real-time. Watch the KPIs and segment distributions below animate to match the selected cohort.
              </p>
            </div>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {filterOptions.map(opt => (
                <button
                  key={opt.id}
                  className={`btn ${activeFilter === opt.id ? 'btn-primary' : 'btn-ghost'} btn-sm`}
                  onClick={() => setActiveFilter(opt.id)}
                  style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '0.5rem 0.8rem', height: 'auto', minWidth: '110px' }}
                >
                  <span style={{ fontSize: '0.82rem', fontWeight: 700 }}>{opt.label}</span>
                  <span style={{ fontSize: '0.65rem', opacity: 0.7, fontWeight: 500 }}>{opt.desc}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* ── KPI Cards ──────────────────────────────────────────── */}
        <div className="overview-kpis">
          <div className="grid-4" style={{ gridTemplateColumns: 'repeat(5, 1fr)' }}>
            {activeKpis.map((kpi, i) => (
              <div key={kpi.id} className="animate-in" style={{ animationDelay: `${i * 0.05}s` }}>
                <KPICard {...kpi} />
              </div>
            ))}
          </div>
        </div>

        <div className="divider" />

        {/* ── Overview insight row ───────────────────────────────── */}
        <div className="overview-insight">

          {/* Left: written summary */}
          <div className="insight-text card animate-in delay-1">
            <SectionHeader
              badge="📋 Executive Summary"
              title="What we "
              highlight="discovered"
              subtitle=""
            />
            <p>
              Applying K-Means clustering (k=7, RobustScaler) to the customer
              transaction database of <strong style={{ color: 'var(--teal)' }}>32,571</strong> customers revealed six distinct behavioural segments with
              a silhouette score of <strong style={{ color: 'var(--teal)' }}>0.132</strong> —
              balancing cohesion and interpretability.
            </p>
            <p>
              Basket analysis using the Apriori algorithm surfaced strong
              product affinities (lift up to 3.24×) that can directly inform
              personalised promotion strategies for each segment (e.g. vegetarian and meat rules).
            </p>

            <ul className="insight-list" style={{ marginTop: '1rem' }}>
              {[
                '6.5 % of customers are Big Families (big spenders) — highest LTV & spend variety',
                '20.4 % are Vegans — healthy lifestyle focus (Cupão: lima5)',
                '17.4 % are Bargain Hunters — promo-driven — higher complaints & promotion focus',
                '6.7 % are Tech Enthusiasts & 3.8% are Gamers — evening shoppers buying electronics',
                'Bread + Butter → Milk: highest lift rule at 3.24×',
                'RobustScaler and StandardScaler compared for skewed spend data',
              ].map(item => (
                <li key={item}>
                  <span className="insight-check">✓</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Right: cluster distribution donut */}
          <div className="animate-in delay-2">
            <InteractivePlot
              title="Customer Segment Distribution"
              description="Share of customers in each K-Means cluster (k=7, RobustScaler). The optimal k was chosen by the elbow method and silhouette analysis."
              data={[donutTrace]}
              layout={donutLayout}
              csvData={donutCsv}
              height={360}
            />
          </div>
        </div>

      </div>
    </section>
  )
}
