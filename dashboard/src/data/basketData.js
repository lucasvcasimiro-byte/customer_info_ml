/**
 * basketData.js
 * ─────────────────────────────────────────────────────────────────────────────
 * Real basket/transaction association rules and discount tiers.
 * Automatically generated from basket_fixed.ipynb outputs.
 * ─────────────────────────────────────────────────────────────────────────────
 */

// ── Association rules (from mlxtend / Apriori) ───────────────────────────────
export const associationRules = [
  {
    "antecedents": "Airpods",
    "consequents": "Iphone 10",
    "support": 0.008,
    "confidence": 0.4211,
    "lift": 9.15
  },
  {
    "antecedents": "Iphone 10",
    "consequents": "Airpods",
    "support": 0.008,
    "confidence": 0.3529,
    "lift": 9.15
  },
  {
    "antecedents": "Energy Drink",
    "consequents": "Bluetooth Headphones",
    "support": 0.012,
    "confidence": 0.4571,
    "lift": 9.06
  },
  {
    "antecedents": "Bluetooth Headphones",
    "consequents": "Energy Drink",
    "support": 0.012,
    "confidence": 0.3812,
    "lift": 9.06
  },
  {
    "antecedents": "Iphone 10",
    "consequents": "Bluetooth Headphones",
    "support": 0.009,
    "confidence": 0.3958,
    "lift": 8.8
  },
  {
    "antecedents": "Bluetooth Headphones",
    "consequents": "Iphone 10",
    "support": 0.009,
    "confidence": 0.2857,
    "lift": 8.8
  },
  {
    "antecedents": "Energy Drink",
    "consequents": "Protein Bar",
    "support": 0.011,
    "confidence": 0.3667,
    "lift": 8.12
  },
  {
    "antecedents": "Protein Bar",
    "consequents": "Energy Drink",
    "support": 0.011,
    "confidence": 0.3235,
    "lift": 8.12
  },
  {
    "antecedents": "Megaman Zero 3",
    "consequents": "Airpods",
    "support": 0.004,
    "confidence": 0.5417,
    "lift": 7.74
  },
  {
    "antecedents": "Airpods",
    "consequents": "Megaman Zero 3",
    "support": 0.004,
    "confidence": 0.2105,
    "lift": 7.74
  },
  {
    "antecedents": "Bluetooth Headphones",
    "consequents": "Protein Bar",
    "support": 0.01,
    "confidence": 0.3125,
    "lift": 7.57
  },
  {
    "antecedents": "Protein Bar",
    "consequents": "Bluetooth Headphones",
    "support": 0.01,
    "confidence": 0.2941,
    "lift": 7.57
  },
  {
    "antecedents": "Airpods",
    "consequents": "Energy Drink",
    "support": 0.008,
    "confidence": 0.4211,
    "lift": 7.43
  },
  {
    "antecedents": "Energy Drink",
    "consequents": "Airpods",
    "support": 0.008,
    "confidence": 0.3077,
    "lift": 7.43
  },
  {
    "antecedents": "Final Fantasy Xxii",
    "consequents": "Airpods",
    "support": 0.0065,
    "confidence": 0.913,
    "lift": 7.38
  }
];

// ── Top items by frequency ────────────────────────────────────────────────────
export const topItems = {
  labels: ['Milk', 'Fresh Bread', 'Butter', 'Eggs', 'Vegetables', 'Fruit', 'Meat', 'Snacks'],
  counts: [14200, 12800, 9500, 8900, 7500, 6900, 6100, 4800]
};

// ── Customer recommendations (simulator offline database) ────────────────────
export const sampleRecommendations = {
  '3032': {
    segment: 'Vegans',
    nextBestOffer: '15% off Organic Vegetables Subscription',
    propensity: 0.88,
    items: ['salad', 'tomatoes', 'carrots'],
    discount: '15%'
  },
  '1': {
    segment: 'Loyal big spenders',
    nextBestOffer: '10% off Grocery Essentials',
    propensity: 0.32,
    items: ['eggs', 'cereals', 'fresh bread'],
    discount: '10%'
  },
  '42': {
    segment: 'Vegans',
    nextBestOffer: '15% off Organic Vegetables Subscription',
    propensity: 0.88,
    items: ['salad', 'tomatoes', 'carrots'],
    discount: '15%'
  },
  '198': {
    segment: 'Bargain hunters',
    nextBestOffer: '25% off Next Promotional Visit',
    propensity: 0.55,
    items: ['laptop', 'energy drink', 'bluetooth headphones'],
    discount: '25%'
  },
  '222': {
    segment: 'Tech enthusiasts',
    nextBestOffer: '12% off Electronics Flash Sale',
    propensity: 0.79,
    items: ['energy drink', 'airpods', 'gadget for tiktok streaming'],
    discount: '12%'
  }
};

// ── Lift chart data per product category ─────────────────────────────────────
export const liftChartData = {
  categories: [
  "Airpods → Iphone 10",
  "Iphone 10 → Airpods",
  "Energy Drink → Bluetooth Headphones",
  "Bluetooth Headphones → Energy Drink",
  "Iphone 10 → Bluetooth Headphones",
  "Bluetooth Headphones → Iphone 10",
  "Energy Drink → Protein Bar",
  "Protein Bar → Energy Drink"
],
  lift: [
  9.154969485614647,
  9.154969485614645,
  9.060181190681622,
  9.060181190681622,
  8.80012570710245,
  8.80012570710245,
  8.123192960402262,
  8.123192960402262
],
  confidence: [
  0.4211,
  0.3529,
  0.4571,
  0.3812,
  0.3958,
  0.2857,
  0.3667,
  0.3235
]
};

// ── Discount tiers ───────────────────────────────────────────────────────────
export const discountTiers = [
  {
    "segment": "Loyal big spenders",
    "discount": "10%",
    "type": "Loyalty Reward",
    "icon": "👑"
  },
  {
    "segment": "Vegans",
    "discount": "15%",
    "type": "Healthy Subscriptions",
    "icon": "🥗"
  },
  {
    "segment": "Bargain hunters",
    "discount": "25%",
    "type": "Win-Back Promotion",
    "icon": "📢"
  },
  {
    "segment": "Karens",
    "discount": "10%",
    "type": "Service Resolution",
    "icon": "🚨"
  },
  {
    "segment": "Tech enthusiasts",
    "discount": "12%",
    "type": "Electronics Flash Sale",
    "icon": "⚡"
  },
  {
    "segment": "Big families (big spenders)",
    "discount": "15%",
    "type": "Family Essentials",
    "icon": "👨‍👩‍👧‍👦"
  },
  {
    "segment": "Gamers",
    "discount": "10%",
    "type": "Bundle Deals",
    "icon": "🎮"
  },
  {
    "segment": "Clean and healthy",
    "discount": "10%",
    "type": "Healthy Choice",
    "icon": "🟢"
  },
  {
    "segment": "Average customer",
    "discount": "10%",
    "type": "Grocery Essentials",
    "icon": "👤"
  }
];
