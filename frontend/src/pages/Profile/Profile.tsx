import { Box, Typography, TextField, Button, Paper } from '@mui/material'

export default function Profile() {
  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3, color: 'primary.main' }}>
        Profile
      </Typography>
      <Paper sx={{ p: 4 }}>
        <TextField
          label="Name"
          defaultValue="Anupam Thackar"
          fullWidth
          sx={{ mb: 2 }}
        />
        <TextField
          label="Email"
          defaultValue="anupamthackar@gmail.com"
          fullWidth
          sx={{ mb: 2 }}
        />
        <TextField
          label="Location"
          defaultValue="Mumbai, India"
          fullWidth
          sx={{ mb: 2 }}
        />
        <Button variant="contained" color="primary">
          Save Profile
        </Button>
      </Paper>
    </Box>
  )
}