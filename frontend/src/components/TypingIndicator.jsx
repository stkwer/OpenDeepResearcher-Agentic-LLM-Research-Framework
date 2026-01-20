import React from 'react';
import { motion } from 'framer-motion';

const TypingIndicator = () => {
    return (
        <div className="flex items-center space-x-2 px-5 py-4">
            <div className="flex space-x-1.5">
                {[0, 1, 2].map((index) => (
                    <motion.div
                        key={index}
                        className="w-2.5 h-2.5 bg-gradient-to-r from-teal-500 to-purple-500 rounded-full"
                        animate={{
                            y: [0, -8, 0],
                            opacity: [0.5, 1, 0.5],
                        }}
                        transition={{
                            duration: 1,
                            repeat: Infinity,
                            delay: index * 0.15,
                            ease: "easeInOut",
                        }}
                    />
                ))}
            </div>
            <span className="text-slate-400 text-sm ml-2">Researching...</span>
        </div>
    );
};

export default TypingIndicator;
