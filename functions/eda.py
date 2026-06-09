import ast
from collections import Counter

import contextily as ctx
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec
from shapely.geometry import Point
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN


# Columns with lifetime_spend_, for convenience in EDA and preprocessing
SPEND_COLS = [
    'lifetime_spend_groceries',
    'lifetime_spend_electronics',
    'lifetime_spend_vegetables',
    'lifetime_spend_nonalcohol_drinks',
    'lifetime_spend_alcohol_drinks',
    'lifetime_spend_meat',
    'lifetime_spend_fish',
    'lifetime_spend_hygiene',
    'lifetime_spend_videogames',
    'lifetime_spend_petfood']



# AI-generated custom palette and styling for plots
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


# MISSING VALUES

def plot_missing_values(df):
    """
    Bar chart of missing-value percentages per column
    """
    miss_pct = (df.isnull().mean() * 100).sort_values(ascending=False)
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
    fig.tight_layout()
    plt.show()


# DEMOGRAPHICS

def plot_demographics(df):
    """
    Age distribution, gender split, education level, household size
    """
    df = df.copy()

    # Education
    df["education_level"] = (
        df["customer_name"]
        .str.extract(r"^(Bsc|Msc|Phd)\.", expand=False)
        .fillna("No Degree"))

    fig = plt.figure(figsize=(14, 8), facecolor=BG_COLOR)
    fig.suptitle("Customer Demographics", fontsize=14, fontweight="bold", y=1.01)
    gs = GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    # Age distribution
    ax1 = fig.add_subplot(gs[0, 0])
    sns.histplot(df["age"].dropna(), discrete=True,bins=30, color=ACCENT, ax=ax1, edgecolor="white", linewidth=0.4)
    ax1.axvline(df["age"].median(), color=ACCENT2, linestyle="--", linewidth=1.5, label=f"Median: {df['age'].median():.0f}")
    ax1.set_title("Age Distribution")
    ax1.set_xlabel("Age (years)")
    ax1.set_ylabel("Count")
    ax1.legend(fontsize=8)

    # Gender split
    ax2 = fig.add_subplot(gs[0, 1])
    gender_counts = df["customer_gender"].value_counts()
    colors = [ACCENT, ACCENT2]
    wedges, texts, autotexts = ax2.pie(
        gender_counts.values,
        labels=gender_counts.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops=dict(edgecolor="white", linewidth=1.5))
    
    for t in autotexts:
        t.set_fontsize(10)
    ax2.set_title("Gender Split")

    # Education level
    ax3 = fig.add_subplot(gs[1, 0])
    edu_order = ["No Degree", "Bsc", "Msc", "Phd"]
    edu_counts = df["education_level"].value_counts().reindex(edu_order)
    bars = ax3.bar(edu_counts.index, edu_counts.values, color=[ACCENT, ACCENT2, "#457B9D", "#A8DADC"],
                   edgecolor="white", linewidth=0.5)
    for bar in bars:
        ax3.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 50,
                 f"{bar.get_height():,.0f}",
                 ha="center", fontsize=8)
    ax3.set_title("Education Level")
    ax3.set_ylabel("Customers")

    # Dependants 
    ax4 = fig.add_subplot(gs[1, 1])
    hh_counts = df["dependants"].value_counts().sort_index()
    ax4.bar(hh_counts.index.astype(int), hh_counts.values, color=ACCENT, edgecolor="white", linewidth=0.5)
    ax4.set_title("Dependencies (kids + teens)")
    ax4.set_xlabel("Number of dependants")
    ax4.set_ylabel("Customers")

    fig.tight_layout()
    plt.show()


# Customer behavior

def plot_customer_behavior(df):
    """
    Tenure, loyalty card, typical shopping hour, complaints, promo %
    """

    df = df.copy()
    df["customer_tenure"] = 2026 - df["year_first_transaction"].clip(upper=2026)
    df["number_complaints"] = df["number_complaints"].fillna(0)
    df["typical_hour"] = df["typical_hour"].fillna(df["typical_hour"].median())
    df["percentage_of_products_bought_promotion"] = (
        df["percentage_of_products_bought_promotion"]
        .fillna(df["percentage_of_products_bought_promotion"].median())
    )

    fig = plt.figure(figsize=(15, 9), facecolor=BG_COLOR)
    fig.suptitle("Customer Behaviour", fontsize=14, fontweight="bold", y=1.01)
    gs = GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.38)

    # Customer tenure
    ax1 = fig.add_subplot(gs[0, 0])
    sns.histplot(df["customer_tenure"].dropna(), bins=25, kde=True, color=ACCENT, ax=ax1, edgecolor="white", linewidth=0.4)
    ax1.set_title("Customer Tenure (years)")
    ax1.set_xlabel("Years as customer")
    ax1.set_ylabel("Count")

    # Loyalty card
    ax2 = fig.add_subplot(gs[0, 1])
    lc_counts = df["has_loyalty_card"].value_counts()
    ax2.bar(["No Card", "Has Card"], lc_counts.reindex([False, True]).values,
            color=[ACCENT2, ACCENT], edgecolor="white")
    for i, v in enumerate(lc_counts.reindex([False, True]).values):
        ax2.text(i, v + 100, f"{v:,}\n({v/len(df)*100:.0f}%)", ha="center", fontsize=9)
    ax2.set_title("Loyalty Card Ownership")
    ax2.set_ylabel("Customers")

    # Typical shopping hour
    ax3 = fig.add_subplot(gs[0, 2])
    hour_counts = df["typical_hour"].value_counts().sort_index()
    ax3.bar(hour_counts.index, hour_counts.values,
            color=ACCENT, edgecolor="white", linewidth=0.4)
    ax3.set_title("Typical Shopping Hour")
    ax3.set_xlabel("Hour of day (0–23)")
    ax3.set_ylabel("Customers")
    ax3.xaxis.set_major_locator(mticker.MultipleLocator(4))

    # Complaints
    ax4 = fig.add_subplot(gs[1, 0])
    comp_counts = df["number_complaints"].value_counts().sort_index()
    ax4.bar(comp_counts.index.astype(int), comp_counts.values,
            color=ACCENT2, edgecolor="white", linewidth=0.4)
    ax4.set_title("Number of Complaints")
    ax4.set_xlabel("Complaints")
    ax4.set_ylabel("Customers")
    ax4.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    # Promotions % distribution
    ax5 = fig.add_subplot(gs[1, 1])
    sns.histplot(df["percentage_of_products_bought_promotion"] * 100,bins=30, kde=True, color="#457B9D", ax=ax5,
                 edgecolor="white", linewidth=0.4)
    ax5.set_title("% Products Bought on Promotion")
    ax5.set_xlabel("Promotion %")
    ax5.set_ylabel("Count")

    # Distinct stores visited
    ax6 = fig.add_subplot(gs[1, 2])
    stores = df["distinct_stores_visited"].fillna(df["distinct_stores_visited"].median())
    store_counts = stores.value_counts().sort_index()
    ax6.bar(store_counts.index.astype(int), store_counts.values,
            color=ACCENT, edgecolor="white", linewidth=0.4)
    ax6.set_title("Distinct Stores Visited")
    ax6.set_xlabel("Number of stores")
    ax6.set_ylabel("Customers")
    ax6.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    fig.tight_layout()
    plt.show()


# Spending analysis

def plot_spend_analysis(df):
    """
    Total spend distribution + category spend shares
    """

    df = df.copy()
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

    # Total spend distribution
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

    # Spend by category (median bar chart)
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

    # Category shares pie chart
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

    # Box-plot: log-scaled spend per category 
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

    fig.tight_layout()
    plt.show()


# Geographic distribution
def plot_geographic_distribution(df):
    """
    GeoPandas map of customer home locations overlaid on a CartoDB basemap
    Axes show WGS-84 latitude / longitude degrees.
    """
    from pyproj import Transformer

    df = df.copy()

    # Build GeoDataFrame (WGS-84) then reproject to Web Mercator
    geometry = [Point(lon, lat) for lon, lat in zip(df["longitude"], df["latitude"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    gdf_merc = gdf.to_crs(epsg=3857)

    # Single panel map 
    fig, ax_map = plt.subplots(figsize=(10, 9), facecolor=BG_COLOR)
    fig.suptitle(
        "Geographic Distribution of Customers",
        fontsize=15, fontweight="bold", y=1.01,
    )

    ax_map.set_facecolor(BG_COLOR)

    gdf_merc.plot(
        ax=ax_map,
        color=ACCENT,
        markersize=8,
        alpha=0.6,
        linewidths=0,
    )

    # Zoom out 20% 
    x_min, y_min, x_max, y_max = gdf_merc.total_bounds
    x_pad = (x_max - x_min) * 0.20
    y_pad = (y_max - y_min) * 0.20
    ax_map.set_xlim(x_min - x_pad, x_max + x_pad)
    ax_map.set_ylim(y_min - y_pad, y_max + y_pad)

    # Basemap tile (CartoDB Positron – clean, light)
    try:
        ctx.add_basemap(
            ax_map,
            crs=gdf_merc.crs.to_string(),
            source=ctx.providers.CartoDB.Positron,
            zoom="auto",
            attribution_size=6,
        )
    except Exception:
        try:
            ctx.add_basemap(
                ax_map,
                crs=gdf_merc.crs.to_string(),
                source=ctx.providers.OpenStreetMap.Mapnik,
                zoom="auto",
                attribution_size=6,
            )
        except Exception:
            pass  

    # Convert Web Mercator tick positions → lat/lon for axis labels 
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

    x_ticks = ax_map.get_xticks()
    y_ticks = ax_map.get_yticks()

    # Filter to ticks within the current view
    xl, xr = ax_map.get_xlim()
    yb, yt = ax_map.get_ylim()
    x_ticks = [t for t in x_ticks if xl <= t <= xr]
    y_ticks = [t for t in y_ticks if yb <= t <= yt]

    lon_labels = [f"{transformer.transform(t, 0)[0]:.3f}°" for t in x_ticks]
    lat_labels = [f"{transformer.transform(0, t)[1]:.3f}°" for t in y_ticks]

    ax_map.set_xticks(x_ticks)
    ax_map.set_yticks(y_ticks)
    ax_map.set_xticklabels(lon_labels, fontsize=8)
    ax_map.set_yticklabels(lat_labels, fontsize=8)
    ax_map.set_xlabel("Longitude", fontsize=9)
    ax_map.set_ylabel("Latitude", fontsize=9)
    ax_map.tick_params(length=3, color="#AAAAAA")
    for spine in ax_map.spines.values():
        spine.set_edgecolor("#CCCCCC")

    ax_map.set_title("Customer Locations", fontweight="bold")

    fig.tight_layout()
    plt.show()


def plot_correlation_heatmap(df, feature_cols):
    """
    Lower-triangle correlation heatmap of the engineered feature set
    """
    corr = df[feature_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(figsize=(14, 11), facecolor=BG_COLOR)
    sns.heatmap(
        corr, mask=mask, annot=False, cmap="coolwarm",
        vmin=-1, vmax=1, linewidths=0.3, linecolor="white",
        cbar_kws={"shrink": 0.8}, ax=ax,
    )
    ax.set_title("Feature Correlation Heatmap", fontweight="bold", pad=14)
    ax.tick_params(axis="x", rotation=90, labelsize=7)
    ax.tick_params(axis="y", labelsize=7)

    fig.tight_layout()
    plt.show()
    return corr


def plot_high_correlations(df, threshold=0.5, max_plots=6):
    """
    Automatically finds feature pairs with absolute correlation > threshold 
    and plots individual scatterplots for the top pairs to analyze point distributions
    """
    corr = df.corr()
    pairs = corr.unstack()
    high_corr = pairs[(abs(pairs) > threshold) & (pairs != 1.0)].drop_duplicates()
    
    # Sort by absolute correlation magnitude
    high_corr = high_corr.reindex(high_corr.abs().sort_values(ascending=False).index)
    
    if len(high_corr) == 0:
        print(f"No correlations above {threshold} found.")
        return
        
    n_plots = min(len(high_corr), max_plots)
    
    for i, (idx, val) in enumerate(high_corr.head(n_plots).items()):
        var1, var2 = idx
        
        # Create a separate, large figure for each pair
        fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG_COLOR)
        
        sns.scatterplot(data=df, x=var1, y=var2, ax=ax, color=ACCENT, alpha=0.4, s=30, edgecolor="none")
        ax.set_title(f"{var1} vs {var2}  (r = {val:.2f})", fontweight="bold", pad=15)
        
        fig.tight_layout()
        plt.show()

def plot_k_distance(data, k):
    """
    Plots the k-distance graph to help find the optimal 'eps' for DBSCAN.
    """
    nbr = NearestNeighbors(n_neighbors=k)
    nbrs = nbr.fit(data)
    distances, indices = nbrs.kneighbors(data)
    # Sort the distances to the k nearest neighbor
    distances = np.sort(distances[:, k-1], axis=0)
    
    plt.figure(figsize=(10, 6), facecolor=BG_COLOR)
    plt.plot(distances, color=ACCENT)
    plt.xlabel('Points sorted by distance')
    plt.ylabel(f'{k}-th Nearest Neighbor Distance')
    plt.title(f'K-distance Graph for k = {k}', fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.show()

def detect_outliers_dbscan(data, scaled_data, eps, min_samples):
    """
    Detect outliers in the data using DBSCAN.
    Fits DBSCAN on `scaled_data` and returns the original `data` 
    with an additional 'outlier' boolean column.
    """
    data = data.copy()
        
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    dbscan.fit(scaled_data)
    
    data['cluster'] = dbscan.labels_
    # Points labeled as -1 are outliers
    data['outlier'] = data['cluster'] == -1
    
    print(f"Detected {data['outlier'].sum()} outliers out of {len(data)} points.")
    return data

def visualize_outliers_vs_normal(data_outliers, feature1, feature2, n_samples=None):
    """
    Visualize normal data vs outliers for two chosen features
    """
    outliers = data_outliers[data_outliers['outlier']]
    normal = data_outliers[~data_outliers['outlier']]
    
    if n_samples is not None and len(outliers) > n_samples:
        outliers = outliers.sample(n=n_samples, random_state=42)
        
    plt.figure(figsize=(10, 7), facecolor=BG_COLOR)
    plt.scatter(normal[feature1], normal[feature2], c=ACCENT, alpha=0.3, label='Normal Data', s=15, edgecolor='none')
    plt.scatter(outliers[feature1], outliers[feature2], c=ACCENT2, alpha=1.0, label='Outliers', s=25, edgecolor='black')
    
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.title(f'Outliers vs Normal: {feature1} & {feature2}', fontweight='bold')
    plt.legend()
    plt.show()