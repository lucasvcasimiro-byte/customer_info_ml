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
import { CaptchaModal, WheelModal, SupportModal, AboutUsModal } from './components/InteractiveModals'
import EvaluationForm from './components/EvaluationForm'

// Section IDs must match the ids used in CartNavigation
const SECTION_IDS = ['overview', 'clustering', 'visualizations', 'promotions', 'store']

export default function App() {
  // One ref per section, keyed by section id
  const sectionRefs = useRef(
    Object.fromEntries(SECTION_IDS.map(id => [id, { current: null }]))
  )

  const [activeSection, setActiveSection] = useState('overview')
  // Shared voucher state — set by Promotions, consumed by Store
  const [activeVoucher, setActiveVoucher] = useState(null)

  // Interactive header modal states
  const [showCaptcha, setShowCaptcha] = useState(true)
  const [showWheel,     setShowWheel]     = useState(false)
  const [showSupport,   setShowSupport]   = useState(false)
  const [showAbout,     setShowAbout]     = useState(false)

  const handleSectionChange = useCallback((id) => {
    setActiveSection(id)
    window.scrollTo({ top: 0, behavior: 'instant' })
  }, [])

  return (
    <div id="app">
      <CartNavigation
        onNavigate={handleSectionChange}
        activeSection={activeSection}
        onOpenWheel={() => setShowWheel(true)}
        onOpenSupport={() => setShowSupport(true)}
        onOpenAbout={() => setShowAbout(true)}
      />

      <main style={{ paddingTop: '68px' }}>
        {activeSection === 'overview' && <Overview />}
        {activeSection === 'clustering' && <Clustering />}
        {activeSection === 'visualizations' && <Visualizations />}
        {activeSection === 'promotions' && <Promotions onVoucherChange={setActiveVoucher} />}
        {activeSection === 'store' && <Store activeVoucher={activeVoucher} />}
        <EvaluationForm />
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
            ⬡ ClusterNova
          </span>
        </div>
        <p>Customer Segmentation Dashboard · Machine Learning 2 · NOVA IMS</p>
        <p style={{ marginTop: '0.25rem' }}>
          Built with React + Vite · Plotly.js · Real notebook exports from ClusterNova
        </p>
      </footer>

      {/* ── Modals ── */}
      {showCaptcha && <CaptchaModal onClose={() => setShowCaptcha(false)} />}
      {showWheel && <WheelModal onClose={() => setShowWheel(false)} />}
      {showSupport && <SupportModal onClose={() => setShowSupport(false)} />}
      {showAbout && <AboutUsModal onClose={() => setShowAbout(false)} />}
    </div>
  )
}
