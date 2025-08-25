import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { GiCheckeredFlag, GiStopwatch, GiPodium } from 'react-icons/gi'
import { FaTrophy, FaFlagCheckered, FaGasPump } from 'react-icons/fa'

const RaceTracker = () => {
  const [lapTime, setLapTime] = useState(0)
  const [position, setPosition] = useState(1)
  const [fuel, setFuel] = useState(85)

  useEffect(() => {
    // Simulate lap time counter
    const timer = setInterval(() => {
      setLapTime(prev => (prev + 0.1) % 120)
    }, 100)

    return () => clearInterval(timer)
  }, [])

  useEffect(() => {
    // Simulate fuel consumption
    const fuelTimer = setInterval(() => {
      setFuel(prev => Math.max(0, prev - 0.1))
    }, 1000)

    return () => clearInterval(fuelTimer)
  }, [])

  const drivers = [
    { position: 1, name: 'Ross Chastain', number: '1', team: 'Trackhouse', gap: '---' },
    { position: 2, name: 'Daniel Suárez', number: '99', team: 'Trackhouse', gap: '+0.324' },
    { position: 3, name: 'Driver 3', number: '22', team: 'Team Penske', gap: '+1.245' },
    { position: 4, name: 'Driver 4', number: '9', team: 'Hendrick', gap: '+2.567' },
    { position: 5, name: 'Driver 5', number: '11', team: 'JGR', gap: '+3.890' },
  ]

  return (
    <div className="space-y-4">
      {/* Live Timing Card */}
      <motion.div 
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        className="bg-racing-gray/50 backdrop-blur-md border-2 border-racing-red/30 rounded-xl p-4 shadow-xl"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-white font-racing text-sm tracking-wider">LIVE TIMING</h3>
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
            <span className="text-xs text-red-500 font-racing">LIVE</span>
          </div>
        </div>

        {/* Lap Timer */}
        <div className="bg-racing-black/50 rounded-lg p-3 mb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <GiStopwatch className="text-racing-orange" />
              <span className="text-xs text-gray-400">LAP TIME</span>
            </div>
            <motion.div 
              className="text-xl font-racing text-white"
              animate={{ 
                color: lapTime < 30 ? '#00FF00' : lapTime < 60 ? '#FFD700' : '#FF0000'
              }}
            >
              {lapTime.toFixed(1)}s
            </motion.div>
          </div>
        </div>

        {/* Speedometer */}
        <div className="relative h-32 mb-3">
          <svg className="w-full h-full" viewBox="0 0 200 100">
            <path
              d="M 20 80 A 60 60 0 0 1 180 80"
              stroke="#2A2A2A"
              strokeWidth="10"
              fill="none"
              strokeLinecap="round"
            />
            <motion.path
              d="M 20 80 A 60 60 0 0 1 180 80"
              stroke="url(#speedGradient)"
              strokeWidth="10"
              fill="none"
              strokeLinecap="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 0.75 }}
              transition={{ duration: 2, repeat: Infinity, repeatType: "reverse" }}
            />
            <defs>
              <linearGradient id="speedGradient">
                <stop offset="0%" stopColor="#00FF00" />
                <stop offset="50%" stopColor="#FFD700" />
                <stop offset="100%" stopColor="#FF0000" />
              </linearGradient>
            </defs>
            <text x="100" y="60" textAnchor="middle" className="fill-white font-racing text-2xl">
              185
            </text>
            <text x="100" y="75" textAnchor="middle" className="fill-gray-400 text-xs">
              MPH
            </text>
          </svg>
        </div>

        {/* Fuel Gauge */}
        <div className="bg-racing-black/50 rounded-lg p-3">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <FaGasPump className={fuel < 20 ? 'text-red-500 animate-pulse' : 'text-racing-orange'} />
              <span className="text-xs text-gray-400">FUEL</span>
            </div>
            <span className={`text-sm font-racing ${fuel < 20 ? 'text-red-500' : 'text-white'}`}>
              {fuel.toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-racing-gray rounded-full h-2">
            <motion.div 
              className={`h-2 rounded-full ${
                fuel > 50 ? 'bg-green-500' : fuel > 20 ? 'bg-yellow-500' : 'bg-red-500'
              }`}
              style={{ width: `${fuel}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>
      </motion.div>

      {/* Leaderboard */}
      <motion.div 
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-racing-gray/50 backdrop-blur-md border-2 border-racing-red/30 rounded-xl p-4 shadow-xl"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-white font-racing text-sm tracking-wider">LEADERBOARD</h3>
          <GiCheckeredFlag className="text-racing-red" />
        </div>

        <div className="space-y-2">
          {drivers.map((driver, index) => (
            <motion.div
              key={driver.position}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              className={`bg-racing-black/30 rounded-lg p-2 flex items-center justify-between ${
                driver.team === 'Trackhouse' ? 'border border-racing-red/50' : ''
              }`}
            >
              <div className="flex items-center gap-3">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center font-racing text-sm ${
                  driver.position === 1 ? 'bg-gradient-to-br from-yellow-400 to-yellow-600 text-black' :
                  driver.position === 2 ? 'bg-gradient-to-br from-gray-300 to-gray-500 text-black' :
                  driver.position === 3 ? 'bg-gradient-to-br from-orange-600 to-orange-800 text-white' :
                  'bg-racing-gray text-white'
                }`}>
                  {driver.position}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-white text-sm font-medium">{driver.name}</span>
                    <span className="text-racing-orange text-xs font-racing">#{driver.number}</span>
                  </div>
                  <span className="text-xs text-gray-400">{driver.team}</span>
                </div>
              </div>
              <span className={`text-xs font-racing ${
                driver.gap === '---' ? 'text-green-500' : 'text-gray-400'
              }`}>
                {driver.gap}
              </span>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Race Stats */}
      <motion.div 
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-racing-gray/50 backdrop-blur-md border-2 border-racing-red/30 rounded-xl p-4 shadow-xl"
      >
        <h3 className="text-white font-racing text-sm tracking-wider mb-3">RACE STATS</h3>
        
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-racing-black/30 rounded-lg p-3 text-center">
            <FaTrophy className="text-yellow-500 mx-auto mb-1" />
            <div className="text-lg font-racing text-white">42</div>
            <div className="text-xs text-gray-400">LAPS LED</div>
          </div>
          
          <div className="bg-racing-black/30 rounded-lg p-3 text-center">
            <GiPodium className="text-racing-orange mx-auto mb-1" />
            <div className="text-lg font-racing text-white">3</div>
            <div className="text-xs text-gray-400">PIT STOPS</div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default RaceTracker