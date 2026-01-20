import React from 'react';
import { motion } from 'framer-motion';

const Header = ({ onClearChat }) => {
    return (
        <motion.header
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="bg-slate-900/80 backdrop-blur-lg border-b border-slate-800 px-6 py-3 sticky top-0 z-10"
        >
            <div className="max-w-5xl mx-auto flex items-center justify-between">
                <div className="flex items-center space-x-2">
                    {/* Empty space for balance */}
                </div>

                <button
                    onClick={onClearChat}
                    className="flex items-center space-x-1.5 px-3 py-1.5 text-slate-400 hover:text-teal-400 hover:bg-slate-800 rounded-lg transition-all duration-200 text-sm"
                    title="Clear conversation"
                >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    <span className="hidden sm:inline">Clear</span>
                </button>
            </div>
        </motion.header>
    );
};

export default Header;
