import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Header from './components/Header'
import WelcomeScreen from './components/WelcomeScreen'
import ChatContainer from './components/ChatContainer'
import SpeedLines from './components/SpeedLines'
import FloatingCar from './components/FloatingCar'

function App() {
  const [isStarted, setIsStarted] = useState(false)
  const [messages, setMessages] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState('checking')

  useEffect(() => {
    checkAPIConnection()
  }, [])

  const checkAPIConnection = async () => {
    try {
      const response = await fetch('http://localhost:8765/health')
      if (response.ok) {
        setConnectionStatus('online')
      } else {
        setConnectionStatus('offline')
      }
    } catch (error) {
      setConnectionStatus('offline')
    }
  }

  const handleStart = () => {
    setIsStarted(true)
    setMessages([
      {
        id: 1,
        type: 'ai',
        content: "Welcome to Pit Box AI! I'm your NASCAR intelligence assistant. Ask me anything about racing, strategies, drivers, teams, or race analytics!",
        timestamp: new Date()
      }
    ])
  }

  const sendMessage = async (content) => {
    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      content,
      timestamp: new Date()
    }
    
    setMessages(prev => [...prev, userMessage])
    setIsTyping(true)

    try {
      const response = await fetch('http://localhost:8765/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: content })
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const data = await response.json()
      
      const aiMessage = {
        id: messages.length + 2,
        type: 'ai',
        content: data.response,
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage = {
        id: messages.length + 2,
        type: 'ai',
        content: 'Sorry, I encountered an error. Please make sure the backend server is running on port 8765.',
        timestamp: new Date(),
        isError: true
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsTyping(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-racing-black via-racing-gray to-racing-black relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-carbon-fiber opacity-20"></div>
      <SpeedLines />
      <FloatingCar />
      
      {/* Racing grid pattern */}
      <div className="absolute inset-0 bg-checkered opacity-5"></div>
      
      {/* Main Content */}
      <div className="relative z-10">
        <Header connectionStatus={connectionStatus} />
        
        <AnimatePresence mode="wait">
          {!isStarted ? (
            <WelcomeScreen onStart={handleStart} />
          ) : (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
              className="container mx-auto px-4 py-8"
            >
              <ChatContainer 
                messages={messages}
                onSendMessage={sendMessage}
                isTyping={isTyping}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

export default App