import React from 'react'
import { motion } from 'framer-motion'

const SpeedLines = () => {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden">
      {/* Horizontal speed lines */}
      {[...Array(5)].map((_, i) => (
        <motion.div
          key={`h-${i}`}
          className="absolute h-0.5 bg-gradient-to-r from-transparent via-racing-red/20 to-transparent"
          style={{
            top: `${20 + i * 15}%`,
            width: `${60 + i * 10}%`,
          }}
          animate={{
            x: ['-100%', '200%'],
          }}
          transition={{
            duration: 3 + i * 0.5,
            repeat: Infinity,
            delay: i * 0.3,
            ease: "linear"
          }}
        />
      ))}
      
      {/* Diagonal speed lines */}
      {[...Array(3)].map((_, i) => (
        <motion.div
          key={`d-${i}`}
          className="absolute h-0.5 bg-gradient-to-r from-transparent via-racing-orange/10 to-transparent transform rotate-12"
          style={{
            top: `${30 + i * 20}%`,
            width: '80%',
          }}
          animate={{
            x: ['-100%', '200%'],
          }}
          transition={{
            duration: 4 + i * 0.5,
            repeat: Infinity,
            delay: i * 0.5,
            ease: "linear"
          }}
        />
      ))}

      {/* Corner vignette effect */}
      <div className="absolute inset-0 bg-gradient-to-t from-racing-black/30 via-transparent to-racing-black/30" />
      <div className="absolute inset-0 bg-gradient-to-r from-racing-black/30 via-transparent to-racing-black/30" />
    </div>
  )
}

export default SpeedLines