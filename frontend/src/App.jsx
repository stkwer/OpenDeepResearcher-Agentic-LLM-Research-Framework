import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import MessageBubble from './components/MessageBubble';
import ChatInput from './components/ChatInput';
import TypingIndicator from './components/TypingIndicator';
import TiltedCard from './components/TiltedCard';
import ShinyText from './components/ShinyText';
import { motion, AnimatePresence } from 'framer-motion';
const API_BASE_URL = 'http://localhost:8000';

function App() {
    const [conversations, setConversations] = useState([]);
    const [currentConversationId, setCurrentConversationId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState('');
    const messagesEndRef = useRef(null);

    // Sidebar collapse state
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [isSidebarPinned, setIsSidebarPinned] = useState(false);
    const hoverTimeoutRef = useRef(null);

    // Load conversations from backend on mount
    useEffect(() => {
        loadConversationsFromBackend();
    }, []);

    // Save conversations to localStorage whenever they change (for offline cache)
    useEffect(() => {
        if (conversations.length > 0) {
            localStorage.setItem('research_conversations', JSON.stringify(conversations));
        }
    }, [conversations]);

    // Load conversations from backend
    const loadConversationsFromBackend = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/conversations`);
            const backendConversations = response.data;

            if (backendConversations.length > 0) {
                setConversations(backendConversations);
                const mostRecent = backendConversations[0];
                setCurrentConversationId(mostRecent.id);
                setMessages(mostRecent.messages);
                setSessionId(mostRecent.session_id);
            } else {
                // No conversations in backend, create a new one
                createNewConversation();
            }
        } catch (error) {
            console.error('Error loading conversations from backend:', error);
            // Fallback to localStorage
            const savedConversations = localStorage.getItem('research_conversations');
            if (savedConversations) {
                const parsed = JSON.parse(savedConversations);
                setConversations(parsed);
                if (parsed.length > 0) {
                    const mostRecent = parsed[0];
                    setCurrentConversationId(mostRecent.id);
                    setMessages(mostRecent.messages);
                    setSessionId(mostRecent.sessionId);
                }
            } else {
                createNewConversation();
            }
        }
    };

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        scrollToBottom();
    }, [messages, isLoading]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const createNewConversation = async () => {
        const newSessionId = uuidv4();
        const newConversation = {
            id: uuidv4(),
            session_id: newSessionId,
            sessionId: newSessionId,  // Keep for backward compatibility
            title: 'New Research',
            messages: [],
            created_at: new Date().toISOString(),
            createdAt: new Date().toISOString(),  // Keep for backward compatibility
            updated_at: new Date().toISOString(),
            updatedAt: new Date().toISOString(),  // Keep for backward compatibility
        };

        // Save to backend
        try {
            await axios.post(`${API_BASE_URL}/conversations`, {
                id: newConversation.id,
                session_id: newSessionId,
                title: 'New Research'
            });
        } catch (error) {
            console.error('Error creating conversation in backend:', error);
        }

        setConversations(prev => [newConversation, ...prev]);
        setCurrentConversationId(newConversation.id);
        setSessionId(newSessionId);
        setMessages([]);

        // Store session ID for backend
        localStorage.setItem('research_session_id', newSessionId);
    };

    const switchConversation = (conversationId) => {
        const conversation = conversations.find(c => c.id === conversationId);
        if (conversation) {
            setCurrentConversationId(conversationId);
            setMessages(conversation.messages);
            setSessionId(conversation.sessionId);
            localStorage.setItem('research_session_id', conversation.sessionId);
        }
    };

    const updateConversationTitle = async (conversationId, firstMessage) => {
        // Generate title from first message (first 50 chars)
        const title = firstMessage.length > 50
            ? firstMessage.substring(0, 50) + '...'
            : firstMessage;

        // Update in backend
        try {
            await axios.put(`${API_BASE_URL}/conversations/${conversationId}`, { title });
        } catch (error) {
            console.error('Error updating conversation title:', error);
        }

        setConversations(prev => prev.map(conv =>
            conv.id === conversationId
                ? { ...conv, title, updatedAt: new Date().toISOString(), updated_at: new Date().toISOString() }
                : conv
        ));
    };

    const updateCurrentConversation = (newMessages) => {
        setConversations(prev => prev.map(conv =>
            conv.id === currentConversationId
                ? { ...conv, messages: newMessages, updatedAt: new Date().toISOString() }
                : conv
        ));
    };

    const deleteConversation = async (conversationId) => {
        // Delete from backend
        try {
            await axios.delete(`${API_BASE_URL}/conversations/${conversationId}`);
        } catch (error) {
            console.error('Error deleting conversation from backend:', error);
        }

        setConversations(prev => {
            const filtered = prev.filter(c => c.id !== conversationId);

            // If we deleted the current conversation, switch to another or create new
            if (conversationId === currentConversationId) {
                if (filtered.length > 0) {
                    const newCurrent = filtered[0];
                    setCurrentConversationId(newCurrent.id);
                    setMessages(newCurrent.messages);
                    setSessionId(newCurrent.sessionId || newCurrent.session_id);
                } else {
                    createNewConversation();
                }
            }

            return filtered;
        });
    };

    const handleSendMessage = async (messageText) => {
        if (!messageText.trim() || !sessionId) return;

        // Add user message to chat
        const userMessage = {
            role: 'user',
            content: messageText,
            timestamp: new Date().toISOString(),
        };

        const newMessages = [...messages, userMessage];
        setMessages(newMessages);
        updateCurrentConversation(newMessages);

        // Update conversation title if this is the first message
        if (messages.length === 0) {
            updateConversationTitle(currentConversationId, messageText);
        }

        setIsLoading(true);

        try {
            // Send request to backend
            const response = await axios.post(`${API_BASE_URL}/research`, {
                message: messageText,
                session_id: sessionId,
            });

            // Add assistant response to chat
            const assistantMessage = {
                role: 'assistant',
                content: response.data.response,
                timestamp: response.data.timestamp,
            };

            const updatedMessages = [...newMessages, assistantMessage];
            setMessages(updatedMessages);
            updateCurrentConversation(updatedMessages);
        } catch (err) {
            console.error('Error sending message:', err);

            let errorMessage = 'Failed to get response. Please try again.';

            if (err.response) {
                errorMessage = `Error: ${err.response.data.detail || err.response.statusText}`;
            } else if (err.request) {
                errorMessage = 'Cannot connect to server. Make sure the backend is running on http://localhost:8000';
            }

            // Add error message to chat
            const errorMsg = {
                role: 'assistant',
                content: `⚠️ **Error**: ${errorMessage}`,
                timestamp: new Date().toISOString(),
            };

            const updatedMessages = [...newMessages, errorMsg];
            setMessages(updatedMessages);
            updateCurrentConversation(updatedMessages);
        } finally {
            setIsLoading(false);
        }
    };

    const handleClearChat = () => {
        if (window.confirm('Are you sure you want to clear this conversation?')) {
            const clearedMessages = [];
            setMessages(clearedMessages);
            updateCurrentConversation(clearedMessages);
        }
    };

    // Sidebar interaction handlers
    const handleSidebarToggle = () => {
        const newPinnedState = !isSidebarPinned;
        setIsSidebarPinned(newPinnedState);
        setIsSidebarOpen(newPinnedState);

        // Clear any pending hover timeout
        if (hoverTimeoutRef.current) {
            clearTimeout(hoverTimeoutRef.current);
            hoverTimeoutRef.current = null;
        }
    };

    const handleSidebarMouseEnter = () => {
        // Open sidebar on hover if not pinned
        if (!isSidebarPinned) {
            setIsSidebarOpen(true);
        }

        // Clear any pending close timeout
        if (hoverTimeoutRef.current) {
            clearTimeout(hoverTimeoutRef.current);
            hoverTimeoutRef.current = null;
        }
    };

    const handleSidebarMouseLeave = () => {
        // Only close on hover leave if not pinned
        if (!isSidebarPinned) {
            // Add delay before closing to prevent flickering
            hoverTimeoutRef.current = setTimeout(() => {
                setIsSidebarOpen(false);
            }, 250); // 250ms delay
        }
    };

    return (
        <div className="flex h-screen bg-slate-950">
            {/* Sidebar */}
            <Sidebar
                conversations={conversations}
                currentConversationId={currentConversationId}
                onNewChat={createNewConversation}
                onSelectConversation={switchConversation}
                onDeleteConversation={deleteConversation}
                isOpen={isSidebarOpen}
                onToggle={handleSidebarToggle}
                onMouseEnter={handleSidebarMouseEnter}
                onMouseLeave={handleSidebarMouseLeave}
            />

            {/* Main Content */}
            <div className="flex-1 flex flex-col">
                <Header onClearChat={handleClearChat} />

                {/* Messages Container */}
                <div className="flex-1 overflow-y-auto custom-scrollbar px-6 py-6">
                    <div className="max-w-4xl mx-auto">
                        {messages.length === 0 ? (
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="text-center mt-16"
                            >
                                <div className="w-20 h-20 bg-gradient-to-br from-teal-500 to-purple-600 rounded-2xl mx-auto mb-6 flex items-center justify-center shadow-2xl shadow-teal-500/50">
                                    <svg
                                        className="w-10 h-10 text-white"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            strokeWidth={2}
                                            d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                                        />
                                    </svg>
                                </div>
                                <h2 className="text-3xl font-bold mb-3">
                                    <ShinyText
                                        text="Welcome to Deep Research AI"
                                        speed={3}
                                        className="text-3xl font-bold"
                                    />
                                </h2>
                                <p className="text-slate-400 text-lg max-w-2xl mx-auto mb-8">
                                    Ask me anything and I'll conduct comprehensive research using advanced AI agents.
                                    I can help you explore complex topics, analyze trends, and provide detailed insights.
                                </p>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-3xl mx-auto">
                                    {[
                                        { icon: '🔍', title: 'Deep Research', desc: 'Multi-source analysis', color: 'from-teal-900/50 to-teal-800/50' },
                                        { icon: '🧠', title: 'AI-Powered', desc: 'LangGraph pipeline', color: 'from-purple-900/50 to-purple-800/50' },
                                        { icon: '💬', title: 'Conversational', desc: 'Context-aware responses', color: 'from-blue-900/50 to-blue-800/50' },
                                    ].map((feature, idx) => (
                                        <TiltedCard
                                            key={idx}
                                            rotateAmplitude={12}
                                            scaleOnHover={1.08}
                                        >
                                            <motion.div
                                                initial={{ opacity: 0, y: 20 }}
                                                animate={{ opacity: 1, y: 0 }}
                                                transition={{ delay: idx * 0.1 + 0.2 }}
                                                className={`glass bg-gradient-to-br ${feature.color} rounded-xl p-5 text-center shadow-lg transition-shadow duration-300`}
                                            >
                                                <div className="text-3xl mb-2">{feature.icon}</div>
                                                <h3 className="font-semibold text-slate-200 mb-1">{feature.title}</h3>
                                                <p className="text-sm text-slate-400">{feature.desc}</p>
                                            </motion.div>
                                        </TiltedCard>
                                    ))}
                                </div>
                            </motion.div>
                        ) : (
                            <AnimatePresence>
                                {messages.map((message, index) => (
                                    <MessageBubble
                                        key={index}
                                        message={message}
                                        isUser={message.role === 'user'}
                                    />
                                ))}
                            </AnimatePresence>
                        )}

                        {isLoading && <TypingIndicator />}

                        <div ref={messagesEndRef} />
                    </div>
                </div>

                {/* Input Area */}
                <ChatInput onSend={handleSendMessage} disabled={isLoading} />
            </div>
        </div>
    );
}

export default App;
