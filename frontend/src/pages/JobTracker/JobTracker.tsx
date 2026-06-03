import { Box, Typography, Chip, IconButton, TextField, Button, Paper } from '@mui/material'
import { Add, Refresh, FilterList } from '@mui/icons-material'
import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { jobAPI } from '../../services/api'

interface Job {
  id: string
  title: string
  company: string
  location: string
  salary?: string
  score: number
  match: string
  sponsorship: boolean
  source?: string
  url?: string
}

export default function JobTracker() {
  const [showSponsoredOnly, setShowSponsoredOnly] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')

  const { data: jobs = [], isLoading, refetch } = useQuery({
    queryKey: ['jobs', showSponsoredOnly],
    queryFn: () => jobAPI.getJobs({ sponsored: showSponsoredOnly }).then(res => res.data),
  })

  useEffect(() => {
    // Load jobs on mount
    refetch()
  }, [showSponsoredOnly])

  const filteredJobs = jobs.filter(job =>
    job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    job.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
    job.location.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ color: 'primary.main' }}>
          🎯 Job Tracker
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            size="small"
            placeholder="Search jobs..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            sx={{ width: 250 }}
          />
          <IconButton
            color={showSponsoredOnly ? 'primary' : 'default'}
            onClick={() => setShowSponsoredOnly(!showSponsoredOnly)}
          >
            <FilterList />
          </IconButton>
          <IconButton onClick={() => refetch()} disabled={isLoading}>
            <Refresh />
          </IconButton>
        </Box>
      </Box>

      {isLoading ? (
        <Typography>Loading jobs...</Typography>
      ) : (
        <Box>
          {filteredJobs.length === 0 ? (
            <Paper sx={{ p: 4, textAlign: 'center' }}>
              <Typography>No jobs found. Check backend connection or run job hunt agent.</Typography>
              <Button
                variant="contained"
                sx={{ mt: 2 }}
                onClick={() => window.location.href = 'http://localhost:8000/jobs'}
              >
                Check Backend API
              </Button>
            </Paper>
          ) : (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {filteredJobs.map((job) => (
                <Paper
                  key={job.id}
                  sx={{
                    p: 3,
                    borderLeft: '4px solid',
                    borderColor: job.score >= 85 ? 'success.main' : job.score >= 65 ? 'warning.main' : 'error.main',
                    transition: 'transform 0.2s',
                    '&:hover': { transform: 'translateX(4px)' },
                  }}
                >
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="h6">{job.title}</Typography>
                    <Chip
                      label={`${job.score}/100`}
                      color={job.score >= 85 ? 'success' : job.score >= 65 ? 'warning' : 'error'}
                      size="small"
                    />
                  </Box>
                  <Typography color="text.secondary" sx={{ mb: 1 }}>
                    {job.company} • {job.location}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Chip label={job.match} size="small" />
                    <Chip
                      label={job.sponsorship ? "✅ Sponsorship" : "⚠️ Self-Funded"}
                      color={job.sponsorship ? 'success' : 'warning'}
                      size="small"
                    />
                    {job.salary && <Chip label={job.salary} size="small" variant="outlined" />}
                    {job.source && <Chip label={job.source} size="small" variant="outlined" />}
                  </Box>
                </Paper>
              ))}
            </Box>
          )}
        </Box>
      )}
    </Box>
  )
}