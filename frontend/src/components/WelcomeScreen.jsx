import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { GiRaceCar, GiSteeringWheel, GiCheckeredFlag } from 'react-icons/gi'
import { FaFlag, FaTachometerAlt } from 'react-icons/fa'

const WelcomeScreen = ({ onStart }) => {
  const [countdown, setCountdown] = useState(null)

  const startCountdown = () => {
    setCountdown(3)
  }

  useEffect(() => {
    if (countdown === null) return
    
    if (countdown === 0) {
      onStart()
      return
    }

    const timer = setTimeout(() => {
      setCountdown(countdown - 1)
    }, 1000)

    return () => clearTimeout(timer)
  }, [countdown, onStart])

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-[calc(100vh-88px)] flex items-center justify-center p-8"
    >
      <div className="max-w-4xl w-full">
        {/* Race Track Animation */}
        <div className="relative mb-12">
          <svg className="w-full h-32" viewBox="0 0 400 100">
            <motion.path
              d="M 50 50 Q 100 20, 200 50 T 350 50"
              stroke="#FF0000"
              strokeWidth="2"
              fill="none"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 2, repeat: Infinity }}
            />
            <motion.circle
              r="5"
              fill="#FF6600"
              initial={{ offsetDistance: "0%" }}
              animate={{ offsetDistance: "100%" }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            >
              <animateMotion dur="2s" repeatCount="indefinite">
                <mpath href="#racePath" />
              </animateMotion>
            </motion.circle>
            <path
              id="racePath"
              d="M 50 50 Q 100 20, 200 50 T 350 50"
              fill="none"
            />
          </svg>
        </div>

        {/* Main Content */}
        <motion.div 
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-center"
        >
          {/* Logo */}
          <motion.div 
            className="inline-block mb-8"
            animate={{ 
              rotate: [0, 5, -5, 0],
            }}
            transition={{ 
              duration: 4,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            <div className="relative">
              <div className="w-32 h-32 mx-auto bg-gradient-to-br from-racing-red to-racing-orange rounded-full flex items-center justify-center shadow-2xl red-glow">
                <GiRaceCar className="text-6xl text-white" />
              </div>
              <motion.div
                className="absolute -top-4 -right-4"
                animate={{ rotate: 360 }}
                transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
              >
                <GiSteeringWheel className="text-4xl text-racing-red" />
              </motion.div>
            </div>
          </motion.div>

          {/* Title */}
          <motion.h1 
            className="text-6xl font-display text-white mb-4 tracking-wider"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            PIT BOX AI
          </motion.h1>
          
          <motion.p 
            className="text-xl text-racing-orange font-racing mb-12 tracking-widest"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.6 }}
          >
            YOUR NASCAR INTELLIGENCE ASSISTANT
          </motion.p>

          {/* Features */}
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.7 }}
          >
            <div className="bg-racing-gray/50 backdrop-blur-sm border border-racing-red/30 rounded-lg p-6">
              <FaTachometerAlt className="text-4xl text-racing-red mx-auto mb-4" />
              <h3 className="font-racing text-sm text-white mb-2">REAL-TIME INSIGHTS</h3>
              <p className="text-xs text-gray-400">Live race data and analytics</p>
            </div>
            
            <div className="bg-racing-gray/50 backdrop-blur-sm border border-racing-red/30 rounded-lg p-6">
              <GiCheckeredFlag className="text-4xl text-racing-orange mx-auto mb-4" />
              <h3 className="font-racing text-sm text-white mb-2">STRATEGY ANALYSIS</h3>
              <p className="text-xs text-gray-400">Pit stop and race strategies</p>
            </div>
            
            <div className="bg-racing-gray/50 backdrop-blur-sm border border-racing-red/30 rounded-lg p-6">
              <FaFlag className="text-4xl text-green-500 mx-auto mb-4" />
              <h3 className="font-racing text-sm text-white mb-2">TEAM INTELLIGENCE</h3>
              <p className="text-xs text-gray-400">Driver and team information</p>
            </div>
          </motion.div>

          {/* Start Button or Countdown */}
          {countdown === null ? (
            <motion.button
              onClick={startCountdown}
              className="relative px-12 py-6 bg-gradient-to-r from-racing-red to-racing-orange text-white font-racing text-xl tracking-widest rounded-lg shadow-2xl overflow-hidden group"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.8 }}
            >
              <span className="relative z-10">START YOUR ENGINES</span>
              <motion.div 
                className="absolute inset-0 bg-gradient-to-r from-racing-orange to-racing-red"
                initial={{ x: "-100%" }}
                whileHover={{ x: 0 }}
                transition={{ duration: 0.3 }}
              />
              <div className="absolute -inset-1 bg-gradient-to-r from-racing-red to-racing-orange rounded-lg blur-lg opacity-50 group-hover:opacity-75 transition-opacity" />
            </motion.button>
          ) : (
            <motion.div 
              className="text-8xl font-racing text-white"
              initial={{ scale: 0 }}
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 0.5 }}
            >
              {countdown === 0 ? 'GO!' : countdown}
            </motion.div>
          )}

          {/* Racing Lights */}
          {countdown !== null && countdown > 0 && (
            <motion.div 
              className="flex justify-center gap-4 mt-8"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              {[3, 2, 1].map((light) => (
                <div
                  key={light}
                  className={`w-12 h-12 rounded-full ${
                    countdown <= light ? 'bg-racing-red shadow-lg red-glow' : 'bg-racing-gray'
                  }`}
                />
              ))}
            </motion.div>
          )}
        </motion.div>
      </div>
    </motion.div>
  )
}

export default WelcomeScreen