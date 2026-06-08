/**
 * KPICard.jsx
 * Metric card shown in the Overview section.
 * Props: { id, label, value, change, trend, icon, color }
 * color: 'purple' | 'teal' | 'amber' | 'rose' | 'blue'
 */
export default function KPICard({ label, value, change, trend, icon, color = 'purple' }) {
  const trendClass = trend === 'up' ? 'up' : trend === 'down' ? 'down' : ''
  const trendArrow = trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'

  return (
    <div className={`kpi-card kpi-card-${color}`}>
      {/* Icon */}
      <div
        className="kpi-icon"
        style={{ background: iconBg[color] }}
        aria-hidden="true"
      >
        {icon}
      </div>

      {/* Value */}
      <div className="kpi-value" style={{ color: accentColor[color] }}>
        {value}
      </div>

      {/* Label */}
      <div className="kpi-label">{label}</div>

      {/* Change indicator */}
      {change && (
        <span className={`kpi-change ${trendClass}`}>
          {trendClass && <span>{trendArrow}</span>}
          {change}
        </span>
      )}
    </div>
  )
}

const accentColor = {
  purple: 'var(--purple-light)',
  teal:   'var(--teal)',
  amber:  'var(--amber)',
  rose:   'var(--rose-light)',
  blue:   'var(--blue-light)',
}

const iconBg = {
  purple: 'rgba(124,58,237,0.18)',
  teal:   'rgba(45,212,191,0.15)',
  amber:  'rgba(245,158,11,0.15)',
  rose:   'rgba(244,63,94,0.15)',
  blue:   'rgba(59,130,246,0.15)',
}
