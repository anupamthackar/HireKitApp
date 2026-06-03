import { Drawer, List, ListItemButton, ListItemIcon, ListItemText, Box, Typography } from '@mui/material'
import { Chat, Description, Work, Send, Assessment, Storage, Person } from '@mui/icons-material'
import { useNavigate, useLocation } from 'react-router-dom'

const menuItems = [
  { text: 'Chat', icon: <Chat />, path: '/chat' },
  { text: 'Resume Builder', icon: <Description />, path: '/resume' },
  { text: 'Interview Prep', icon: <Assessment />, path: '/interview' },
  { text: 'Outreach', icon: <Send />, path: '/outreach' },
  { text: 'Job Hunt', icon: <Work />, path: '/jobs' },
  { text: 'Database', icon: <Storage />, path: '/database' },
  { text: 'Profile', icon: <Person />, path: '/profile' },
]

export default function Sidebar() {
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: 240,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: 240,
          boxSizing: 'border-box',
          background: 'linear-gradient(180deg, #0a0a0a 0%, #1a1a2a 100%)',
          borderRight: '1px solid rgba(255,255,255,0.05)',
        },
      }}
    >
      <Box sx={{ p: 2 }}>
        <Typography variant="h5" sx={{ color: 'primary.main', fontWeight: 'bold' }}>
          Career OS
        </Typography>
      </Box>
      <List>
        {menuItems.map((item) => (
          <ListItemButton
            key={item.text}
            selected={location.pathname === item.path}
            onClick={() => navigate(item.path)}
            sx={{
              mx: 1,
              my: 0.5,
              borderRadius: 2,
              '&.Mui-selected': {
                background: 'linear-gradient(90deg, #00d4ff20 0%, transparent 100%)',
                borderLeft: '3px solid',
                borderColor: 'primary.main',
              },
            }}
          >
            <ListItemIcon sx={{ color: 'primary.main' }}>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  )
}