import React, { useState } from 'react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import jsPDF from 'jspdf';

const MessageBubble = ({ message, isUser }) => {
    const [copied, setCopied] = useState(false);
    const [exported, setExported] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(message.content);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    const handleExportPDF = () => {
        const doc = new jsPDF();
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const margin = 20;
        const maxWidth = pageWidth - (margin * 2);

        // Add title
        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.text('Deep Research AI - Export', margin, margin);

        // Add timestamp
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        const timestamp = new Date(message.timestamp).toLocaleString();
        doc.text(`Generated: ${timestamp}`, margin, margin + 10);

        // Add content
        doc.setFontSize(11);
        const lines = doc.splitTextToSize(message.content, maxWidth);
        let yPosition = margin + 25;

        lines.forEach((line) => {
            if (yPosition > pageHeight - margin) {
                doc.addPage();
                yPosition = margin;
            }
            doc.text(line, margin, yPosition);
            yPosition += 7;
        });

        // Save the PDF
        const filename = `deep-research-${new Date().getTime()}.pdf`;
        doc.save(filename);

        setExported(true);
        setTimeout(() => setExported(false), 2000);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-6`}
        >
            <div className={`message-bubble ${isUser ? 'message-user' : 'message-assistant'} relative group`}>
                {!isUser && (
                    <div className="absolute top-3 right-3 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                        <button
                            onClick={handleCopy}
                            className="bg-slate-800 hover:bg-slate-700 p-2 rounded-lg border border-slate-700"
                            title="Copy to clipboard"
                        >
                            {copied ? (
                                <svg className="w-4 h-4 text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                            ) : (
                                <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                                        d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                </svg>
                            )}
                        </button>
                        <button
                            onClick={handleExportPDF}
                            className="bg-slate-800 hover:bg-slate-700 p-2 rounded-lg border border-slate-700"
                            title="Export to PDF"
                        >
                            {exported ? (
                                <svg className="w-4 h-4 text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                            ) : (
                                <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                            )}
                        </button>
                    </div>
                )}

                <div className={`prose prose-invert max-w-none ${isUser ? 'prose-sm' : ''}`}>
                    {isUser ? (
                        <p className="m-0 whitespace-pre-wrap text-white">{message.content}</p>
                    ) : (
                        <ReactMarkdown
                            components={{
                                h1: ({ node, ...props }) => (
                                    <h1
                                        className="text-3xl font-bold mt-6 mb-4 bg-gradient-to-r from-teal-400 via-cyan-400 to-purple-500 bg-clip-text text-transparent"
                                        {...props}
                                    />
                                ),
                                h2: ({ node, ...props }) => (
                                    <h2
                                        className="text-2xl font-bold mt-8 mb-4 text-teal-400 border-l-4 border-teal-500 pl-4 bg-slate-800/50 py-2 rounded-r-lg"
                                        {...props}
                                    />
                                ),
                                h3: ({ node, ...props }) => (
                                    <h3
                                        className="text-xl font-semibold mt-6 mb-3 text-cyan-400"
                                        {...props}
                                    />
                                ),
                                p: ({ node, ...props }) => (
                                    <p
                                        className="mb-4 leading-relaxed text-slate-300"
                                        {...props}
                                    />
                                ),
                                ul: ({ node, ...props }) => (
                                    <ul
                                        className="space-y-3 mb-6"
                                        {...props}
                                    />
                                ),
                                ol: ({ node, ...props }) => (
                                    <ol
                                        className="list-decimal list-inside mb-6 space-y-3 text-slate-300"
                                        {...props}
                                    />
                                ),
                                li: ({ node, children, ...props }) => {
                                    const text = String(children);
                                    // Check if this is a key finding (contains bold text at start)
                                    const isKeyFinding = text.includes('**') || text.includes('•');

                                    if (isKeyFinding) {
                                        return (
                                            <li
                                                className="bg-slate-800/40 border border-slate-700/50 rounded-lg p-4 hover:bg-slate-800/60 transition-colors duration-200 list-none"
                                                {...props}
                                            >
                                                <div className="flex items-start gap-3">
                                                    <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-teal-500 to-purple-600 rounded-lg flex items-center justify-center mt-0.5">
                                                        <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                                        </svg>
                                                    </div>
                                                    <div className="flex-1 text-slate-200">
                                                        {children}
                                                    </div>
                                                </div>
                                            </li>
                                        );
                                    }

                                    return (
                                        <li className="ml-6 text-slate-300 flex items-start gap-2" {...props}>
                                            <span className="text-teal-400 mt-1.5">•</span>
                                            <span className="flex-1">{children}</span>
                                        </li>
                                    );
                                },
                                strong: ({ node, ...props }) => (
                                    <strong
                                        className="font-bold text-teal-300"
                                        {...props}
                                    />
                                ),
                                em: ({ node, ...props }) => (
                                    <em
                                        className="italic text-purple-400"
                                        {...props}
                                    />
                                ),
                                code: ({ node, inline, ...props }) =>
                                    inline ? (
                                        <code
                                            className="bg-slate-800 px-2 py-1 rounded text-teal-400 text-sm font-mono border border-slate-700"
                                            {...props}
                                        />
                                    ) : (
                                        <code
                                            className="block bg-slate-800 p-4 rounded-lg text-sm overflow-x-auto font-mono border border-slate-700 shadow-lg"
                                            {...props}
                                        />
                                    ),
                                blockquote: ({ node, ...props }) => (
                                    <blockquote
                                        className="border-l-4 border-purple-500 pl-4 py-2 my-4 bg-slate-800/30 rounded-r-lg italic text-slate-400"
                                        {...props}
                                    />
                                ),
                            }}
                        >
                            {message.content}
                        </ReactMarkdown>
                    )}
                </div>

                <div className={`text-xs mt-2 opacity-70 ${isUser ? 'text-teal-100' : 'text-slate-500'}`}>
                    {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
            </div>
        </motion.div>
    );
};

export default MessageBubble;
