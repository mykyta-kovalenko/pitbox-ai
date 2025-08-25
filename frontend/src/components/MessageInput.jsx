import React, { useState, useRef } from 'react'
import { motion } from 'framer-motion'
import { IoSend } from 'react-icons/io5'
import { GiRaceCar } from 'react-icons/gi'
import { FaMicrophone, FaPaperclip } from 'react-icons/fa'

const MessageInput = ({ onSendMessage, disabled }) => {
  const [message, setMessage] = useState('')
  const [isFocused, setIsFocused] = useState(false)
  const inputRef = useRef(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !disabled) {
      onSendMessage(message)
      setMessage('')
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="border-t border-racing-red/30 bg-racing-black/50 p-4">
      <div className="flex items-center gap-3">
        {/* Attachment Button */}
        <motion.button
          type="button"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          className="p-3 rounded-full bg-racing-gray hover:bg-racing-lightGray transition-colors"
          title="Attach file (coming soon)"
        >
          <FaPaperclip className="text-gray-400" />
        </motion.button>

        {/* Input Field */}
        <div className={`flex-1 relative transition-all ${
          isFocused ? 'scale-[1.02]' : ''
        }`}>
          <input
            ref={inputRef}
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            disabled={disabled}
            placeholder="Ask about NASCAR, racing strategies, or race analytics..."
            className={`w-full px-5 py-3 bg-racing-gray/70 border-2 rounded-full text-white placeholder-gray-500 transition-all ${
              isFocused 
                ? 'border-racing-red shadow-lg shadow-racing-red/20' 
                : 'border-racing-gray hover:border-racing-red/50'
            } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
          />
          
          {/* Racing effect when typing */}
          {message.length > 0 && (
            <motion.div
              className="absolute right-4 top-1/2 -translate-y-1/2"
              initial={{ x: -20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 20, opacity: 0 }}
            >
              <GiRaceCar className="text-racing-orange text-xl animate-pulse" />
            </motion.div>
          )}
        </div>

        {/* Voice Button */}
        <motion.button
          type="button"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          className="p-3 rounded-full bg-racing-gray hover:bg-racing-lightGray transition-colors"
          title="Voice input (coming soon)"
        >
          <FaMicrophone className="text-gray-400" />
        </motion.button>

        {/* Send Button */}
        <motion.button
          type="submit"
          disabled={!message.trim() || disabled}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className={`relative px-6 py-3 rounded-full font-racing tracking-wider transition-all overflow-hidden group ${
            message.trim() && !disabled
              ? 'bg-gradient-to-r from-racing-red to-racing-orange text-white shadow-lg hover:shadow-racing-red/50' 
              : 'bg-racing-gray text-gray-500 cursor-not-allowed'
          }`}
        >
          {/* Button Background Animation */}
          {message.trim() && !disabled && (
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-racing-orange to-racing-red"
              initial={{ x: "-100%" }}
              animate={{ x: "100%" }}
              transition={{ duration: 1, repeat: Infinity }}
            />
          )}
          
          <span className="relative z-10 flex items-center gap-2">
            <span className="hidden sm:inline">SEND</span>
            <IoSend className="text-lg" />
          </span>

          {/* Exhaust effect */}
          {message.trim() && !disabled && (
            <div className="absolute right-0 top-1/2 -translate-y-1/2">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-racing-orange rounded-full exhaust-smoke"></div>
                <div className="w-2 h-2 bg-racing-red rounded-full exhaust-smoke animation-delay-200"></div>
                <div className="w-2 h-2 bg-racing-orange rounded-full exhaust-smoke animation-delay-400"></div>
              </div>
            </div>
          )}
        </motion.button>
      </div>

      {/* Character counter */}
      {message.length > 0 && (
        <motion.div 
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-2 text-right"
        >
          <span className={`text-xs font-racing ${
            message.length > 500 ? 'text-racing-red' : 'text-gray-500'
          }`}>
            {message.length} / 500
          </span>
        </motion.div>
      )}
    </form>
  )
}

export default MessageInput