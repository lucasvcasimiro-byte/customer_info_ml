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
              { label: 'K-Means Clustering', dot: '#2dd4bf' },
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
              Applying K-Means Clustering (RobustScaler, k=8) combined with an isolated Vegans segment (resulting in <strong style={{ color: 'var(--teal)' }}>9 segments</strong> in total) to the customer database of <strong style={{ color: 'var(--teal)' }}>32,571</strong> customers revealed distinct behavioral segments with a K-Means silhouette score of <strong style={{ color: 'var(--teal)' }}>0.138</strong>. Features were scaled using RobustScaler to minimize the impact of purchase frequency and LTV outliers.
            </p>
            <p>
              Basket analysis using the Apriori algorithm was subsequently run for each cluster separately, surfacing strong product affinities that can directly inform personalized promotion bundles and discount strategies.
            </p>

            <ul className="insight-list" style={{ marginTop: '1.25rem' }}>
              {[
                '27.3% of customers belong to the Average Customer segment — the largest cohort',
                '16.6% are Loyal Big Spenders — primary revenue drivers with the highest LTV',
                '13.7% are Vegans — healthy lifestyle focus, buying vegetables and organic produce (Coupon: lima5)',
                '10.7% are Karens — critical segment with the highest rate of customer complaints and churn risk',
                '7.6% are Bargain Hunters — promo-driven — higher discount sensitivity (Coupon: lince5)',
                '7.3% are Big Families — largest household size with 6+ dependants and bulk spending',
                '7.1% are Tech Enthusiasts & 3.4% are Gamers — tech-driven shopping segments',
                '6.2% are Clean and Healthy — health-focused groceries purchases',
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
