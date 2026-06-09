/**
 * Promotions.jsx  —  Basket Analysis & Promotions section
 *
 * Features:
 *   • Lift chart (bar) for top association rules
 *   • Association rules table with sortable columns
 *   • Customer ID lookup (placeholder — no backend yet)
 *   • Discount tier cards per segment
 *
 * TODO: Connect customer lookup to a real recommendation model.
 *       Replace associationRules and liftChartData with mlxtend exports.
 */
import { useState, useMemo } from 'react'
import SectionHeader from '../components/common/SectionHeader'
import InteractivePlot from '../components/common/InteractivePlot'
import { associationRules, liftChartData, discountTiers, sampleRecommendations } from '../data/basketData'

// Função auxiliar de preço case-insensitive para os 164 produtos
const getItemPrice = (item) => {
  if (!item) return 1.50;
  const itemLower = item.toLowerCase();
  
  const prices = {
    'milk': 0.89,
    'fresh bread': 0.75,
    'bread': 0.75,
    'butter': 1.69,
    'eggs': 1.89,
    'asparagus': 2.49,
    'tomatoes': 1.59,
    'spinach': 1.49,
    'zucchini': 1.29,
    'rice': 1.09,
    'pasta': 0.85,
    'tomato sauce': 0.95,
    'chicken': 5.49,
    'beef': 7.99,
    'ground beef': 4.99,
    'salmon': 8.99,
    'fish': 6.49,
    'bacon': 2.19,
    'cheese': 2.49,
    'parmesan cheese': 2.99,
    'olive oil': 4.50,
    'cooking oil': 1.99,
    'shampoo': 2.89,
    'deodorant': 2.49,
    'toothpaste': 1.49,
    'toilet paper': 3.29,
    'napkins': 0.99,
    'dog food': 4.99,
    'cat food': 3.49,
    'babies food': 2.79,
    'protein bar': 1.79,
    'energy bar': 1.59,
    'gluten free bar': 1.99,
    'green tea': 1.39,
    'tea': 1.19,
    'coffee': 2.49,
    'water': 0.35,
    'orange juice': 1.59,
    'antioxydant juice': 2.19,
    'beer': 0.99,
    'white wine': 3.99,
    'red wine': 4.99,
    'snacks': 1.29,
    'chips': 1.19,
    'cookies': 1.49,
    'cereal': 2.29,
    'cereals': 2.29,
    'oatmeal': 1.19,
    'honey': 3.49,
    'fruit': 1.89,
    'vegetables': 1.69,
    'electronics': 49.99,
    'videogames': 59.99,
    'non-alcoholic drinks': 0.89
  };
  
  if (prices[itemLower] !== undefined) {
    return prices[itemLower];
  }
  
  if (itemLower.includes('phone') || itemLower.includes('galaxy') || itemLower.includes('samsung') || itemLower.includes('iphone') || itemLower.includes('tablet') || itemLower.includes('laptop')) {
    return 299.99;
  }
  if (itemLower.includes('airpods') || itemLower.includes('headphones') || itemLower.includes('earbuds') || itemLower.includes('speaker') || itemLower.includes('bluetooth')) {
    return 49.99;
  }
  if (itemLower.includes('watch')) {
    return 129.99;
  }
  if (itemLower.includes('ring light')) {
    return 19.99;
  }
  if (itemLower.includes('videogame') || itemLower.includes('game') || itemLower.includes('console')) {
    return 59.99;
  }
  
  let hashVal = 0;
  for (let i = 0; i < item.length; i++) {
    hashVal += item.charCodeAt(i);
  }
  return parseFloat((0.99 + (hashVal % 900) / 100).toFixed(2));
}

export default function Promotions({ onVoucherChange }) {
  const [customerId, setCustomerId] = useState('')
  const [recommendation, setRecommendation] = useState(null)
  const [sortBy, setSortBy] = useState('lift')
  
  // Interactive send panel states
  const [showSendPanel, setShowSendPanel] = useState(false)
  const [sendChannel, setSendChannel] = useState('email')
  const [contactInput, setContactInput] = useState('')
  const [isSending, setIsSending] = useState(false)
  const [sendSuccess, setSendSuccess] = useState(false)

  // Real-time API connection states
  const [isSearchingRealtime, setIsSearchingRealtime] = useState(false)
  const [isRealtimeApiActive, setIsRealtimeApiActive] = useState(false)

  // Sort rules table
  const sortedRules = useMemo(() =>
    [...associationRules].sort((a, b) => b[sortBy] - a[sortBy])
  , [sortBy])

  // Mock/Real-time customer lookup
  const handleLookup = async () => {
    const trimmedId = customerId.trim()
    if (!trimmedId) return

    setIsSearchingRealtime(true)
    setRecommendation(null)
    setSendSuccess(false)
    setShowSendPanel(false)

    try {
      // Tentar ligar ao servidor Flask local
      const response = await fetch(`http://localhost:5000/api/recommendations?customer_id=${trimmedId}`)
      if (response.ok) {
        const data = await response.json()
        setRecommendation(data)
        if (onVoucherChange && !data.notFound) onVoucherChange(data)
        setIsRealtimeApiActive(true)
      } else {
        throw new Error('Customer ID not found or API error')
      }
    } catch (err) {
      console.warn('Real-Time API offline or error, falling back to mock:', err.message)
      const offlineRec = sampleRecommendations[trimmedId.toUpperCase()]
      if (offlineRec) {
        setRecommendation(offlineRec)
        if (onVoucherChange) onVoucherChange(offlineRec)
        setIsRealtimeApiActive(false)
      } else {
        setRecommendation({ notFound: true })
      }
    } finally {
      setIsSearchingRealtime(false)
    }
  }

  const handleSend = () => {
    if (!contactInput.trim()) return
    setIsSending(true)
    setTimeout(() => {
      setIsSending(false)
      setSendSuccess(true)
    }, 1200)
  }

  // Função para abrir o talão num pop-up de impressão limpo
  const handlePrint = (rec, id) => {
    // O talão é um cupão: o desconto aplica-se aos campaignItems (que batem com a oferta)
    const calcItems = rec.campaignItems || rec.items || [];
    const crossSellItems = rec.items || [];
    const subtotal = calcItems.reduce((sum, item) => sum + getItemPrice(item), 0);
    const discPct = parseInt(rec.discount) / 100;
    const discountVal = subtotal * discPct;
    const total = subtotal - discountVal;

    const printWindow = window.open('', '_blank', 'width=450,height=720');
    if (!printWindow) {
      alert('Please enable pop-ups in your browser to print the receipt!');
      return;
    }

    const itemsHtml = calcItems.map(item => {
      const price = getItemPrice(item).toFixed(2);
      return `
        <div style="display: flex; justify-content: space-between; margin: 4px 0;">
          <span>1x ${item}</span>
          <span>${price} EUR</span>
        </div>
      `;
    }).join('');

    // Cross-selling suggestions (sem desconto)
    let crossSellHtml = '';
    if (crossSellItems.length > 0) {
      const rows = crossSellItems.map(item => `
        <div style="display: flex; justify-content: space-between; margin: 4px 0; color: #555;">
          <span>1x ${item}</span>
          <span>${getItemPrice(item).toFixed(2)} EUR</span>
        </div>
      `).join('');
      crossSellHtml = `
        <div class="dashed"></div>
        <div style="font-size: 0.82rem;">
          <div class="bold" style="margin-bottom: 6px;">ADDITIONAL SUGGESTIONS:</div>
          ${rows}
        </div>
      `;
    }

    const barcodeHtml = [1, 2, 1, 3, 1, 2, 4, 1, 3, 2, 1, 2, 1, 4, 2, 1, 3, 1, 2, 1, 3, 2, 1, 2, 1, 4, 1, 2, 3, 1].map((w, idx) => {
      const bg = idx % 2 === 0 ? '#000' : 'transparent';
      return `<div class="bar" style="width: ${w}px; background: ${bg};"></div>`;
    }).join('');

    printWindow.document.write(`
      <html>
        <head>
          <title>Supermarket Receipt - Customer ${rec.customerId || id}</title>
          <style>
            @media print {
              body { margin: 0; padding: 0; background: #fff; }
              .no-print { display: none !important; }
            }
            body {
              font-family: 'Courier New', Courier, monospace;
              color: #111;
              background: #f0f0f0;
              padding: 20px;
              display: flex;
              flex-direction: column;
              align-items: center;
              margin: 0;
            }
            .btn-print {
              margin-bottom: 20px;
              padding: 10px 20px;
              font-family: system-ui, -apple-system, sans-serif;
              font-size: 0.9rem;
              font-weight: bold;
              background: #7c3aed;
              color: white;
              border: none;
              border-radius: 6px;
              cursor: pointer;
              box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
              transition: all 0.2s ease;
            }
            .btn-print:hover {
              background: #6d28d9;
              transform: translateY(-1px);
            }
            .receipt {
              background: #fff;
              width: 320px;
              padding: 30px 24px;
              border: 1px solid #ddd;
              box-shadow: 0 10px 25px rgba(0,0,0,0.08);
              box-sizing: border-box;
            }
            .center { text-align: center; }
            .bold { font-weight: bold; }
            .dashed { border-top: 1px dashed #333; margin: 12px 0; }
            .flex { display: flex; justify-content: space-between; }
            .barcode-bars {
              display: flex;
              height: 40px;
              justify-content: center;
              margin: 12px 0 6px 0;
            }
            .bar {
              background: #000;
              margin-right: 1px;
            }
          </style>
        </head>
        <body>
          <button class="btn-print no-print" onclick="window.print()">🖨️ Confirm Print / Save as PDF</button>
          <div class="receipt">
            <div class="center bold" style="font-size: 1.1em; letter-spacing: 1px;">NOVAIMS GROCERY</div>
            <div class="center" style="font-size: 0.82rem; margin-top: 4px; color: #444;">Rua de Campolide, 1070-312 Lisboa</div>
            <div class="center" style="font-size: 0.82rem; color: #444;">NIF: 501234567 | Tel: 213 828 610</div>
            <div class="center" style="margin-top: 5px;">
              <span style="font-size: 0.65rem; border: 1px solid #777; padding: 2px 6px; font-weight: bold; text-transform: uppercase;">
                ${isRealtimeApiActive ? 'REAL-TIME API (ONLINE)' : 'SIMULATION (OFFLINE)'}
              </span>
            </div>
            
            <div class="dashed"></div>
            
            <div class="center bold" style="font-size: 0.88rem; letter-spacing: 0.5px;">DISCOUNT VOUCHER</div>
            
            <div class="dashed"></div>
            
            <div style="font-size: 0.82rem; line-height: 1.45;">
              <div class="flex"><span>CASHIER:</span> <span>Group 31</span></div>
              <div class="flex"><span>DATE:</span> <span>${new Date().toLocaleString('en-GB')}</span></div>
              <div class="flex"><span>CUSTOMER ID:</span> <span class="bold">${rec.customerId || id}</span></div>
              <div class="flex"><span>SEGMENT:</span> <span>${rec.segment}</span></div>
            </div>
            
            <div class="dashed"></div>

            <div style="font-size: 0.82rem;">
              <div class="bold" style="margin-bottom: 2px;">CAMPAIGN / OFFER:</div>
              <div style="margin-bottom: 6px; font-weight: bold; color: #7c3aed;">${rec.nextBestOffer}</div>
            </div>

            <div class="dashed"></div>
            
            <div style="font-size: 0.82rem;">
              <div class="bold" style="margin-bottom: 6px;">SUGGESTED ITEMS (CROSS-SELLING):</div>
              ${itemsHtml}
            </div>
            
            ${crossSellHtml}
            
            <div class="dashed"></div>
            
            <div style="font-size: 0.82rem; line-height: 1.45;">
              <div class="flex"><span>SUBTOTAL</span> <span>${subtotal.toFixed(2)} EUR</span></div>
              <div class="flex bold" style="color: #b91c1c;">
                <span>DISCOUNT (${rec.discount})</span> 
                <span>-${discountVal.toFixed(2)} EUR</span>
              </div>
              <div class="dashed"></div>
              <div class="flex bold" style="font-size: 1.05em;">
                <span>TOTAL TO PAY</span> 
                <span>${total.toFixed(2)} EUR</span>
              </div>
            </div>
            
            <div class="dashed"></div>
            
            <div style="font-size: 0.82rem; line-height: 1.45; color: #333;">
              <div>• Purchase Propensity: ${(rec.propensity * 100).toFixed(0)}%</div>
              <div>• Algorithm: ${rec.algorithm || 'K-Means (k=8 + Vegans, K=9)'}</div>
            </div>
            
            <div class="dashed"></div>
            
            <div class="barcode-container" style="display: flex; flex-direction: column; align-items: center;">
              <div class="barcode-bars">
                ${barcodeHtml}
              </div>
              <div style="font-size: 0.75em; letter-spacing: 3px; font-weight: bold;">*C-${rec.customerId || id}*</div>
            </div>
            
            <div class="dashed"></div>
            
            <div class="center" style="font-size: 0.8em; margin-top: 10px; font-style: italic; color: #444;">
              Thank you for shopping with us!<br>
              NOVAIMS Analytics - ML2 2026
            </div>
          </div>
          <script>
            setTimeout(function() {
              window.print();
            }, 400);
          </script>
        </body>
      </html>
    `)
    printWindow.document.close();
  }

  // ── Lift bar chart ─────────────────────────────────────────────
  const liftTraces = useMemo(() => [
    {
      // TODO: replace with real lift values from your mlxtend rules
      type:        'bar',
      x:           liftChartData.lift,
      y:           liftChartData.categories,
      orientation: 'h',
      name:        'Lift',
      marker: {
        color:   liftChartData.lift.map(l =>
          l > 3 ? '#7c3aed' : l > 2.5 ? '#2dd4bf' : l > 2 ? '#3b82f6' : '#64748b'
        ),
        opacity: 0.88,
      },
      text:        liftChartData.lift.map(l => l.toFixed(2)),
      textposition:'outside',
      hovertemplate: '<b>%{y}</b><br>Lift: %{x:.2f}<extra></extra>',
    },
    {
      // Baseline at lift=1
      type:  'scatter', mode: 'lines',
      x:     [1, 1],
      y:     [liftChartData.categories[0], liftChartData.categories.at(-1)],
      name:  'Baseline (lift=1)',
      line:  { color: '#f43f5e', width: 1.5, dash: 'dot' },
      hoverinfo: 'skip',
    },
  ], [])

  const liftCsv = {
    headers: ['Rule', 'Lift', 'Confidence'],
    rows:    liftChartData.categories.map((cat, i) => [cat, liftChartData.lift[i], liftChartData.confidence[i]]),
  }

  return (
    <section id="promotions" className="section" style={{ background: 'var(--bg-surface)' }}>
      <div className="container">

        <SectionHeader
          badge="🛍️ Basket Analysis"
          badgeClass="badge-amber"
          title="Promotions &amp; "
          highlight="Recommendations"
          subtitle="Apriori association rules reveal product affinities. Use these insights to create personalised bundle offers and targeted discounts per segment."
        />

        <div className="placeholder-notice">
          🔌 <strong>Model Lineage</strong>. Connected to the local AI API on port <code>5000</code>. If the Flask server is offline, it automatically reverts to local simulation. Supported IDs: Any customer ID (e.g., 1, 42, 198, 222, 1000, 32900).
        </div>

        {/* ── Top row: lift chart + customer lookup ─────────────── */}
        <div className="promo-hero">

          {/* Lift chart */}
          <InteractivePlot
            title="Association Rule Lift Chart"
            description="Lift > 1 means the items are bought together more often than by chance. Rules with lift > 2.5 are strong candidates for bundle promotions."
            data={liftTraces}
            layout={{
              xaxis:      { title: { text: 'Lift', font: { color: '#64748b' } }, range: [0, 10.0] },
              showlegend: true,
              bargap:     0.3,
              margin:     { l: 180, r: 60, t: 20, b: 40 },
            }}
            csvData={liftCsv}
            height={380}
          />

          {/* Customer lookup card */}
          <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <div>
              <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.05rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                🔍 Promotion Simulator <span className="badge badge-teal" style={{ fontSize: '0.7rem' }}>Interactive</span>
              </h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                Enter any numeric ID (0 to 32938) or test ID to dynamically compute the customer segment and cross-selling recommendations using the K-Means (RobustScaler, k=8 + Vegans) model.
              </p>
            </div>

            {/* Input row */}
            <div className="promo-search">
              <input
                id="customer-id-input"
                className="input"
                type="text"
                placeholder="Customer ID or Invoice ID (e.g., 3032 or 10011206)"
                value={customerId}
                onChange={e => setCustomerId(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleLookup()}
                disabled={isSearchingRealtime}
              />
              <button 
                className="btn btn-primary" 
                onClick={handleLookup}
                disabled={isSearchingRealtime || !customerId.trim()}
              >
                {isSearchingRealtime ? 'Processing...' : 'Simulate'}
              </button>
            </div>

            {/* Quick-select test IDs */}
            <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Quick Search:</span>
              {[
                { label: 'Customer 3032 (Vegetarian/Flex)', value: '3032' },
                { label: 'Invoice 10011206 (Basket 3032)', value: '10011206' },
                { label: 'C042', value: 'C042' },
                { label: 'C198', value: 'C198' }
              ].map(item => (
                <button
                  key={item.value}
                  className="btn btn-ghost btn-sm"
                  style={{ padding: '0.15rem 0.45rem', fontSize: '0.72rem', height: 'auto', border: '1px solid var(--border-subtle)', background: customerId === item.value ? 'var(--bg-elevated)' : 'transparent' }}
                  onClick={async () => {
                    setCustomerId(item.value)
                    setIsSearchingRealtime(true)
                    setRecommendation(null)
                    setSendSuccess(false)
                    setShowSendPanel(false)
                    try {
                      const response = await fetch(`http://localhost:5000/api/recommendations?customer_id=${item.value}`)
                      if (response.ok) {
                        const data = await response.json()
                        setRecommendation(data)
                        if (onVoucherChange && !data.notFound) onVoucherChange(data)
                        setIsRealtimeApiActive(true)
                      } else {
                        throw new Error('404')
                      }
                    } catch (err) {
                      console.warn('Offline fallback for quick ID:', item.value)
                      const offlineRec = sampleRecommendations[item.value]
                      if (offlineRec && onVoucherChange) onVoucherChange(offlineRec)
                      setRecommendation(offlineRec || { notFound: true })
                      setIsRealtimeApiActive(false)
                    } finally {
                      setIsSearchingRealtime(false)
                    }
                  }}
                  disabled={isSearchingRealtime}
                >
                  {item.label}
                </button>
              ))}
            </div>

            {/* Inline CSS styling for physical receipt and mockups */}
            <style>{`
              .receipt-paper {
                background: #faf9f5;
                color: #1a1a1a;
                font-family: 'Courier New', Courier, monospace;
                padding: 2.25rem 1.5rem;
                position: relative;
                box-shadow: 0 15px 35px rgba(0,0,0,0.35), inset 0 0 20px rgba(0,0,0,0.02);
                border-radius: 2px;
                display: flex;
                flex-direction: column;
                gap: 0.65rem;
                border-left: 1px solid rgba(0,0,0,0.04);
                border-right: 1px solid rgba(0,0,0,0.04);
                margin: 0.5rem 0;
              }
              
              .receipt-paper::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 8px;
                background-image: linear-gradient(135deg, var(--bg-card) 4px, transparent 0), linear-gradient(225deg, var(--bg-card) 4px, transparent 0);
                background-position: left top;
                background-repeat: repeat-x;
                background-size: 8px 8px;
              }
              
              .receipt-paper::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 8px;
                background-image: linear-gradient(45deg, var(--bg-card) 4px, transparent 0), linear-gradient(-45deg, var(--bg-card) 4px, transparent 0);
                background-position: left bottom;
                background-repeat: repeat-x;
                background-size: 8px 8px;
              }

              .receipt-divider {
                border-top: 1px dashed #777;
                margin: 4px 0;
              }
              
              .phone-sms-mockup {
                background: #090d16;
                border: 2px solid #1e293b;
                border-radius: 12px;
                padding: 0.75rem;
                margin-top: 0.5rem;
                animation: fadeInUp 0.4s ease;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
              }
            `}</style>

            {/* Result - Digital Voucher mockup */}
            {recommendation && !recommendation.notFound && (
              <div className="animate-in" style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '0.5rem' }}>
                
                {/* Physical thermal receipt */}
                <div className="receipt-paper">
                  {/* Header */}
                  <div style={{ textAlign: 'center', marginTop: '4px' }}>
                    <div style={{ fontWeight: 'bold', fontSize: '0.95rem', letterSpacing: '1px' }}>NOVAIMS GROCERY</div>
                    <div style={{ fontSize: '0.7rem', color: '#444', marginTop: '2px' }}>Rua de Campolide, 1070-312 Lisboa</div>
                    <div style={{ fontSize: '0.7rem', color: '#444' }}>NIF: 501234567 | TEL: 213 828 610</div>
                    <div style={{ display: 'flex', justifyContent: 'center', gap: '0.4rem', marginTop: '0.4rem' }}>
                      <span style={{ 
                        fontSize: '0.55rem', 
                        background: isRealtimeApiActive ? 'rgba(16,185,129,0.1)' : 'rgba(245,158,11,0.1)', 
                        color: isRealtimeApiActive ? '#059669' : '#d97706', 
                        padding: '0.1rem 0.45rem', 
                        borderRadius: '4px', 
                        fontWeight: 700, 
                        border: isRealtimeApiActive ? '1px solid rgba(16,185,129,0.2)' : '1px solid rgba(245,158,11,0.2)',
                        letterSpacing: '0.5px'
                      }}>
                        {isRealtimeApiActive ? '● REAL-TIME API (ONLINE)' : '○ SIMULATION (OFFLINE)'}
                      </span>
                    </div>
                  </div>

                  <div className="receipt-divider" />

                  {/* Voucher Header Info */}
                  <div style={{ fontSize: '0.72rem', display: 'flex', flexDirection: 'column', gap: '3px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span>CASHIER:</span>
                      <span>Group 31</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span>DATE:</span>
                      <span>{new Date().toLocaleString('en-GB')}</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span>CUSTOMER:</span>
                      <span style={{ fontWeight: 'bold' }}>{recommendation.customerId || customerId.toUpperCase()}</span>
                    </div>
                    {recommendation.invoiceId && recommendation.invoiceId !== 'N/A' && (
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span>INVOICE ID:</span>
                        <span style={{ fontWeight: 'bold' }}>{recommendation.invoiceId}</span>
                      </div>
                    )}
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span>SEGMENT:</span>
                      <span style={{ fontWeight: 'bold' }}>{recommendation.segment}</span>
                    </div>
                  </div>

                  <div className="receipt-divider" />

                  {/* Campaign / Offer Details */}
                  <div style={{ fontSize: '0.72rem' }}>
                    <div style={{ fontWeight: 'bold', marginBottom: '2px' }}>CAMPAIGN / OFFER:</div>
                    <div style={{ fontWeight: 'bold', color: 'var(--purple-light)', marginBottom: '6px' }}>{recommendation.nextBestOffer}</div>
                  </div>

                  <div className="receipt-divider" />

                  {/* Itens com desconto — batem com a campanha */}
                  {(() => {
                    const campaignItems = recommendation.campaignItems || recommendation.items || [];
                    const crossSell = recommendation.items || [];
                    const subtotal = campaignItems.reduce((sum, item) => sum + getItemPrice(item), 0);
                    const discPct = parseInt(recommendation.discount) / 100;
                    const discountVal = subtotal * discPct;
                    const total = subtotal - discountVal;

                    return (
                      <>
                        {/* Produtos com desconto */}
                        <div style={{ fontSize: '0.72rem' }}>
                          <div style={{ fontWeight: 'bold', marginBottom: '6px' }}>PRODUCTS WITH DISCOUNT ({recommendation.discount}):</div>
                          {campaignItems.map(item => {
                            const price = getItemPrice(item);
                            return (
                              <div key={item} style={{ display: 'flex', justifyContent: 'space-between', margin: '2px 0' }}>
                                <span>1x {item}</span>
                                <span>{price.toFixed(2)} EUR</span>
                              </div>
                            );
                          })}
                        </div>

                        <div className="receipt-divider" />

                        {/* Cálculo do desconto */}
                        <div style={{ fontSize: '0.72rem', display: 'flex', flexDirection: 'column', gap: '3px' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <span>SUBTOTAL</span>
                            <span>{subtotal.toFixed(2)} EUR</span>
                          </div>
                          <div style={{ display: 'flex', justifyContent: 'space-between', color: '#b91c1c', fontWeight: 'bold' }}>
                            <span>DISCOUNT ({recommendation.discount})</span>
                            <span>-{discountVal.toFixed(2)} EUR</span>
                          </div>
                          <div className="receipt-divider" />
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 'bold', fontSize: '0.88rem' }}>
                            <span>TOTAL TO PAY</span>
                            <span>{total.toFixed(2)} EUR</span>
                          </div>
                        </div>

                        {/* Sugestões adicionais de cross-selling (sem desconto) */}
                        {crossSell.length > 0 && (
                          <>
                            <div className="receipt-divider" />
                            <div style={{ fontSize: '0.72rem' }}>
                              <div style={{ fontWeight: 'bold', marginBottom: '6px', color: '#555' }}>ADDITIONAL SUGGESTIONS:</div>
                              {crossSell.map(item => (
                                <div key={item} style={{ display: 'flex', justifyContent: 'space-between', margin: '2px 0', color: '#555' }}>
                                  <span>1x {item}</span>
                                  <span style={{ fontSize: '0.65rem', color: '#888' }}>view store</span>
                                </div>
                              ))}
                            </div>
                          </>
                        )}
                      </>
                    );
                  })()}

                  <div className="receipt-divider" />

                  {/* Segmentation Details */}
                  <div style={{ fontSize: '0.72rem', display: 'flex', flexDirection: 'column', gap: '2px', color: '#333' }}>
                    <div>• Purchase Propensity: <strong>{(recommendation.propensity * 100).toFixed(0)}%</strong></div>
                    <div>• Algorithm: <strong>{recommendation.algorithm || 'K-Means (k=8 + Vegans, K=9) + Apriori'}</strong></div>
                  </div>

                  <div className="receipt-divider" />

                  {/* Barcode drawing */}
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '4px' }}>
                    <div style={{ display: 'flex', height: '32px', background: 'transparent', alignItems: 'stretch' }}>
                      {[1, 2, 1, 3, 1, 2, 4, 1, 3, 2, 1, 2, 1, 4, 2, 1, 3, 1, 2, 1, 3, 2, 1, 2, 1, 4, 1, 2, 3, 1].map((w, idx) => (
                        <div key={idx} style={{
                          width: `${w}px`,
                          background: idx % 2 === 0 ? '#111' : 'transparent',
                          marginRight: idx % 2 === 0 ? '1px' : '0px'
                        }} />
                      ))}
                    </div>
                    <span style={{ fontSize: '0.65rem', letterSpacing: '3px', marginTop: '3px', color: '#111', fontFamily: 'monospace', fontWeight: 'bold' }}>
                      *C-{customerId.toUpperCase()}*
                    </span>
                  </div>

                  <div className="receipt-divider" />

                  <div style={{ textAlign: 'center', fontSize: '0.7rem', fontStyle: 'italic', color: '#555', marginTop: '4px' }}>
                    Thank you for shopping with us!<br />
                    NOVAIMS Analytics - ML2 2026
                  </div>
                </div>

                {/* Dashboard controls (under receipt) */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem', marginTop: '0.25rem' }}>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button
                      className="btn btn-primary btn-sm"
                      style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem' }}
                      onClick={() => handlePrint(recommendation, customerId)}
                    >
                      🖨️ Print / Save PDF
                    </button>
                    <button
                      className="btn btn-ghost btn-sm"
                      style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem', border: '1px solid var(--border-soft)' }}
                      onClick={() => setShowSendPanel(!showSendPanel)}
                    >
                      ✉️ {showSendPanel ? 'Close Sending' : 'Send Coupon'}
                    </button>
                  </div>

                  {/* Send Panel */}
                  {showSendPanel && !sendSuccess && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', background: 'var(--bg-elevated)', padding: '0.75rem', borderRadius: '8px', border: '1px solid var(--border-soft)', animation: 'fadeInUp 0.3s ease' }}>
                      <div style={{ display: 'flex', gap: '0.4rem' }}>
                        <button
                          className={`btn ${sendChannel === 'email' ? 'btn-primary' : 'btn-ghost'} btn-xs`}
                          style={{ flex: 1, height: 'auto', padding: '0.25rem' }}
                          onClick={() => { setSendChannel('email'); setContactInput(''); }}
                        >
                          📧 E-mail
                        </button>
                        <button
                          className={`btn ${sendChannel === 'sms' ? 'btn-primary' : 'btn-ghost'} btn-xs`}
                          style={{ flex: 1, height: 'auto', padding: '0.25rem' }}
                          onClick={() => { setSendChannel('sms'); setContactInput(''); }}
                        >
                          📱 Mobile
                        </button>
                      </div>

                      <div style={{ display: 'flex', gap: '0.4rem' }}>
                        <input
                          className="input"
                          type={sendChannel === 'email' ? 'email' : 'tel'}
                          placeholder={sendChannel === 'email' ? 'exemplo@cliente.com' : 'e.g. 912345678'}
                          value={contactInput}
                          onChange={e => setContactInput(e.target.value)}
                          style={{ fontSize: '0.78rem', padding: '0.35rem 0.6rem', height: 'auto' }}
                        />
                        <button
                          className="btn btn-primary btn-sm"
                          onClick={handleSend}
                          disabled={isSending || !contactInput.trim()}
                          style={{ height: 'auto', padding: '0 0.8rem', fontSize: '0.78rem' }}
                        >
                          {isSending ? 'Sending...' : 'Send'}
                        </button>
                      </div>
                    </div>
                  )}

                  {/* Success feedback and SMS/Email mockup preview */}
                  {sendSuccess && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', background: 'var(--bg-elevated)', padding: '0.75rem', borderRadius: '8px', border: '1px solid var(--border-soft)', animation: 'fadeInUp 0.4s ease' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--teal)', fontSize: '0.78rem', fontWeight: 600 }}>
                        <span>✅</span>
                        <span>Successfully sent to {contactInput}!</span>
                      </div>

                      {/* Chat Bubble Mockup */}
                      {sendChannel === 'sms' && (
                        <div className="phone-sms-mockup" style={{ marginTop: '0.25rem' }}>
                          <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: '0.25rem', display: 'flex', justifyContent: 'space-between' }}>
                            <span>💬 SMS NOVAIMS Grocery</span>
                            <span>Just now</span>
                          </div>
                          <div style={{ background: '#1e293b', padding: '0.5rem 0.75rem', borderRadius: '12px 12px 12px 0', fontSize: '0.72rem', color: '#fff', lineHeight: 1.4 }}>
                            Hello! Since you belong to the <b>{recommendation.segment}</b> segment, you have a <b>{recommendation.discount}</b> discount on your next basket. Present the code <b>*C-{customerId.toUpperCase()}*</b> at checkout!
                          </div>
                        </div>
                      )}

                      {/* Email Mockup */}
                      {sendChannel === 'email' && (
                        <div className="phone-sms-mockup" style={{ marginTop: '0.25rem' }}>
                          <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: '0.25rem', borderBottom: '1px solid var(--border-soft)', paddingBottom: '0.25rem' }}>
                            <div><b>De:</b> cupoes@novaimsgrocery.pt</div>
                            <div><b>Para:</b> {contactInput}</div>
                          </div>
                          <div style={{ fontSize: '0.7rem', color: '#fff', lineHeight: 1.4, padding: '0.25rem 0' }}>
                            Hello!<br />Since you belong to the <b>{recommendation.segment}</b> segment, we offer you <b>{recommendation.discount}</b> off on your next purchases.
                            <br /><br />
                            <b>Suggested products:</b><br />
                            {recommendation.items.map(item => (
                              <div key={item}>• {item}</div>
                            ))}
                            <br />
                            Present the code <b>C-{customerId.toUpperCase()}</b> at checkout.
                          </div>
                        </div>
                      )}

                      <button
                        className="btn btn-ghost btn-xs"
                        style={{ marginTop: '0.25rem', width: '100%', fontSize: '0.68rem', height: 'auto', padding: '0.1rem' }}
                        onClick={() => { setSendSuccess(false); setContactInput(''); }}
                      >
                        Send Again
                      </button>
                    </div>
                  )}
                </div>

              </div>
            )}

            {recommendation?.notFound && (
              <div style={{ color: 'var(--rose)', fontSize: '0.875rem', textAlign: 'center', padding: '1rem', background: 'rgba(244,63,94,0.08)', borderRadius: 'var(--radius-md)', border: '1px solid rgba(244,63,94,0.2)' }}>
                ⚠️ Customer ID not found. Try: C001, C042, C198, C222
              </div>
            )}
            {/* Note */}
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 'auto' }}>
              TODO: Connect to a real recommendation model. Replace <code>sampleRecommendations</code> in basketData.js with model outputs.
            </p>
          </div>
        </div>

        <div className="divider" />

        {/* ── Association rules table ───────────────────────────── */}
        <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', marginBottom: '0.5rem' }}>
          Top Association Rules
        </h3>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
          Sort by any metric. Support = how often the rule occurs. Confidence = precision. Lift = strength above random.
        </p>

        {/* Sort controls */}
        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
          {['lift','confidence','support'].map(col => (
            <button
              key={col}
              id={`sort-${col}`}
              className={`btn ${sortBy === col ? 'btn-primary' : 'btn-ghost'} btn-sm`}
              onClick={() => setSortBy(col)}
            >
              Sort by {col}
            </button>
          ))}
        </div>

        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <table className="promo-rules-table">
            <thead>
              <tr>
                <th>Antecedents → Consequents</th>
                <th>Support</th>
                <th>Confidence</th>
                <th>Lift</th>
              </tr>
            </thead>
            <tbody>
              {sortedRules.map((rule, i) => (
                <tr key={i}>
                  <td style={{ color: 'var(--text-primary)', fontWeight: 500 }}>
                    <span style={{ color: 'var(--text-muted)' }}>{rule.antecedents}</span>
                    {' → '}
                    <span style={{ color: 'var(--purple-light)', fontWeight: 600 }}>{rule.consequents}</span>
                  </td>
                  <td>{(rule.support * 100).toFixed(1)}%</td>
                  <td>{(rule.confidence * 100).toFixed(0)}%</td>
                  <td>
                    <span className={`lift-badge ${rule.lift > 3 ? 'lift-high' : rule.lift > 2 ? 'lift-medium' : 'lift-low'}`}>
                      {rule.lift.toFixed(2)}×
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="divider" />

        {/* ── Discount tier cards ───────────────────────────────── */}
        <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', marginBottom: '1.5rem' }}>
          Segment Discount Strategy
        </h3>
        <div className="grid-4">
          {discountTiers.map((tier, i) => {
            const activeSegment = recommendation && !recommendation.notFound ? recommendation.segment : null;
            const hasActiveSearch = activeSegment !== null;
            const isActive = activeSegment === tier.segment;

            const cardStyle = {
              textAlign: 'center',
              animationDelay: `${i * 0.1}s`,
              position: 'relative',
              transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
              ...(hasActiveSearch ? (
                isActive ? {
                  border: '2px solid var(--purple-light)',
                  boxShadow: '0 0 20px rgba(167, 139, 250, 0.45)',
                  transform: 'scale(1.06)',
                  background: 'var(--bg-elevated)',
                  zIndex: 2,
                } : {
                  opacity: 0.35,
                  transform: 'scale(0.95)',
                  filter: 'grayscale(30%)',
                }
              ) : {})
            };

            return (
              <div key={i} className="card" style={cardStyle}>
                {isActive && (
                  <span style={{
                    position: 'absolute',
                    top: '0.6rem',
                    right: '0.6rem',
                    fontSize: '0.62rem',
                    fontWeight: 700,
                    background: 'var(--purple-light)',
                    color: '#fff',
                    padding: '0.2rem 0.5rem',
                    borderRadius: '4px',
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                    boxShadow: '0 0 8px rgba(167, 139, 250, 0.6)',
                  }}>
                    Matched
                  </span>
                )}
                <div style={{ fontSize: '2rem', marginBottom: '0.75rem' }}>{tier.icon}</div>
                <div style={{ fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: '0.95rem', marginBottom: '0.25rem' }}>
                  {tier.segment}
                </div>
                <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.6rem', fontWeight: 800, color: 'var(--amber)', margin: '0.5rem 0' }}>
                  {tier.discount}
                </div>
                <span className="badge badge-amber" style={{ marginBottom: '0.75rem' }}>{tier.type}</span>
                
                {/* Associated Products list */}
                <div style={{ marginTop: '0.75rem', borderTop: '1px solid var(--border-subtle)', paddingTop: '0.75rem' }}>
                  <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.4rem', fontWeight: 600, letterSpacing: '0.05em', textTransform: 'uppercase' }}>
                    Associated Products
                  </span>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem', justifyContent: 'center' }}>
                    {tier.items?.map((prod, idx) => (
                      <span key={idx} style={{
                        fontSize: '0.65rem',
                        background: 'rgba(255, 255, 255, 0.04)',
                        border: '1px solid var(--border-soft)',
                        padding: '0.12rem 0.4rem',
                        borderRadius: '4px',
                        color: 'var(--text-secondary)'
                      }}>
                        {prod}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )
          })}
        </div>

        <div className="divider" style={{ margin: '3rem 0' }} />

        {/* ── Customer Segment Promotions Strategy ────────────────── */}
        <div className="card" style={{ background: 'var(--bg-surface)', border: '1px solid var(--border-soft)', padding: '2.5rem', textAlign: 'left' }}>
          <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.4rem', fontWeight: 800, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            🎯 Customer Segment Promotions Strategy
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '2rem', lineHeight: 1.6 }}>
            Based on the Apriori association rules derived from actual basket co-occurrences, we have designed targeted promotions for each customer segment. These promotions leverage high-lift item pairings to drive cross-selling and increase average order value.
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1.5rem' }}>
            
            {/* Gamers & Tech Enthusiasts */}
            <div className="card" style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '1.5rem', border: '1px solid var(--border-soft)' }}>
              <h4 style={{ fontFamily: 'var(--font-display)', fontSize: '1.05rem', color: 'var(--purple-light)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                🎮 Gamers & Tech Enthusiasts
              </h4>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
                <strong>Key Associations:</strong> Energy Drinks ↔ AirPods ↔ Bluetooth Headphones ↔ Laptops
              </p>
              <div style={{ background: 'rgba(167, 139, 250, 0.05)', padding: '0.75rem 1rem', borderRadius: '6px', borderLeft: '3px solid var(--purple-light)', fontSize: '0.8rem', lineHeight: 1.5 }}>
                <strong>Promotion:</strong> "Level Up Your Setup" <br />
                <strong>Offer:</strong> Buy any premium wireless audio device (AirPods or Bluetooth Headphones) and get a 12-pack of Energy Drinks for 50% off.
              </div>
            </div>

            {/* Vegans */}
            <div className="card" style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '1.5rem', border: '1px solid var(--border-soft)' }}>
              <h4 style={{ fontFamily: 'var(--font-display)', fontSize: '1.05rem', color: 'var(--teal)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                🥗 Vegans
              </h4>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
                <strong>Key Associations:</strong> Salad ↔ Asparagus ↔ Avocado ↔ Spinach ↔ Tomatoes
              </p>
              <div style={{ background: 'rgba(45, 212, 191, 0.05)', padding: '0.75rem 1rem', borderRadius: '6px', borderLeft: '3px solid var(--teal)', fontSize: '0.8rem', lineHeight: 1.5 }}>
                <strong>Promotion:</strong> "Fresh Harvest Bundle" <br />
                <strong>Offer:</strong> 15% off a "Green Core" bundle (Asparagus, Spinach, and Tomatoes) when purchased alongside any pre-made Salad or Avocado.
              </div>
            </div>

            {/* Big Families */}
            <div className="card" style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '1.5rem', border: '1px solid var(--border-soft)' }}>
              <h4 style={{ fontFamily: 'var(--font-display)', fontSize: '1.05rem', color: '#60a5fa', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                👨‍👩‍👧‍👦 Big Families
              </h4>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
                <strong>Key Associations:</strong> Dog Food ↔ Babies Food ↔ Napkins ↔ Toilet Paper
              </p>
              <div style={{ background: 'rgba(59, 130, 246, 0.05)', padding: '0.75rem 1rem', borderRadius: '6px', borderLeft: '3px solid #3b82f6', fontSize: '0.8rem', lineHeight: 1.5 }}>
                <strong>Promotion:</strong> "Family & Furry Friends Stock-Up" <br />
                <strong>Offer:</strong> Buy 2 large bags of Pet Food, get a jumbo pack of household paper goods (Napkins/Toilet Paper) or Baby Food for 20% off.
              </div>
            </div>

            {/* Clean & Healthy / Karens */}
            <div className="card" style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '1.5rem', border: '1px solid var(--border-soft)' }}>
              <h4 style={{ fontFamily: 'var(--font-display)', fontSize: '1.05rem', color: 'var(--rose)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                🧼 Clean & Healthy / Karens
              </h4>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
                <strong>Key Associations:</strong> Deodorant ↔ Shampoo ↔ Shower Gel ↔ Toothpaste
              </p>
              <div style={{ background: 'rgba(244, 63, 94, 0.05)', padding: '0.75rem 1rem', borderRadius: '6px', borderLeft: '3px solid var(--rose)', fontSize: '0.8rem', lineHeight: 1.5 }}>
                <strong>Promotion:</strong> "Premium Personal Care Package" <br />
                <strong>Offer:</strong> Buy any 3 daily personal care items (Shampoo, Shower Gel, Deodorant) and get a free travel-size premium toothpaste or 10% off the total.
              </div>
            </div>

            {/* Average Customers & Loyal Big Spenders */}
            <div className="card" style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '1.5rem', border: '1px solid var(--border-soft)', gridColumn: 'span 2' }}>
              <h4 style={{ fontFamily: 'var(--font-display)', fontSize: '1.05rem', color: 'var(--amber)', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                🍞 Average Customers & Loyal Big Spenders
              </h4>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
                <strong>Key Associations:</strong> Eggs ↔ Butter ↔ Honey ↔ Cereals ↔ Fresh Bread
              </p>
              <div style={{ background: 'rgba(245, 158, 11, 0.05)', padding: '0.75rem 1rem', borderRadius: '6px', borderLeft: '3px solid var(--amber)', fontSize: '0.8rem', lineHeight: 1.5 }}>
                <strong>Promotion:</strong> "Morning Essentials Weekend Special" <br />
                <strong>Offer:</strong> The Ultimate Breakfast Bundle — Fresh Bread, Butter, and a dozen Eggs for a fixed discounted price (e.g., €5.99).
              </div>
            </div>

          </div>
        </div>

      </div>
    </section>
  )
}
