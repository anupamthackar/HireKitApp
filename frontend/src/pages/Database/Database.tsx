import { Box, Typography, Paper, Button } from '@mui/material'

export default function Database() {
  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3, color: 'primary.main' }}>
        Database
      </Typography>
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          View and manage your job database
        </Typography>
        <Button variant="contained" color="primary">
          View Jobs
        </Button>
      </Paper>
    </Box>
  )
}