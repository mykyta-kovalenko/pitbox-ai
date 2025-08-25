import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Message from './Message'
import MessageInput from './MessageInput'
import TypingIndicator from './TypingIndicator'

const ChatContainer = ({ messages, onSendMessage, isTyping }) => {
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="bg-racing-gray/50 backdrop-blur-md border-2 border-racing-red/30 rounded-2xl shadow-2xl overflow-hidden h-[calc(100vh-240px)]"
    >
      {/* Chat Header */}
      <div className="bg-gradient-to-r from-racing-black to-racing-lightGray border-b border-racing-red/30 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <div className="absolute inset-0 w-3 h-3 bg-green-500 rounded-full animate-ping"></div>
            </div>
            <div>
              <h3 className="text-white font-racing text-lg">PIT BOX ASSISTANT</h3>
              <p className="text-racing-orange text-xs">NASCAR Intelligence System</p>
            </div>
          </div>
          
          {/* Lap Counter Animation */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-400 font-racing">LAP</span>
            <motion.div 
              className="text-2xl font-racing text-racing-red"
              animate={{ 
                textShadow: [
                  "0 0 10px rgba(255,0,0,0.5)",
                  "0 0 20px rgba(255,0,0,0.8)",
                  "0 0 10px rgba(255,0,0,0.5)"
                ]
              }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              {messages.length}
            </motion.div>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 h-[calc(100%-140px)] racing-stripes">
        <AnimatePresence initial={false}>
          {messages.map((message) => (
            <Message key={message.id} message={message} />
          ))}
          {isTyping && <TypingIndicator />}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <MessageInput onSendMessage={onSendMessage} disabled={isTyping} />
    </motion.div>
  )
}

export default ChatContainer