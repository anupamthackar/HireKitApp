import { Box, Typography, Paper, Button } from '@mui/material'

export default function InterviewPrep() {
  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3, color: 'primary.main' }}>
        Interview Prep
      </Typography>
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Practice technical and behavioral questions
        </Typography>
        <Button variant="contained" color="primary">
          Start Mock Interview
        </Button>
      </Paper>
    </Box>
  )
}