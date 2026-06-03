import { Box, Typography, Button, Paper } from '@mui/material'

export default function ResumeBuilder() {
  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3, color: 'primary.main' }}>
        Resume Builder
      </Typography>
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Generate tailored resumes for each job application
        </Typography>
        <Button variant="contained" color="primary">
          Build New Resume
        </Button>
      </Paper>
    </Box>
  )
}