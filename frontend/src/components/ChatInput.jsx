import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const ChatInput = ({ onSend, disabled }) => {
    const [input, setInput] = useState('');
    const [mode, setMode] = useState('normal'); // 'normal' or 'deepthink'
    const [showModeMenu, setShowModeMenu] = useState(false);
    const [isHovered, setIsHovered] = useState(false);
    const [isScrolled, setIsScrolled] = useState(false);
    const fileInputRef = useRef(null);
    const imageInputRef = useRef(null);

    // Detect scroll to add glow effect
    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 50);
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim() && !disabled) {
            onSend(input.trim());
            setInput('');
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    const handleFileAttach = () => {
        fileInputRef.current?.click();
    };

    const handleImageAttach = () => {
        imageInputRef.current?.click();
    };

    const handleFileChange = (e) => {
        const files = e.target.files;
        if (files && files.length > 0) {
            console.log('Files selected:', files);
            // TODO: Handle file upload
            alert(`Selected ${files.length} file(s). File upload will be implemented.`);
        }
    };

    const handleVoiceInput = () => {
        // Check if browser supports speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            alert('Voice input is not supported in your browser. Please use Chrome or Edge.');
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => {
            console.log('Voice recognition started');
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            setInput(prev => prev + (prev ? ' ' : '') + transcript);
        };

        recognition.onerror = (event) => {
            console.error('Voice recognition error:', event.error);
            alert('Voice recognition error: ' + event.error);
        };

        recognition.start();
    };

    return (
        <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="bg-transparent px-6 py-4 sticky bottom-0"
            style={{ backgroundColor: 'rgba(0, 0, 0, 0.8)', backdropFilter: 'blur(10px)' }}
        >
            <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
                <div
                    className={`ambient-glow-container ${isHovered || isScrolled ? 'active animated' : ''} transition-all duration-300`}
                    onMouseEnter={() => setIsHovered(true)}
                    onMouseLeave={() => setIsHovered(false)}
                >
                    <div className="flex items-end space-x-2 bg-slate-950 rounded-2xl border border-slate-800 p-3 relative z-10 shadow-2xl">
                        {/* Left side buttons */}
                        <div className="flex items-center space-x-1 pb-2">
                            {/* Add button */}
                            <button
                                type="button"
                                onClick={handleFileAttach}
                                className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-all duration-200"
                                title="Attach file"
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                                </svg>
                            </button>

                            {/* Mode Selector */}
                            <div className="relative">
                                <button
                                    type="button"
                                    onClick={() => setShowModeMenu(!showModeMenu)}
                                    className="flex items-center space-x-1.5 px-3 py-1.5 text-sm text-slate-300 hover:bg-slate-800 rounded-lg transition-all duration-200 border border-slate-700"
                                >
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                    </svg>
                                    <span className="font-medium capitalize">{mode}</span>
                                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                    </svg>
                                </button>

                                <AnimatePresence>
                                    {showModeMenu && (
                                        <motion.div
                                            initial={{ opacity: 0, y: -10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            exit={{ opacity: 0, y: -10 }}
                                            className="absolute bottom-full left-0 mb-2 bg-slate-900 border border-slate-700 rounded-lg shadow-lg overflow-hidden z-10 min-w-[180px]"
                                        >
                                            <button
                                                type="button"
                                                onClick={() => {
                                                    setMode('normal');
                                                    setShowModeMenu(false);
                                                }}
                                                className={`w-full px-4 py-2.5 text-left text-sm hover:bg-slate-800 transition-colors ${mode === 'normal' ? 'bg-teal-900/50 text-teal-300 font-medium' : 'text-slate-300'
                                                    }`}
                                            >
                                                <div className="flex items-center space-x-2">
                                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                                    </svg>
                                                    <div>
                                                        <div className="font-medium">Normal</div>
                                                        <div className="text-xs text-slate-400">Fast responses</div>
                                                    </div>
                                                </div>
                                            </button>
                                            <button
                                                type="button"
                                                onClick={() => {
                                                    setMode('deepthink');
                                                    setShowModeMenu(false);
                                                }}
                                                className={`w-full px-4 py-2.5 text-left text-sm hover:bg-slate-800 transition-colors ${mode === 'deepthink' ? 'bg-teal-900/50 text-teal-300 font-medium' : 'text-slate-300'
                                                    }`}
                                            >
                                                <div className="flex items-center space-x-2">
                                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                                                    </svg>
                                                    <div>
                                                        <div className="font-medium">DeepThink</div>
                                                        <div className="text-xs text-slate-400">Detailed analysis</div>
                                                    </div>
                                                </div>
                                            </button>
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>

                            {/* DeepThink indicator */}
                            {mode === 'deepthink' && (
                                <motion.div
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    className="px-2 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded-md"
                                >
                                    Deep Mode
                                </motion.div>
                            )}
                        </div>

                        {/* Text Input */}
                        <div className="flex-1 relative">
                            <textarea
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={handleKeyDown}
                                placeholder="Ask anything..."
                                disabled={disabled}
                                rows={1}
                                className="w-full bg-transparent border-none px-2 py-2 text-white placeholder-slate-500 focus:outline-none resize-none custom-scrollbar min-h-[40px] max-h-[200px]"
                                style={{
                                    height: 'auto',
                                    resize: 'none',
                                }}
                                onInput={(e) => {
                                    e.target.style.height = 'auto';
                                    e.target.style.height = Math.min(e.target.scrollHeight, 200) + 'px';
                                }}
                            />
                        </div>

                        {/* Right side buttons */}
                        <div className="flex items-center space-x-1 pb-2">
                            {/* Voice Input */}
                            <button
                                type="button"
                                onClick={handleVoiceInput}
                                disabled={disabled}
                                className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-all duration-200 disabled:opacity-50"
                                title="Voice input"
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                                </svg>
                            </button>

                            {/* Send Button */}
                            <button
                                type="submit"
                                disabled={disabled || !input.trim()}
                                className="p-2.5 bg-gradient-to-r from-teal-600 to-teal-500 hover:from-teal-700 hover:to-teal-600 text-white rounded-lg transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                                title="Send message"
                            >
                                {disabled ? (
                                    <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                    </svg>
                                ) : (
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                                    </svg>
                                )}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Hidden file inputs */}
                <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    onChange={handleFileChange}
                    className="hidden"
                    accept="*/*"
                />
                <input
                    ref={imageInputRef}
                    type="file"
                    multiple
                    onChange={handleFileChange}
                    className="hidden"
                    accept="image/*"
                />
            </form>
        </motion.div>
    );
};

export default ChatInput;
