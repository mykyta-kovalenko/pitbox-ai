import React from 'react'
import { motion } from 'framer-motion'
import { GiRaceCar, GiCheckeredFlag } from 'react-icons/gi'
import { FaWifi } from 'react-icons/fa'
import { AiOutlineDisconnect } from 'react-icons/ai'

const Header = ({ connectionStatus }) => {
  return (
    <motion.header 
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ type: "spring", stiffness: 100 }}
      className="bg-gradient-to-r from-racing-black via-racing-red to-racing-black border-b-4 border-racing-red shadow-2xl"
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo Section */}
          <div className="flex items-center gap-4">
            <motion.div 
              whileHover={{ rotate: 360 }}
              transition={{ duration: 0.5 }}
              className="relative"
            >
              <div className="w-16 h-16 bg-gradient-to-br from-racing-red to-racing-orange rounded-full flex items-center justify-center shadow-lg red-glow">
                <span className="text-2xl font-racing font-black text-white">PB</span>
              </div>
              <GiCheckeredFlag className="absolute -top-2 -right-2 text-white text-xl" />
            </motion.div>
            
            <div>
              <h1 className="text-3xl font-display text-white tracking-wider">
                PIT BOX AI
              </h1>
              <p className="text-racing-orange text-sm font-racing tracking-widest">
                NASCAR INTELLIGENCE ASSISTANT
              </p>
            </div>
          </div>

          {/* Status Section */}
          <div className="flex items-center gap-6">
            {/* Speedometer */}
            <div className="hidden md:block">
              <div className="relative w-20 h-20">
                <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
                  <path
                    className="text-racing-gray"
                    stroke="currentColor"
                    strokeWidth="3"
                    fill="none"
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <motion.path
                    className="text-racing-red"
                    stroke="currentColor"
                    strokeWidth="3"
                    fill="none"
                    strokeLinecap="round"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 0.75 }}
                    transition={{ duration: 2, ease: "easeOut" }}
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-xs font-racing text-white">MPH</span>
                </div>
              </div>
            </div>

            {/* Racing Flags */}
            <div className="flex gap-2">
              <motion.div 
                animate={{ y: [0, -3, 0] }}
                transition={{ repeat: Infinity, duration: 2 }}
                className="w-8 h-6 bg-green-500 rounded-sm shadow-md"
                title="Green Flag - GO!"
              />
              <motion.div 
                animate={{ y: [0, -3, 0] }}
                transition={{ repeat: Infinity, duration: 2, delay: 0.2 }}
                className="w-8 h-6 bg-yellow-400 rounded-sm shadow-md"
                title="Yellow Flag - Caution"
              />
              <motion.div 
                animate={{ y: [0, -3, 0] }}
                transition={{ repeat: Infinity, duration: 2, delay: 0.4 }}
                className="w-8 h-6 checkered-flag rounded-sm shadow-md"
                title="Checkered Flag - Finish"
              />
            </div>

            {/* Connection Status */}
            <motion.div 
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className={`flex items-center gap-2 px-4 py-2 rounded-full backdrop-blur-sm ${
                connectionStatus === 'online' 
                  ? 'bg-green-500/20 border border-green-500' 
                  : connectionStatus === 'offline'
                  ? 'bg-red-500/20 border border-red-500'
                  : 'bg-yellow-500/20 border border-yellow-500'
              }`}
            >
              {connectionStatus === 'online' ? (
                <>
                  <FaWifi className="text-green-500" />
                  <span className="text-xs font-racing text-green-500">SYSTEM ONLINE</span>
                </>
              ) : connectionStatus === 'offline' ? (
                <>
                  <AiOutlineDisconnect className="text-red-500" />
                  <span className="text-xs font-racing text-red-500">OFFLINE</span>
                </>
              ) : (
                <>
                  <motion.div 
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
                    className="w-4 h-4 border-2 border-yellow-500 border-t-transparent rounded-full"
                  />
                  <span className="text-xs font-racing text-yellow-500">CONNECTING</span>
                </>
              )}
            </motion.div>
          </div>
        </div>
      </div>
    </motion.header>
  )
}

export default Header