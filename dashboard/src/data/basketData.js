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
    "antecedents": "Airpods, Iphone 10",
    "consequents": "Energy Drink, Bluetooth Headphones",
    "support": 0.004,
    "confidence": 0.2097,
    "lift": 9.15
  },
  {
    "antecedents": "Energy Drink, Bluetooth Headphones",
    "consequents": "Airpods, Iphone 10",
    "support": 0.004,
    "confidence": 0.1757,
    "lift": 9.15
  },
  {
    "antecedents": "Iphone 10, Bluetooth Headphones",
    "consequents": "Airpods, Energy Drink",
    "support": 0.004,
    "confidence": 0.3421,
    "lift": 9.06
  },
  {
    "antecedents": "Airpods, Energy Drink",
    "consequents": "Iphone 10, Bluetooth Headphones",
    "support": 0.004,
    "confidence": 0.1066,
    "lift": 9.06
  },
  {
    "antecedents": "Energy Drink, Iphone 10",
    "consequents": "Airpods, Bluetooth Headphones",
    "support": 0.004,
    "confidence": 0.3023,
    "lift": 8.8
  },
  {
    "antecedents": "Airpods, Bluetooth Headphones",
    "consequents": "Energy Drink, Iphone 10",
    "support": 0.004,
    "confidence": 0.1171,
    "lift": 8.8
  },
  {
    "antecedents": "Energy Drink, Bluetooth Headphones",
    "consequents": "Airpods, Protein Bar",
    "support": 0.005,
    "confidence": 0.2162,
    "lift": 8.12
  },
  {
    "antecedents": "Airpods, Protein Bar",
    "consequents": "Energy Drink, Bluetooth Headphones",
    "support": 0.005,
    "confidence": 0.186,
    "lift": 8.12
  },
  {
    "antecedents": "Megaman Zero 3, Airpods",
    "consequents": "Bluetooth Headphones",
    "support": 0.004,
    "confidence": 0.5417,
    "lift": 7.74
  },
  {
    "antecedents": "Bluetooth Headphones, Protein Bar",
    "consequents": "Airpods, Energy Drink",
    "support": 0.005,
    "confidence": 0.2857,
    "lift": 7.57
  },
  {
    "antecedents": "Airpods, Energy Drink",
    "consequents": "Bluetooth Headphones, Protein Bar",
    "support": 0.005,
    "confidence": 0.1311,
    "lift": 7.57
  },
  {
    "antecedents": "Airpods, Energy Drink, Iphone 10",
    "consequents": "Bluetooth Headphones",
    "support": 0.004,
    "confidence": 0.52,
    "lift": 7.43
  },
  {
    "antecedents": "Bluetooth Headphones, Final Fantasy Xxii",
    "consequents": "Airpods",
    "support": 0.0065,
    "confidence": 0.913,
    "lift": 7.38
  },
  {
    "antecedents": "Bluetooth Headphones",
    "consequents": "Samsung Galaxy 10, Airpods",
    "support": 0.0056,
    "confidence": 0.0796,
    "lift": 7.35
  },
  {
    "antecedents": "Samsung Galaxy 10, Airpods",
    "consequents": "Bluetooth Headphones",
    "support": 0.0056,
    "confidence": 0.5143,
    "lift": 7.35
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
    items: ['napkins', 'babies food', 'cooking oil'],
    discount: '15%'
  },
  '1': {
    segment: 'Loyal core spenders',
    nextBestOffer: '10% off Grocery Essentials',
    propensity: 0.32,
    items: ['eggs', 'cereals', 'fresh bread'],
    discount: '10%'
  },
  '42': {
    segment: 'Vegans',
    nextBestOffer: '15% off Organic Vegetables Subscription',
    propensity: 0.88,
    items: ['napkins', 'babies food', 'cooking oil'],
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
  "Airpods+Iphone 10\u2192Energy Drink+Bluetooth Headphones",
  "Energy Drink+Bluetooth Headphones\u2192Airpods+Iphone 10",
  "Iphone 10+Bluetooth Headphones\u2192Airpods+Energy Drink",
  "Airpods+Energy Drink\u2192Iphone 10+Bluetooth Headphones",
  "Energy Drink+Iphone 10\u2192Airpods+Bluetooth Headphones",
  "Airpods+Bluetooth Headphones\u2192Energy Drink+Iphone 10",
  "Energy Drink+Bluetooth Headphones\u2192Airpods+Protein Bar",
  "Airpods+Protein Bar\u2192Energy Drink+Bluetooth Headphones"
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
  0.2096774193548387,
  0.17567567567567566,
  0.34210526315789475,
  0.10655737704918031,
  0.3023255813953488,
  0.11711711711711711,
  0.21621621621621623,
  0.18604651162790697
]
};

// ── Discount tiers ───────────────────────────────────────────────────────────
export const discountTiers = [
  {
    "segment": "Loyal core spenders",
    "discount": "5\u201310%",
    "type": "Loyalty Reward",
    "icon": "\ud83d\udc51"
  },
  {
    "segment": "Vegans",
    "discount": "15%",
    "type": "Healthy Subscriptions",
    "icon": "\ud83e\udd57"
  },
  {
    "segment": "Bargain hunters",
    "discount": "20\u201325%",
    "type": "Win-Back Promotion",
    "icon": "\ud83d\udce2"
  },
  {
    "segment": "Karens",
    "discount": "10%",
    "type": "Service Resolution",
    "icon": "\ud83d\udea8"
  },
  {
    "segment": "Tech enthusiasts",
    "discount": "10\u201315%",
    "type": "Late Flash Sales",
    "icon": "\u26a1"
  },
  {
    "segment": "Big families (big spenders)",
    "discount": "15\u201320%",
    "type": "Family Essentials",
    "icon": "\ud83d\udc68\u200d\ud83d\udc69\u200d\ud83d\udc67\u200d\ud83d\udc66"
  },
  {
    "segment": "Gamers",
    "discount": "10%",
    "type": "Bundle Deals",
    "icon": "\ud83c\udfae"
  }
];
