/**
 * CartNavigation.jsx
 * Shopping-cart icon (top-right) that expands into a slide-in navigation drawer.
 * Each link smoothly scrolls to the corresponding section via the onNavigate callback.
 */
import { useState, useRef, useEffect } from 'react'

const sections = [
  {
    id: 'overview',
    label: 'Executive Summary',
    desc: 'Key metrics & dataset overview',
    emoji: '📊',
    bg: 'rgba(124,58,237,0.18)',
  },
  {
    id: 'clustering',
    label: 'Clustering Analysis',
    desc: 'Segment exploration & controls',
    emoji: '🔮',
    bg: 'rgba(45,212,191,0.15)',
  },
  {
    id: 'visualizations',
    label: 'Visualizations',
    desc: 'Interactive charts & plots',
    emoji: '📈',
    bg: 'rgba(59,130,246,0.15)',
  },
  {
    id: 'promotions',
    label: 'Promotions & Basket',
    desc: 'Association rules & discounts',
    emoji: '🛍️',
    bg: 'rgba(245,158,11,0.15)',
  },
  {
    id: 'store',
    label: 'Loja NOVAIMS Grocery',
    desc: 'Carrinho de compras com voucher',
    emoji: '🛒',
    bg: 'rgba(192,57,43,0.15)',
  },
  {
    id: 'future',
    label: 'Future Analysis',
    desc: 'Upcoming features & roadmap',
    emoji: '🚀',
    bg: 'rgba(244,63,94,0.12)',
  },
]

export default function CartNavigation({ onNavigate, activeSection, onOpenWheel, onOpenSupport, onOpenAbout }) {
  const [isOpen, setIsOpen] = useState(false)
  const drawerRef = useRef(null)

  // Close drawer when clicking outside
  useEffect(() => {
    const handleOutsideClick = (e) => {
      if (drawerRef.current && !drawerRef.current.contains(e.target)) {
        setIsOpen(false)
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleOutsideClick)
    }
    return () => document.removeEventListener('mousedown', handleOutsideClick)
  }, [isOpen])

  // Close on Escape
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') setIsOpen(false)
    }
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [])

  const handleNavigate = (id) => {
    onNavigate(id)
    setIsOpen(false)
  }

  return (
    <>
      {/* ── Top navigation bar ── */}
      <header className="nav-header">
        {/* Logo */}
        <div className="nav-logo">
          <div className="nav-logo-hexagon" aria-hidden="true" />
          <span>SegmentIQ</span>
        </div>

        {/* Active section indicator */}
        <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
          {activeSection && (
            <span style={{
              fontSize: '0.8rem',
              color: 'var(--text-muted)',
              fontWeight: 500,
              letterSpacing: '0.05em',
            }}>
              {sections.find(s => s.id === activeSection)?.emoji}{' '}
              {sections.find(s => s.id === activeSection)?.label}
            </span>
          )}
        </div>

        {/* Header navigation actions */}
        <div className="header-nav-actions" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginRight: '0.75rem' }}>
          <HeaderButton onClick={onOpenWheel} label="Roleta" emoji="🎰" />
          <HeaderButton onClick={onOpenSupport} label="Apoio" emoji="💬" />
          <HeaderButton onClick={onOpenAbout} label="Sobre Nós" emoji="👥" />
        </div>

        {/* Cart / Menu button */}
        <button
          id="nav-cart-btn"
          className={`cart-btn${isOpen ? ' active' : ''}`}
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Open navigation menu"
          aria-expanded={isOpen}
        >
          <CartIcon />
          <span className="cart-badge">{sections.length}</span>
        </button>
      </header>

      {/* ── Dark overlay ── */}
      <div
        className={`nav-overlay${isOpen ? ' visible' : ''}`}
        onClick={() => setIsOpen(false)}
        aria-hidden="true"
      />

      {/* ── Slide-in drawer ── */}
      <nav
        ref={drawerRef}
        className={`nav-drawer${isOpen ? ' open' : ''}`}
        aria-label="Main navigation"
      >
        {/* Drawer header */}
        <div className="nav-drawer-header">
          <h3>Navigate</h3>
          <button
            className="close-btn"
            onClick={() => setIsOpen(false)}
            aria-label="Close navigation"
          >
            ✕
          </button>
        </div>

        {/* Section links */}
        <ul className="nav-list">
          {sections.map((section, i) => (
            <li
              key={section.id}
              style={{
                animation: isOpen
                  ? `fadeInUp 0.35s ease both ${i * 0.07}s`
                  : 'none',
              }}
            >
              <button
                className="nav-link"
                id={`nav-link-${section.id}`}
                onClick={() => handleNavigate(section.id)}
                aria-current={activeSection === section.id ? 'page' : undefined}
                style={
                  activeSection === section.id
                    ? { background: 'var(--bg-card)', borderColor: 'var(--border-soft)', color: 'var(--text-primary)' }
                    : {}
                }
              >
                {/* Icon */}
                <div
                  className="nav-link-icon-wrapper"
                  style={{ background: section.bg }}
                >
                  {section.emoji}
                </div>

                {/* Text */}
                <div className="nav-link-content">
                  <span className="nav-link-label">{section.label}</span>
                  <span className="nav-link-desc">{section.desc}</span>
                </div>

                {/* Arrow */}
                <span className="nav-link-arrow" aria-hidden="true">→</span>
              </button>
            </li>
          ))}
        </ul>

        {/* Footer */}
        <div className="nav-drawer-footer">
          <span>⬡</span>
          <span>SegmentIQ · Customer Analytics</span>
        </div>
      </nav>
    </>
  )
}

/** Shopping cart SVG icon */
function CartIcon() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <circle cx="8"  cy="21" r="1" />
      <circle cx="19" cy="21" r="1" />
      <path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12" />
    </svg>
  )
}

function HeaderButton({ onClick, label, emoji }) {
  const [hover, setHover] = useState(false)
  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        background: hover ? 'var(--accent-primary)' : 'rgba(255,255,255,0.06)',
        border: hover ? '1px solid var(--accent-primary)' : '1px solid rgba(255,255,255,0.12)',
        color: hover ? '#fff' : '#e2e8f0',
        borderRadius: '20px',
        padding: '0.4rem 0.85rem',
        fontSize: '0.82rem',
        fontWeight: 600,
        cursor: 'pointer',
        transition: 'all 0.2s',
        boxShadow: hover ? '0 0 10px rgba(124,58,237,0.3)' : 'none',
        display: 'flex',
        alignItems: 'center',
        gap: '0.35rem',
      }}
    >
      <span>{emoji}</span>
      <span className="header-btn-text">{label}</span>
    </button>
  )
}
