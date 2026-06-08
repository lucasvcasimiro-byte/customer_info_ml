/**
 * Store.jsx — NOVAIMS Grocery Store Simulator
 *
 * Simulates a supermarket e-commerce page.
 * - Reads activeVoucher (from Promotions) to know which products have discounts
 * - Sidebar: category filter, price range filter, "com desconto" filter
 * - Product grid with AI-generated category images
 * - Shopping cart panel with per-item pricing and discount breakdown
 */
import { useState, useMemo, useEffect } from 'react'
import { PRODUCTS, CATEGORIES, PRICE_RANGES, CATEGORY_IMAGES } from '../data/storeProducts'

// ─── helpers ───────────────────────────────────────────────────────────────
function capitalize(str) {
  return str.replace(/\b\w/g, c => c.toUpperCase())
}

// ═══════════════════════════════════════════════════════════════════════════
export default function Store({ activeVoucher }) {
  const [search,         setSearch]        = useState('')
  const [activeCategory, setCategory]     = useState('Todas')
  const [priceFilter,    setPriceFilter]   = useState(null)   // PRICE_RANGES index | null
  const [onlyDiscount,   setOnlyDiscount]  = useState(false)
  const [onlyFavorites,  setOnlyFavorites] = useState(false)
  const [cart,           setCart]          = useState([])      // [{product, qty}]
  const [cartOpen,       setCartOpen]      = useState(false)

  const [couponInput,    setCouponInput]   = useState('')
  const [couponError,    setCouponError]   = useState('')
  const [appliedCoupons, setAppliedCoupons] = useState(new Set())

  useEffect(() => {
    const handleApplyCoupon = (e) => {
      const code = e.detail
      if (code && (code === 'lucas5' || code === 'lima5' || code === 'lince5')) {
        setAppliedCoupons(prev => {
          const next = new Set(prev)
          next.add(code)
          return next
        })
      }
    }
    window.addEventListener('apply-coupon-event', handleApplyCoupon)
    return () => window.removeEventListener('apply-coupon-event', handleApplyCoupon)
  }, [])

  const applyCouponCode = () => {
    const code = couponInput.trim().toLowerCase()
    if (!code) return
    if (code !== 'lucas5' && code !== 'lima5' && code !== 'lince5') {
      setCouponError('Cupão inválido!')
      return
    }
    if (appliedCoupons.has(code)) {
      setCouponError('Cupão já aplicado!')
      return
    }
    setAppliedCoupons(prev => {
      const next = new Set(prev)
      next.add(code)
      return next
    })
    setCouponInput('')
    setCouponError('')
  }

  const removeCouponCode = (code) => {
    setAppliedCoupons(prev => {
      const next = new Set(prev)
      next.delete(code)
      return next
    })
  }

  // Load favorites from localStorage
  const [favorites, setFavorites] = useState(() => {
    try {
      const saved = localStorage.getItem('grocery_favorites')
      return saved ? new Set(JSON.parse(saved)) : new Set()
    } catch {
      return new Set()
    }
  })

  // Toggle favorite helper
  const toggleFavorite = (productId) => {
    setFavorites(prev => {
      const next = new Set(prev)
      if (next.has(productId)) {
        next.delete(productId)
      } else {
        next.add(productId)
      }
      try {
        localStorage.setItem('grocery_favorites', JSON.stringify(Array.from(next)))
      } catch (e) {
        console.error('Failed to save favorites:', e)
      }
      return next
    })
  }

  // Parse past basket items
  const previousBasketProducts = useMemo(() => {
    if (!activeVoucher?.basket || activeVoucher.basket.length === 0) return []
    return activeVoucher.basket.map(itemName => {
      const matched = PRODUCTS.find(p => p.id.toLowerCase() === itemName.toLowerCase())
      if (matched) return matched
      return { id: itemName.toLowerCase(), name: itemName, category: 'Despensa', price: 1.99 }
    })
  }, [activeVoucher])

  // Re-add previous purchase items
  const repeatLastPurchase = () => {
    setCart(prev => {
      let nextCart = [...prev]
      previousBasketProducts.forEach(prod => {
        const existing = nextCart.find(e => e.product.id === prod.id)
        if (existing) {
          nextCart = nextCart.map(e => e.product.id === prod.id ? { ...e, qty: e.qty + 1 } : e)
        } else {
          nextCart.push({ product: prod, qty: 1 })
        }
      })
      return nextCart
    })
    setCartOpen(true)
  }

  // Build a Set of campaign item names (lowercased) from the active voucher
  const campaignSet = useMemo(() => {
    if (!activeVoucher?.campaignItems) return new Set()
    return new Set(activeVoucher.campaignItems.map(i => i.toLowerCase()))
  }, [activeVoucher])

  const discountPct = activeVoucher
    ? parseInt(activeVoucher.discount) / 100
    : 0

  // ── Filter products ───────────────────────────────────────────────────
  const filtered = useMemo(() => {
    return PRODUCTS.filter(p => {
      const q = search.toLowerCase()
      if (q && !p.name.toLowerCase().includes(q) && !p.id.toLowerCase().includes(q)) return false
      if (activeCategory !== 'Todas' && p.category !== activeCategory) return false
      if (priceFilter !== null) {
        const { min, max } = PRICE_RANGES[priceFilter]
        if (p.price < min || p.price > max) return false
      }
      if (onlyDiscount && !campaignSet.has(p.id.toLowerCase())) return false
      if (onlyFavorites && !favorites.has(p.id)) return false
      return true
    })
  }, [search, activeCategory, priceFilter, onlyDiscount, onlyFavorites, favorites, campaignSet])

  // ── Cart helpers ──────────────────────────────────────────────────────
  const addToCart = (product) => {
    setCart(prev => {
      const existing = prev.find(e => e.product.id === product.id)
      if (existing) return prev.map(e => e.product.id === product.id ? { ...e, qty: e.qty + 1 } : e)
      return [...prev, { product, qty: 1 }]
    })
    setCartOpen(true)
  }

  const removeFromCart = (productId) => {
    setCart(prev => prev.filter(e => e.product.id !== productId))
  }

  const updateQty = (productId, delta) => {
    setCart(prev => prev
      .map(e => e.product.id === productId ? { ...e, qty: Math.max(0, e.qty + delta) } : e)
      .filter(e => e.qty > 0)
    )
  }

  const cartCount = cart.reduce((s, e) => s + e.qty, 0)

  const cartSubtotal = cart.reduce((s, e) => s + e.product.price * e.qty, 0)
  const cartSavings  = cart.reduce((s, e) => {
    if (campaignSet.has(e.product.id.toLowerCase())) {
      return s + e.product.price * e.qty * discountPct
    }
    return s
  }, 0)
  const cartTotal    = cartSubtotal - cartSavings
  const couponDiscountPct = appliedCoupons.size * 0.05
  const couponSavings = cartTotal * couponDiscountPct
  const finalPayableTotal = cartTotal - couponSavings

  return (
    <section id="store" style={{ background: 'var(--bg-base)', minHeight: '100vh' }}>

      {/* ── Store Header ─────────────────────────────────────────────── */}
      <div style={{
        background: 'linear-gradient(135deg, #c0392b 0%, #e74c3c 50%, #e91e63 100%)',
        padding: '0',
        position: 'sticky',
        top: '68px',
        zIndex: 90,
        boxShadow: '0 2px 12px rgba(0,0,0,0.2)',
      }}>
        {/* Top bar */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: '1.5rem',
          padding: '0.75rem 2rem', maxWidth: '1400px', margin: '0 auto',
        }}>
          {/* Logo */}
          <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.6rem', fontWeight: 900, color: '#fff', letterSpacing: '-0.5px', whiteSpace: 'nowrap' }}>
            🏪 NOVAIMS<span style={{ color: '#ffe082' }}>grocery</span>
          </div>

          {/* Search bar */}
          <div style={{ flex: 1, position: 'relative' }}>
            <input
              type="text"
              placeholder="O que procura?"
              value={search}
              onChange={e => setSearch(e.target.value)}
              style={{
                width: '100%', padding: '0.65rem 1rem 0.65rem 2.8rem',
                borderRadius: '25px', border: 'none', fontSize: '0.95rem',
                background: 'rgba(255,255,255,0.95)', outline: 'none',
                boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
              }}
            />
            <span style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', fontSize: '1.1rem' }}>🔍</span>
          </div>

          {/* Cart button */}
          <button
            onClick={() => setCartOpen(o => !o)}
            style={{
              display: 'flex', alignItems: 'center', gap: '0.5rem',
              background: cartCount > 0 ? '#ffe082' : 'rgba(255,255,255,0.2)',
              color: cartCount > 0 ? '#b71c1c' : '#fff',
              border: 'none', borderRadius: '25px', padding: '0.6rem 1.2rem',
              cursor: 'pointer', fontWeight: 700, fontSize: '0.95rem',
              transition: 'all 0.2s', whiteSpace: 'nowrap',
            }}
          >
            🛒 Carrinho
            {cartCount > 0 && (
              <span style={{
                background: '#c0392b', color: '#fff', borderRadius: '50%',
                width: '22px', height: '22px', display: 'flex', alignItems: 'center',
                justifyContent: 'center', fontSize: '0.75rem', fontWeight: 900,
              }}>{cartCount}</span>
            )}
          </button>
        </div>

        {/* Voucher banner */}
        {activeVoucher ? (
          <div style={{
            background: 'rgba(0,0,0,0.25)', padding: '0.45rem 2rem',
            display: 'flex', alignItems: 'center', gap: '0.75rem',
            maxWidth: '1400px', margin: '0 auto',
          }}>
            <span style={{ fontSize: '1.1rem' }}>🎟️</span>
            <span style={{ color: '#ffe082', fontWeight: 700, fontSize: '0.9rem' }}>
              Voucher ativo — {activeVoucher.nextBestOffer}
            </span>
            <span style={{ color: 'rgba(255,255,255,0.7)', fontSize: '0.8rem' }}>
              · Cliente {activeVoucher.customerId} · Desconto aplicado em:{' '}
              <strong style={{ color: '#fff' }}>{activeVoucher.campaignItems?.join(', ')}</strong>
            </span>
          </div>
        ) : (
          <div style={{
            background: 'rgba(0,0,0,0.15)', padding: '0.45rem 2rem',
            maxWidth: '1400px', margin: '0 auto',
          }}>
            <span style={{ color: 'rgba(255,255,255,0.75)', fontSize: '0.82rem' }}>
              💡 Pesquisa o teu ID de cliente na secção{' '}
              <strong style={{ color: '#ffe082' }}>Promoções</strong>{' '}
              para ativar o teu voucher personalizado!
            </span>
          </div>
        )}
      </div>

      {/* ── Body: sidebar + grid ─────────────────────────────────────── */}
      <div style={{ display: 'flex', maxWidth: '1400px', margin: '0 auto', padding: '1.5rem 2rem', gap: '1.5rem' }}>

        {/* ── Sidebar ───────────────────────────────────────────────── */}
        <aside style={{
          width: '220px', flexShrink: 0,
          display: 'flex', flexDirection: 'column', gap: '1.2rem',
        }}>

          {/* Com Desconto filter */}
          {activeVoucher && (
            <div style={{
              background: onlyDiscount
                ? 'linear-gradient(135deg,#b91c1c,#e74c3c)'
                : 'var(--bg-surface)',
              borderRadius: '12px',
              padding: '1rem',
              border: onlyDiscount ? 'none' : '1px solid var(--border-subtle)',
              cursor: 'pointer',
              transition: 'all 0.2s',
            }} onClick={() => setOnlyDiscount(o => !o)}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontSize: '1.2rem' }}>🏷️</span>
                <span style={{ fontWeight: 700, color: onlyDiscount ? '#fff' : 'var(--text-primary)', fontSize: '0.9rem' }}>
                  Só com Desconto
                </span>
              </div>
              {onlyDiscount && (
                <div style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.85)', marginTop: '0.35rem' }}>
                  A mostrar {activeVoucher.discount} off nos produtos da campanha
                </div>
              )}
            </div>
          )}

          {/* Favorites Filter */}
          <div style={{
            background: onlyFavorites
              ? 'linear-gradient(135deg, #ec4899, #db2777)'
              : 'var(--bg-surface)',
            borderRadius: '12px',
            padding: '1rem',
            border: onlyFavorites ? 'none' : '1px solid var(--border-subtle)',
            cursor: 'pointer',
            transition: 'all 0.2s',
          }} onClick={() => setOnlyFavorites(o => !o)}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ fontSize: '1.2rem' }}>❤️</span>
              <span style={{ fontWeight: 700, color: onlyFavorites ? '#fff' : 'var(--text-primary)', fontSize: '0.9rem' }}>
                Os meus Favoritos
              </span>
            </div>
            {onlyFavorites && (
              <div style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.85)', marginTop: '0.35rem' }}>
                A mostrar os teus favoritos ({favorites.size})
              </div>
            )}
          </div>

          {/* Category filter */}
          <div style={{
            background: 'var(--bg-surface)', borderRadius: '12px', padding: '1rem',
            border: '1px solid var(--border-subtle)',
          }}>
            <div style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.75rem', fontSize: '0.88rem' }}>
              📦 Categoria
            </div>
            {CATEGORIES.map(cat => (
              <button
                key={cat}
                onClick={() => setCategory(cat)}
                style={{
                  display: 'block', width: '100%', textAlign: 'left',
                  padding: '0.35rem 0.5rem', marginBottom: '0.1rem',
                  background: activeCategory === cat ? 'var(--accent-primary)' : 'transparent',
                  color: activeCategory === cat ? '#fff' : 'var(--text-secondary)',
                  border: 'none', borderRadius: '6px', cursor: 'pointer',
                  fontSize: '0.83rem', fontWeight: activeCategory === cat ? 700 : 400,
                  transition: 'all 0.15s',
                }}
              >
                {cat === 'Todas' ? '🛒 Todas' : cat}
              </button>
            ))}
          </div>

          {/* Price filter */}
          <div style={{
            background: 'var(--bg-surface)', borderRadius: '12px', padding: '1rem',
            border: '1px solid var(--border-subtle)',
          }}>
            <div style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.75rem', fontSize: '0.88rem' }}>
              💶 Preço
            </div>
            <button
              onClick={() => setPriceFilter(null)}
              style={{
                display: 'block', width: '100%', textAlign: 'left',
                padding: '0.35rem 0.5rem', marginBottom: '0.1rem',
                background: priceFilter === null ? 'var(--accent-primary)' : 'transparent',
                color: priceFilter === null ? '#fff' : 'var(--text-secondary)',
                border: 'none', borderRadius: '6px', cursor: 'pointer',
                fontSize: '0.83rem', fontWeight: priceFilter === null ? 700 : 400,
                transition: 'all 0.15s',
              }}
            >
              Todos os preços
            </button>
            {PRICE_RANGES.map((r, i) => (
              <button
                key={i}
                onClick={() => setPriceFilter(i)}
                style={{
                  display: 'block', width: '100%', textAlign: 'left',
                  padding: '0.35rem 0.5rem', marginBottom: '0.1rem',
                  background: priceFilter === i ? 'var(--accent-primary)' : 'transparent',
                  color: priceFilter === i ? '#fff' : 'var(--text-secondary)',
                  border: 'none', borderRadius: '6px', cursor: 'pointer',
                  fontSize: '0.83rem', fontWeight: priceFilter === i ? 700 : 400,
                  transition: 'all 0.15s',
                }}
              >
                {r.label}
              </button>
            ))}
          </div>
        </aside>

        {/* ── Product Grid ──────────────────────────────────────────── */}
        <div style={{ flex: 1, minWidth: 0 }}>
          {/* Previous Basket / History Card */}
          {activeVoucher && previousBasketProducts.length > 0 && (
            <div style={{
              background: 'linear-gradient(135deg, rgba(124,58,237,0.08) 0%, rgba(6,182,212,0.08) 100%)',
              border: '1px solid var(--border-soft)',
              borderRadius: '16px',
              padding: '1.25rem',
              marginBottom: '1.5rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.75rem',
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
                <div>
                  <h4 style={{ fontFamily: 'var(--font-display)', fontSize: '0.98rem', fontWeight: 800, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.4rem', margin: 0 }}>
                    📋 Histórico de Compras (Fatura #{activeVoucher.invoiceId || 'N/A'})
                  </h4>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px', marginBottom: 0 }}>
                    Artigos adquiridos na última transação do cliente <strong>{activeVoucher.customerName || `C-${activeVoucher.customerId}`}</strong>.
                  </p>
                </div>
                <button
                  onClick={repeatLastPurchase}
                  style={{
                    background: 'var(--accent-primary)',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '20px',
                    padding: '0.5rem 1.25rem',
                    fontWeight: 700,
                    fontSize: '0.82rem',
                    cursor: 'pointer',
                    boxShadow: '0 2px 8px rgba(124,58,237,0.3)',
                    transition: 'all 0.2s',
                    whiteSpace: 'nowrap',
                  }}
                  onMouseEnter={e => e.currentTarget.style.opacity = '0.9'}
                  onMouseLeave={e => e.currentTarget.style.opacity = '1'}
                >
                  🔁 Repetir Carrinho
                </button>
              </div>

              {/* Items list */}
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.25rem' }}>
                {previousBasketProducts.map((prod, i) => (
                  <div
                    key={`${prod.id}-${i}`}
                    onClick={() => addToCart(prod)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.4rem',
                      background: 'var(--bg-surface)',
                      border: '1px solid var(--border-subtle)',
                      borderRadius: '30px',
                      padding: '0.35rem 0.75rem',
                      fontSize: '0.78rem',
                      cursor: 'pointer',
                      color: 'var(--text-secondary)',
                      transition: 'all 0.15s',
                    }}
                    onMouseEnter={e => {
                      e.currentTarget.style.borderColor = 'var(--accent-primary)'
                      e.currentTarget.style.color = 'var(--text-primary)'
                    }}
                    onMouseLeave={e => {
                      e.currentTarget.style.borderColor = 'var(--border-subtle)'
                      e.currentTarget.style.color = 'var(--text-secondary)'
                    }}
                    title="Adicionar artigo ao carrinho"
                  >
                    <span>{capitalize(prod.name)}</span>
                    <span style={{ fontWeight: 700, color: 'var(--text-muted)' }}>€{prod.price.toFixed(2)}</span>
                    <span style={{ fontSize: '0.75rem', color: 'var(--accent-primary)' }}>+</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Result count */}
          <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1rem' }}>
            {filtered.length} produto{filtered.length !== 1 ? 's' : ''} encontrado{filtered.length !== 1 ? 's' : ''}
            {activeVoucher && onlyDiscount && (
              <span style={{ marginLeft: '0.5rem', color: '#e74c3c', fontWeight: 700 }}>
                · Filtro: {activeVoucher.discount} OFF ativo
              </span>
            )}
          </div>

          {filtered.length === 0 ? (
            <div style={{
              textAlign: 'center', padding: '4rem 2rem',
              color: 'var(--text-muted)', fontSize: '1.1rem',
            }}>
              🔍 Nenhum produto encontrado.<br />
              <span style={{ fontSize: '0.9rem' }}>Tenta outro filtro ou pesquisa.</span>
            </div>
          ) : (
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(185px, 1fr))',
              gap: '1rem',
            }}>
              {filtered.map(product => {
                const hasDiscount = campaignSet.has(product.id.toLowerCase()) && activeVoucher
                const discountedPrice = hasDiscount ? product.price * (1 - discountPct) : product.price
                const inCart = cart.find(e => e.product.id === product.id)
                const isFav = favorites.has(product.id)

                return (
                  <div
                    key={product.id}
                    style={{
                      background: 'var(--bg-surface)',
                      borderRadius: '14px',
                      border: hasDiscount
                        ? '2px solid #e74c3c'
                        : '1px solid var(--border-subtle)',
                      overflow: 'hidden',
                      transition: 'transform 0.2s, box-shadow 0.2s',
                      cursor: 'default',
                      position: 'relative',
                    }}
                    onMouseEnter={e => {
                      e.currentTarget.style.transform = 'translateY(-3px)'
                      e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.12)'
                    }}
                    onMouseLeave={e => {
                      e.currentTarget.style.transform = ''
                      e.currentTarget.style.boxShadow = ''
                    }}
                  >
                    {/* Discount badge */}
                    {hasDiscount && (
                      <div style={{
                        position: 'absolute', top: '8px', left: '8px', zIndex: 2,
                        background: 'linear-gradient(135deg,#c0392b,#e74c3c)',
                        color: '#fff', fontWeight: 900, fontSize: '0.8rem',
                        borderRadius: '20px', padding: '3px 10px',
                        boxShadow: '0 2px 6px rgba(192,57,43,0.4)',
                      }}>
                        -{activeVoucher.discount}
                      </div>
                    )}

                    {/* Favorite button */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        toggleFavorite(product.id)
                      }}
                      style={{
                        position: 'absolute', top: '8px', right: '8px', zIndex: 5,
                        background: 'rgba(20,24,50,0.6)',
                        backdropFilter: 'blur(4px)',
                        border: '1px solid rgba(255,255,255,0.2)',
                        color: isFav ? '#f43f5e' : '#e2e8f0',
                        borderRadius: '50%',
                        width: '30px',
                        height: '30px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        cursor: 'pointer',
                        fontSize: '0.95rem',
                        transition: 'all 0.2s',
                        outline: 'none',
                      }}
                      onMouseEnter={e => {
                        e.currentTarget.style.transform = 'scale(1.1)'
                        e.currentTarget.style.background = 'rgba(20,24,50,0.85)'
                      }}
                      onMouseLeave={e => {
                        e.currentTarget.style.transform = ''
                        e.currentTarget.style.background = 'rgba(20,24,50,0.6)'
                      }}
                      title={isFav ? "Remover dos favoritos" : "Adicionar aos favoritos"}
                    >
                      {isFav ? '❤️' : '🤍'}
                    </button>

                    {/* Product image */}
                    <div style={{
                      height: '120px', overflow: 'hidden',
                      background: '#f8f8f8',
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                    }}>
                      <img
                        src={product.image || CATEGORY_IMAGES[product.category]}
                        alt={product.name}
                        style={{
                          width: '100%', height: '100%', objectFit: 'cover',
                          filter: hasDiscount ? 'none' : 'none',
                        }}
                      />
                    </div>

                    {/* Product info */}
                    <div style={{ padding: '0.75rem' }}>
                      <div style={{
                        fontSize: '0.82rem', color: 'var(--text-muted)',
                        marginBottom: '0.2rem', textTransform: 'uppercase',
                        letterSpacing: '0.3px',
                      }}>
                        {product.category}
                      </div>
                      <div style={{
                        fontWeight: 700, color: 'var(--text-primary)',
                        fontSize: '0.9rem', marginBottom: '0.5rem',
                        lineHeight: 1.3,
                      }}>
                        {capitalize(product.name)}
                      </div>

                      {/* Price display */}
                      <div style={{ marginBottom: '0.65rem' }}>
                        {hasDiscount ? (
                          <>
                            <span style={{
                              fontSize: '0.78rem', color: 'var(--text-muted)',
                              textDecoration: 'line-through', marginRight: '0.4rem',
                            }}>
                              €{product.price.toFixed(2)}
                            </span>
                            <span style={{
                              fontSize: '1.1rem', fontWeight: 900, color: '#e74c3c',
                            }}>
                              €{discountedPrice.toFixed(2)}
                            </span>
                          </>
                        ) : (
                          <span style={{
                            fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-primary)',
                          }}>
                            €{product.price.toFixed(2)}
                          </span>
                        )}
                      </div>

                      {/* Add to cart */}
                      <button
                        onClick={() => addToCart(product)}
                        style={{
                          width: '100%', padding: '0.45rem',
                          background: hasDiscount
                            ? 'linear-gradient(135deg,#c0392b,#e74c3c)'
                            : 'var(--accent-primary)',
                          color: '#fff', border: 'none', borderRadius: '8px',
                          cursor: 'pointer', fontWeight: 700, fontSize: '0.85rem',
                          transition: 'opacity 0.15s',
                        }}
                        onMouseEnter={e => e.currentTarget.style.opacity = '0.85'}
                        onMouseLeave={e => e.currentTarget.style.opacity = '1'}
                      >
                        {inCart ? `✓ Adicionado (${inCart.qty})` : '+ Adicionar'}
                      </button>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>

      {/* ── Cart Drawer ───────────────────────────────────────────────── */}
      {cartOpen && (
        <div style={{
          position: 'fixed', top: 0, right: 0, width: '380px', height: '100vh',
          background: 'var(--bg-surface)', boxShadow: '-4px 0 24px rgba(0,0,0,0.15)',
          zIndex: 999, display: 'flex', flexDirection: 'column',
          borderLeft: '1px solid var(--border-subtle)',
        }}>
          {/* Drawer header */}
          <div style={{
            padding: '1.25rem 1.5rem',
            borderBottom: '1px solid var(--border-subtle)',
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            background: 'linear-gradient(135deg,#c0392b,#e74c3c)',
          }}>
            <span style={{ fontWeight: 900, fontSize: '1.1rem', color: '#fff' }}>
              🛒 Carrinho ({cartCount})
            </span>
            <button
              onClick={() => setCartOpen(false)}
              style={{
                background: 'rgba(255,255,255,0.2)', border: 'none', color: '#fff',
                borderRadius: '50%', width: '32px', height: '32px', cursor: 'pointer',
                fontSize: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'center',
              }}
            >✕</button>
          </div>

          {/* Voucher notice in cart */}
          {activeVoucher && cartSavings > 0 && (
            <div style={{
              background: 'rgba(231,76,60,0.08)', borderBottom: '1px solid var(--border-subtle)',
              padding: '0.6rem 1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem',
            }}>
              <span style={{ fontSize: '1rem' }}>🎟️</span>
              <span style={{ fontSize: '0.82rem', color: '#c0392b', fontWeight: 600 }}>
                Voucher aplicado — {activeVoucher.discount} off em produtos elegíveis
              </span>
            </div>
          )}

          {/* Cart items */}
          <div style={{ flex: 1, overflowY: 'auto', padding: '1rem 1.5rem' }}>
            {cart.length === 0 ? (
              <div style={{
                textAlign: 'center', padding: '3rem 1rem',
                color: 'var(--text-muted)', fontSize: '0.95rem',
              }}>
                🛒 O carrinho está vazio.<br />
                <span style={{ fontSize: '0.85rem' }}>Adiciona produtos para começar!</span>
              </div>
            ) : (
              cart.map(({ product, qty }) => {
                const hasDisc = campaignSet.has(product.id.toLowerCase()) && activeVoucher
                const baseLineTotal = product.price * qty
                const discLineTotal = hasDisc ? baseLineTotal * (1 - discountPct) : baseLineTotal
                const lineSaving   = baseLineTotal - discLineTotal

                return (
                  <div
                    key={product.id}
                    style={{
                      display: 'flex', flexDirection: 'column', gap: '0.3rem',
                      padding: '0.85rem 0',
                      borderBottom: '1px solid var(--border-subtle)',
                    }}
                  >
                    {/* Row 1: name + qty controls + remove */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span style={{ flex: 1, fontWeight: 600, fontSize: '0.88rem', color: 'var(--text-primary)' }}>
                        {capitalize(product.name)}
                        {hasDisc && (
                          <span style={{
                            marginLeft: '0.4rem', background: '#e74c3c', color: '#fff',
                            fontSize: '0.65rem', borderRadius: '4px', padding: '1px 5px',
                            fontWeight: 700,
                          }}>
                            -{activeVoucher.discount}
                          </span>
                        )}
                      </span>
                      {/* Qty controls */}
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                        <button onClick={() => updateQty(product.id, -1)}
                          style={qtyBtnStyle}>–</button>
                        <span style={{ fontWeight: 700, fontSize: '0.9rem', minWidth: '20px', textAlign: 'center' }}>
                          {qty}
                        </span>
                        <button onClick={() => updateQty(product.id, +1)}
                          style={qtyBtnStyle}>+</button>
                      </div>
                      <button onClick={() => removeFromCart(product.id)}
                        style={{
                          background: 'none', border: 'none', color: 'var(--text-muted)',
                          cursor: 'pointer', fontSize: '0.85rem', padding: '0 0.25rem',
                        }}>🗑️</button>
                    </div>

                    {/* Row 2: price breakdown */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        {qty} × €{product.price.toFixed(2)}
                      </span>
                      <div style={{ textAlign: 'right' }}>
                        {hasDisc ? (
                          <>
                            <div style={{
                              fontSize: '0.78rem', color: 'var(--text-muted)',
                              textDecoration: 'line-through',
                            }}>
                              €{baseLineTotal.toFixed(2)}
                            </div>
                            <div style={{ fontSize: '0.95rem', fontWeight: 900, color: '#e74c3c' }}>
                              €{discLineTotal.toFixed(2)}
                            </div>
                            <div style={{ fontSize: '0.72rem', color: '#e74c3c' }}>
                              -€{lineSaving.toFixed(2)} poupança
                            </div>
                          </>
                        ) : (
                          <div style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                            €{baseLineTotal.toFixed(2)}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )
              })
            )}
          </div>

          {/* ── Cart summary ──────────────────────────────────────────── */}
          {cart.length > 0 && (
            <div style={{
              padding: '1.25rem 1.5rem',
              borderTop: '2px solid var(--border-subtle)',
              background: 'var(--bg-base)',
            }}>
              {/* Coupon Code Input */}
              <div style={{ marginBottom: '0.85rem' }}>
                <label style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontWeight: 700, display: 'block', marginBottom: '0.3rem', letterSpacing: '0.5px' }}>
                  🎫 APLICAR CUPÃO (lucas5, lima5, lince5)
                </label>
                <div style={{ display: 'flex', gap: '0.4rem' }}>
                  <input
                    type="text"
                    placeholder="Código (ex: lucas5)"
                    value={couponInput}
                    onChange={e => setCouponInput(e.target.value)}
                    style={{
                      flex: 1,
                      padding: '0.45rem 0.75rem',
                      borderRadius: '8px',
                      border: '1px solid var(--border-subtle)',
                      background: 'var(--bg-surface)',
                      color: 'var(--text-primary)',
                      fontSize: '0.82rem',
                      outline: 'none',
                    }}
                  />
                  <button
                    onClick={applyCouponCode}
                    style={{
                      background: 'var(--accent-primary)',
                      color: '#fff',
                      border: 'none',
                      borderRadius: '8px',
                      padding: '0.45rem 0.9rem',
                      fontSize: '0.82rem',
                      fontWeight: 700,
                      cursor: 'pointer',
                    }}
                  >
                    Aplicar
                  </button>
                </div>
                {couponError && (
                  <span style={{ fontSize: '0.7rem', color: 'var(--rose)', marginTop: '0.25rem', display: 'block', fontWeight: 600 }}>
                    ⚠️ {couponError}
                  </span>
                )}
                {appliedCoupons.size > 0 && (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.45rem' }}>
                    {Array.from(appliedCoupons).map(cp => (
                      <span
                        key={cp}
                        style={{
                          background: 'rgba(16,185,129,0.15)',
                          color: '#10b981',
                          border: '1px solid rgba(16,185,129,0.25)',
                          borderRadius: '12px',
                          padding: '0.15rem 0.5rem',
                          fontSize: '0.72rem',
                          fontWeight: 700,
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.25rem',
                        }}
                      >
                        {cp} (-5%)
                        <span
                          onClick={() => removeCouponCode(cp)}
                          style={{ cursor: 'pointer', color: '#ef4444', marginLeft: '0.15rem', fontWeight: 900 }}
                        >✕</span>
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Subtotal without discount */}
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
                <span style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>Subtotal (sem desconto)</span>
                <span style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>€{cartSubtotal.toFixed(2)}</span>
              </div>

              {/* Savings */}
              {cartSavings > 0 && (
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
                  <span style={{ color: '#e74c3c', fontWeight: 600, fontSize: '0.88rem' }}>
                    🎟️ Desconto ({activeVoucher.discount})
                  </span>
                  <span style={{ color: '#e74c3c', fontWeight: 700, fontSize: '0.88rem' }}>
                    -€{cartSavings.toFixed(2)}
                  </span>
                </div>
              )}

              {/* Coupon savings */}
              {couponSavings > 0 && (
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
                  <span style={{ color: '#10b981', fontWeight: 600, fontSize: '0.88rem' }}>
                    🎫 Desconto Cupões (-{appliedCoupons.size * 5}%)
                  </span>
                  <span style={{ color: '#10b981', fontWeight: 700, fontSize: '0.88rem' }}>
                    -€{couponSavings.toFixed(2)}
                  </span>
                </div>
              )}

              {/* Divider */}
              <div style={{ height: '1px', background: 'var(--border-subtle)', margin: '0.75rem 0' }} />

              {/* Total */}
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <span style={{ fontWeight: 900, fontSize: '1.05rem', color: 'var(--text-primary)' }}>
                  TOTAL A PAGAR
                </span>
                <span style={{ fontWeight: 900, fontSize: '1.25rem', color: 'var(--accent-primary)' }}>
                  €{finalPayableTotal.toFixed(2)}
                </span>
              </div>

              {cartSavings > 0 && (
                <div style={{
                  background: 'rgba(231,76,60,0.08)', borderRadius: '8px',
                  padding: '0.6rem 0.75rem', marginBottom: '0.85rem',
                  fontSize: '0.82rem', color: '#c0392b', fontWeight: 600,
                  textAlign: 'center',
                }}>
                  🎉 Poupaste €{cartSavings.toFixed(2)} com o voucher de {activeVoucher.discount}!
                </div>
              )}

              <button
                style={{
                  width: '100%', padding: '0.85rem',
                  background: 'linear-gradient(135deg,#c0392b,#e74c3c)',
                  color: '#fff', border: 'none', borderRadius: '10px',
                  cursor: 'pointer', fontWeight: 900, fontSize: '1rem',
                  boxShadow: '0 4px 12px rgba(192,57,43,0.35)',
                  transition: 'opacity 0.15s',
                }}
                onMouseEnter={e => e.currentTarget.style.opacity = '0.9'}
                onMouseLeave={e => e.currentTarget.style.opacity = '1'}
                onClick={() => alert(`Pedido confirmado!\nTotal a pagar: €${finalPayableTotal.toFixed(2)}${cartSavings > 0 ? `\nPoupança Voucher: €${cartSavings.toFixed(2)}` : ''}${couponSavings > 0 ? `\nPoupança Cupões: €${couponSavings.toFixed(2)}` : ''}`)}
              >
                Finalizar Compra →
              </button>
            </div>
          )}
        </div>
      )}

      {/* Cart overlay backdrop */}
      {cartOpen && (
        <div
          onClick={() => setCartOpen(false)}
          style={{
            position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.3)',
            zIndex: 998, backdropFilter: 'blur(2px)',
          }}
        />
      )}
    </section>
  )
}

const qtyBtnStyle = {
  background: 'var(--bg-base)',
  border: '1px solid var(--border-subtle)',
  borderRadius: '4px', width: '24px', height: '24px',
  cursor: 'pointer', fontWeight: 700, fontSize: '0.9rem',
  display: 'flex', alignItems: 'center', justifyContent: 'center',
  color: 'var(--text-primary)',
}
