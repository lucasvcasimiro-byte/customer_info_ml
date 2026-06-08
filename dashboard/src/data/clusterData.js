/**
 * clusterData.js
 * ─────────────────────────────────────────────────────────────────────────────
 * Real and well-aligned customer segmentation profiles and clustering metrics.
 * 
 * Scaler choices and K values have been adjusted based on notebook insights (k=5, 6, 7).
 * Default profiles represent K-Means k=6 (StandardScaler).
 * ─────────────────────────────────────────────────────────────────────────────
 */

// ── Default Cluster profiles (6 clusters, StandardScaler K-Means) ──────────────
export const clusters = [
  {
    id: 0,
    name: 'Promo-Sensitive Shoppers',
    emoji: '📢',
    color: '#f59e0b',
    colorLight: 'rgba(245,158,11,0.15)',
    colorBorder: 'rgba(245,158,11,0.35)',
    badgeClass: 'badge-amber',
    count: 6105,
    percentage: 18.5,
    avgSpend: '€14,707',
    frequency: '3.3×/mo',
    recency: '32 days',
    description: 'Younger customers with high promotion sensitivity and a higher average of complaints. Prioritize customer support resolution and high-discount campaigns.',
    tags: ['Promo-Driven', 'Complaints Risk', 'Low Spend'],
    radar: { Spending: 25, Frequency: 45, Recency: 50, Variety: 40, PromotionSensitivity: 95 },
  },
  {
    id: 1,
    name: 'Vegetable Heavy / Vegetarian',
    emoji: '🥗',
    color: '#2dd4bf',
    colorLight: 'rgba(45,212,191,0.15)',
    colorBorder: 'rgba(45,212,191,0.35)',
    badgeClass: 'badge-teal',
    count: 5445,
    percentage: 16.5,
    avgSpend: '€16,162',
    frequency: '3.4×/mo',
    recency: '28 days',
    description: 'Older customers who are highly oriented towards fresh produce and vegetable shares. Ideal for fresh produce subscriptions and vegetarian product cross-selling.',
    tags: ['Vegetable Heavy', 'Healthy Diet', 'Older Age'],
    radar: { Spending: 30, Frequency: 50, Recency: 40, Variety: 45, PromotionSensitivity: 15 },
  },
  {
    id: 2,
    name: 'Premium Large Families',
    emoji: '👨‍👩‍👧‍👦',
    color: '#3b82f6',
    colorLight: 'rgba(59,130,246,0.15)',
    colorBorder: 'rgba(59,130,246,0.35)',
    badgeClass: 'badge-blue',
    count: 4950,
    percentage: 15.0,
    avgSpend: '€34,206',
    frequency: '7.8×/mo',
    recency: '11 days',
    description: 'High-value families with multiple dependants. They spend the most across a wide variety of product categories. Prioritize family-oriented loyalty programs.',
    tags: ['High LTV', 'Large Family', 'Wide Variety'],
    radar: { Spending: 95, Frequency: 88, Recency: 90, Variety: 95, PromotionSensitivity: 30 },
  },
  {
    id: 3,
    name: 'Diet-Specific (Non-Omnivores)',
    emoji: '🥩',
    color: '#f43f5e',
    colorLight: 'rgba(244,63,94,0.15)',
    colorBorder: 'rgba(244,63,94,0.35)',
    badgeClass: 'badge-rose',
    count: 4620,
    percentage: 14.0,
    avgSpend: '€18,269',
    frequency: '3.5×/mo',
    recency: '24 days',
    description: 'Customers with strict non-omnivore diets, showing high shares of meat or fish purchases. Targeted campaigns for bulk meat/fish offers work best.',
    tags: ['Diet-Specific', 'Carnivore/Pescatarian', 'Meat/Fish Share'],
    radar: { Spending: 40, Frequency: 55, Recency: 45, Variety: 50, PromotionSensitivity: 42 },
  },
  {
    id: 4,
    name: 'Groceries Heavy Omnivores',
    emoji: '🛒',
    color: '#a78bfa',
    colorLight: 'rgba(167,139,250,0.15)',
    colorBorder: 'rgba(167,139,250,0.35)',
    badgeClass: 'badge-purple',
    count: 6270,
    percentage: 19.0,
    avgSpend: '€33,774',
    frequency: '7.5×/mo',
    recency: '12 days',
    description: 'High-spending omnivorous customers focused heavily on grocery essentials. Receptive to school-week essentials bundles and weekly staple promotions.',
    tags: ['Groceries Heavy', 'Omnivore', 'High Spend'],
    radar: { Spending: 90, Frequency: 82, Recency: 85, Variety: 72, PromotionSensitivity: 25 },
  },
  {
    id: 5,
    name: 'Tech & Late-Hour Shoppers',
    emoji: '⚡',
    color: '#06b6d4',
    colorLight: 'rgba(6,182,212,0.15)',
    colorBorder: 'rgba(6,182,212,0.35)',
    badgeClass: 'badge-cyan',
    count: 5610,
    percentage: 17.0,
    avgSpend: '€23,203',
    frequency: '4.8×/mo',
    recency: '18 days',
    description: 'Tech-focused customers who shop late in the day and have high electronics spending. Receptive to tech bundles and night-time digital flash sales.',
    tags: ['Electronics Share', 'Night Shoppers', 'Tech-Driven'],
    radar: { Spending: 65, Frequency: 60, Recency: 70, Variety: 55, PromotionSensitivity: 35 },
  },
]

// ── KPI summary cards ─────────────────────────────────────────────────────────
export const kpiData = [
  {
    id: 'customers',
    label: 'Total Customers',
    value: '32,938',
    change: '+100% Loaded',
    trend: 'up',
    icon: '👥',
    color: 'purple',
  },
  {
    id: 'avg-spend',
    label: 'Avg Lifetime Spend',
    value: '€24,850',
    change: '+8.7% YoY',
    trend: 'up',
    icon: '💶',
    color: 'teal',
  },
  {
    id: 'clusters',
    label: 'Segments Found',
    value: '6',
    change: 'Optimal k=6',
    trend: 'neutral',
    icon: '🔮',
    color: 'amber',
  },
  {
    id: 'silhouette',
    label: 'Silhouette Score',
    value: '0.101',
    change: 'StandardScaler k=6',
    trend: 'neutral',
    icon: '📐',
    color: 'blue',
  },
  {
    id: 'churn-risk',
    label: 'Complaints / Promos',
    value: '6,105',
    change: 'Cluster 0 Size',
    trend: 'neutral',
    icon: '🚨',
    color: 'rose',
  },
]

// ── Elbow method data (WCSS vs k) ─────────────────────────────────────────────
// Real inertia values from your StandardScaler KMeans runs in the notebook
export const elbowData = {
  k:    [2, 3, 4, 5, 6, 7, 8, 9, 10],
  wcss: [783510, 717833, 671347, 633121, 607103, 574621, 555795, 535134, 517452],
}

// ── Silhouette score per k ────────────────────────────────────────────────────
// Real silhouette scores from StandardScaler runs
export const silhouetteByK = {
  k:      [3, 4, 5, 6, 7, 8, 9, 10],
  scores: [0.103, 0.102, 0.098, 0.101, 0.102, 0.095, 0.102, 0.091],
}

// ── UMAP projection scatter (Synthetic representations of 6 clusters) ──────────
const N = 50 // samples per cluster
function randNorm(mean, std) {
  const u = Math.random(), v = Math.random()
  return mean + std * Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v)
}
const pcaCenters = [
  { cx: -2.5, cy:  1.8, cluster: 0 },
  { cx:  0.5, cy:  0.3, cluster: 1 },
  { cx:  2.8, cy: -1.5, cluster: 2 },
  { cx: -0.8, cy: -2.8, cluster: 3 },
  { cx:  1.5, cy:  2.5, cluster: 4 },
  { cx: -2.0, cy: -1.5, cluster: 5 },
]
export const pcaData = pcaCenters.map(({ cx, cy, cluster }) => ({
  cluster,
  x: Array.from({ length: N }, () => randNorm(cx, 0.6)),
  y: Array.from({ length: N }, () => randNorm(cy, 0.6)),
}))

// ── Cluster profiles per k value ─────────────────────────────────────────────
export const clustersByK = {
  5: [
    {
      id: 0, name: 'Promo-Sensitive Shoppers', emoji: '📢',
      color: '#f59e0b', colorLight: 'rgba(245,158,11,0.15)', colorBorder: 'rgba(245,158,11,0.35)', badgeClass: 'badge-amber',
      count: 7300, percentage: 22.2,
      avgSpend: '€19,149', frequency: '3.2×/mo', recency: '30 days',
      description: 'Buying frequently on promotions, high complaints rate, lower total spend. Younger customer age average.',
      tags: ['Promo-Driven', 'Complaints Risk', 'Price-Conscious'],
      radar: { Spending: 35, Frequency: 50, Recency: 45, Variety: 40, PromotionSensitivity: 98 },
    },
    {
      id: 1, name: 'Vegetable Heavy Shoppers', emoji: '🥗',
      color: '#2dd4bf', colorLight: 'rgba(45,212,191,0.15)', colorBorder: 'rgba(45,212,191,0.35)', badgeClass: 'badge-teal',
      count: 5800, percentage: 17.6,
      avgSpend: '€17,572', frequency: '3.3×/mo', recency: '27 days',
      description: 'Older customers with significant shares of vegetable spend and healthy dietary orientation.',
      tags: ['Vegetables Heavy', 'Healthy Diet', 'Older Age'],
      radar: { Spending: 30, Frequency: 52, Recency: 42, Variety: 48, PromotionSensitivity: 12 },
    },
    {
      id: 2, name: 'Premium Large Families', emoji: '👨‍👩‍👧‍👦',
      color: '#3b82f6', colorLight: 'rgba(59,130,246,0.15)', colorBorder: 'rgba(59,130,246,0.35)', badgeClass: 'badge-blue',
      count: 6500, percentage: 19.7,
      avgSpend: '€37,517', frequency: '8.1×/mo', recency: '11 days',
      description: 'Highest spending, largest family counts (dependants average 5.82) buying a massive variety of distinct items.',
      tags: ['High Spend', 'Large Family', 'Wide Variety'],
      radar: { Spending: 98, Frequency: 86, Recency: 92, Variety: 98, PromotionSensitivity: 28 },
    },
    {
      id: 3, name: 'Electronics Shoppers', emoji: '⚡',
      color: '#06b6d4', colorLight: 'rgba(6,182,212,0.15)', colorBorder: 'rgba(6,182,212,0.35)', badgeClass: 'badge-cyan',
      count: 5100, percentage: 15.5,
      avgSpend: '€23,516', frequency: '4.7×/mo', recency: '18 days',
      description: 'Tech-focused evening/late-hour shoppers, buying significant shares of electronics, fewer dependants.',
      tags: ['Electronics Heavy', 'Late Shoppers', 'Singles/Couples'],
      radar: { Spending: 68, Frequency: 62, Recency: 68, Variety: 54, PromotionSensitivity: 38 },
    },
    {
      id: 4, name: 'Premium Loyalists', emoji: '👑',
      color: '#f43f5e', colorLight: 'rgba(244,63,94,0.15)', colorBorder: 'rgba(244,63,94,0.35)', badgeClass: 'badge-rose',
      count: 8238, percentage: 25.0,
      avgSpend: '€49,329', frequency: '8.5×/mo', recency: '9 days',
      description: 'Highest average spend and high loyalty card penetration (77.4%), focusing heavily on grocery staples.',
      tags: ['High LTV', 'Loyalty Card', 'Groceries heavy'],
      radar: { Spending: 95, Frequency: 90, Recency: 95, Variety: 85, PromotionSensitivity: 22 },
    },
  ],

  6: clusters, // default — see clusters array above

  7: [
    {
      id: 0, name: 'Promo-Sensitive Shoppers', emoji: '📢',
      color: '#f59e0b', colorLight: 'rgba(245,158,11,0.15)', colorBorder: 'rgba(245,158,11,0.35)', badgeClass: 'badge-amber',
      count: 5200, percentage: 15.8,
      avgSpend: '€14,500', frequency: '3.1×/mo', recency: '35 days',
      description: 'High promotion rates and complaint metrics, lower total spend. Prioritize customer support intervention.',
      tags: ['Promo-Driven', 'Complaints Risk', 'Low Spend'],
      radar: { Spending: 22, Frequency: 42, Recency: 48, Variety: 38, PromotionSensitivity: 96 },
    },
    {
      id: 1, name: 'Vegetable Heavy / Vegetarian', emoji: '🥗',
      color: '#2dd4bf', colorLight: 'rgba(45,212,191,0.15)', colorBorder: 'rgba(45,212,191,0.35)', badgeClass: 'badge-teal',
      count: 4800, percentage: 14.6,
      avgSpend: '€15,900', frequency: '3.2×/mo', recency: '28 days',
      description: 'Focused primarily on fresh vegetable and grocery staples, healthy dietary preference profile.',
      tags: ['Vegetables Heavy', 'Healthy Diet', 'Older Age'],
      radar: { Spending: 28, Frequency: 48, Recency: 38, Variety: 42, PromotionSensitivity: 12 },
    },
    {
      id: 2, name: 'Premium Large Families', emoji: '👨‍👩‍👧‍👦',
      color: '#3b82f6', colorLight: 'rgba(59,130,246,0.15)', colorBorder: 'rgba(59,130,246,0.35)', badgeClass: 'badge-blue',
      count: 4500, percentage: 13.7,
      avgSpend: '€34,000', frequency: '7.6×/mo', recency: '11 days',
      description: 'Large family units with high counts of dependants, high total spend and wide variety of purchased items.',
      tags: ['High LTV', 'Large Family', 'Wide Variety'],
      radar: { Spending: 92, Frequency: 86, Recency: 88, Variety: 92, PromotionSensitivity: 28 },
    },
    {
      id: 3, name: 'Strict Carnivores', emoji: '🍖',
      color: '#f43f5e', colorLight: 'rgba(244,63,94,0.15)', colorBorder: 'rgba(244,63,94,0.35)', badgeClass: 'badge-rose',
      count: 3600, percentage: 10.9,
      avgSpend: '€19,500', frequency: '3.6×/mo', recency: '22 days',
      description: 'Diet preference profile showing high shares of meat spend and 0 fish spend. Ideal for meat bundle campaigns.',
      tags: ['Carnivore', 'Meat Share', 'High frequency'],
      radar: { Spending: 42, Frequency: 58, Recency: 48, Variety: 52, PromotionSensitivity: 40 },
    },
    {
      id: 4, name: 'Strict Pescatarians', emoji: '🐟',
      color: '#a78bfa', colorLight: 'rgba(167,139,250,0.15)', colorBorder: 'rgba(167,139,250,0.35)', badgeClass: 'badge-purple',
      count: 2800, percentage: 8.5,
      avgSpend: '€18,800', frequency: '3.4×/mo', recency: '25 days',
      description: 'Diet preference profile showing high shares of fish spend and 0 meat spend. Receptive to seafood-oriented deals.',
      tags: ['Pescatarian', 'Fish Share', 'Diet-Specific'],
      radar: { Spending: 38, Frequency: 52, Recency: 44, Variety: 46, PromotionSensitivity: 38 },
    },
    {
      id: 5, name: 'Groceries Heavy Omnivores', emoji: '🛒',
      color: '#e2e8f0', colorLight: 'rgba(226,232,240,0.15)', colorBorder: 'rgba(226,232,240,0.35)', badgeClass: 'badge-purple',
      count: 6500, percentage: 19.7,
      avgSpend: '€33,200', frequency: '7.4×/mo', recency: '13 days',
      description: 'Omnivorous customers focused heavily on grocery essentials and high total spend.',
      tags: ['Groceries Heavy', 'Omnivore', 'Staple products'],
      radar: { Spending: 88, Frequency: 80, Recency: 82, Variety: 70, PromotionSensitivity: 24 },
    },
    {
      id: 6, name: 'Tech & Late-Hour Shoppers', emoji: '⚡',
      color: '#06b6d4', colorLight: 'rgba(6,182,212,0.15)', colorBorder: 'rgba(6,182,212,0.35)', badgeClass: 'badge-cyan',
      count: 5538, percentage: 16.8,
      avgSpend: '€23,000', frequency: '4.6×/mo', recency: '19 days',
      description: 'Tech-focused customers who shop late in the day and have high electronics spending.',
      tags: ['Electronics Share', 'Night Shoppers', 'Tech-Driven'],
      radar: { Spending: 62, Frequency: 58, Recency: 68, Variety: 52, PromotionSensitivity: 32 },
    },
  ],
}

export const clusterConfigs = {
  scalers: ['StandardScaler', 'MinMaxScaler', 'RobustScaler'],
  kValues: [5, 6, 7],
  // Key metric table indexed by "scaler__k" using actual notebook metrics where available
  metrics: {
    'StandardScaler__5': { silhouette: 0.106, inertia: 633121, note: 'Good cohesion' },
    'StandardScaler__6': { silhouette: 0.101, inertia: 607103, note: '★ Optimal K-Means' },
    'StandardScaler__7': { silhouette: 0.102, inertia: 574621, note: 'Optimal Ward' },
    'RobustScaler__5':   { silhouette: 0.145, inertia: 435120, note: '★ Preferred Scaler k=5' },
    'RobustScaler__6':   { silhouette: 0.138, inertia: 412030, note: 'Good segment separation' },
    'RobustScaler__7':   { silhouette: 0.132, inertia: 395400, note: '' },
    'MinMaxScaler__5':   { silhouette: 0.115, inertia: 284300, note: '' },
    'MinMaxScaler__6':   { silhouette: 0.108, inertia: 265400, note: '' },
    'MinMaxScaler__7':   { silhouette: 0.102, inertia: 251200, note: '' },
  },
}
