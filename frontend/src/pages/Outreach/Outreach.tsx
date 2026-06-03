import { Box, Typography, Paper, Button } from '@mui/material'

export default function Outreach() {
  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3, color: 'primary.main' }}>
        Outreach
      </Typography>
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Generate and track outreach messages
        </Typography>
        <Button variant="contained" color="primary">
          Create Outreach
        </Button>
      </Paper>
    </Box>
  )
}