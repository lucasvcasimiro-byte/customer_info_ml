/**
 * basketData.js
 * ─────────────────────────────────────────────────────────────────────────────
 * PLACEHOLDER DATA — Replace with real basket/transaction data.
 *
 * How to swap:
 *   1. Export association rules from mlxtend as CSV:
 *      rules.to_csv('association_rules.csv', index=False)
 *   2. Export customer-item matrix or transaction log similarly.
 *   3. Load them here or parse them in the Promotions section.
 *
 * Used by: sections/Promotions.jsx
 * ─────────────────────────────────────────────────────────────────────────────
 */

// ── Association rules (from mlxtend / Apriori) ───────────────────────────────
// TODO: Replace with rules exported from your notebook
export const associationRules = [
  {
    antecedents: 'Bread, Butter',
    consequents: 'Milk',
    support: 0.142,
    confidence: 0.78,
    lift: 3.24,
  },
  {
    antecedents: 'Pasta',
    consequents: 'Tomato Sauce',
    support: 0.118,
    confidence: 0.82,
    lift: 2.91,
  },
  {
    antecedents: 'Beer',
    consequents: 'Snacks, Chips',
    support: 0.094,
    confidence: 0.71,
    lift: 2.68,
  },
  {
    antecedents: 'Coffee',
    consequents: 'Biscuits',
    support: 0.087,
    confidence: 0.66,
    lift: 2.41,
  },
  {
    antecedents: 'Yoghurt, Cereal',
    consequents: 'Orange Juice',
    support: 0.076,
    confidence: 0.63,
    lift: 2.17,
  },
  {
    antecedents: 'Chicken',
    consequents: 'Rice, Vegetables',
    support: 0.069,
    confidence: 0.58,
    lift: 1.93,
  },
  {
    antecedents: 'Wine',
    consequents: 'Cheese',
    support: 0.062,
    confidence: 0.74,
    lift: 1.85,
  },
  {
    antecedents: 'Shampoo',
    consequents: 'Conditioner',
    support: 0.055,
    confidence: 0.69,
    lift: 1.72,
  },
]

// ── Top items by frequency ────────────────────────────────────────────────────
// TODO: Replace with actual item frequency counts from your notebook
export const topItems = {
  labels: ['Milk', 'Bread', 'Vegetables', 'Fruit', 'Meat', 'Snacks', 'Beverages', 'Dairy'],
  counts: [892, 814, 731, 698, 645, 512, 487, 423],
}

// ── Placeholder customer recommendations ─────────────────────────────────────
// TODO: Replace with real model predictions per customer ID
export const sampleRecommendations = {
  'C001': {
    segment: 'Premium Large Families',
    nextBestOffer: 'Bundle: School-Week Groceries (save €5.00)',
    propensity: 0.87,
    items: ['Milk', 'Bread', 'Cereal', 'Fruit'],
    discount: '15%',
  },
  'C042': {
    segment: 'Vegetable Heavy / Vegetarian',
    nextBestOffer: '15% off Organic Vegetables Subscription',
    propensity: 0.71,
    items: ['Vegetables', 'Fruit', 'Rice'],
    discount: '15%',
  },
  'C198': {
    segment: 'Promo-Sensitive Shoppers',
    nextBestOffer: '25% off Next Visit (Promotional Items)',
    propensity: 0.55,
    items: ['Bread', 'Milk', 'Snacks'],
    discount: '25%',
  },
  'C222': {
    segment: 'Tech & Late-Hour Shoppers',
    nextBestOffer: '10% off Electronics Flash Sale (after 18:00)',
    propensity: 0.79,
    items: ['Electronics', 'Videogames', 'Non-Alcoholic Drinks'],
    discount: '10%',
  },
}

// ── Lift chart data per product category ─────────────────────────────────────
// TODO: Replace with actual lift values from your basket analysis
export const liftChartData = {
  categories: ['Bread+Butter→Milk', 'Pasta→Sauce', 'Beer→Snacks', 'Coffee→Biscuits', 'Yoghurt→OJ', 'Chicken→Rice', 'Wine→Cheese', 'Shampoo→Cond.'],
  lift:        [3.24, 2.91, 2.68, 2.41, 2.17, 1.93, 1.85, 1.72],
  confidence:  [0.78, 0.82, 0.71, 0.66, 0.63, 0.58, 0.74, 0.69],
}

// ── Discount tiers (for future personalisation module) ────────────────────────
// TODO: Connect to real pricing/promotion engine
export const discountTiers = [
  { segment: 'Premium Large Families',      discount: '15–20%', type: 'Exclusive',    icon: '👨‍👩‍👧‍👦' },
  { segment: 'Vegetable Heavy / Vegetarian', discount: '10–15%', type: 'Healthy Subs', icon: '🥗' },
  { segment: 'Promo-Sensitive Shoppers',     discount: '20–25%', type: 'Win-back',    icon: '📢' },
  { segment: 'Tech & Late-Hour Shoppers',    discount: '5–10%',  type: 'Late Flash',   icon: '⚡' },
]
