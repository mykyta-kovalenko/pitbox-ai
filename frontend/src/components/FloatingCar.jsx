import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { GiRaceCar } from 'react-icons/gi'

const FloatingCar = () => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY })
    }

    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [])

  return (
    <>
      {/* Floating race car that follows mouse subtly */}
      <motion.div
        className="fixed pointer-events-none z-0 opacity-10"
        animate={{
          x: mousePosition.x * 0.02,
          y: mousePosition.y * 0.02,
        }}
        transition={{ type: "spring", stiffness: 50 }}
        style={{
          top: '20%',
          right: '10%',
        }}
      >
        <GiRaceCar className="text-racing-red text-[200px] transform rotate-45" />
      </motion.div>

      {/* Small racing cars animation */}
      {[...Array(3)].map((_, i) => (
        <motion.div
          key={i}
          className="fixed pointer-events-none z-0"
          style={{
            bottom: `${10 + i * 5}%`,
            fontSize: '30px',
          }}
          animate={{
            x: ['-100px', 'calc(100vw + 100px)'],
          }}
          transition={{
            duration: 10 + i * 2,
            repeat: Infinity,
            delay: i * 3,
            ease: "linear"
          }}
        >
          <div className="relative">
            <GiRaceCar className="text-racing-orange/20" />
            {/* Exhaust trail */}
            <div className="absolute top-1/2 -left-4 -translate-y-1/2 flex gap-1">
              <div className="w-2 h-2 bg-white/10 rounded-full animate-pulse"></div>
              <div className="w-1.5 h-1.5 bg-white/5 rounded-full animate-pulse animation-delay-200"></div>
              <div className="w-1 h-1 bg-white/5 rounded-full animate-pulse animation-delay-400"></div>
            </div>
          </div>
        </motion.div>
      ))}

      {/* Race track pattern overlay */}
      <svg className="fixed inset-0 w-full h-full pointer-events-none z-0 opacity-5">
        <motion.path
          d="M 100 300 Q 300 100, 600 300 T 1000 300 Q 1200 100, 1400 300"
          stroke="white"
          strokeWidth="2"
          fill="none"
          strokeDasharray="10 5"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        />
      </svg>

      {/* Tire marks */}
      <div className="fixed bottom-0 left-0 right-0 h-32 pointer-events-none z-0 opacity-5">
        <div className="absolute bottom-10 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-white to-transparent transform skew-y-1"></div>
        <div className="absolute bottom-16 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-white to-transparent transform -skew-y-1"></div>
      </div>
    </>
  )
}

export default FloatingCar