import ast
from collections import Counter

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec

from preprocessing import SPEND_COLS, build_features


PALETTE   = "muted"
BG_COLOR  = "#F8F7F4"
ACCENT    = "#2D6A4F"
ACCENT2   = "#E76F51"
TEXT_CLR  = "#1A1A2E"

sns.set_theme(style="whitegrid", palette=PALETTE)
plt.rcParams.update({
    "figure.facecolor":  BG_COLOR,
    "axes.facecolor":    BG_COLOR,
    "axes.edgecolor":    "#CCCCCC",
    "axes.labelcolor":   TEXT_CLR,
    "xtick.color":       TEXT_CLR,
    "ytick.color":       TEXT_CLR,
    "text.color":        TEXT_CLR,
    "font.family":       "DejaVu Sans",
    "axes.titlesize":    12,
    "axes.labelsize":    10,
    "figure.titlesize":  14,
})



def _save_or_show(fig, name: str) -> None:
    """Show the figure.  Replace with fig.savefig(f'{name}.png') if needed."""
    fig.tight_layout()
    plt.show()
    plt.close(fig)




def load_raw_data(info_path: str = "data/customer_info.csv",
                  basket_path: str = "data/customer_basket.csv"):
    df_info   = pd.read_csv(info_path)
    df_basket = pd.read_csv(basket_path)
    return df_info, df_basket


def print_overview(df_info: pd.DataFrame, df_basket: pd.DataFrame) -> None:
    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)
    print(f"\ncustomer_info  : {df_info.shape[0]:,} rows  ×  {df_info.shape[1]} columns")
    print(f"customer_basket: {df_basket.shape[0]:,} rows  ×  {df_basket.shape[1]} columns")

    spend_cols = [c for c in df_info.columns if c.startswith("lifetime_spend")]
    df_info_copy = df_info.copy()
    df_info_copy["total_spend"] = df_info_copy[spend_cols].fillna(0).sum(axis=1)

    print(f"\nUnique customers in info  : {df_info['customer_id'].nunique():,}")
    print(f"Unique customers in basket: {df_basket['customer_id'].nunique():,}")
    print(f"\nTotal spend — mean : €{df_info_copy['total_spend'].mean():,.0f}")
    print(f"Total spend — median : €{df_info_copy['total_spend'].median():,.0f}")
    print(f"Total spend — max  : €{df_info_copy['total_spend'].max():,.0f}")
    print("=" * 60)



# MISSING VALUES


def plot_missing_values(df_info: pd.DataFrame) -> None:
    """Bar chart of missing-value percentages per column."""
    miss_pct = (df_info.isnull().mean() * 100).sort_values(ascending=False)
    miss_pct = miss_pct[miss_pct > 0]

    fig, ax = plt.subplots(figsize=(10, 4), facecolor=BG_COLOR)
    bars = ax.barh(miss_pct.index, miss_pct.values,
                   color=ACCENT2, edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, miss_pct.values):
        ax.text(val + 0.2, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", fontsize=8, color=TEXT_CLR)

    ax.set_xlabel("Missing (%)")
    ax.set_title("Missing Values per Column", fontweight="bold", pad=12)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter())
    ax.invert_yaxis()
    _save_or_show(fig, "missing_values")



# DEMOGRAPHICS


def plot_demographics(df_info: pd.DataFrame) -> None:
    """Age distribution, gender split, education level, household size."""

    df = df_info.copy()

    # Age
    df["customer_birthdate"] = pd.to_datetime(
        df["customer_birthdate"], format="%m/%d/%Y %I:%M %p", errors="coerce"
    )
    df["age"] = 2026 - df["customer_birthdate"].dt.year

    # Education
    df["education_level"] = (
        df["customer_name"]
        .str.extract(r"^(Bsc|Msc|Phd)\.", expand=False)
        .fillna("No Degree")
    )

    # Household size
    df["kids_home"]   = df["kids_home"].fillna(0)
    df["teens_home"]  = df["teens_home"].fillna(0)
    df["household_size"] = df["kids_home"] + df["teens_home"]

    fig = plt.figure(figsize=(14, 8), facecolor=BG_COLOR)
    fig.suptitle("Customer Demographics", fontsize=14, fontweight="bold", y=1.01)
    gs = GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    # ── Age distribution ──────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    sns.histplot(df["age"].dropna(), bins=30, kde=True,
                 color=ACCENT, ax=ax1, edgecolor="white", linewidth=0.4)
    ax1.axvline(df["age"].median(), color=ACCENT2, linestyle="--", linewidth=1.5,
                label=f"Median: {df['age'].median():.0f}")
    ax1.set_title("Age Distribution")
    ax1.set_xlabel("Age (years)")
    ax1.set_ylabel("Count")
    ax1.legend(fontsize=8)

    # ── Gender split ──────────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    gender_counts = df["customer_gender"].value_counts()
    colors = [ACCENT, ACCENT2]
    wedges, texts, autotexts = ax2.pie(
        gender_counts.values,
        labels=gender_counts.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops=dict(edgecolor="white", linewidth=1.5),
    )
    for t in autotexts:
        t.set_fontsize(10)
    ax2.set_title("Gender Split")

    # ── Education level ───────────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    edu_order = ["No Degree", "Bsc", "Msc", "Phd"]
    edu_counts = df["education_level"].value_counts().reindex(edu_order)
    bars = ax3.bar(edu_counts.index, edu_counts.values,
                   color=[ACCENT, ACCENT2, "#457B9D", "#A8DADC"],
                   edgecolor="white", linewidth=0.5)
    for bar in bars:
        ax3.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 50,
                 f"{bar.get_height():,.0f}",
                 ha="center", fontsize=8)
    ax3.set_title("Education Level")
    ax3.set_ylabel("Customers")

    # ── Household size ────────────────────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    hh_counts = df["household_size"].value_counts().sort_index()
    ax4.bar(hh_counts.index.astype(int), hh_counts.values,
            color=ACCENT, edgecolor="white", linewidth=0.5)
    ax4.set_title("Household Size (kids + teens)")
    ax4.set_xlabel("Number of dependants")
    ax4.set_ylabel("Customers")
    ax4.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    _save_or_show(fig, "demographics")


# ─────────────────────────────────────────────────────────────────────────────
# 4. CUSTOMER BEHAVIOUR
# ─────────────────────────────────────────────────────────────────────────────

def plot_customer_behaviour(df_info: pd.DataFrame) -> None:
    """Tenure, loyalty card, typical shopping hour, complaints, promo %."""

    df = df_info.copy()
    df["customer_tenure"] = 2026 - df["year_first_transaction"].clip(upper=2026)
    df["has_loyalty_card"] = df["loyalty_card_number"].notna()
    df["number_complaints"] = df["number_complaints"].fillna(0)
    df["typical_hour"] = df["typical_hour"].fillna(df["typical_hour"].median())
    df["percentage_of_products_bought_promotion"] = (
        df["percentage_of_products_bought_promotion"]
        .fillna(df["percentage_of_products_bought_promotion"].median())
    )

    fig = plt.figure(figsize=(15, 9), facecolor=BG_COLOR)
    fig.suptitle("Customer Behaviour", fontsize=14, fontweight="bold", y=1.01)
    gs = GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.38)

    # ── Customer tenure ───────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    sns.histplot(df["customer_tenure"].dropna(), bins=25, kde=True,
                 color=ACCENT, ax=ax1, edgecolor="white", linewidth=0.4)
    ax1.set_title("Customer Tenure (years)")
    ax1.set_xlabel("Years as customer")
    ax1.set_ylabel("Count")

    # ── Loyalty card ──────────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    lc_counts = df["has_loyalty_card"].value_counts()
    ax2.bar(["No Card", "Has Card"], lc_counts.reindex([False, True]).values,
            color=[ACCENT2, ACCENT], edgecolor="white")
    for i, v in enumerate(lc_counts.reindex([False, True]).values):
        ax2.text(i, v + 100, f"{v:,}\n({v/len(df)*100:.0f}%)",
                 ha="center", fontsize=9)
    ax2.set_title("Loyalty Card Ownership")
    ax2.set_ylabel("Customers")

    # ── Typical shopping hour ─────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[0, 2])
    hour_counts = df["typical_hour"].value_counts().sort_index()
    ax3.bar(hour_counts.index, hour_counts.values,
            color=ACCENT, edgecolor="white", linewidth=0.4)
    ax3.set_title("Typical Shopping Hour")
    ax3.set_xlabel("Hour of day (0–23)")
    ax3.set_ylabel("Customers")
    ax3.xaxis.set_major_locator(mticker.MultipleLocator(4))

    # ── Complaints distribution ───────────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 0])
    comp_counts = df["number_complaints"].value_counts().sort_index()
    ax4.bar(comp_counts.index.astype(int), comp_counts.values,
            color=ACCENT2, edgecolor="white", linewidth=0.4)
    ax4.set_title("Number of Complaints")
    ax4.set_xlabel("Complaints")
    ax4.set_ylabel("Customers")
    ax4.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    # ── Promo % distribution ──────────────────────────────────────────────
    ax5 = fig.add_subplot(gs[1, 1])
    sns.histplot(df["percentage_of_products_bought_promotion"] * 100,
                 bins=30, kde=True, color="#457B9D", ax=ax5,
                 edgecolor="white", linewidth=0.4)
    ax5.set_title("% Products Bought on Promotion")
    ax5.set_xlabel("Promotion %")
    ax5.set_ylabel("Count")

    # ── Distinct stores visited ───────────────────────────────────────────
    ax6 = fig.add_subplot(gs[1, 2])
    stores = df["distinct_stores_visited"].fillna(df["distinct_stores_visited"].median())
    store_counts = stores.value_counts().sort_index()
    ax6.bar(store_counts.index.astype(int), store_counts.values,
            color=ACCENT, edgecolor="white", linewidth=0.4)
    ax6.set_title("Distinct Stores Visited")
    ax6.set_xlabel("Number of stores")
    ax6.set_ylabel("Customers")
    ax6.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    _save_or_show(fig, "customer_behaviour")


# ─────────────────────────────────────────────────────────────────────────────
# 5. SPEND ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

def plot_spend_analysis(df_info: pd.DataFrame) -> None:
    """Total spend distribution + category spend shares."""

    df = df_info.copy()
    for col in SPEND_COLS:
        df[col] = df[col].fillna(0)
    df["total_spend"] = df[SPEND_COLS].sum(axis=1)

    # Compute median category shares
    shares = {}
    for col in SPEND_COLS:
        cat = col.replace("lifetime_spend_", "")
        s = df[col] / df["total_spend"].replace(0, np.nan)
        shares[cat] = s.median()
    shares = dict(sorted(shares.items(), key=lambda x: -x[1]))

    fig = plt.figure(figsize=(15, 9), facecolor=BG_COLOR)
    fig.suptitle("Spend Analysis", fontsize=14, fontweight="bold", y=1.01)
    gs = GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    # ── Total spend distribution ──────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    sns.histplot(df["total_spend"], bins=50, kde=True,
                 color=ACCENT, ax=ax1, edgecolor="white", linewidth=0.4)
    ax1.axvline(df["total_spend"].median(), color=ACCENT2, linestyle="--",
                linewidth=1.5, label=f"Median €{df['total_spend'].median():,.0f}")
    ax1.set_title("Total Lifetime Spend Distribution")
    ax1.set_xlabel("Total spend (€)")
    ax1.set_ylabel("Count")
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x/1000:.0f}k"))
    ax1.legend(fontsize=8)

    # ── Spend by category (median absolute) ──────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    cat_medians = {
        col.replace("lifetime_spend_", ""): df[col].median()
        for col in SPEND_COLS
    }
    cat_medians = dict(sorted(cat_medians.items(), key=lambda x: -x[1]))
    palette_n = sns.color_palette("muted", len(cat_medians))
    ax2.barh(list(cat_medians.keys()), list(cat_medians.values()),
             color=palette_n, edgecolor="white")
    ax2.set_title("Median Spend by Category (€)")
    ax2.set_xlabel("Median lifetime spend (€)")
    ax2.invert_yaxis()
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x:,.0f}"))

    # ── Category spend shares (pie) ───────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    share_vals = list(shares.values())
    share_labels = [f"{k}\n{v*100:.1f}%" for k, v in shares.items()]
    colors_pie = sns.color_palette("muted", len(shares))
    wedges, _ = ax3.pie(share_vals, labels=None, colors=colors_pie,
                        startangle=140,
                        wedgeprops=dict(edgecolor="white", linewidth=1.2))
    ax3.legend(wedges, share_labels, loc="center left",
               bbox_to_anchor=(1, 0, 0.5, 1), fontsize=7)
    ax3.set_title("Median Category Share of Total Spend")

    # ── Box-plot: log-scaled spend per category ───────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    spend_long = pd.melt(
        df[[c for c in SPEND_COLS]].rename(
            columns={c: c.replace("lifetime_spend_", "") for c in SPEND_COLS}
        ),
        var_name="category", value_name="spend"
    )
    spend_long = spend_long[spend_long["spend"] > 0]
    spend_long["spend_log"] = np.log1p(spend_long["spend"])
    category_order = list(cat_medians.keys())
    sns.boxplot(data=spend_long, x="spend_log", y="category",
                order=category_order, palette="muted", ax=ax4,
                fliersize=1.5, linewidth=0.8)
    ax4.set_title("Spend Distribution per Category (log scale)")
    ax4.set_xlabel("log(1 + spend)")
    ax4.set_ylabel("")

    _save_or_show(fig, "spend_analysis")


# ─────────────────────────────────────────────────────────────────────────────
# 6. GEOGRAPHIC DISTRIBUTION
# ─────────────────────────────────────────────────────────────────────────────

def plot_geographic_distribution(df_info: pd.DataFrame) -> None:
    """Scatter map of customer home locations, coloured by total spend."""

    df = df_info.copy()
    spend_cols = [c for c in df.columns if c.startswith("lifetime_spend")]
    df["total_spend"] = df[spend_cols].fillna(0).sum(axis=1)

    fig, ax = plt.subplots(figsize=(9, 8), facecolor=BG_COLOR)
    sc = ax.scatter(
        df["longitude"], df["latitude"],
        c=df["total_spend"],
        cmap="YlOrRd",
        s=4,
        alpha=0.4,
        linewidths=0,
    )
    cbar = plt.colorbar(sc, ax=ax, pad=0.02)
    cbar.set_label("Total lifetime spend (€)", fontsize=9)
    cbar.formatter = mticker.FuncFormatter(lambda x, _: f"€{x/1000:.0f}k")
    cbar.update_ticks()

    ax.set_title("Geographic Distribution of Customers\n(colour = total spend)",
                 fontweight="bold")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    _save_or_show(fig, "geographic_distribution")


# ─────────────────────────────────────────────────────────────────────────────
# 7. BASKET ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

def plot_basket_analysis(df_basket: pd.DataFrame, top_n: int = 20) -> None:
    """Top N most frequent products and basket size distribution."""

    # Parse product lists
    all_products = []
    basket_sizes = []
    for row in df_basket["list_of_goods"].dropna():
        try:
            items = ast.literal_eval(row)
            all_products.extend(items)
            basket_sizes.append(len(items))
        except (ValueError, SyntaxError):
            pass

    top_products = Counter(all_products).most_common(top_n)
    products_df  = pd.DataFrame(top_products, columns=["product", "count"])

    fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor=BG_COLOR)
    fig.suptitle("Basket Analysis", fontsize=14, fontweight="bold")

    # ── Top products ──────────────────────────────────────────────────────
    ax1 = axes[0]
    palette_n = sns.color_palette("muted", top_n)
    ax1.barh(products_df["product"][::-1], products_df["count"][::-1],
             color=palette_n[::-1], edgecolor="white", linewidth=0.4)
    ax1.set_title(f"Top {top_n} Most Frequent Products")
    ax1.set_xlabel("Appearances in baskets")
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))

    # ── Basket size distribution ──────────────────────────────────────────
    ax2 = axes[1]
    sizes = pd.Series(basket_sizes)
    sns.histplot(sizes, bins=30, kde=True, color=ACCENT,
                 ax=ax2, edgecolor="white", linewidth=0.4)
    ax2.axvline(sizes.median(), color=ACCENT2, linestyle="--",
                linewidth=1.5, label=f"Median: {sizes.median():.0f} items")
    ax2.set_title("Basket Size Distribution")
    ax2.set_xlabel("Items per basket")
    ax2.set_ylabel("Count")
    ax2.legend(fontsize=8)

    _save_or_show(fig, "basket_analysis")


# ─────────────────────────────────────────────────────────────────────────────
# 8. CORRELATION HEATMAP
# ─────────────────────────────────────────────────────────────────────────────

def plot_correlation_heatmap(df_features: pd.DataFrame,
                             feature_cols: list) -> None:
    """Lower-triangle correlation heatmap of the engineered feature set."""
    corr = df_features[feature_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(figsize=(14, 11), facecolor=BG_COLOR)
    sns.heatmap(
        corr, mask=mask, annot=False, cmap="coolwarm",
        vmin=-1, vmax=1, linewidths=0.3, linecolor="white",
        cbar_kws={"shrink": 0.8}, ax=ax,
    )
    ax.set_title("Feature Correlation Heatmap", fontweight="bold", pad=14)
    ax.tick_params(axis="x", rotation=45, labelsize=7)
    ax.tick_params(axis="y", labelsize=7)

    _save_or_show(fig, "correlation_heatmap")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def run_eda(info_path: str = "data/customer_info.csv",
            basket_path: str = "data/customer_basket.csv") -> None:
    """Run the full EDA pipeline end-to-end."""

    from preprocessing import FEATURE_COLS

    # Load raw data
    df_info, df_basket = load_raw_data(info_path, basket_path)

    # 1. Overview
    print_overview(df_info, df_basket)

    # 2. Missing values
    print("\n[1/7] Plotting missing values...")
    plot_missing_values(df_info)

    # 3. Demographics
    print("[2/7] Plotting demographics...")
    plot_demographics(df_info)

    # 4. Behaviour
    print("[3/7] Plotting customer behaviour...")
    plot_customer_behaviour(df_info)

    # 5. Spend analysis
    print("[4/7] Plotting spend analysis...")
    plot_spend_analysis(df_info)

    # 6. Geography
    print("[5/7] Plotting geographic distribution...")
    plot_geographic_distribution(df_info)

    # 7. Basket analysis
    print("[6/7] Plotting basket analysis...")
    plot_basket_analysis(df_basket)

    # 8. Correlation heatmap (needs engineered features)
    print("[7/7] Plotting correlation heatmap...")
    df_features = build_features(df_info)
    plot_correlation_heatmap(df_features, FEATURE_COLS)

    print("\nEDA complete.")


if __name__ == "__main__":
    run_eda()
