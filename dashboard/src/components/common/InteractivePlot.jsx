/**
 * InteractivePlot.jsx
 * Wrapper around Plotly.js with:
 *   - Dark-themed layout injected automatically
 *   - Plotly toolbar (zoom, pan, PNG download) enabled
 *   - Additional CSV download button
 *   - Loading spinner while Plotly renders
 *   - Descriptive header with title + explanation
 *
 * Props:
 *   title       {string}   Chart title
 *   description {string}   Short explanation shown below the title
 *   data        {Array}    Plotly traces array
 *   layout      {Object}   Plotly layout overrides (merged with dark defaults)
 *   csvData     {Object}   Optional { headers: string[], rows: any[][] }
 *                          If provided, a "↓ CSV" button is shown.
 *   height      {number}   Plot height in px (default 400)
 */
import { useEffect, useRef, useState } from 'react'
import Plotly from 'plotly.js-dist-min'

// Shared dark theme layout applied to every chart
const DARK_LAYOUT_BASE = {
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor:  'rgba(0,0,0,0)',
  font: {
    family: 'Inter, system-ui, sans-serif',
    color:  '#94a3b8',
    size:   12,
  },
  xaxis: {
    gridcolor:     'rgba(124,58,237,0.1)',
    zerolinecolor: 'rgba(124,58,237,0.18)',
    linecolor:     'rgba(124,58,237,0.15)',
    tickcolor:     'rgba(148,163,184,0.4)',
    color:         '#94a3b8',
  },
  yaxis: {
    gridcolor:     'rgba(124,58,237,0.1)',
    zerolinecolor: 'rgba(124,58,237,0.18)',
    linecolor:     'rgba(124,58,237,0.15)',
    tickcolor:     'rgba(148,163,184,0.4)',
    color:         '#94a3b8',
  },
  legend: {
    bgcolor:     'rgba(20,24,50,0.85)',
    bordercolor: 'rgba(124,58,237,0.3)',
    borderwidth: 1,
    font:        { color: '#94a3b8', size: 11 },
  },
  margin:  { l: 50, r: 30, t: 20, b: 50 },
  hoverlabel: {
    bgcolor:     '#1a2140',
    bordercolor: '#7c3aed',
    font:        { color: '#eef2ff', family: 'Inter, sans-serif', size: 12 },
  },
  modebar: {
    bgcolor:     'rgba(0,0,0,0)',
    color:       '#4b5563',
    activecolor: '#7c3aed',
  },
}

const PLOTLY_CONFIG = {
  displaylogo:              false,
  responsive:               true,
  modeBarButtonsToRemove:   ['lasso2d', 'select2d', 'autoScale2d'],
  toImageButtonOptions: {
    format:   'png',
    scale:    2,
    // filename is set dynamically from the title prop
  },
}

export default function InteractivePlot({
  title       = 'Chart',
  description = '',
  data        = [],
  layout      = {},
  csvData     = null,
  height      = 400,
}) {
  const containerRef = useRef(null)
  const [isLoading, setIsLoading]   = useState(true)
  const [hasError, setHasError]     = useState(false)

  // Merge caller's layout with the dark base
  const mergedLayout = {
    ...DARK_LAYOUT_BASE,
    ...layout,
    xaxis:  { ...DARK_LAYOUT_BASE.xaxis,  ...(layout.xaxis  || {}) },
    yaxis:  { ...DARK_LAYOUT_BASE.yaxis,  ...(layout.yaxis  || {}) },
    legend: { ...DARK_LAYOUT_BASE.legend, ...(layout.legend || {}) },
    height,
  }

  const config = {
    ...PLOTLY_CONFIG,
    toImageButtonOptions: {
      ...PLOTLY_CONFIG.toImageButtonOptions,
      filename: title.replace(/\s+/g, '_').toLowerCase(),
    },
  }

  useEffect(() => {
    if (!containerRef.current || !data.length) return

    setIsLoading(true)
    setHasError(false)

    Plotly.newPlot(containerRef.current, data, mergedLayout, config)
      .then(() => setIsLoading(false))
      .catch(() => {
        setIsLoading(false)
        setHasError(true)
      })

    // Cleanup when component unmounts or data changes
    return () => {
      if (containerRef.current) Plotly.purge(containerRef.current)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data, height])

  /** Download the provided csvData as a .csv file */
  const handleDownloadCSV = () => {
    if (!csvData) return
    const lines = [
      csvData.headers.join(','),
      ...csvData.rows.map(row => row.map(cell =>
        typeof cell === 'string' && cell.includes(',') ? `"${cell}"` : cell
      ).join(',')),
    ]
    const blob = new Blob([lines.join('\n')], { type: 'text/csv;charset=utf-8;' })
    const url  = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href     = url
    link.download = `${title.replace(/\s+/g, '_').toLowerCase()}.csv`
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="plot-card">
      {/* Header */}
      <div className="plot-card-header">
        <div>
          <div className="plot-card-title">{title}</div>
          {description && (
            <div className="plot-card-desc">{description}</div>
          )}
        </div>

        {/* Action buttons */}
        <div className="plot-actions">
          {csvData && (
            <button
              className="btn btn-ghost btn-sm"
              onClick={handleDownloadCSV}
              title="Download data as CSV"
            >
              ↓ CSV
            </button>
          )}
          <span
            style={{ fontSize: '0.72rem', color: 'var(--text-muted)', alignSelf: 'center' }}
            title="Use Plotly toolbar to download PNG or zoom"
          >
            🔍 hover to interact
          </span>
        </div>
      </div>

      {/* Plot area */}
      <div className="plot-body" style={{ minHeight: height + 32 }}>
        {/* Loading spinner */}
        {isLoading && (
          <div className="plot-loading">
            <div className="plot-loading-spinner" />
            <span>Rendering visualisation…</span>
          </div>
        )}

        {/* Error state */}
        {hasError && (
          <div className="plot-loading" style={{ color: 'var(--rose)' }}>
            <span>⚠️ Failed to render chart. Check the data prop.</span>
          </div>
        )}

        {/* Plotly mount point */}
        <div ref={containerRef} style={{ width: '100%' }} />
      </div>
    </div>
  )
}
