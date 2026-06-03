import { Box, TextField, IconButton, Paper, Typography, Avatar } from '@mui/material'
import { Send } from '@mui/icons-material'
import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface Message {
  id: number
  text: string
  sender: 'user' | 'ai'
  timestamp: Date
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Hi! I'm your AI Career Assistant. How can I help you today?",
      sender: 'ai',
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (!input.trim()) return
    
    const userMessage: Message = {
      id: Date.now(),
      text: input,
      sender: 'user',
      timestamp: new Date(),
    }
    setMessages([...messages, userMessage])
    setInput('')
    
    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        id: Date.now() + 1,
        text: "I'll help you find iOS jobs with visa sponsorship. Would you like me to run the job hunt agent?",
        sender: 'ai',
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiMessage])
    }, 1000)
  }

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ flexGrow: 1, mb: 2, overflow: 'auto' }}>
        <AnimatePresence>
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              style={{ display: 'flex', mb: 2, alignItems: 'flex-start' }}
            >
              <Avatar
                sx={{
                  bgcolor: msg.sender === 'ai' ? 'primary.main' : 'secondary.main',
                  mr: 1,
                }}
              >
                {msg.sender === 'ai' ? 'AI' : 'U'}
              </Avatar>
              <Paper
                sx={{
                  p: 2,
                  bgcolor: msg.sender === 'ai' ? 'background.paper' : 'primary.dark',
                  maxWidth: '70%',
                }}
              >
                <Typography>{msg.text}</Typography>
              </Paper>
            </motion.div>
          ))}
        </AnimatePresence>
      </Box>
      
      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Ask about jobs, resumes, or interviews..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          sx={{
            '& .MuiOutlinedInput-root': {
              borderRadius: 3,
            },
          }}
        />
        <IconButton
          color="primary"
          onClick={handleSend}
          sx={{
            background: 'linear-gradient(135deg, #00d4ff 0%, #7928ca 100%)',
            '&:hover': {
              opacity: 0.9,
            },
          }}
        >
          <Send />
        </IconButton>
      </Box>
    </Box>
  )
}