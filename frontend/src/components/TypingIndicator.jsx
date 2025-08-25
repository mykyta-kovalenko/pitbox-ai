import React from 'react'
import { motion } from 'framer-motion'
import { GiRaceCar } from 'react-icons/gi'

const TypingIndicator = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="flex gap-3"
    >
      {/* AI Avatar */}
      <div className="flex-shrink-0">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-racing-red to-racing-orange flex items-center justify-center shadow-lg">
          <GiRaceCar className="text-white text-xl" />
        </div>
      </div>

      {/* Typing Animation */}
      <div className="bg-gradient-to-r from-racing-gray to-racing-lightGray border border-racing-red/20 px-5 py-3 rounded-2xl shadow-lg">
        <div className="flex items-center gap-2">
          {/* Racing dots */}
          <div className="flex gap-1.5">
            {[0, 1, 2].map((index) => (
              <motion.div
                key={index}
                className="w-2 h-2 bg-racing-red rounded-full"
                animate={{
                  y: [0, -8, 0],
                  backgroundColor: ['#FF0000', '#FF6600', '#FF0000']
                }}
                transition={{
                  duration: 0.6,
                  repeat: Infinity,
                  delay: index * 0.15,
                  ease: "easeInOut"
                }}
              />
            ))}
          </div>
          
          {/* Race car animation */}
          <motion.div
            className="ml-2"
            animate={{ x: [0, 10, 0] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            <GiRaceCar className="text-racing-orange text-sm" />
          </motion.div>
        </div>
      </div>
    </motion.div>
  )
}

export default TypingIndicator