import { useState, useEffect, useRef } from 'react'

/**
 * 1. CaptchaModal ("Não sou um Robô")
 * Blocks all interactions until the user confirms they are not a robot
 * and checks three humorous conditions.
 */
export function CaptchaModal({ onClose }) {
  const [agreeML, setAgreeML] = useState(false)
  const [agreeIvo, setAgreeIvo] = useState(false)
  const [agreeWheel, setAgreeWheel] = useState(false)
  const [notRobot, setNotRobot] = useState(false)

  // Disable body scroll when open
  useEffect(() => {
    document.body.style.overflow = 'hidden'
    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [])

  const canSubmit = notRobot && agreeML && agreeIvo && agreeWheel

  return (
    <div className="modal-overlay captcha-overlay">
      <div className="modal-card captcha-card animate-in">
        <div className="captcha-header">
          <div className="captcha-shield-icon">🛡️</div>
          <h2>Security Verification</h2>
          <p>Please confirm you are a legitimate user before accessing the dashboard.</p>
        </div>

        <div className="captcha-body">
          <label className="captcha-row primary-row">
            <input
              type="checkbox"
              checked={notRobot}
              onChange={(e) => setNotRobot(e.target.checked)}
            />
            <span className="checkbox-custom" />
            <span className="label-text">I am not a robot</span>
          </label>

          {notRobot && (
            <div className="captcha-subpanel animate-slide-down">
              <p className="subpanel-title">Please verify the following additional declarations:</p>
              
              <label className="captcha-row sub-row">
                <input
                  type="checkbox"
                  checked={agreeML}
                  onChange={(e) => setAgreeML(e.target.checked)}
                />
                <span className="checkbox-custom" />
                <span className="label-text">I promise that I find the Machine Learning II course the best at NOVA IMS.</span>
              </label>

              <label className="captcha-row sub-row">
                <input
                  type="checkbox"
                  checked={agreeIvo}
                  onChange={(e) => setAgreeIvo(e.target.checked)}
                />
                <span className="checkbox-custom" />
                <span className="label-text">I acknowledge that Professor Ivo is an outstanding and motivating lecturer.</span>
              </label>

              <label className="captcha-row sub-row">
                <input
                  type="checkbox"
                  checked={agreeWheel}
                  onChange={(e) => setAgreeWheel(e.target.checked)}
                />
                <span className="checkbox-custom" />
                <span className="label-text">I am aware that the discount wheel can reward me with the 'lucas5' coupon.</span>
              </label>
            </div>
          )}
        </div>

        <div className="captcha-footer">
          <button
            className={`captcha-submit-btn ${canSubmit ? 'active' : ''}`}
            disabled={!canSubmit}
            onClick={onClose}
          >
            Access Dashboard
          </button>
        </div>
      </div>
    </div>
  )
}

/**
 * 2. WheelModal ("Roleta da Sorte")
 * Let users spin a CSS/SVG wheel for a 25% chance to win coupon code 'lucas5'.
 */
export function WheelModal({ onClose }) {
  const [isSpinning, setIsSpinning] = useState(false)
  const [rotation, setRotation] = useState(0)
  const [result, setResult] = useState(null)
  const [couponCode, setCouponCode] = useState(null)

  // 8 segments
  const slices = [
    { text: 'Try Again 😢', color: '#1e1b4b' },
    { text: 'So Close... 😭', color: '#111827' },
    { text: 'lima5? No! 🍋', color: '#0f172a' },
    { text: 'lucas5 🎉', color: '#7c3aed' }, // WINNER at index 3
    { text: 'Try Again 😢', color: '#1e1b4b' },
    { text: 'lince5? No! 🐱', color: '#0f172a' },
    { text: 'Try Again... 🔄', color: '#111827' },
    { text: 'Getting Closer... 🎯', color: '#0f172a' },
  ]

  const handleSpin = () => {
    if (isSpinning) return
    
    setIsSpinning(true)
    setResult(null)
    setCouponCode(null)

    // 25% win rate (winning index is 3)
    const isWin = Math.random() < 0.25
    const targetSlice = isWin ? 3 : [0, 1, 2, 4, 5, 6, 7][Math.floor(Math.random() * 7)]

    // Calculate rotation angle to align the chosen slice under the pointer (12 o'clock / 270 degrees in SVG coordinates)
    const targetSliceCenter = (targetSlice * 45) + 22.5
    const offset = 270 - targetSliceCenter
    
    const extraSpins = 5 * 360 // 5 full rotations
    const currentRotMod = rotation % 360
    let delta = offset - currentRotMod
    if (delta <= 0) {
      delta += 360
    }
    const targetRotation = rotation + extraSpins + delta
    
    setRotation(targetRotation)

    setTimeout(() => {
      setIsSpinning(false)
      const chosenSlice = slices[targetSlice]
      if (targetSlice === 3) {
        setResult('Congratulations! You won the discount coupon!')
        setCouponCode('lucas5')
      } else {
        setResult(`Better luck next time! It landed on: "${chosenSlice.text}"`)
      }
    }, 3200)
  }

  const copyToClipboard = () => {
    if (couponCode) {
      navigator.clipboard.writeText(couponCode)
      alert('Coupon code copied to clipboard!')
    }
  }

  const applyToCart = () => {
    if (couponCode) {
      window.dispatchEvent(new CustomEvent('apply-coupon-event', { detail: couponCode }))
      alert(`Coupon "${couponCode}" applied directly to your cart!`)
      onClose()
    }
  }

  return (
    <div className="modal-overlay">
      <div className="modal-card wheel-card animate-in">
        <button className="modal-close-btn" onClick={onClose}>✕</button>
        
        <div className="wheel-modal-header">
          <h2>🎰 Wheel of Fortune</h2>
          <p>You have a 25% chance of winning the coupon code <strong>lucas5</strong> (5% accumulative store discount!).</p>
        </div>

        <div className="wheel-container">
          <div className="wheel-pointer" />
          
          <div 
            className="wheel-canvas-wrapper"
            style={{
              transform: `rotate(${rotation}deg)`,
              transition: isSpinning ? 'transform 3s cubic-bezier(0.1, 0.8, 0.1, 1)' : 'none'
            }}
          >
            <svg viewBox="0 0 200 200" width="100%" height="100%">
              {slices.map((slice, index) => {
                const angle = 45
                const startAngle = index * angle
                const endAngle = (index + 1) * angle
                
                const rad = Math.PI / 180
                const x1 = 100 + 90 * Math.cos(startAngle * rad)
                const y1 = 100 + 90 * Math.sin(startAngle * rad)
                const x2 = 100 + 90 * Math.cos(endAngle * rad)
                const y2 = 100 + 90 * Math.sin(endAngle * rad)
                
                const pathData = `
                  M 100 100
                  L ${x1} ${y1}
                  A 90 90 0 0 1 ${x2} ${y2}
                  Z
                `
                
                const textAngle = startAngle + angle / 2
                const textRad = textAngle * rad
                const tx = 100 + 55 * Math.cos(textRad)
                const ty = 100 + 55 * Math.sin(textRad)
                
                return (
                  <g key={index}>
                    <path
                      d={pathData}
                      fill={slice.color}
                      stroke="rgba(255,255,255,0.08)"
                      strokeWidth="1"
                    />
                    <text
                      x={tx}
                      y={ty}
                      fill="#fff"
                      fontSize="5"
                      fontWeight="bold"
                      textAnchor="middle"
                      dominantBaseline="middle"
                      transform={`rotate(${textAngle}, ${tx}, ${ty})`}
                    >
                      {slice.text}
                    </text>
                  </g>
                )
              })}
              <circle cx="100" cy="100" r="14" fill="#0d1128" stroke="var(--border-soft)" strokeWidth="2" />
              <circle cx="100" cy="100" r="8" fill="var(--amber)" />
            </svg>
          </div>
        </div>

        <div className="wheel-actions">
          <button
            className="spin-button"
            onClick={handleSpin}
            disabled={isSpinning}
          >
            {isSpinning ? 'Spinning...' : 'SPIN WHEEL'}
          </button>
        </div>

        {result && (
          <div className={`wheel-result-box ${couponCode ? 'win' : 'lose'} animate-in`}>
            {couponCode ? (
              <>
                <p className="result-title">🎉 Congratulations! You won!</p>
                <p className="result-text">You discovered the special coupon code <strong>{couponCode}</strong>!</p>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
                  This code grants an extra 5% accumulative discount on our virtual store.
                </p>
                <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'center' }}>
                  <button className="copy-btn" onClick={copyToClipboard}>
                    📋 Copy Code
                  </button>
                  <button className="apply-btn" onClick={applyToCart}>
                    🛒 Apply to Cart
                  </button>
                </div>
              </>
            ) : (
              <>
                <p className="result-title">😢 {result}</p>
                <p className="result-text">You can try spinning the wheel again to win the discount!</p>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

/**
 * 3. SupportModal ("Apoio ao Cliente")
 * FAQ chat window with artificial typing delays.
 */
export function SupportModal({ onClose }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'agent',
      text: 'Hello! I am the virtual assistant for ClusterNova. How can I help you today? 😊',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ])
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)

  const faqs = [
    {
      q: 'How does clustering work in ClusterNova?',
      a: 'ClusterNova utilizes the Hierarchical Clustering algorithm (with Ward linkage) to group customers based on purchase behavior metrics like frequency and total spend. This helps segment customers into distinct behavioral profiles (like "Vegans" or "Loyal Core Spenders"), enabling targeted marketing campaigns.'
    },
    {
      q: 'What is the optimal number of clusters (k)?',
      a: 'Based on the Silhouette Score and WCSS (elbow method) analyses, the optimal value chosen for this dataset was k=7. This balances internal cohesion (compactness) with clear group boundaries.'
    },
    {
      q: 'How was data preprocessing and cleaning handled?',
      a: 'We cleaned records with null or logically inconsistent variables in our EDA notebooks. We also identified and removed wholesale/business accounts acting as LTV outliers, ensuring the model focuses strictly on end-consumers.'
    },
    {
      q: 'Why did you select RobustScaler to scale features?',
      a: 'Since purchase histories and lifetime spend have highly skewed distributions with long tails, StandardScaler would be heavily distorted by outliers. RobustScaler scales features using the median and Interquartile Range (IQR), mitigating the impact of large outliers.'
    },
    {
      q: 'How does UMAP dimensionality reduction work in this project?',
      a: 'We utilized UMAP to project our 10+ scaled RFM and demographic dimensions onto a 2D coordinate space. This allowed us to plot the scatter visualization in the gallery, revealing the true topological layout of the segments.'
    },
    {
      q: 'How do the Apriori Association Rules work?',
      a: 'We ran the Apriori algorithm separately for each cluster in our basket analysis notebooks. By tuning minimum support and confidence thresholds per segment (e.g. 2% support for Loyal Core, but 0.4% for Gamers), we extracted high-lift associations (such as "Airpods -> Iphone") to drive our cross-selling engine.'
    },
    {
      q: 'Who are the creators of this project?',
      a: 'This project was designed and built by three Data Science undergraduate students at NOVA IMS: Afonso Lince, Lourenço Lima, and Lucas Casemiro, merging advanced statistical modeling with modern web design.'
    },
    {
      q: 'Will Professor Ivo give us a 20/20 grade?',
      a: 'We certainly hope so! We went far beyond the basic requirements: implementing Hierarchical clustering, segment-decoupled basket analysis, a live simulated store, hidden promo codes, the wheel of fortune, and this interactive support chat. Hopefully, the effort is well rewarded! 😉'
    },
    {
      q: 'How do the discount coupons work?',
      a: 'You can find special codes hidden across the dashboard (there is one in the Overview and another in the Visualizations). The wheel code is "lucas5". Each coupon code grants an extra 5% discount that can be stacked up to 15% off at checkout!'
    }
  ]

  // Auto-scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const handleSendQuestion = (faq) => {
    if (isTyping) return

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: faq.q,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
    setMessages(prev => [...prev, userMsg])
    setIsTyping(true)

    // Simulate typing delay
    setTimeout(() => {
      setIsTyping(false)
      const agentMsg = {
        id: Date.now() + 1,
        sender: 'agent',
        text: faq.a,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
      setMessages(prev => [...prev, agentMsg])
    }, 1200)
  }

  return (
    <div className="modal-overlay">
      <div className="modal-card chat-card animate-in">
        <button className="modal-close-btn" onClick={onClose}>✕</button>

        <div className="chat-header">
          <div className="chat-avatar">🤖</div>
          <div>
            <h3>Customer Support</h3>
            <span className="chat-status"><span className="status-dot" /> Online</span>
          </div>
        </div>

        <div className="chat-messages">
          {messages.map((msg) => (
            <div key={msg.id} className={`chat-bubble-wrapper ${msg.sender}`}>
              <div className="chat-bubble">
                <p>{msg.text}</p>
                <span className="chat-time">{msg.time}</span>
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="chat-bubble-wrapper agent">
              <div className="chat-bubble typing">
                <span className="dot" />
                <span className="dot" />
                <span className="dot" />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-faq-list">
          <p className="faq-title">Select a frequently asked question:</p>
          <div className="faq-buttons">
            {faqs.map((faq, i) => (
              <button
                key={i}
                className="faq-btn"
                disabled={isTyping}
                onClick={() => handleSendQuestion(faq)}
              >
                {faq.q}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

/**
 * 4. AboutUsModal ("Sobre Nós")
 * Team biographies and appreciation of the ML2 course and Prof. Ivo.
 */
export function AboutUsModal({ onClose }) {
  const students = [
    {
      name: 'Lucas Casemiro',
      role: 'ML & Basket Engineer',
      desc: 'The brain behind the association rules. Spent nights tuning the Apriori algorithm to ensure vegan/vegetarian customers wouldn\'t get suggested sausages... unless they were soy sausages!',
      color: 'var(--purple)'
    },
    {
      name: 'Lourenço Lima',
      role: 'Data & Analytics Guru',
      desc: 'The master of interactive plots. Projected the UMAP coordinates onto 2D interactive charts so anyone can visualize the core distribution of our customer segments.',
      color: 'var(--teal)'
    },
    {
      name: 'Afonso Lince',
      role: 'UX & Frontend Architect',
      desc: 'The interaction designer. Added the wheel of fortune, the anti-bot captcha, and the support chat to prove that Data Science and UI/UX design go hand in hand.',
      color: 'var(--amber)'
    }
  ]

  return (
    <div className="modal-overlay">
      <div className="modal-card about-card animate-in" style={{ maxWidth: '650px' }}>
        <button className="modal-close-btn" onClick={onClose}>✕</button>

        <div className="about-header">
          <h2>👥 About Us</h2>
          <p>The team behind ClusterNova — Bachelor's in Data Science at NOVA IMS.</p>
        </div>

        <div className="about-grid">
          {students.map((student, i) => (
            <div key={i} className="student-card" style={{ borderColor: `${student.color}33` }}>
              <div className="student-avatar" style={{ background: `${student.color}15`, color: student.color }}>
                {student.name.charAt(0)}
              </div>
              <h3 style={{ color: student.color }}>{student.name}</h3>
              <span className="student-role">{student.role}</span>
              <p>{student.desc}</p>
            </div>
          ))}
        </div>

        <div className="about-dedication">
          <h4>🏫 Machine Learning II</h4>
          <p>
            Special thanks to <strong>Professor Ivo</strong> for his dedication, academic rigor, and the
            continuous challenge that pushed us to elevate this practical project to a professional standard of software engineering and data analytics.
          </p>
        </div>
      </div>
    </div>
  )
}
