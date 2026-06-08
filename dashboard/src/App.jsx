/**
 * App.jsx  —  Root application component
 *
 * Responsibilities:
 *   • Renders the fixed CartNavigation (cart icon + drawer)
 *   • Renders all five sections in order
 *   • Provides smooth-scroll navigation via section refs
 *   • Tracks which section is currently visible (IntersectionObserver)
 *     so the nav bar can show the active section name
 */
import { useRef, useState, useEffect, useCallback } from 'react'
import CartNavigation from './components/Navigation/CartNavigation'
import Overview       from './sections/Overview'
import Clustering     from './sections/Clustering'
import Visualizations from './sections/Visualizations'
import Promotions     from './sections/Promotions'
import Store          from './sections/Store'
import Future         from './sections/Future'

// Section IDs must match the ids used in CartNavigation
const SECTION_IDS = ['overview', 'clustering', 'visualizations', 'promotions', 'store', 'future']

export default function App() {
  // One ref per section, keyed by section id
  const sectionRefs = useRef(
    Object.fromEntries(SECTION_IDS.map(id => [id, { current: null }]))
  )

  const [activeSection, setActiveSection] = useState('overview')
  // Shared voucher state — set by Promotions, consumed by Store
  const [activeVoucher, setActiveVoucher] = useState(null)

  // ── Smooth scroll to a section ──────────────────────────────────
  const scrollToSection = useCallback((id) => {
    const el = document.getElementById(id)
    if (el) {
      // Offset for the fixed nav bar (~68px)
      const y = el.getBoundingClientRect().top + window.scrollY - 68
      window.scrollTo({ top: y, behavior: 'smooth' })
    }
  }, [])

  // ── Track active section with IntersectionObserver ───────────────
  useEffect(() => {
    const observers = []

    SECTION_IDS.forEach(id => {
      const el = document.getElementById(id)
      if (!el) return

      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) setActiveSection(id)
        },
        { threshold: 0.25, rootMargin: '-68px 0px 0px 0px' }
      )
      observer.observe(el)
      observers.push(observer)
    })

    return () => observers.forEach(o => o.disconnect())
  }, [])

  return (
    <div id="app">
      {/* Fixed navigation — cart icon in top-right */}
      <CartNavigation
        onNavigate={scrollToSection}
        activeSection={activeSection}
      />

      {/* Main content — sections stacked vertically */}
      <main style={{ paddingTop: '68px' }}>
        <Overview />
        <Clustering />
        <Visualizations />
        <Promotions onVoucherChange={setActiveVoucher} />
        <Store activeVoucher={activeVoucher} />
        <Future />
      </main>

      {/* ── Footer ── */}
      <footer style={{
        background:   'var(--bg-surface)',
        borderTop:    '1px solid var(--border-subtle)',
        padding:      '2rem',
        textAlign:    'center',
        fontSize:     '0.8rem',
        color:        'var(--text-muted)',
      }}>
        <div style={{ marginBottom: '0.5rem' }}>
          <span style={{ fontFamily: 'var(--font-display)', fontWeight: 700, color: 'var(--text-secondary)' }}>
            ⬡ SegmentIQ
          </span>
        </div>
        <p>Customer Segmentation Dashboard · Machine Learning 2 · NOVA IMS</p>
        <p style={{ marginTop: '0.25rem' }}>
          Built with React + Vite · Plotly.js · Placeholder data — replace with real notebook exports
        </p>
      </footer>
    </div>
  )
}
