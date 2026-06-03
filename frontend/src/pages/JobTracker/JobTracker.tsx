import { Box, Typography, Chip, Tooltip } from '@mui/material'
import { AgGridReact } from 'ag-grid-react'
import 'ag-grid-community/styles/ag-theme-quartz.css'

export default function JobTracker() {
  const rowData = [
    {
      title: 'Senior iOS Engineer',
      company: 'Revolut',
      location: 'Dubai, UAE',
      salary: '15K-22K AED',
      score: 95,
      match: 'H',
      sponsorship: true,
      source: 'LinkedIn',
      url: 'https://linkedin.com/jobs/...',
    },
  ]

  const columnDefs = [
    { field: 'title', headerName: 'Job Title', flex: 2 },
    { field: 'company', headerName: 'Company', flex: 1 },
    { field: 'location', headerName: 'Location', flex: 1 },
    { field: 'salary', headerName: 'Salary', flex: 1 },
    {
      field: 'score',
      headerName: 'Score',
      flex: 1,
      cellRenderer: (params) => (
        <Chip
          label={`${params.value}/100`}
          color={params.value >= 85 ? 'success' : params.value >= 65 ? 'warning' : 'error'}
          size="small"
        />
      ),
    },
    {
      field: 'sponsorship',
      headerName: 'Visa',
      flex: 1,
      cellRenderer: (params) =>
        params.value ? (
          <Chip label="✅ Sponsorship" color="success" size="small" />
        ) : (
          <Chip label="⚠️ Self-Funded" color="warning" size="small" />
        ),
    },
  ]

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3, color: 'primary.main' }}>
        Job Tracker
      </Typography>
      <div className="ag-theme-quartz" style={{ height: 600 }}>
        <AgGridReact rowData={rowData} columnDefs={columnDefs} />
      </div>
    </Box>
  )
}