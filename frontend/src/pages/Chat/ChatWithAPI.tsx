import { useEffect, useState } from 'react'
import { Box, CircularProgress, Alert } from '@mui/material'
import Chat from '../pages/Chat/Chat'
import { chatAPI } from '../services/api'

export default function ChatWithAPI() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Check API health
    chatAPI.sendMessage('health check')
      .catch(() => setError('API not connected'))
  }, [])

  return (
    <Box>
      {loading && <CircularProgress />}
      {error && <Alert severity="warning">{error}</Alert>}
      <Chat />
    </Box>
  )
}