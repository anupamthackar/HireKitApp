import { Routes, Route } from 'react-router-dom'
import { ThemeProvider, CssBaseline, Box } from '@mui/material'
import { theme } from './theme'
import Sidebar from '../components/Sidebar/Sidebar'
import Chat from '../pages/Chat/Chat'
import ResumeBuilder from '../pages/ResumeBuilder/ResumeBuilder'
import InterviewPrep from '../pages/InterviewPrep/InterviewPrep'
import Outreach from '../pages/Outreach/Outreach'
import JobTracker from '../pages/JobTracker/JobTracker'
import Database from '../pages/Database/Database'
import Profile from '../pages/Profile/Profile'

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
        <Sidebar />
        <Box sx={{ flexGrow: 1, p: 3 }}>
          <Routes>
            <Route path="/" element={<Chat />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/resume" element={<ResumeBuilder />} />
            <Route path="/interview" element={<InterviewPrep />} />
            <Route path="/outreach" element={<Outreach />} />
            <Route path="/jobs" element={<JobTracker />} />
            <Route path="/database" element={<Database />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </Box>
      </Box>
    </ThemeProvider>
  )
}

export default App