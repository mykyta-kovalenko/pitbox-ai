import React from 'react'
import { motion } from 'framer-motion'
import { GiRaceCar, GiFullMotorcycleHelmet } from 'react-icons/gi'
import { FaUser } from 'react-icons/fa'
import ReactMarkdown from 'react-markdown'

const Message = ({ message }) => {
  const isAI = message.type === 'ai'
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 ${isAI ? '' : 'flex-row-reverse'}`}
    >
      {/* Avatar */}
      <motion.div 
        whileHover={{ scale: 1.1, rotate: 360 }}
        transition={{ duration: 0.5 }}
        className="flex-shrink-0"
      >
        <div className={`w-10 h-10 rounded-full flex items-center justify-center shadow-lg ${
          isAI 
            ? 'bg-gradient-to-br from-racing-red to-racing-orange' 
            : 'bg-gradient-to-br from-gray-600 to-gray-800'
        }`}>
          {isAI ? (
            <GiRaceCar className="text-white text-xl" />
          ) : (
            <GiFullMotorcycleHelmet className="text-white text-lg" />
          )}
        </div>
      </motion.div>

      {/* Message Content */}
      <motion.div 
        className={`flex-1 max-w-[70%] ${isAI ? '' : 'flex justify-end'}`}
        whileHover={{ scale: 1.01 }}
        transition={{ type: "spring", stiffness: 500 }}
      >
        <div className={`relative group ${
          isAI ? '' : 'text-right'
        }`}>
          {/* Message Bubble */}
          <div className={`inline-block px-5 py-3 rounded-2xl shadow-lg ${
            isAI 
              ? 'bg-gradient-to-r from-racing-gray to-racing-lightGray border border-racing-red/20' 
              : 'bg-gradient-to-r from-racing-red/20 to-racing-orange/20 border border-racing-orange/30'
          } ${message.isError ? 'border-red-500 bg-red-500/10' : ''}`}>
            <div className="text-white text-sm leading-relaxed">
              <ReactMarkdown
                components={{
                  p: ({children}) => <p className="mb-2 last:mb-0">{children}</p>,
                  ul: ({children}) => <ul className="list-disc list-inside mb-2">{children}</ul>,
                  ol: ({children}) => <ol className="list-decimal list-inside mb-2">{children}</ol>,
                  li: ({children}) => <li className="mb-1">{children}</li>,
                  code: ({inline, children}) => 
                    inline 
                      ? <code className="bg-racing-black/50 px-1 py-0.5 rounded text-racing-orange font-mono text-xs">{children}</code>
                      : <pre className="bg-racing-black/50 p-3 rounded-lg overflow-x-auto my-2"><code className="text-racing-orange font-mono text-xs">{children}</code></pre>,
                  strong: ({children}) => <strong className="font-bold text-racing-orange">{children}</strong>,
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>
            
            {/* Timestamp */}
            <div className={`text-xs text-gray-500 mt-2 ${isAI ? '' : 'text-right'}`}>
              {new Date(message.timestamp).toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </div>
          </div>

          {/* Racing effect on hover */}
          <div className={`absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none ${
            isAI ? 'bg-racing-red/5' : 'bg-racing-orange/5'
          }`} />
          
          {/* Speed lines effect */}
          {isAI && (
            <div className="absolute -left-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity">
              <div className="w-8 h-0.5 bg-gradient-to-r from-racing-red to-transparent mb-1"></div>
              <div className="w-6 h-0.5 bg-gradient-to-r from-racing-orange to-transparent mb-1"></div>
              <div className="w-4 h-0.5 bg-gradient-to-r from-racing-red to-transparent"></div>
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
  )
}

export default Message