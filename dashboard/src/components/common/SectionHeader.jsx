/**
 * SectionHeader.jsx
 * Reusable section heading with badge, title, and subtitle.
 * Props: { badge, badgeClass, title, highlight, subtitle }
 * highlight is the part of title rendered in gradient colour.
 */
export default function SectionHeader({ badge, badgeClass = 'badge-purple', title, highlight, subtitle }) {
  // Split the title around the highlighted word so we can colour it
  const parts = highlight ? title.split(highlight) : [title]

  return (
    <div className="section-header">
      {badge && <span className={`badge ${badgeClass}`}>{badge}</span>}
      <h2>
        {parts[0]}
        {highlight && <span className="gradient-text">{highlight}</span>}
        {parts[1]}
      </h2>
      {subtitle && <p>{subtitle}</p>}
    </div>
  )
}
