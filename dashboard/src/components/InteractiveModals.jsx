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
          <h2>Verificação de Segurança</h2>
          <p>Confirme que é um utilizador legítimo antes de aceder ao painel.</p>
        </div>

        <div className="captcha-body">
          <label className="captcha-row primary-row">
            <input
              type="checkbox"
              checked={notRobot}
              onChange={(e) => setNotRobot(e.target.checked)}
            />
            <span className="checkbox-custom" />
            <span className="label-text">Não sou um Robô (I am not a robot)</span>
          </label>

          {notRobot && (
            <div className="captcha-subpanel animate-slide-down">
              <p className="subpanel-title">Verifique as seguintes declarações adicionais:</p>
              
              <label className="captcha-row sub-row">
                <input
                  type="checkbox"
                  checked={agreeML}
                  onChange={(e) => setAgreeML(e.target.checked)}
                />
                <span className="checkbox-custom" />
                <span className="label-text">Prometo que acho a cadeira de ML2 a melhor de toda a NOVA IMS.</span>
              </label>

              <label className="captcha-row sub-row">
                <input
                  type="checkbox"
                  checked={agreeIvo}
                  onChange={(e) => setAgreeIvo(e.target.checked)}
                />
                <span className="checkbox-custom" />
                <span className="label-text">Reconheço que o Professor Ivo é um excelente e motivador docente.</span>
              </label>

              <label className="captcha-row sub-row">
                <input
                  type="checkbox"
                  checked={agreeWheel}
                  onChange={(e) => setAgreeWheel(e.target.checked)}
                />
                <span className="checkbox-custom" />
                <span className="label-text">Tenho consciência que a roleta de descontos me pode dar o cupão lucas5.</span>
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
            Aceder ao Dashboard
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
    { text: 'Tenta Novamente 😢', color: '#1e1b4b' },
    { text: 'Quase... 😭', color: '#111827' },
    { text: 'lima5? Não! 🍋', color: '#0f172a' },
    { text: 'lucas5 🎉', color: '#7c3aed' }, // WINNER at index 3
    { text: 'Tenta Novamente 😢', color: '#1e1b4b' },
    { text: 'lince5? Não! 🐱', color: '#0f172a' },
    { text: 'Outra vez... 🔄', color: '#111827' },
    { text: 'Mais perto... 🎯', color: '#0f172a' },
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
        setResult('Parabéns! Ganhaste o cupão de desconto!')
        setCouponCode('lucas5')
      } else {
        setResult(`Não foi desta vez! Calhou em: "${chosenSlice.text}"`)
      }
    }, 3200)
  }

  const copyToClipboard = () => {
    if (couponCode) {
      navigator.clipboard.writeText(couponCode)
      alert('Cupão copiado para a área de transferência!')
    }
  }

  const applyToCart = () => {
    if (couponCode) {
      window.dispatchEvent(new CustomEvent('apply-coupon-event', { detail: couponCode }))
      alert(`Cupão "${couponCode}" aplicado diretamente no carrinho!`)
      onClose()
    }
  }

  return (
    <div className="modal-overlay">
      <div className="modal-card wheel-card animate-in">
        <button className="modal-close-btn" onClick={onClose}>✕</button>
        
        <div className="wheel-modal-header">
          <h2>🎰 Roleta da Sorte</h2>
          <p>Tens 25% de probabilidade de ganhar o cupão <strong>lucas5</strong> (5% desconto acumulável na loja!).</p>
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
            {isSpinning ? 'A girar...' : 'GIRAR ROLETA'}
          </button>
        </div>

        {result && (
          <div className={`wheel-result-box ${couponCode ? 'win' : 'lose'} animate-in`}>
            {couponCode ? (
              <>
                <p className="result-title">🎉 Parabéns! Ganhaste!</p>
                <p className="result-text">Descobriste o cupão especial <strong>{couponCode}</strong>!</p>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
                  Este código concede 5% de desconto extra acumulável na nossa mercearia.
                </p>
                <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'center' }}>
                  <button className="copy-btn" onClick={copyToClipboard}>
                    📋 Copiar Código
                  </button>
                  <button className="apply-btn" onClick={applyToCart}>
                    🛒 Aplicar no Carrinho
                  </button>
                </div>
              </>
            ) : (
              <>
                <p className="result-title">😢 {result}</p>
                <p className="result-text">Podes tentar girar a roleta novamente para obter o desconto!</p>
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
      text: 'Olá! Sou o assistente virtual do SegmentIQ. Como posso ajudar hoje? 😊',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ])
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)

  const faqs = [
    {
      q: 'Como funciona o clustering no SegmentIQ?',
      a: 'O SegmentIQ utiliza o algoritmo K-Means para agrupar clientes com base em métricas como Frequência e Valor de compras. Isso ajuda a segmentar os clientes em grupos como "Premium Loyalists" ou "At-Risk", permitindo campanhas de marketing direcionadas!'
    },
    {
      q: 'Qual o número ideal de clusters (k)?',
      a: 'Com base na análise do Silhouette Score e da Inércia (método do cotovelo), o valor ideal determinado para este conjunto de dados foi k=7. Esse valor equilibra perfeitamente a coesão interna com a separação dos grupos.'
    },
    {
      q: 'Quem são os criadores deste projeto?',
      a: 'Este projeto foi desenvolvido por três alunos da Licenciatura em Ciência de Dados da NOVA IMS: Afonso Lima, Lucas Casimiro e Lince Silva, combinando modelação estatística com design de interfaces moderno.'
    },
    {
      q: 'O Professor Ivo vai dar-nos um 20?',
      a: 'Esperamos que sim! Focámo-nos em ir muito além dos requisitos: implementámos clustering rigoroso, basket analysis com regras dinâmicas, uma loja simulada, cupões escondidos, a roleta da sorte e este chat. Professor Ivo, o 20 está ganho? 😉'
    },
    {
      q: 'Como funcionam os cupões de desconto?',
      a: 'Podes encontrar os códigos escondidos pelo site (há um na Overview e outro nas Visualizações). O código da roleta é "lucas5". Cada código dá 5% de desconto acumulável e pode ser aplicado na nossa mercearia virtual!'
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
            <h3>Apoio ao Cliente</h3>
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
          <p className="faq-title">Selecione uma dúvida frequente:</p>
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
      name: 'Lucas Casimiro',
      role: 'ML & Basket Engineer',
      desc: 'O cérebro das regras de associação. Passou noites a afinar o Apriori para garantir que os clientes vegetarianos não recebessem sugestões de salsichas... a menos que fossem de soja!',
      color: 'var(--purple)'
    },
    {
      name: 'Afonso Lima',
      role: 'Data & Analytics Guru',
      desc: 'O mestre dos gráficos interativos. Transformou coordenadas do PCA em arte visual tridimensional para que qualquer pessoa consiga ver a alma de um Premium Loyalist.',
      color: 'var(--teal)'
    },
    {
      name: 'Lince Silva',
      role: 'UX & Frontend Architect',
      desc: 'O designer de interações. Adicionou a roleta, o captcha anti-robô e o chat para provar que a Ciência de Dados e o design andam sempre de mãos dadas.',
      color: 'var(--amber)'
    }
  ]

  return (
    <div className="modal-overlay">
      <div className="modal-card about-card animate-in" style={{ maxWidth: '650px' }}>
        <button className="modal-close-btn" onClick={onClose}>✕</button>

        <div className="about-header">
          <h2>👥 Sobre Nós</h2>
          <p>A equipa por trás do SegmentIQ — Licenciatura em Ciência de Dados na NOVA IMS.</p>
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
            Um agradecimento especial ao <strong>Professor Ivo</strong> pela dedicação, exigência académica e pelo 
            desafio contínuo que nos impulsionou a elevar este trabalho prático a um patamar profissional de engenharia de software e análise de dados.
          </p>
        </div>
      </div>
    </div>
  )
}
