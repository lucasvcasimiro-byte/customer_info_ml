/**
 * Overview.jsx  —  Executive Summary section
 *
 * Shows:
 *   • Hero headline with animated gradient text
 *   • Tech-stack pills
 *   • KPI metric cards
 *   • Written project summary
 */
import KPICard from '../components/common/KPICard'
import SectionHeader from '../components/common/SectionHeader'
import { kpiData } from '../data/clusterData'

export default function Overview() {
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
              { label: 'Hierarchical Clustering', dot: '#2dd4bf' },
              { label: 'Apriori / mlxtend',     dot: '#f59e0b' },
              { label: 'RobustScaler scaling',  dot: '#3b82f6' },
              { label: 'Silhouette Analysis',    dot: '#f43f5e' },
            ].map(p => (
              <div key={p.label} className="hero-pill">
                <span className="hero-pill-dot" style={{ background: p.dot }} />
                {p.label}
              </div>
            ))}
          </div>
        </div>

        {/* Academic Data Lineage Warning Notice */}
        <div className="placeholder-notice animate-in" style={{
          padding: '1.25rem 1.5rem',
          marginBottom: '2.5rem',
          display: 'flex',
          alignItems: 'flex-start',
          gap: '0.75rem',
          background: 'rgba(245, 158, 11, 0.05)',
          border: '1px solid rgba(245, 158, 11, 0.2)'
        }}>
          <span style={{ fontSize: '1.25rem', marginTop: '-2px' }}>⚠️</span>
          <div>
            <strong>Data Lineage Notice:</strong> While customer transaction histories, segment sizes, and association rules represent real metrics computed directly from the dataset, the individual customer demographic cards, Value Scores, and customer service complaint status are synthesized parameters generated to enrich the interactive simulator experience.
          </div>
        </div>

        {/* ── KPI Cards ──────────────────────────────────────────── */}
        <div className="overview-kpis" style={{ marginBottom: '2rem' }}>
          <div className="grid-4" style={{ gridTemplateColumns: 'repeat(5, 1fr)' }}>
            {kpiData.map((kpi, i) => (
              <div key={kpi.id} className="animate-in" style={{ animationDelay: `${i * 0.05}s` }}>
                <KPICard {...kpi} />
              </div>
            ))}
          </div>
        </div>

        <div className="divider" />

        {/* ── Overview insight row ───────────────────────────────── */}
        <div className="overview-insight" style={{ gridTemplateColumns: '1fr' }}>

          {/* Left: written summary */}
          <div className="insight-text card animate-in delay-1" style={{ width: '100%' }}>
            <SectionHeader
              badge="📋 Executive Summary"
              title="What we "
              highlight="discovered"
              subtitle=""
            />
            <p>
              Applying Hierarchical Clustering (Ward linkage, k=7, RobustScaler) to the customer database of <strong style={{ color: 'var(--teal)' }}>32,571</strong> customers revealed seven distinct behavioral segments with a silhouette score of <strong style={{ color: 'var(--teal)' }}>0.132</strong> — balancing segment cohesion and model complexity. Features were scaled using RobustScaler to minimize the impact of purchase frequency and lifetime value outliers.
            </p>
            <p>
              Basket analysis using the Apriori algorithm was subsequently run for each cluster separately, surfacing strong product affinities (with lift scores reaching up to <strong style={{ color: 'var(--teal)' }}>9.15×</strong>) that can directly inform personalized promotion bundles and discount strategies.
            </p>

            <ul className="insight-list" style={{ marginTop: '1.25rem' }}>
              {[
                '35.6% of customers are Loyal Core Spenders — the largest segment and primary revenue drivers',
                '20.4% are Vegans — healthy lifestyle focus, buying vegetables and organic produce (Coupon: lima5)',
                '17.4% are Bargain Hunters — promo-driven — higher complaints & promotion focus',
                '9.6% are Karens — critical segment with the highest rate of customer complaints and churn risk',
                '6.7% are Tech Enthusiasts & 3.8% are Gamers — evening shoppers buying electronics and entertainment',
                '6.5% are Big Families — high transaction variety and largest dependants count',
                'Airpods + Iphone 10 → Energy Drink + Bluetooth Headphones: highest lift rule at 9.15×',
              ].map(item => (
                <li key={item}>
                  <span className="insight-check">✓</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

      </div>
    </section>
  )
}
